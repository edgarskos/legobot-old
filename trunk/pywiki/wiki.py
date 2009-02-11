#!usr/bin/env python
"""

Custom library for interfacing with MediaWiki through API

Released under the MIT License
(C) Legoktm 2008-2009
See COPYING for full License

"""
import urllib2, urllib, re, time, getpass, cookielib
from datetime import datetime
import config
import simplejson, sys, os

class NotLoggedIn(Exception):
	"""User is not logged in"""

class UserBlocked(Exception):
	"""User is blocked"""

class NoPage(Exception):
	"""Page does not exist"""

class IsRedirectPage(Exception):
	"""Page is a redirect to target"""

class APIError(Exception):
	"""General API error"""

class NotCategory(Exception):
	"""When expected page should be category, but is not"""

class API:
	
	def __init__(self, wiki = config.wiki, login=False, debug=False, qcontinue = True):
		#set up the cookies
		self.COOKIEFILE = os.environ['PWD'] + '/cookies/'+ config.username +'.data'
		self.cj = cookielib.LWPCookieJar()
		if os.path.isfile(self.COOKIEFILE):
			self.cj.load(self.COOKIEFILE)
		elif not login:
			raise NotLoggedIn('Please login by first running wiki.py')
		if wiki == 'commons':
			self.wiki = 'commons.wikimedia'
		else:
			self.wiki = wiki
		self.debug = debug
		self.qcontinue = qcontinue
	def query(self, params, after = None, write = False):
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
#		print 'Querying API'
		self.response = urllib2.urlopen(self.request)
		self.cj.save(self.COOKIEFILE)
		text = self.response.read()
		newtext = simplejson.loads(text)
		#errors should be handled now
		try:
			if newtext.has_key('error'):
				raise APIError(newtext['error'])
		except AttributeError:
			raise APIError(newtext)
		#finish query-continues
		if ('query-continue' in newtext) and self.qcontinue:
			newtext = self.__longQuery(newtext)
		return newtext
	def __longQuery(self, firstres):
		total = res = firstres
		params = self.params
		numkeys = len(res['query-continue'].keys())
		while numkeys > 0:
			keylist = res['query-continue'].keys()
			keylist.reverse()
			key1 = keylist[0]
			key2 = res['query-continue'][key1].keys()[0]
			if isinstance(res['query-continue'][key1][key2], int):
				cont = res['query-continue'][key1][key2]
			else:
				cont = res['query-continue'][key1][key2].encode('utf-8')
			params[key2] = cont
			res = API(qcontinue=False).query(params)
			for type in keylist:
				total = self.__resultCombine(type, total, res)
			if 'query-continue' in res:
				numkeys = len(res['query-continue'].keys())
			else:
				numkeys = 0
		return total
	def __resultCombine(self, type, old, new):
		"""
		Experimental-ish result-combiner thing
		If the result isn't something from action=query,
		this will just explode, but that shouldn't happen hopefully?
		(taken from python-wikitools)
		"""
		ret = old
		if type in new['query']: # Basic list, easy
			ret['query'][type].extend(new['query'][type])
		else: # Else its some sort of prop=thing and/or a generator query
			for key in new['query']['pages'].keys(): # Go through each page
				if not key in old['query']['pages']: # if it only exists in the new one
					ret['query']['pages'][key] = new['query']['pages'][key] # add it to the list
				else:
					for item in new['query']['pages'][key][type]:
						if item not in ret['query']['pages'][key][type]: # prevent duplicates
							ret['query']['pages'][key][type].append(item) # else update the existing one
		return ret

class Page:
	
	def __init__(self, page):
		self.API = API()
		self.page = page
		self.__basicinfo = self.__basicinfo()
		if self.__basicinfo.has_key('redirect'):
			self.redirect = True
		else:
			self.redirect = False
		self.ns = self.__basicinfo['ns']
		self.Site = Site()
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
	def title(self):
		return self.page
	def get(self, force = False):
		if self.redirect and (not force):
			raise IsRedirectPage(self.API.query({'action':'query','titles':self.page,'redirects':''})['query']['redirects'][0]['to'])
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
#		print token

		#do the edit
		params = {
			'action':'edit',
			'title':self.page,
			'text':newtext,
			'summary':summary,
			'token':token,
		}
		print 'Going to change [[%s]]' %(self.page)
		if watch:
			params['watch'] = ''
		if newsection:
			params['section'] = 'new'
		#check if we have waited 10 seconds since the last edit 
		FILE = os.environ['PWD'] + '/cookies/lastedit.data'
		try:
			text = open(FILE, 'r').read()
			split = text.split('|')
			date = datetime(int(split[0]), int(split[1]), int(split[2]), int(split[3]), int(split[4]), int(split[5]))
		except IOError:
			date = datetime.now()
		delta = datetime.now() - date
		if delta.seconds < 10:
			print 'Sleeping %s seconds' %(10-delta.seconds)
			time.sleep(10-delta.seconds)
		else:
			print 'Last editted %s seconds ago.' %delta.seconds
			print 'Sleeping for 2 seconds'
			time.sleep(2)
		#update the file
		d = datetime.now()
		newtext = str(d.year) +'|'+ str(d.month) +'|'+ str(d.day) +'|'+ str(d.hour) +'|'+ str(d.minute) +'|'+ str(d.second)
		write = open(FILE, 'w')
		write.write(newtext)
		write.close()
		#the actual write query
		res=self.API.query(params, write = True)
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
	def namespace(self):
		return self.ns
	def lastedit(self, prnt = False):
		params = {
			'action':'query',
			'prop':'revisions',
			'titles':self.page,
			'rvprop':'user|comment',
		}
		res = self.API.query(params)['query']['pages']
		ret = res[res.keys()[0]]['revisions'][0]
		print ret
		if prnt:
			print 'The last edit on %s was made by: %s with the comment of: %s.' %(page, ret['user'], ret['comment'])
		return ret
	def istalk(self):
		if self.ns != -1 or self.ns != -2:
			if self.ns%2 == 0:
				return False
			elif self.ns%2 == 1:
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
		nsnum = self.Site.namespacelist()[1][nstext]
		if nsnum == -1 or nsnum == -2:
			print 'Cannot toggle the talk of a Special or Media page.'
			return self.page
		istalk = self.istalk()
		if istalk:
			nsnewtext = self.Site.namespacelist()[0][nsnum-1]
		else:
			nsnewtext = self.Site.namespacelist()[0][nsnum+1]
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
	def namespacelist(self):
		params = {
			'action':'query',
			'meta':'siteinfo',
			'siprop':'namespaces',
		}
		res = API().query(params)
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
		raise APIError(query)

	
if __name__ == "__main__":
	login()