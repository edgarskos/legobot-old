#!/usr/bin/python
#
# (C) Legoktm 2008-2011, MIT License
# 
import cgitb; cgitb.enable()
import cgi
import MySQLdb

import monobook2
print "Content-Type: text/html\n"

def getdb():
    db = MySQLdb.connect(db='toolserver', host="sql", read_default_file="/home/legoktm/.my.cnf")
    cur = db.cursor()
    cur.execute("SELECT domain, dbname, server FROM `wiki`")
    res = cur.fetchall()
    text = ''
    for i in res:
    	text += res[0] + ' (' + res[1] + ') on sql-s' + str(res[2]) +'\n'
    return text


page = monobook2.Page('Server List','/~legoktm/cgi-bin/servers.py')
text = getdb()

print text
