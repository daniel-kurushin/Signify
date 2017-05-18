#Пока что класс делает разбор по составу, с остальным пока разбираюсь
import pymorphy2
import re


class sentence:
    def __init__(self, text):
        self.mas_sentences = re.split(r'(?<=[.!?…]) ',text)


class TrainingText:
    def __init__(self, text):
        self.Lxm = []
        self._sentences = sentence(text).mas_sentences
        self.mass = list()
        self.dt = {}
        self.morph = pymorphy2.MorphAnalyzer()
        self.break_text()

    def break_text(self):
        for temp in self._sentences:
            _w = re.findall(r"(\w+|\sи т\.д\.|\sи т\.п\.|\sи т\.д\. и т\.п\.)", temp)
            self.mass.append(_w)
        for lt in self.mass:
            for j in lt:
                for i in self.morph.parse(j.lower()):
                    if (i.tag.POS in self.dt):
                        if (not (i.word in self.dt[i.tag.POS])):
                            if (not (len(i.word) <= 2 and len(i.normal_form) > 2)):
                                self.dt[i.tag.POS].append(i.word)
                                self.Lxm.append(i.normal_form)
                    else:
                        self.dt[i.tag.POS] = []
                        self.dt[i.tag.POS].append(i.word)
                        self.Lxm.append(i.normal_form)


#Тестировал на таких ядерных предложениях:
#Профессор осматривает пациента.
#Художник нарисовал картину. Он спит.
#Мальчики играют в войнушку.
#Корова посется на лугу.
#Кристалл характеризуется состоянием.
#Объект движется вперед.
#Антон играет на гитаре и поет песню.
#Учитель начал урок.
#Растения растут в нашем дворе.

#Результат:{'NOUN': ['профессор', 'пациента', 'художник', 'картину',
#  'мальчики', 'войнушку', 'корова', 'лугу', 'кристалл', 'состоянием', 'объект',
# 'антон', 'гитаре', 'песню', 'учитель', 'начал', 'урок', 'растения', 'дворе'],
# 'VERB': ['осматривает', 'нарисовал', 'спит', 'играют', 'посётся', 'характеризуется',
# 'движется', 'играет', 'поёт', 'начал', 'растут'], 'NPRO': ['он'], 'PRTS': ['спит'],
# 'PREP': ['в', 'на', 'вперёд'], 'PRCL': ['на', 'и'], 'INTJ': ['на', 'и'], 'ADVB':
# ['вперёд'], 'CONJ': ['и'], 'ADJF': ['нашем']}


