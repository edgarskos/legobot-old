#!/usr/bin/python
#
# (C) Legoktm 2008-2011, MIT License
# 
import cgitb; cgitb.enable()
import cgi, sys, urllib2, re, time
import monobook2, BeautifulSoup
import pywikibot
print "Content-Type: text/html\n"
page = monobook2.Page('Watchlist Filter-er','/~legoktm/cgi-bin/watchlist.py')


input_content = """\
<form name="input" action="/~legoktm/cgi-bin/watchlist.py" method="POST">

Wiki: <input type="text" name="wiki"> (Example: en.wikipedia.org)
<textarea name="watchlist">Copy/paste your entire raw-watchlist here.
Delete these two lines first.</textarea>
<br /><br />
<input type="submit" value="Filter Watchlist">
</form>
"""

def parse_site(url):
    if url == 'commons.wikimedia.org':
        return pywikibot.Site('commons', 'commons')
    split = url.split('.')
    if len(split) != 3:
        return pywikibot.Site()
    try:
        return pywikibot.Site(split[0], split[1])
    except:
        return pywikibot.Site()

def filter_list(site, list):
    newlist = []
    for line in list.splitlines():
        pg = pywikibot.Page(site, line.strip())
        tp = pg.toggleTalkPage()
        if (not pg.exists()) and (not tp.exists()):
            continue
        elif pg.isRedirectPage() and tp.isRedirectPage():
            continue
        else:
            newlist.append(pg.title())
    return '\n'.join(newlist)



def printcontent(content):
    global page
    ret = page.top()
    ret += page.body(content)
    ret += page.footer()
    return ret

def main():
    form = cgi.FieldStorage()
    try:
        wiki = form["wiki"].value
        watchlist = form["watchlist"].value
        value = True
    except KeyError:
        value = False
    if value:
        site = parse_site(wiki)
        newlist = filter_list(site, watchlist)
        content = """\

<textarea>%s</textarea>
        """ %(watchlist)
    else:
        content = input_content
    print printcontent(content)
    
    

    
if __name__ == "__main__":
    main()
