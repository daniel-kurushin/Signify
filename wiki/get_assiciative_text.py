#!/usr/bin/python3
from get_definition import get_definition
from get_keywords2 import get_keywords, filter_keywords
from normalize_term import normalize_term
import sys

tree = {}

def get_graph(definition = "Дерево", n = 0):
	global tree

	print(n, definition, file=sys.stderr)

	if n < 3:
		definition_text = get_definition(definition)
		open('/tmp/rez.txt','a').write("=\n%s\n=\n" % definition_text)

		keywords = get_keywords(definition_text)
		keywords = filter_keywords(keywords, set(['гео', 'фам']), set([r'англ', r"displaystyle.*"]))

		for word in keywords:
			if word != definition and len(word) > 3:
				tree.update({(definition, word):1})
				get_graph(word, n+1)

		#print(tree)

if __name__ == '__main__':
	terms = ["информационные технологии", "информация", "информатика", "защита информации", "вычислительная техника", "искусственный интеллект", "программирование"]
	for term in terms:
		get_graph(term, 0)
	print("digraph g {\n\trankdir=LR;")
	for definition, word in tree.keys():
		definition, word = [ normalize_term(_) for _ in [definition, word] ]
		if definition != word: print("\t\"%s\" -> \"%s\"" % (definition, word))
	print("}")
	#graph = get_graph(definition = "дерево")
	# понятие -> понятие2
