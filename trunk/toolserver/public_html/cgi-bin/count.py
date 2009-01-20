#!/usr/bin/python
import cgitb; cgitb.enable()
import cgi, sys
import MySQLdb


class NonExistWiki (Exception):
	"""Wiki specified does not exist or is not supported"""

class NonExistantUser (Exception):
	"""User specified does not exist"""
import monobook
print "Content-Type: text/html\n"
def count(username, wiki, database, truewiki):
	try:
		db = MySQLdb.connect(db=wiki+'_p', host="sql-%s" %(database), read_default_file="/home/legoktm/.my.cnf")
	except:
		raise NonExistWiki, 'ERROR: Non-existant wiki specified.'
		sys.exit()
	cur = db.cursor()
	cur.execute("SELECT user_editcount FROM user WHERE user_name = '%s';" %(username))
	try:
		query = cur.fetchall()[0][0]
	except IndexError:
		raise NonExistantUser, 'ERROR: Non-existant user specified.'
		sys.exit()
	cur.close()
	return query

s2 = ['bgwiki',' bgwiktionary',' commonswiki',' cswiki',' dewiki',' enwikiquote','enwiktionary',' eowiki',' fiwiki',' idwiki',' itwiki',' nlwiki',' nowiki',' plwiki','ptwiki',' svwiki',' thwiki',' trwiki',' zhwiki']

def getdb(wiki, s2):
	wiki = wiki.split('.')
	lang = wiki[0]
	try:
		fam = wiki[1]
	except IndexError:
		raise NonExistWiki, 'ERROR: Non-existant wiki specified.'
	lang = lang.lower()
	fam = fam.lower()
	if fam == 'wikipedia':
		fam = 'wiki'
	if fam == 'wikimedia':
		if lang == 'commons':
			db = 'commonswiki'
		elif lang == 'meta':
			db = 'metawiki'
		else:
			db = lang + 'wiki'
	else:
		db = lang + fam
	if db == 'enwiki':
		return [db, 's1']
	for i in s2:
		if i == db:
			return [db, 's2']
	return [db, 's3']
form = cgi.FieldStorage()
try:
	username = form["username"].value
	value = True
	
except:
	value = False

if value:
	wiki = form["wiki"].value
	dbset = getdb(wiki, s2)
	editcount = count(username, dbset[0], dbset[1], wiki)
	print editcount
else:
	content = """\
	<h2>Raw Edit counter</h2>
<form name="input" action="/~legoktm/cgi-bin/count.py" method="get">

Username: <input type="text" name="username">

<br />
Wiki: <input type="text" name="wiki"> <i>(en.wikipedia.org)</i>
<br />
<input type="submit" value="Get count!">
</form>
	"""
	print monobook.header('Raw edit counter')
	print monobook.body(content)
	print monobook.navbar(other = 'http://code.google.com/p/legobot/source/browse/trunk/toolserver/count.py|Source')
	print monobook.footer()