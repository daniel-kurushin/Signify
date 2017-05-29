from django.db import models
import re
import pymorphy2
from pymystem3 import Mystem


morph = pymorphy2.MorphAnalyzer()
# Create your models here.
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
    # PARTS_OF_SPEECH = (('S', 'Substantive'), ('V', 'Verb'))  # todo
    part_of_speech = models.CharField(max_length=4)

class Sentence(models.Model):
    def __init__(self, text):
        #super().__init__(None,None)

        # тут сказали пока оставить так , как-нибудь добавим код с использованием продвинутых библиотек.
        # {
        _sentenceList = re.split(r'(?<=[.!?…]) ', text)
        # } в итоге имеем массив предложений.
        # Далее делаем синтаксический анализ предложений
        self.mass = list()
        t = Mystem()
        for temp in _sentenceList:
            self.mass.append(t.analyze(temp))


class Phrase(models.Model):
    lexeme_1 = models.ManyToManyField(Lexeme)
    lexeme_2 = models.ManyToManyField(Lexeme)


class Text(models.Model):
    headline = models.CharField(max_length=255)
    body = models.TextField()


class TrainingText(models.Model):
    def __init__(self, text):

        pos_tagging=Sentence(text).mass

        listt = [',', '!', '...', '?', '.', '\n', '\t', '']
        for temp_s in pos_tagging:
            mas_lex = list()
            for dict_az in temp_s:
                s = dict_az['text'].strip(' ')
                if (not (s in listt)):
                    mas_lex.append(dict_az['analysis'][0]['lex'])
                    #Тут записываем лексемы
                    Object_L = Lexeme(lemma=dict_az['analysis'][0]['lex'], part_of_speech=re.split(r',|,=|=',dict_az['analysis'][0]['gr']))
                    Object_L.save()
                    #todo проверить новая ли лексемма
                    Sygnify=morph.parse(dict_az['analysis'][0]['lex'])
                    for st in Sygnify:
                            #Записываем сигнифификаты слова и его признаки тут,пока только часть речи
                            Object_S=Significate(part_of=st.tag.POS,name=dict_az['analysis'][0]['lex'],description="")
                            Object_S.save()

            Object_Ph = Phrase(lexeme_1=mas_lex[0], lexeme_2=mas_lex[1])
            Object_Ph.save()
            Object_Ph = Phrase(lexeme_1=mas_lex[1] , lexeme_2=mas_lex[2])
            Object_Ph.save()

        #Связь:
        Object_Link=Link(weight=1,probability=1)
        















