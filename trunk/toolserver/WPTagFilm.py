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
sys.path.append(os.environ['HOME'] + '/pyenwiki')
import wikipedia, pagegenerators, catlib, query
badcats = ['Category:The Wizard of Oz (1939 film)', 'Category:Dragnet','Category:Dragnet episodes','Category:Monty Python and the Holy Grail','Category:Sholay','Category:Donnie Darko','Category:Chak De India','Category:Enchanted (film)', 'Category:Songs from Enchanted']
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
	key = res.keys()
	list = res[key[0]]['categories']
	cats = []
	for i in list:
		cats.append(i['title'])
	return cats

def checktemp(page):
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
	key = res.keys()
	list = res[key[0]]['categories']
	cats = []
	for i in list:
		cats.append(i['title'])
	return cats
def checktalk():
	site = wikipedia.getSite()
	path = site.put_address('Non-existing_page')
	text = site.getUrl(path)
	if '<div class="usermessage">' in text:
		wikipedia.output(u'NOTE: You have unread messages on %s' % site)
		wikipedia.stopme()
		sys.exit()
def dopage(page):
	wikipedia.setAction('Tagging for [[WP:FILM]] with {{Film}}')
	tag = "{{Film}}"
	tag2 = "{{Film|nested=yes}}"
	badcats = ['Category:The Wizard of Oz (1939 film)', 'Category:Dragnet','Category:Dragnet episodes','Category:Monty Python and the Holy Grail','Category:Sholay','Category:Donnie Darko','Category:Chak De India','Category:Enchanted (film)', 'Category:Songs from Enchanted']
	cats = checkcat(page.toggleTalkPage())
	for cat1 in cats:
		for cat2 in ['Category:The Wizard of Oz (1939 film)', 'Category:Dragnet','Category:Dragnet episodes','Category:Monty Python and the Holy Grail','Category:Sholay','Category:Donnie Darko','Category:Chak De India','Category:Enchanted (film)', 'Category:Songs from Enchanted']:
#			print cat1, cat2
			if cat1 == cat2:
				print '%s has the bad cat of %s' %(str(page), cat2)
				return
	wikipedia.output(page.title())
#	checktalk()
	if page.namespace() == 1:
		if page.exists():
			try:
				text = state0 = page.get()
				if re.search('\{\{Film',text,re.I):
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
	else:
		print 'Not a talk page...'
def main():
	site = wikipedia.getSite()
	cat = catlib.Category(site,'Category:Films by year')
	gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)
	tag = "{{Film}}"
	tag2 = "{{Film|nested=yes}}"
	pages = []
	badcats = ['Category:The Wizard of Oz (1939 film)', 'Category:Dragnet','Category:Dragnet episodes','Category:Monty Python and the Holy Grail','Category:Sholay','Category:Donnie Darko','Category:Chak De India','Category:Enchanted (film)', 'Category:Songs from Enchanted'] 
	for page in gen:
		if page.isTalkPage():
			print 'Adding %s' %str(page)
			pages.append(page)
		else:
			pages.append(page.toggleTalkPage())
			print 'Adding %s' %str(page.toggleTalkPage())
		print 'Sorting'
		pages = sorted(set(pages))
	wikipedia.setAction('Tagging for [[WP:FILM]] %s' % tag)
	for page in pages:
		dopage(page)
		

if __name__ == "__main__":
    try:
    	main()
    finally:
        wikipedia.stopme()