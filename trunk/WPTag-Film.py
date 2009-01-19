#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Reame: TODO
"""
#
# (C) Compwhizii and Betacommand, 2008
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id: $'
#
import re, sys, os
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')
import wikipedia, pagegenerators, catlib, query

def checkcat(page):
	page = re.compile(r'\[\[(.*?)\]\]', re.IGNORECASE).sub(r'\1', str(page))
	params = {
		'action':'query',
		'titles':page,
		'prop':'categories',
		'cllimit':'500',
	}
	res = query.GetData(params, useAPI = True, encodeTitle = False)
	if res.has_key('error'):
		print 'ERROR: %s' %(res['error'])
		return
	res = res['query']['pages']
	print res
	key = res.keys()
	print key
	list = res[key[0]]['categories']
	print list
	cats = []
	for i in list:
		cats.append(i['title'])
	return cats

def checktalk():
	path = site.put_address('Non-existing_page')
	text = site.getUrl(path)
	if '<div class="usermessage">' in text:
		wikipedia.output(u'NOTE: You have unread messages on %s' % self)
		wikipedia.stopme()
		sys.exit()
def dopage(page):
	tag = "{{Film}}"
	tag2 = "{{Film|nested=yes}}"
	badcats = ['Category:The Wizard of Oz (1939 film)', 'Category:Dragnet','Category:Dragnet episodes','Category:Monty Python and the Holy Grail','Category:Sholay','Category:Donnie Darko','Category:Chak De India','Category:Enchanted (film)', 'Category:Songs from Enchanted'] 

	cats = checkcat(page.toggleTalkPage())
	for cat1 in cats:
		for cat2 in batcats:
			print cat1, cat2
			if cat1 == cat2:
				return
	wikipedia.output(page.title())
	checktalk()
	if page.namespace() == 1:
		if page.exists():
			try:
				text = state0 = page.get()
				if re.search('\{\{CephalopodTalk',text,re.I):
					wikipedia.output('Template found passing')
				else:
					wikipedia.output('template not found')
					if re.search('\{\{WikiProjectBannerShell(\s|)(|\n)(|\s)\|1\=',text,re.I):
						text = re.sub('\{\{WikiProjectBannerShell(\s|)(|\n)(|\s)\|1\=','{{WikiProjectBannerShell|1=\n%s' % tag2 ,text,re.I)
						wikipedia.showDiff(state0, text)
						page.put(text)
					else:
						text = tag + text
						wikipedia.showDiff(state0, text)
						page.put(text)
			except wikipedia.IsRedirectPage:
				return
		else:
			page.put(tag)
        
def main():
	site = wikipedia.getSite()
	cat = catlib.Category(site,'Category:Films by year')
	gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True, limit = 500)
	tag = "{{Film}}"
	tag2 = "{{Film|nested=yes}}"
	pages = []
	badcats = ['Category:The Wizard of Oz (1939 film)', 'Category:Dragnet','Category:Dragnet episodes','Category:Monty Python and the Holy Grail','Category:Sholay','Category:Donnie Darko','Category:Chak De India','Category:Enchanted (film)', 'Category:Songs from Enchanted'] 
	for page in gen:
		if page.isTalkPage():
			pages.append(page)
		else:
			pages.append(page.toggleTalkPage())
		pages = sorted(set(pages))
	tagged = pagegenerators.ReferringPageGenerator(wikipedia.Page(site, 'Template:Film'), onlyTemplateInclusion = True)
	for page in tagged:
		try:
			pages.remove(page)
		except:
			pass
	wikipedia.setAction('Tagging for [[WP:FILM]] %s' % tag)
	for page in pages:
		dopage(page)
		

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()