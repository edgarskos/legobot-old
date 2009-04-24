#!usr/bin/python
import cgitb; cgitb.enable()
import cgi, sys, urllib2, re, time, json
import monobook, reflinks

input_content = """\
<h2>Wiki Reference Finder</h2>
<br />
<form name="input" action="/~legoktm/cgi-bin/googlesearch.py" method="get">

Search: <input type="text" name="search">
<br />
<input type="submit" value="Search">
</form>
"""
def printcontent(content):
    return monobook.all('Google Searcher', content, other = 'http://code.google.com/p/legobot/source/browse/trunk/toolserver/public_html/cgi-bin/googlesearch.py|Source')

def main():
    form = cgi.FieldStorage()
    try:
        url = form["search"].value
        value = True
    except KeyError:
        value = False
    if value:
        template = reflinks.createtemp(url)
        content = """\
        <h2>Search Results</h2>
        %s
        """ %(getresults(search))
    else:
        content = input_content
    printcontent(content)

def getresults(search):
    headers = {'User-Agent': 'Wiki Reference Finder'}
    query = urllib.urlencode({'q' : 'damon cortesi'})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
    req=urllib2.Request(url,headers=headers)
    f=urllib2.urlopen(req)
    text = json.loads(f.read())
    results = text['responseData']['results']
    retlist = []
    for i in results: #get only the data we need
        retlist.append({'title':i['title'],'url':i['url'],'content':i['content']})
    return printres(retlist)

def printres(list):
    content = ''
    for result in list:
        temp = ''
        temp += '<b><a href="%s" target="_blank">%s</a></b>\n' %(list['url'], list['url'])
        temp += list['content']
        temp += '\n<a href="http://www.toolserver.org/~legoktm/cgi-bin/reflinks/py?url=%s" target="_blank"><b>Cite this!</b></a>' %(list['url'])
        content += temp
    return content