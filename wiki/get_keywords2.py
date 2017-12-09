#!/usr/bin/python3
from rutermextract import TermExtractor
from pymystem3 import Mystem

ma = Mystem()

def get_keywords(text = ""):
	return [ _.normalized for _ in TermExtractor()(text) if _.count > 4 ]

def filter_keywords(keywords = ["россия", "бердяев", "информатика", "англ"], tag_filter = set (["имя", "отч", "гео", "фам"]), word_filter = set(["англ", "displaystyle"])):
	rez = []
	for keyword in keywords:
		params = []
		for a in ma.analyze(keyword):
			try:
				params += a['analysis'][0]['gr'].split(',')
			except (KeyError, IndexError):
				pass
		if (not tag_filter & set(params)) & (keyword not in word_filter):
			rez += [keyword]
	return rez

if __name__ == '__main__':
	# print(get_keywords("несогласованное использование табуляции несогласованное использование табуляции и пробелов в отступах несогласованное использование табуляции и пробелов в отступах"))
	print(filter_keywords())
