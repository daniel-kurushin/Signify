from django.db import models
import re
import subprocess
import urllib
from pymystem3 import Mystem
from bs4 import BeautifulSoup
from urllib.parse import quote
import pymorphy2
import sys
import graphviz as gv

class Significate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    part_of_speech = models.CharField(max_length=4)
    def __str__(self):
        return self.name


class Link(models.Model):
    weight = models.FloatField()
    significate_from = models.ManyToManyField(Significate)
    link = models.ForeignKey(Significate)
    significate_to = models.ManyToManyField(Significate)
    probability = models.FloatField()

    def __str__(self):
        return self.link.__str__()

class Lexeme(models.Model):
    lemma = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=4)

class Sentence(models.Model):
    sentens=models.ForeignKey(Text)
    sentence=models.TextField()

class Phrase(models.Model):
    lexeme_1 = models.ManyToManyField(Lexeme)
    lexeme_2 = models.ManyToManyField(Lexeme)

class Text(models.Model):
    headline = models.CharField(max_length=255)
    body = models.TextField()

class Dictionary(models.Model):
    lexeme = models.ManyToManyField(Lexeme)
    significate = models.ManyToManyField(Significate)

class TrainingText(models.Model):
    for ij,text in enumerate(Text.objects.all()):
            _sentenceList = re.split(r'(?<=[.!?…]) ', text.body)
            morph = pymorphy2.MorphAnalyzer()
            ZnakiP = [",", "!", "/n", ".", ":", ";", '"', "'", "\n", "...", "?", "!", "(", ")", "-", " ", "  "]
            t = Mystem()
            PARS = []
            for sent in _sentenceList:
                #Сохраняем предложение в таблице предложение
                Sentence.objects.create(sentens=text.id,sentence=sent)                
                input_file = open("input.txt", "w", encoding="utf-8")
                input_file.write(sent)
                input_file.close()

                # Делаем синтаксический анализ текста, находим граматические основы
                process = subprocess.Popen('tomitaparser.exe config.proto', stdout=subprocess.PIPE, shell=True)
                process.communicate()
                process.wait()

                predicate = []
                Nouns = []
                DOP = []
                DOP.append({})
                OPR = []
                with open("pretty.html", encoding='utf8') as fp:
                    soup = BeautifulSoup(fp, "html.parser")
                par_f = soup.find_all('table')
                for table in par_f:
                    th = table.find('th')
                    if (th.text == "Noun1"):
                        slovo = th.find_parent("table").find('a').text
                        Nouns.append(slovo)
                    if (th.text == "Verb1"):
                        slovo = th.find_parent("table").find('a').text
                        predicate.append(slovo)
                    if (th.text == "OPR1"):
                        sl = th.find_parent("table").find_all('a')
                        for slovo in sl:
                            OPR.append(slovo.text)
                    if (th.text == "DOP1"):
                        sl = th.find_parent("table").find_all('a')
                        for slovo in sl:
                            DOP[0][slovo.text.lower()] = slovo.next_element.next_element.next_element.next_element
                TREE = {}
                TREE[Nouns[0]] = {}

                for v in predicate:
                    TREE[Nouns[0]][v] = {}
                if (OPR != []):
                    for temp in OPR:
                        for noun in TREE:
                            if (len(re.split(r"[,' ']", temp)) == 1):
                                TREE[Nouns[0]][temp] = t.analyze(temp)[0]['analysis'][0]['gr']
                            else:
                                m2 = []
                                for f in re.split(r"[,' ']", temp):
                                    if (f != ''):
                                        m2.append(f)
                                if (noun in m2):
                                    mk = t.analyze(temp)
                                    wsp = []
                                    for tr in mk:
                                        if (not tr['text'] in ZnakiP):
                                            if (not 'CONJ' in tr['analysis'][0]['gr']):
                                                wsp.append(tr['text'])
                                    for tl in wsp:
                                        if (tl != noun):
                                            TREE[Nouns[0]][tl] = t.analyze(tl)[0]['analysis'][0]['gr']

                for temp in TREE[Nouns[0]]:
                    if (temp in DOP[0].values()):
                        for sp in DOP[0]:
                            if (DOP[0][sp] == temp):
                                m2 = []
                                for f in re.split(r"[,' ']", sp):
                                    if (f != ''):
                                        m2.append(f)
                                for rg in m2:
                                    TREE[Nouns[0]][temp][rg] = {}
                                    for _opr in OPR:
                                        reg = re.split(r"[,' ']", temp)
                                        if (noun in reg):
                                            mk = t.analyze(_opr)
                                            wsp = []
                                            for tr in mk:
                                                if (not tr['text'] in ZnakiP):
                                                    if (not 'CONJ' in tr['analysis'][0]['gr']):
                                                        wsp.append(tr['text'])
                                            for tl in wsp:
                                                if (tl != rg):

                                                 TREE[Nouns[0]][temp][rg][tl] = t.analyze(tl)[0]['analysis'][0]['gr']
                #Функция для записи лексемм
                def Lexem_in(self,lex,ph):
                    if(not Lexeme.objects.get(lemma=lex)==None):
                        Lexeme.objects.create(lemma=lex,part_of_speech=ph)
                def Phraz_add(self,left,right):
                    if(not Phrase.objects.get(lexeme_1=left,lexeme_2=right)==None):
                        Phrase.objects.create(lexeme_1=left,lexeme_2=right)
                def Sgt_add(self,sg_t):
                    url = "http://dic.academic.ru/searchall.php?SWord=" + quote(sg_t + " толковый словарь Ушакова")
                    DSN=self.parse(self.get_html(url),sg_t)
                    if(not Phrase.objects.get(name=sg_t, description=DSN)==None):
                        Phrase.objects.create(lexeme_1=sg_t,lexeme_2=DSN)
                def dict_add(self,lexem_id,sig_id):
                    Dictionary.objects.create(significate=sig_id,lexem_id=sig_id)

                def Link_add(self, id_a,id_b,link_id):
                    Lexeme.objects.create(significate_from=id_a,significate_to=id_b,weight=1,probability=1,link=link_id)

                def parse(self,html, sl):
                    D = Mystem()
                    soup = BeautifulSoup(html, "html.parser")
                    table = soup.find('ul', class_="terms-list")
                    for temp in table.find_all('li'):
                        if (sl.upper() == temp.a.text):
                            url = re.findall(r'"(.+)"', temp.a.__str__())[0]
                            html = self.get_html(url)
                            soup2 = BeautifulSoup(html, "html.parser")
                            tb = soup2.find('div', id='article')
                            rw = tb.find('dd', itemprop="definition")
                            rww = rw.find_all('div')[1:]
                            temp = ""
                            for t in rww:
                                temp = temp + t.text + " "
                            return temp

                def get_html(url):
                    response = urllib.request.urlopen(url)
                    return response.read().decode("utf8")

                for noun in TREE:
                    d1 = [noun]
                    Sgt_add(noun)
                    Lexem_in(noun,'S')
                    dict_add(Lexeme.objects.get(lemma=noun).id,Significate.objects.get(name=noun).id)
                    for verb in TREE[noun]:
                        Sgt_add(verb)
                        Lexem_in(verb, 'V')
                        dict_add(Lexeme.objects.get(lemma=verb).id, Significate.objects.get(name=verb).id)
                        if (morph.parse(verb)[0].tag.POS == 'ADJF'):
                            d2 = [noun, 'быть']
                            d2.append(verb)
                            Phraz_add(noun,'быть')
                            Phraz_add("быть", verb)
                            if (not d2 in PARS):
                                Link_add(Significate.objects.get(name=d2[0]).id,
                                                         Significate.objects.get(name=d2[1]).id,
                                                         Significate.objects.get(name=d2[2]).id)
                                PARS.append(d2.copy())
                            d2.pop()
                        else:
                            d4 = [verb, "может быть"]
                            d1.append(verb)
                            Phraz_add(verb, "может быть")
                            Phraz_add(noun, verb)
                            for temp in TREE[noun][verb]:
                                Sgt_add(temp)
                                Lexem_in(temp, 'Dop')
                                dict_add(Lexeme.objects.get(lemma=temp).id, Significate.objects.get(name=temp).id)
                                if (morph.parse(temp)[0].tag.POS == 'NOUN'):
                                    d1.append(morph.parse(temp)[0].normal_form)
                                    Phraz_add(verb, morph.parse(temp)[0].normal_form)
                                    if (not d1 in PARS):
                                        Link_add(Significate.objects.get(name=d1[0]).id,
                                                 Significate.objects.get(name=d1[1]).id,
                                                 Significate.objects.get(name=d1[2]).id)
                                        PARS.append(d1.copy())
                                    d1.pop()
                                    d3 = [temp, 'быть']
                                    Phraz_add(temp, "быть")

                                    for temp2 in TREE[noun][verb][temp]:
                                        Sgt_add(temp2)
                                        Lexem_in(temp2, 'Opr')
                                        dict_add(Lexeme.objects.get(lemma=temp2).id,
                                                 Significate.objects.get(name=temp2).id)
                                        d3.append(temp2)
                                        Phraz_add("быть", temp2)
                                        Link_add(Significate.objects.get(name=d3[0]).id,
                                                 Significate.objects.get(name=d3[1]).id,
                                                 Significate.objects.get(name=d3[2]).id)
                                        PARS.append(d3.copy())
                                        d3.pop()
                                else:
                                    d4.append(temp)
                                    Phraz_add("может быть", temp)
                                    if (not d4 in PARS):
                                        PARS.append(d4.copy())
                                        Link_add(Significate.objects.get(name=d4[0]).id,
                                                 Significate.objects.get(name=d4[1]).id,
                                                 Significate.objects.get(name=d4[2]).id)
                                    d4.pop()

            obj = PARS.copy()

            g1 = gv.Digraph(format='png')

            for temp in obj:
                a = morph.parse(temp[0])[0].tag.POS
                if (a == 'VERB' or a == 'INFN'):
                    for t in obj:
                        if (t[1] == temp[0]):
                            g1.node(t[0], shape='rect', style='filled', fillcolor='#cccccc')
                            g1.node(temp[0])
                            g1.node(temp[2], shape='rect', style='filled', fillcolor='#cccccc')
                            g1.edge(t[0], temp[0])
                            g1.edge(temp[0], temp[2], label=temp[1])
                            g1.edge(temp[0], t[2])

                else:
                    g1.node(temp[0], shape='rect', style='filled', fillcolor='#cccccc')
                    g1.node(temp[2], shape='rect', style='filled', fillcolor='#cccccc')
                    g1.edge(temp[0], temp[2], label=temp[1])

            g1.render('img/g'+ij)















