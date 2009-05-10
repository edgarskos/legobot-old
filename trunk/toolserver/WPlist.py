#!usr/bin/python
# -*- coding: utf-8  -*-
import os, sys, re
__version__ = '$Id$'
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.environ['HOME'] + '/pythonwikibot')
import wiki
from wiki import catlib, pagegen
def API(params):
	return wiki.API.query(params)
def unicodify(text):
    if not isinstance(text, unicode):
        return text.decode('utf-8')
    return text
def createlist(cat, wpproj, raw = False, cats = True):
	category1 = wiki.Page('Category:'+cat)
	category = catlib.Category(category1)
	gen = pagegen.category(category1, recurse=True)
	wikitext = ''
	wikitext2 = ''
	wikitext3 = ''
	
	if not cats:
		for page in gen:
			wikitext = wikitext+'\n*'+str(page)
			link = page.title()
			print link
			wikitext2 = wikitext2+'\n'+link
		wikitext = unicodify(wikitext)
	if cats:
		subcats = category.subcats(recurse = True)
		for subcat in subcats:
			newtext = retpages(subcat)
			wikitext3 += newtext
		wikitext3 = unicodify(wikitext3)
	
	page = wikipedia.Page(site, wpproj + '/Articles')
	if not cats:
		page.put(wikitext, 'Updating watchlist')
	if cats:
		page.put(wikitext3, 'Updating watchlist')
	wikitext2 = '<pre>\n' + wikitext2 + '\n</pre>'
	wikitext2 = unicodify(wikitext2)
	if raw == True:
		page = wiki.Page(wpproj + '/Articles/raw')
		page.put(wikitext2, 'Updating raw watchlist')
def retpages(cat):
	cat = str(cat.title())
	wikitext = '==[[:%s]]==\n' %cat
	print 'Getting pages in [[%s]] using API...' %cat
	params = {
		'action':'query',
		'list':'categorymembers',
		'cmtitle':cat,
		'cmlimit':'max',
	}
	res = API(params)
	res = res['query']['categorymembers']
	for article in res:
		try:
			if article['ns'] != (14 or '14'):
				artname = unicode(article['title'])
				wikitext += '*[[%s]]\n' %unicode(artname)
		except KeyError:
			return ''
	return wikitext

def main():
	createlist('Canadian football', 'Wikipedia:WikiProject Canadian football', raw = False, cats = True)
	createlist('Ohio', 'Wikipedia:WikiProject Ohio', raw = True)
	
if __name__ == '__main__':
	main()
