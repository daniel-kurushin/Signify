#!/usr/bin/python
#  -*- coding: utf-8 -*-

import json
import math

import requests
from bs4 import BeautifulSoup

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

    return {'word':word, 'res':tuple(results)}


def set_zhur_base(word_file = 'test.txt'):
    words = open(word_file, 'r').readlines()
    f = open('base.json', 'a', encoding='utf-8')
    result_list = []
    for word in words:
        result_list.append(get_zhur_index(word[:-1]))
    json.dump(result_list, f, ensure_ascii = False)
    f.close()


def get_from_base(word = '', base_file = 'base.json'):
    base = json.load(open(base_file, 'r', encoding='utf-8'))
    for item in base:
        if item['word'] == word:
            return item
        else:
            return get_zhur_index(word)


def get_range(vector1 = (), vector2 = ()):
    t = 0.0
    for i in range(len(vector1)):
        t += (vector2[i] - vector1[i])**2
    return math.sqrt(t)


# def set_test(test_words):
#     result_zhur = []
#     for word in test_words:
#         result_zhur.append(get_zhur_index(word))
#     result_range = []
#     for i in range(1,len(test_words)):
#         result_range.append((result_zhur[i]['word'], get_range(result_zhur[0]['res'], result_zhur[i]['res'])))
#
#     return result_range

def set_test(test_words):
    result_zhur = []
    for word in test_words:
        result_zhur.append(get_from_base(word))
    result_range = []
    for i in range(1,len(test_words)):
        result_range.append((result_zhur[i]['word'], get_range(result_zhur[0]['res'], result_zhur[i]['res'])))
    return result_range

if __name__ == "__main__":
    # set_zhur_base()
    print(set_test(['айвазовский', 'армеец', 'наука', 'азия']))