#!usr/bin/python
import re, getpass
import urllib, urllib2, time
import userconfig
"""
Custom library for interfacing with MediaWiki through API
"""

def query(wiki, params, debug=False, format = 'json'):
	apipath = 'http://%s.org/w/api.php' %(wiki)
	params['format'] = format
	params = urllib.urlencode(params)
#	print params
#	time.sleep(5)
	req = urllib2.Request(apipath, params)
#	print req
	response = urllib2.urlopen(req)
#	print response
#	time.sleep(5)
	text = response.read()
	url = urllib.urlopen(apipath, params)
	text = url.read()
	url.close()
	if debug:
		print text
	return text

def login(wiki, username):
	password = getpass.getpass('API Login password: ')
	params = {
		'action' : 'login',
		'lgname' : username,
		'lgpassword' : password,
	}
	print
	res = query(wiki, params, debug=True)
	resd = re.findall('"result":"(.*)","lguserid":"(.*)","lgusername":"(.*)","lgtoken":(.*)","cookieprefix":"(.*)","sessionid":"(.*)"\}\}', res)
	try:
		resd = resd[0]
	except IndexError:
		print 'Login failed.'
		quit()	

	resultdict = {
		'result':resd[0],
		'userid':resd[1],
		'username':resd[2],
		'token':resd[3],
		'prefix':resd[4],
		'sessionid':resd[5],
	}
	print resultdict

	if username != resultdict['username']:
		print 'ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ...'
		print 'Somehow... logged in as a different user!!'
		print 'Now logging out...'
		paramslgut = {
			'action' : 'logout',
		}
		query(wiki, paramslgut)
		quit()
	return resultdict

def get(wiki, page, format = 'dict'):
	params = {
		'action':'query',
		'prop':'revisions',
		'titles':page,
		'rvprop':'content',
	}
	res = query(wiki, params)
	resd = re.findall('"pageid":(.*),"ns":(.*),"title":"(.*)","revisions"', res)
#	print resd
	content = re.findall('"revisions":\[{"\*":"(.*)"\}\]\}\}\}\}', res)
	rdict = {
		'content':content,
		'pageid':resd[0][0],
		'pagename':resd[0][2],
		'ns':resd[0][1]
	}
	if format == 'dict':
		return rdict
	else:
		return content

def namespace(wiki, page):
	params = {
		'action':'query',
		'titles':page,
		'prop':'info',
	}
	res = query(wiki, params)
#	print res
	resd = re.findall(',"ns":(.*),"title":"', res)
	resd = int(resd[0])
#	print resd
	return resd
def isredirect(wiki, page):
	params = {
		'action':'query',
		'titles':page,
		'prop':'info',
	}
	res = query(wiki, params)
	if re.search('"redirect":""', res, re.I):
		return True
	else:
		return False
def lastedit(wiki, page, prnt = False):
		params = {
			'action':'query',
			'prop':'revisions',
			'titles':page,
			'rvprop':'user|comment',
		}
		res = query(wiki, params)
		resd = re.findall(',"revisions":\[\{"user":"(.*)","comment":"(.*)"\}\]\}\}\}\}', res)
#		print resd
		ret = {
			'user':resd[0][0],
			'comment':resd[0][1],
		}
		if prnt:
			print 'The last edit on %s was made by: %s with the comment of: %s.' %(page, resd[0][0], resd[0][1])
		return ret
def getcatmem(wiki, page, limit = 500):
	if userconfig.bot:
		limit = 5000
	if not re.search('Category:(.*)',page, re.I):
		page = 'Category:%s' %(page)
	params = {
		'action':'query',
		'list':'categorymembers',
		'cmtitle':page,
		'cmlimit':str(limit),
	}
	res = query(wiki, params, format = 'xml')
	resd = re.findall('title="(.*?)"', res)
#	print resd
	return resd
def newpages(wiki, limit = 15, patrolled = False, bot = False):
	if userconfig.bot:
		limit = 50
	params = {
		'action':'query',
		'list':'recentchanges',
		'rcprop':'title',
		'rctype':'new',
	}
	if patrolled:
		params['rcshow'] = 'patrolled'
	if bot:
		params['rcshow'] = 'bot'
	if patrolled and bot:
		params['rcshow'] = 'patrolled|bot'
	res = query(wiki, params, format = 'xml')
	resd = re.findall('title="(.*?)"', res)
	print resd