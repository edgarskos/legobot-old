#!usr/bin/python
#
# (C) Legoktm 2009
# Released under the MIT License
#
# All pages should be in the wiki.Page() format

import wiki
#set up api
API = wiki.API()

"""Gets all articles in a certain category and returns a list"""
def category(page, excludens = False):
	if not page.isCategory():
		raise wiki.NotCategory(page.title())
	params = {
		'action':'query',
		'list':'categorymembers',
		'cmtitle':page.title(),
		'cmlimit':'500',
	}
	result = API.query(params)
	#format the list
	list = []
	res = result['query']['categorymembers']
	for page in res:
		try:
			if excludens:
				if page['ns'] != int(excludens):
					list.append(page['title'])
			else:
				list.append(page['title'])
		except UnicodeEncodeError:
			pass
	return list

def prefixindex(page):
	ns = page.namespace()
	prefix = page.titlewonamespace() + '/'
	params = {
		'action':'query',
		'list':'alllinks',
		'alprefix':prefix,
		'alnamespace':ns,
		'allimit':'500',
	}
	res = API.query(params)['query']['alllinks']
	list = []
	for page in res:
		wikipage = wiki.Page(page['title'])
		if not (wikipage in list):
			list.append(wikipage)
	return list