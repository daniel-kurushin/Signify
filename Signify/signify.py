#!/usr/bin/python
#  -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import wikipedia


url = 'https://psi-technology.net/servisfonosemantika.php'
params = {'slovo':'',
             'sub':'submit'
          }

def get_zhur_index(word=''):
    params['slovo'] = word
    # шлем пост-запрос в форму на сайте-журавлезаторе
    req = requests.post(url, data=params)

    # подчищенный реквест резалт
    req_result = str(req.content, encoding="1251").split("</table>\n</div> <!-- end ptn_content -->")[0].split('<table class="prais" border="1" width="100%">')[1]
    # теперь тут в основном танцы на предмет вычищения результата и приведения его в форму набора чисел
    soup = BeautifulSoup(req_result, "html.parser")
    tables = soup.find_all('tr')  # собираем все из результатов реквеста
    tables.__delitem__(0)  # убираем заголовки колонок таблицы
    table_content = []
    results = []
    for table in tables:
        table_content.append(table.find_all('td'))
        table_content[-1].__delitem__(0) #убираем ненужную инфу раз
        table_content[-1].__delitem__(-1) #убираем ненужную инфу два
        table_content[-1].__delitem__(-1) #убираем ненужную инфу три
    for item in table_content: #заменяем остатки хтмл-таблички на нормальное число и пишем его в список
        results.append(float(str(item[0]).split('<td>')[1].split('</td>')[0].replace(',','.')))

    #складываем все полученное и вроде как идентификатор
    zhur_index = 0.0
    for param in results:
        zhur_index += param

    return zhur_index

def add_to_base(word=''):
    with open('base.txt', 'a', encoding='utf-8') as output:
        output.write('"'+str(get_zhur_index(word))+'":"'+word+'",\n')

def signify(zhur_index=0.0):
    f = open('base.txt', 'r', encoding='utf-8-sig')
    local_dict = json.load(f)
    if str(zhur_index) in local_dict.keys():
        print(local_dict[str(zhur_index)])
        try:
            wikipedia.set_lang('ru')
            print(local_dict[str(zhur_index)] +'\n' + wikipedia.summary(local_dict[str(zhur_index)]))
        except:
            print("No such page")

def set_base():
    test_doc = open('test.txt', 'r').readlines()
    f = open('base.txt', 'a', encoding='utf-8')
    f.write('{')
    for line in test_doc:
        add_to_base(line[:-1])
    f.write('}')
    f.close()

#set_base()
signify(74.23)