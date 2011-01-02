 #!usr/bin/python
#
# (C) Legoktm 2008-2011, MIT License
#
import cgitb; cgitb.enable()

def header(title):
#       print "Content-Type: text/html\n"
    x= """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">\n"""
    y= """\n<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<title>"""+title+"""</title>
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
    return x+y

def __getans(res):
    for row in res:
        for col in res:
            ans = str(col[0])
    return ans

def __getcolor(num):
    colors = {'red':'#FF0000', 'green':'#a5ffbb'}
    if int(num) >= 86400:
        return (colors['red'], str(num))
    else:
        return (colors['green'], str(num))
def __convert_timestamp(seconds):
    seconds = int(seconds)
    hours = seconds / 3600
    seconds = seconds % 3600
    minutes = seconds / 60
    seconds = seconds % 60
    return '%sh %sm %ss' % (hours, minutes, seconds)


def repfuncs(db, sx):
	import MySQLdb
	dbs = MySQLdb.connect(db=db, host='sql-'+sx,read_default_file="/home/legoktm/.my.cnf")
	cur = dbs.cursor()
	cur.execute("""SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;""")
	res = cur.fetchall()
	ans = __getans(res)
	set = __getcolor(ans)
	return "\n<tr style='background-color: "+set[0]+"'><td style='width: 25%; padding-left: 1em;'>"+sx+"</td><td>"+__convert_timestamp(set[1])+"</td></tr>"
	
def replagtable():
    z= '\n<table style="width: 100%; border-collapse: collapse;">\n'
    a= repfuncs('enwiki_p','s1')
    b= repfuncs('enwiktionary_p','s2')
    c= repfuncs('frwiktionary_p','s3')
    d= repfuncs('commonswiki_p','s4')
    e= repfuncs('dewiki_p','s5')
    f= repfuncs('frwiki_p','s6')
    g= '\n</table>'
#    f= '\n</div></div>'
    return z+a+b+c+d+e+f+g #+f
    
def body(content):
    a= """\n<body class="mediawiki"><div id="globalWrapper"><div id="column-content"><div id="content">\n"""
    b= content #.replace('\n','<br />') #fix newlines
    c= '\n</div></div>\n'
    return a+b+c
def navbar(replagmessage = 'status', other = False):
    a= """<div id="column-one">
<div class="portlet" id="p-logo"><a href="http://toolserver.org/~legoktm"><img src="http://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Wikimedia_Community_Logo-Toolserver.svg/135px-Wikimedia_Community_Logo-Toolserver.svg.png"></a></div>
<div class='portlet' id='p-navigation'><h5>navigation</h5><div class='pBody'>
<ul>
<li><a href="http://toolserver.org/~legoktm/cgi-bin/index.py">Main Page</a></li>
<li><a href="http://code.google.com/p/legobot/issues/list">Bug tracker</a></li>
<li><a href="http://code.google.com/p/legobot/source/browse#svn/trunk/toolserver">Subversion</a></li>
%s
</ul>
</div></div>

"""
    if other:
        url = other.split('|')[0]
        text = other.split('|')[1]
        a = a %('<li><a href="'+url+'">'+text+'</a></li>')
    else:
        a = a %('')
    b= replagtable() + '\n</div></div>\n</div></div>'
    return a+b
def footer():
    x= """<table id="footer" style="text-align: left; clear:both;" width="100%"><tr><td>
<a href="http://tools.wikimedia.de/"><img src="http://tools.wikimedia.de/images/wikimedia-toolserver-button.png" alt="Toolserver project" /></a>
<a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
<a href="http://wikimediafoundation.org/wiki/Fundraising?s=cl-Wikipedia-free-mini-button.png"><img src="http://upload.wikimedia.org/wikipedia/meta/6/66/Wikipedia-free-mini-button.png" alt="Wikipedia... keep it free." /></a>
</td></tr></table>
</body>
</html>
"""
    return x
def all(title, content, replagmessage = None, other = None):
    x = header(title)
    x+= body(content)
    if replagmessage:
        if other:
            x+= navbar(replagmessage, other)
        else:
            x+= navbar(replagmessage)
    if other and not replagmessage:
        x+= navbar(other = other)
    x+= footer()
    return x
def top(title):
    print header(title)

def bottom(replagmessage = None, other = None):
    print navbar(replagmessage = replagmessage, other = other)
    print footer
