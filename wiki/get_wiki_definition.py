def get_wiki_definition(definition = "Дерево"):
	
	from requests import get
	from bs4 import BeautifulSoup as BS

	url = "https://ru.wikipedia.org/wiki/%s" % definition
	page = get(url).content
	soup = BS(page, 'html.parser')
	x = soup.find('div','mw-content-ltr')
	y = x.find_all('p')
	myStr = ' '.join([ i.text for i in y ])
	return myStr