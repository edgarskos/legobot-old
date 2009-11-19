#!/usr/bin/python
#
# (C) Legoktm 2008-2009, MIT License
# 
import cgitb; cgitb.enable()
import cgi
import MySQLdb

import monobook2
print "Content-Type: text/html\n"
def count(username, wiki, database):
    db = MySQLdb.connect(db=wiki, host="sql-%s" %(database), read_default_file="/home/legoktm/.my.cnf")
    cur = db.cursor()
    cur.execute("SELECT user_editcount FROM user WHERE user_name = '%s';" %(username))
    query = cur.fetchall()
    res = query[0][0]
    cur.close()
    return res


def getdb(wiki):
    db = MySQLdb.connect(db='toolserver', host="sql", read_default_file="/home/legoktm/.my.cnf")
    cur = db.cursor()
    cur.execute("SELECT dbname, server FROM `wiki` WHERE domain = '%s' LIMIT 1" %wiki)
    res = cur.fetchall()[0]
    return [res[0], 's' + str(res[1])]


page = monobook2.Page('Raw edit counter','/~legoktm/cgi-bin/count.py')

username = page.getValue('username')

if username:
    wiki = page.getValue('wiki')
    dbset = getdb(wiki)
    editcount = count(username, dbset[0], dbset[1])
    print editcount
else:
    content = """\
<form name="input" action="/~legoktm/cgi-bin/count.py" method="get">

Username: <input type="text" name="username">

<br />
Wiki: <input type="text" name="wiki"> <i>(en.wikipedia.org)</i>
<br />
<input type="submit" value="Get count!">
</form>
    """
    print page.top()
    print page.body(content)
    print page.footer()
