#!usr/bin/env python
"""

Custom library for interfacing with MediaWiki through API

Released under the MIT License
(C) Legoktm 2008-2009
See COPYING for full License

"""
import urllib2, urllib, re, time, getpass, cookielib
import config
import simplejson, sys, os

class NotLoggedIn(Exception):
	"""User is not logged in"""

class NoPage(Exception):
	"""Page does not exist"""

class APIError(Exception):
	"""General API error"""

class API:
	
	def __init__(self, wiki = config.wiki, login=False, debug=False):
		#set up the cookies
		self.COOKIEFILE = os.environ['PWD'] + '/cookies/'+ config.username +'.data'
		self.cj = cookielib.LWPCookieJar()
		if os.path.isfile(self.COOKIEFILE):
			self.cj.load(self.COOKIEFILE)
		elif not login:
			raise NotLoggedIn('Please login by first running wiki.py')
		self.wiki = wiki
		self.debug = debug
		
	def query(self, params, after= None):
		if os.path.isfile(self.COOKIEFILE):
			self.cj.load(self.COOKIEFILE)
		self.params = params
		self.params['format'] = 'json'
		self.encodeparams = urllib.urlencode(self.params)
		if after:
			self.encodeparams += after
		if self.debug:
			print self.encodeparams
		self.headers = {
			"Content-type": "application/x-www-form-urlencoded",
			"User-agent": config.username,
			"Content-length": len(self.encodeparams),
		}
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(self.opener)
		self.request = urllib2.Request(config.apipath %(self.wiki), self.encodeparams, self.headers)
		self.response = urllib2.urlopen(self.request)
		self.cj.save(self.COOKIEFILE)
		text = self.response.read()
		newtext = simplejson.loads(text)
		return newtext
		
class Page:
	
	def __init__(self, page):
		self.API = API()
		self.page = page
		self.__basicinfo = self.__basicinfo()
	#INTERNAL OPERATION, PLEASE DON'T USE
	def __basicinfo(self):
		params = {
			'action':'query',
			'prop':'info',
			'titles':self.page,
		}
		
		res = self.API.query(params)
		id = res['query']['pages'].keys()[0]
		dict = res['query']['pages'][id]
		return dict
	def get(self):
		params = {
			'action':'query',
			'prop':'revisions',
			'titles':self.page,
			'rvprop':'content',
		}
		res = self.API.query(params)['query']['pages']
		if res.keys()[0] == '-1':
			raise NoPage(self.page)
		content = res[res.keys()[0]]['revisions'][0]['*']
		return content.encode('utf-8')

	def put(self, newtext, summary, watch = False, newsection = False):
		#get the token
		tokenparams = {
			'action':'query',
			'prop':'info',
			'intoken':'edit',
			'titles':self.page
		}
		token = self.API.query(tokenparams)['query']['pages']
		token = token[token.keys()[0]]['edittoken']
		print token

		#do the edit
		params = {
			'action':'edit',
			'title':self.page,
			'text':newtext,
			'summary':summary,
			'token':token,
		}
		if watch:
			params['watch'] = ''
		if newsection:
			params['section'] = 'new'
		res=self.API.query(params)
		if res.has_key('error'):
			raise APIError(res['error'])
		if res['edit']['result'] == 'Success':
			print 'Changing [[%s]] was successful.' %self.page
		else:
			print 'Changing [[%s]] failed.' %self.page
			raise APIError(res)
		
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
		query = self.__basicinfo
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
		res = self.API.query(params)
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
	def isCategory(self):
		return self.namespace() == 14
	def isImage(self):
		return self.namespace() == 6
	def patrol(self, rcid):
		params = {
			'action':'patrol',
			'rcid':rcid,
			'token':self.edittoken
		}
		self.API.query(params)
	def exists(self):
		if self.__basicinfo.has_key('missing'):
			return False
		else:
			return True
	def move(self, newtitle, summary, movetalk = True):
		tokenparams = {
			'action':'query',
			'prop':'info',
			'intoken':'move',
			'titles':self.page
		}
		token = self.API.query(tokenparams)['query']['pages']
		token = token[token.keys()[0]]['movetoken']
		params = {
			'action':'move',
			'from':self.page,
			'to':newtitle,
			'reason':summary,
			'token':token
		}
		if movetalk:
			res = self.API.query(params,'&movetalk')
		else:
			res = self.API.query(params)
		if res.has_key('error'):
			raise APIError(res['error'])
		if res.has_key('move'):
			print 'Page move of %s to %s succeeded' (self.page, newtitle)
		return res

"""
Class that is mainly internal working, but contains information relevant
to the wiki site.
"""
class Site:
	def __iter__(self, wiki = config.wiki):
		self.wiki = wiki
		self.API = API()
	def namespacelist(self, force = False):
		if self.nslist and not force:
				return self.nslist
		params = {
			'action':'query',
			'meta':'siteinfo',
			'siprop':'namespaces',
		}
		res = self.API.query(params)
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
	querycheck = API().query(paramscheck)
	name = querycheck['query']['userinfo']['name']
	print name
	if querycheck['query']['userinfo'].has_key('messages'):
		print 'You have new messages on %s.' %(config.wiki)
		if config.quitonmess:
			sys.exit()
	if querycheck['query']['userinfo'].has_key('anon'):
		return False
	return name
def login(username = False):
	if not username:
		username = config.username
	try:
		password = config.password
	except:
		password = getpass.getpass('API Login Password for %s: ' %username)
	params = {
		'action' : 'login',
		'lgname' : username,
		'lgpassword' : password,
	}
	
	query = API(login=True).query(params)
	result = query['login']['result'].lower()
	if result == 'success':
		print 'Successfully logged in on %s.' %(config.wiki)
	else:
		print 'Failed to login on %s.' %(config.wiki)
		sys.exit()

if __name__ == "__main__":
	login()