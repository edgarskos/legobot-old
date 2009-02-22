#!usr/bin/python
#
# (C) Legoktm 2009
# Released under the MIT License
#
# All pages should be in the wiki.Page() format

import wiki
#set up api

"""
Gets all articles in a certain category and returns a list
"""
def category(page):
	if not page.isCategory():
		raise wiki.NotCategory(page.title())
	API = wiki.API(wiki=page.site())
	print 'Getting [[%s]]...' %page.title()
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
			list.append(wiki.Page(page['title']))
		except UnicodeEncodeError:
			pass
	return list
"""
Unreliable pagegenerator at the moment...
"""
def prefixindex(page):
	API = wiki.API(wiki=page.site())
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
"""
Returns a list with pages
"""
def recentchanges(limit = 500, nobot = True, onlyanon = False, hidepatrolled = True, nponly = False):
	rcshow = []
	if nobot:
		rcshow.append('!bot')
	if onlyanon:
		rcshow.append('anon')
#	if hidepatrolled:
#		rcshow.append('!patrolled')
	rcshowparam = ''
	if len(rcshow) != 0:
		for i in rcshow:
			if i == rcshow[len(rcshow)-1]: #meaning it is the last one..
				rcshowparam += i
			else:
				rcshowparam += i + '|'
	params = {
		'action':'query',
		'list':'recentchanges',
		'rcshow':rcshowparam,
		'rcprop':'title',
		'rclimit':limit
	}
	if nponly:
		params['rctype'] = 'new'
	API = wiki.API(qcontinue=False)
	res = API.query(params)['query']['recentchanges']
	list = []
	for page in res:
		list.append(wiki.Page(page['title']))

	return list
	