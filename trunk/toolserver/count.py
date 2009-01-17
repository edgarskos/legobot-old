#!/usr/bin/python
import cgitb; cgitb.enable()
import cgi
import MySQLdb

print "Content-Type: text/html\n"
def count(username, wiki, database):
	db = MySQLdb.connect(db=wiki+'_p', host="sql-%s" %(database), read_default_file="/home/legoktm/.my.cnf")
	cur = db.cursor()
	cur.execute("SELECT user_editcount FROM user WHERE user_name = '%s';" %(username))
	query = cur.fetchall()[0][0]
	cur.close()
	return query

s2 = ['bgwiki',' bgwiktionary',' commonswiki',' cswiki',' dewiki',' enwikiquote','enwiktionary',' eowiki',' fiwiki',' idwiki',' itwiki',' nlwiki',' nowiki',' plwiki','ptwiki',' svwiki',' thwiki',' trwiki',' zhwiki']

def getdb(wiki, s2):
	wiki = wiki.split('.')
	lang = wiki[0]
	fam = wiki[1]
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
username = form["username"].value
wiki = form["wiki"].value
dbset = getdb(wiki, s2)
editcount = count(username, dbset[0], dbset[1])
print editcount