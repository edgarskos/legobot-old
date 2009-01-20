#!/usr/bin/env python
print "Content-Type: text/html"

import MySQLdb
dbs1 = MySQLdb.connect(db='enwiki_p', host="sql-s1", read_default_file="/home/legoktm/.my.cnf")
dbs2 = MySQLdb.connect(db='dewiki_p', host="sql-s2", read_default_file="/home/legoktm/.my.cnf")
dbs3 = MySQLdb.connect(db='metawiki_p', host="sql-s3", read_default_file="/home/legoktm/.my.cnf")
cur1 = dbs1.cursor()
cur2 = dbs2.cursor()
cur3 = dbs3.cursor()
cur1.execute("""SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;""")
cur2.execute("""SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;""")
cur3.execute("""SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;""")
res1 = cur1.fetchall()
res2 = cur2.fetchall()
res3 = cur3.fetchall()

def getans(res):
	for row in res:
		for col in res:
			ans = str(col[0])
	return ans
ans1 = getans(res1)
ans2 = getans(res2)
ans3 = getans(res3)

print """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">"""
print """<head>
<title>~legoktm</title>
<style type="text/css">
<!--/* <![CDATA[ */
@import "http://en.wikipedia.org/skins-1.5/monobook/main.css"; 
@import "http://en.wikipedia.org/w/index.php?title=MediaWiki:Monobook.css&usemsgcache=yes&action=raw&ctype=text/css&smaxage=2678400";
@import "http://en.wikipedia.org/w/index.php?title=MediaWiki:Common.css&usemsgcache=yes&action=raw&ctype=text/css&smaxage=2678400";
@import "http://en.wikipedia.org/w/index.php?title=-&action=raw&gen=css&maxage=2678400&smaxage=0&ts=20061201185052"; 
td { vertical-align: top; }

/* ]]> */-->
</style>
</head>
"""

print """<body class="mediawiki"><div id="globalWrapper"><div id="column-content"><div id="content">
<h1>Bots running here</h1>
<ul>
<li><a href="http://en.wikipedia.org/wiki/User:Legobot">Legobot</a></li>
<li><a href="http://en.wikipedia.org/wiki/User:ArticleAlertbot">ArticleAlertbot</a></li>
</ul>
<h1>Tools</h1>
<ul>
<li><a href="http://toolserver.org/~legoktm/count.html">Raw edit counter</a></li>
<li><a href="http://toolserver.org/~legoktm/alertbot.html">Alertbot status</a></li>
</ul>
"""

print """</div></div><div id="column-one">
<div class="portlet" id="p-logo"><a style="background-image: url(http://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Wikimedia_Community_Logo-Toolserver.svg/135px-Wikimedia_Community_Logo-Toolserver.svg.png);" href="http://toolserver.org/~legoktm/" title="Home"></a></div>
<div class='portlet' id='p-navigation'><h5>navigation</h5><div class='pBody'>
<ul>
<li><a href="http://tools.wikimedia.de/~legoktm/">Main Page</a></li>
<li><a href="http://code.google.com/p/legobot/issues/list">Bug tracker</a></li>
<li><a href="http://code.google.com/p/legobot/source/list">Subversion</a></li>
</ul>
</div></div>
<div class='portlet' id='p-status'><h5>status</h5><div class='pBody'>

<table style="width: 100%; border-collapse: collapse;">
"""

colors = {'red':'#FF0000', 'green':'#a5ffbb'}
def getcolor(num):
	if int(num) >= 600:
		return (colors['red'], convert_timestamp(str(num)))
	else:
		return (colors['green'], convert_timestamp(str(num)))
def convert_timestamp(seconds):
	seconds = int(seconds)
	hours = seconds / 3600
	seconds = seconds % 3600
	minutes = seconds / 60
	seconds = seconds % 60
	return '%sh %sm %ss' % (hours, minutes, seconds)

set1 = getcolor(ans1)
set2 = getcolor(ans2)
set3 = getcolor(ans3)
print "<tr style='background-color: "+set1[0]+"'><td style='width: 25%; padding-left: 1em;'>s1</td><td>"+set1[1]+"</td></tr>"
print "<tr style='background-color: "+set2[0]+"'><td style='width: 25%; padding-left: 1em;'>s2</td><td>"+set2[1]+"</td></tr>"
print "<tr style='background-color: "+set3[0]+"'><td style='width: 25%; padding-left: 1em;'>s3</td><td>"+set3[1]+"</td></tr>"
print '</table>'
print '</div></div>'
print '</div></div>'


print """<table id="footer" style="text-align: left; clear:both;" width="100%"><tr><td>
<a href="http://tools.wikimedia.de/"><img src="http://tools.wikimedia.de/images/wikimedia-toolserver-button.png" alt="Toolserver project" /></a>
<a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
<a href="http://wikimediafoundation.org/wiki/Fundraising?s=cl-Wikipedia-free-mini-button.png"><img src="http://upload.wikimedia.org/wikipedia/meta/6/66/Wikipedia-free-mini-button.png" alt="Wikipedia... keep it free." /></a>
</td></tr></table>
</body>
</html>
"""
