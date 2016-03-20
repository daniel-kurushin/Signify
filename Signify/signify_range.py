#!/usr/bin/python
#  -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import math

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


def get_range(vector1 = (), vector2 = ()):
    t = 0.0
    for i in range(len(vector1)):
        t += (vector2[i] - vector1[i])**2
    return math.sqrt(t)


def set_test(test_words):
    result_zhur = []
    for word in test_words:
        result_zhur.append(get_zhur_index(word))
    result_range = []
    # число сочетаний маленькое, можно пока руками прописать
    for i in range(1,len(test_words)):
        result_range.append((result_zhur[i]['word'], get_range(result_zhur[0]['res'], result_zhur[i]['res'])))

    return result_range

# y = get_zhur_index('айвазовский')
# h = get_zhur_index('салют')
# t = get_zhur_index('народ')
# u = get_zhur_index('синхрофазотрон')
# print(y)
# print(h)
# print(t)
# print(u)
# print('айвазовский и салют')
# print(get_range(y, h))
# print('айвазовский и народ')
# print(get_range(y, t))
# print('салют и народ')
# print(get_range(t, h))
# print('айвазовский и синхрофазотрон')
# print(get_range(y, u))
# print('салют и синхрофазотрон')
# print(get_range(h, u))
print(set_test(['народ', 'народ', 'кислород', 'нырод', 'нарок', 'намек']))
print(set_test(['кислород', 'кислород', 'кислородный', 'кисларод', 'кислородное', 'кислый', 'сладкий', "водород"]))
print(set_test(['россия', 'россия', 'русь', 'русский', 'расия', 'раша']))

[('народ', 0.0), ('кислород', 1.1013173929435596), ('нырод', 0.702780193232564), ('нарок', 0.0), ('намек', 0.657799361507747)]
[('кислород', 0.0), ('кислородный', 0.12409673645990808), ('кисларод', 0.0), ('кислородное', 0.34205262752974097), ('кислый', 0.3534119409414461), ('сладкий', 1.2270696801730538), ('водород', 1.2180722474467596)]
[('россия', 0.0), ('русь', 1.8104695523537535), ('русский', 0.5431390245600106), ('расия', 0.17146428199482228), ('раша', 1.0955820370926135)]

