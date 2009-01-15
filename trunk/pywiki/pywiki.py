#!usr/bin/env python
"""
Custom library for interfacing with MediaWiki through API

Released under the MIT License
(C) Legoktm 2008-2009
See COPYING for full License
"""
import urllib2, urllib, re, time, getpass
import config
import simplejson, sys

class API:
	
	def __init__(self, params, write = False, wiki = config.wiki):

		self.params = params
		self.params['format'] = 'json'
		self.encodeparams = urllib.urlencode(self.params)
		self.write = write
		self.username = config.username
		self.wiki = wiki
		if write and not self.checklogin:
			try:
				self.password = config.password
			except:
				self.password = getpass.getpass('API Login Password')

		self.headers = {
			"Content-type": "application/x-www-form-urlencoded",
			"User-agent": self.username,
			"Content-length": len(self.encodeparams),
		}
		
		self.response = False
		self.request = urllib2.Request(config.apipath %(self.wiki), self.encodeparams, self.headers)

	def query(self):
		try:
			response = urllib2.urlopen(self.request)
		except urllib2.URLError:
			print 'Cannot connect to %s.' %(config.apipath)
			print 'Please check your internet connection or check if Wikimedia is down.'
			sys.exit()
		text = response.read()
		newtext = simplejson.loads(text)
		return newtext

		
class Page:
	
	def __init__(self, page):
		self.page = page
	#INTERNAL OPERATION, PLEASE DON'T USE
	def __basicinfo(self):
		params = {
			'action':'query',
			'prop':'info',
			'titles':self.page,
		}
		
		res = API(params).query()
		id = res['query']['pages'].keys()
		dict = res['query']['pages'][id]
		return dict
	def get(self):
		params = {
			'action':'query',
			'prop':'revisions',
			'titles':self.page,
			'rvprop':'content',
		}
		res = API(params).query()
		id = self.__basicinfo()['pageid']
		content = res['query']['pages'][id]['revisions'][0]['*']

		return content.encode('utf-8')

	def put(self, newtext, summary, token = False):
		#get the token
		if token:
			self.token = token
		if not self.token:
			paramstoken = {
				'action':'query',
				'prop':'info',
				'intoken':'edit',
				'titles':self.page,
			}
			querytoken = API(paramstoken).query()
			key = querytoken['query']['pages'].keys()[0]
			token = querytoken['query']['pages'][key]['edittoken']
			self.token = token
		#do the edit
		putparams = {
		}
		
	def titlewonamespace(self, ns=False):
		if not ns:
			ns = Page(self.page).namespace()
		else:
			ns = int(ns)
		if ns == 0:
			return self.page
		else:
			return self.page.split(':')[1]
	def namespace(self, force = False):
		if self.ns and not force:
			return self.ns
		query = self.__basicinfo()
		resd = query['ns']
		self.ns = resd
		return self.ns
	def lastedit(self, prnt = False):
		params = {
			'action':'query',
			'prop':'revisions',
			'titles':self.page,
			'rvprop':'user|comment',
		}
		res = API(params).query()
		resd = re.findall(',"revisions":\[\{"user":"(.*)","comment":"(.*)"\}\]\}\}\}\}', res)
#		print resd
		ret = {
			'user':resd[0][0],
			'comment':resd[0][1],
		}
		if prnt:
			print 'The last edit on %s was made by: %s with the comment of: %s.' %(page, resd[0][0], resd[0][1])
		return ret
	def istalk(self, ns=False):
		if not ns:
			ns = Page(self.page).namspace()
		else:
			ns = int(ns)
		if ns != -1 or ns != -2:
			if ns%2 == 0:
				return False
			elif ns%2 == 1:
				return True
			else:
				sys.exit("Error: Python Division error")
		else:
			return False
	def toggletalk(self):
		try:
			nstext = self.page.split(':')[0]
		except:
			nstext = ''
		nsnum = Site.namespacelist()[1][nstext]
		if nsnum == -1 or nsnum == -2:
			print 'Cannot toggle the talk of a Special or Media page.'
			return self.page
		istalk = self.istalk(ns=nsnum)
		if istalk:
			nsnewtext = Site.namespacelist()[0][nsnum-1]
		else:
			nsnewtext = Site.namespacelist()[0][nsnum+1]
		tt = nsnewtext + ':' + self.page.split(':')[1]
		return tt

"""
Class that is mainly internal working, but contains information relevant
to the wiki site.
"""
class Site:
	def __iter__(self, wiki = config.wiki):
		self.wiki = wiki
	
	def namespacelist(self, force = False):
		if self.nslist and not force:
				return self.nslist
		params = {
			'action':'query',
			'meta':'siteinfo',
			'siprop':'namespaces',
		}
		res = API(params).query()
		resd = res['query']['namespaces']
		list = resd.keys()
		nstotext = {}
		texttons = {}
		for ns in list:
			nstotext[int(ns)] = resd[ns]['*']
			texttons[resd[ns]['*']] = int(ns)
		self.nslist = (nstotext,texttons)
		return self.nslist

"""
Other functions
"""
def checklogin():
	paramscheck = {
		'action':'query',
		'meta':'userinfo',
		'uiprop':'hasmsg',
	}
	querycheck = API(paramscheck).query()
	name = querycheck['query']['userinfo']['name']
	print name
	if querycheck['query']['userinfo'].has_key('messages'):
		print 'You have new messages on %s.' %(config.wiki)
		if config.quitonmess:
			sys.exit()
	if querycheck['query']['userinfo'].has_key('anon'):
		return False
	return name
def login(username = False, force = False):
	if not username:
		username = config.username
	else:
		username = username
	check = checklogin()
	print check
	if check and (check == username) and (force == False):
		return
	try:
		password = config.password
	except:
		password = getpass.getpass('API Login Password for %s: ' %username)
	params = {
		'action' : 'login',
		'lgname' : username,
		'lgpassword' : password,
	}
	query = API(params).query()
	result = query['login']['result'].lower()
	if result == 'success':
		print 'Successfully logged in on %s.' %(config.wiki)
	else:
		print 'Failed to login on %s.' %(config.wiki)
		sys.exit()
	print query