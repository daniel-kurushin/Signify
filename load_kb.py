from re import findall, match

def load_kb(filename = "kb.txt"):
	res = {}
	for str in open(filename).readlines():
		try:
			a, b, c = findall(r'.*?"(.*?)".*?"(.*?)".*?"(.*?)".*', str.lower())[0]
			res.update({(a,c,b):1})
		except ValueError:
			pass
		except TypeError:
			pass
		except IndexError:
			pass
	return res

if __name__ == '__main__':
	kb = load_kb("graph.dot")
