#!/usr/bin/python3
#  -*- coding: utf-8 -*-

from django.db import models


class Significate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Link(models.Model):
    weight = models.FloatField()
    denotation_1 = models.ManyToManyField(Significate)
    link = models.ForeignKey(Significate)
    denotation_2 = models.ManyToManyField(Significate)
    # probability = models.FloatField()

    def __str__(self):
        return self.link.__str__()


class Lexeme(models.Model):
    lemma = models.CharField(max_length=255)
    # набор лингвистических характеристик, зависит от того, что парсим и что учитываем
    PARTS_OF_SPEECH = (('S', 'Substantive'), ('V', 'Verb'))  # todo
    part_of_speech = models.CharField(max_length=1, choices=PARTS_OF_SPEECH)


class Phrase(models.Model):
    # todo: класс, отвечающий за набор лингвистических характеристик,
    # присущий предикативным и полупредикативным единицам
    # представляет собой две лексемы, раскладывается из текста по непосредственным составляющим
    # возможна замена на ядерные предложения?
    lexeme_1 = models.ManyToManyField(Lexeme)
    lexeme_2 = models.ManyToManyField(Lexeme)
    # харктеристики


class Text(models.Model):
    # тексты, из которых берутся данные для процессинга:  раскладываем предложения по непосредственным составляющим,
    # собираем данные о лексемах, раскладываем все в соответствующие структуры
    # Пользовательский запрос тоже представляет собой Текст, с ним работаем точно так же, как с обучающими
    headline = models.CharField(max_length=255)
    body = models.TextField()


class Dictionary(models.Model):
    lexeme = models.ManyToManyField(Lexeme)  # лексема, которой выражается сигнификат
    significate = models.ManyToManyField(Significate)

# Данные поступают и записываются в таблицу Текст. Оттуда мы их берем и обрабатываем, разбираем на предложения и слова,
# парсим лингвистические характеристики, потом записываем в таблицу Фраз и Лексем (если Лексема новая) при помощи
# Словаря соотносим лексемы и сигнификаты, после чего на базе Фраз строим Связь, распределяя роли на основе
# грамматических характеристик (хотя бы частеречной принадлежности)
# Текст: Кристалл характеризуется состоянием
# Лексемы: кристалл, характеризоваться, состояние
# Фразы: кристалл характеризоваться, характеризоваться состояние
# Сигнификаты: Кристалл, Характеризоваться, Состояние
# Связь: Кристалл -> Характеризоваться -> Состояние
