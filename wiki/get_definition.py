from get_wiki_definition import get_wiki_definition

def get_definition(definition = "Дерево"):
	try:
		rez = open("database/%s.dat" % definition).read()
	except FileNotFoundError:
		rez = get_wiki_definition(definition)
		open("database/%s.dat" % definition, 'w').write(rez)
	return rez

if __name__ == '__main__':
	get_definition()

	# for word in ["Слово", "Дерево", "Растение"]:
	# 	print("\n", word, "\n\n", get_definition(word))

	# assert get_definition("Дерево") == DEREVO_DEFINITION
	# assert texts_are_alike(get_definition(), "Дерево - это жизненная форма\
	# 	деревянистых растений с единственной, отчётливо выраженной,\
	# 	многолетней, в разной степени одревесневшей, сохраняющейся\
	# 	в течение всей жизни, разветвлённой (кроме пальм) главной\
	# 	осью — стволом")