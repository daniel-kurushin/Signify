from pymystem3 import Mystem

ma = Mystem()

def normalize_term(term):
	rez = []
	for a in ma.analyze(term):
		try:
			rez += [a['analysis'][0]['lex']]
		except (KeyError, IndexError):
			rez += [a['text']]
	return ''.join(rez).strip('\n')

if __name__ == '__main__':
	print(normalize_term("какие-то длинные слова"))
