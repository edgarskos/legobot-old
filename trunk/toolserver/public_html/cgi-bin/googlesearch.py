#!usr/bin/python
import cgitb; cgitb.enable()
import urllib2, simplejson
import monobook2

page = monobook2.Page('Google Searcher','/~legoktm/cgi-bin/googlesearch.py')
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
    global page
    ret = page.top()
    ret += page.body(content)
    ret += page.footer()
    print ret

def main():
    global page
    url = page.getValue('search')
    if url:
        content = """\
        <h2>Search Results</h2>
        %s
        """ %(getresults(url))
    else:
        content = input_content
    printcontent(content)

def getresults(search):
    headers = {'User-Agent': 'Wiki Reference Finder'}
    query = urllib.urlencode({'q' : 'damon cortesi'})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
    req=urllib2.Request(url,headers=headers)
    f=urllib2.urlopen(req)
    text = simplejson.loads(f.read())
    f.close()
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

main()
print 'Done...'