#!/usr/bin/python
#
# (C) Legoktm 2008-2009, MIT License
# 
import cgitb; cgitb.enable()
import cgi, sys
import MySQLdb

import monobook
print "Content-Type: text/html\n"
def count(username, wiki, database):
	db = MySQLdb.connect(db=wiki+'_p', host="sql-%s" %(database), read_default_file="/home/legoktm/.my.cnf")
	cur = db.cursor()
	cur.execute("SELECT user_editcount FROM user WHERE user_name = '%s';" %(username))
	query = cur.fetchall()[0][0]
	cur.close()
	return query


def getdb(wiki):
	db = MySQLdb.connect(db='toolserver', host="sql", read_default_file="/home/legoktm/.my.cnf")
	cur = db.cursor()
	cur.execute("SELECT dbname, server FROM `wiki` WHERE domain = '%s' LIMIT 1" %wiki)
	res = cur.fetchall()[0]
	return [res[0], 's' + str(res[1])]
form = cgi.FieldStorage()
try:
	username = form["username"].value
	value = True
	
except:
	value = False

if value:
	wiki = form["wiki"].value
	dbset = getdb(wiki)
	editcount = count(username, dbset[0], dbset[1])
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