#!usr/bin/python
import sys
try:
	import MySQLdb
except ImportError:
	sys.exit('MySQLdb not installed.')
import config
if config.ts:
	TSUser = config.ts
else:
	raise wiki.NoTSUsername('No Toolserver username given.')
"""
Script that has MySQL Functions for toolserver users
Wiki should be in the form of langproject (ex. enwiki) without the '_p' on the end
Host is either 1, 2, or 3.  Can be left blank
"""
	self.wiki = wiki + '_p'
	if not host:
		self.host = self.query(q="SELECT server FROM wiki WHERE dbname = '%s_p';" %(wiki), db='toolserver', host='sql')[0][0]
	else:
		self.host = host

def query(q, db, host=False):
	if (db != 'toolserver') and (not ('_p' in db)):
		db += '_p'
	if not host:
		host = gethost(db)
	elif host == 'sql':
		host = host #does nothing
	else:
		host = 'sql-s' + str(host)
	conn = MySQLdb.connect(db=db, host=host, read_default_file="/home/%s/.my.cnf" %(TSUser))
	cur = conn.cursor()
	cur.execute(q)
	res = cur.fetchall()
	cur.close()
	return res
def gethost(db):
	if not ('_p' in db):
		db += '_p'
	host = query(q="SELECT server FROM wiki WHERE dbname = '%s';" %(db), db='toolserver', host='sql')[0][0]
	return host
def editcount(user):
	res = query("SELECT user_editcount FROM user WHERE user_name = '%s';" %(user))
	try:
		return res[0][0]
	except IndexError:
		raise NoUsername('%s doesnt exist on %s' %(user, self.wiki))