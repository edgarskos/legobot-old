#!usr/bin/python
import os, sys, re
sys.path.append(os.environ['HOME'] + '/pyenwiki')
import wikipedia, catlib, pagegenerators
def unicodify(text):
    if not isinstance(text, unicode):
        return text.decode('utf-8')
    return text
def delink(link):
	link = re.compile(r'\[\[(.*?)\]\]', re.IGNORECASE).sub(r'\1', link)
	return link
site = wikipedia.getSite()
def createlist(cat, wpproj, raw = False):
	category = catlib.Category(site, cat)
	gen = pagegenerators.CategorizedPageGenerator(category, recurse=True)
	wikitext = ''
	wikitext2 = ''
	for page in gen:
		wikitext = wikitext+'\n*'+str(page)
		link = delink(str(page))
		print link
		wikitext2 = wikitext2+'\n'+link
	wikitext = unicodify(wikitext)
	page = wikipedia.Page(site, wpproj + '/Articles')
	page.put(wikitext, 'Updating watchlist (Trial BRFA)')

	wikitext2 = '<pre>\n' + wikitext2 + '\n</pre>'
	wikitext2 = unicodify(wikitext2)
	if raw == True:
		page = wikipedia.Page(site, wpproj + '/Articles/raw')
		page.put(wikitext2, 'Updating raw watchlist (Trial BRFA)')

createlist('Canadian football', 'Wikipedia:WikiProject Canadian football', raw = True)