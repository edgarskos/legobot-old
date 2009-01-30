#!/usr/bin/python
#
# (C) Legoktm 2008-2009, MIT License
# 
import cgitb; cgitb.enable()
import cgi, sys, urllib2, re, time
import monobook, BeautifulSoup
print "Content-Type: text/html\n"

months = {
	'1':'01',
	'2':'02',
	'3':'03',
	'4':'04',
	'5':'05',
	'6':'06',
	'7':'07',
	'8':'08',
	'9':'09',
	'10':'10',
	'11':'11',
	'12':'12',
}
subpagelink = '<div id="contentSub"><span class="subpages">&lt; <a href="http://toolserver.org/~legoktm/cgi-bin/reflinks.py" title="reflinks.py">Template filler</a></span></div>'

def gettitle(url, errorrep = False):
	try:
		check = urllib2.urlopen(url)
		error = False
		soup = BeautifulSoup.BeautifulSoup(check)
		title = soup.title.string
		title = title.replace('|','-') #so the onwiki template isnt messed up
		title = title.replace('\n',' ') #remove extra line breaks
		title = title.replace('\t',' ') #remove extra tabs
		return title
	except urllib2.HTTPError, e:
		error = e
		#print error
		title = internetarch(url)
		if title:
			return title
		if errorrep:
			return error
		return False
#		sys.exit()
#		title = internetarch(url)

def getreftag(url):
	if '.com' in url:
		list = '<ref name="' + url.split('.com')[0] + '.com">'
		return list
	if '.org' in url:
		list = '<ref name="' + url.split('.org')[0] + '.org">'
		return list
	if '.net' in url:
		list = '<ref name="' + url.split('.net')[0] + '.net">'
		return list
	return '<ref>'
	
	
def deahref(text):
	text = re.findall('<a(.*?)>(.*?)</a>', text)
	try:
		return text[0][1]
	except IndexError:
		return text

def internetarch(url):
#	check = urllib2.urlopen('http://web.archive.org/' + url)
	return False
def createtemp(url, notemp = False):
	url = url.replace(' ', '_')
	if 'http' not in url:
		url = 'http://' +url
	title = gettitle(url)
	if not notemp:
		cur = time.localtime()
		month = months[str(cur[1])]
		monthname = time.strftime('%B')		
		year = cur[0]
		day = cur[2]
		frontreftag = getreftag(url)
		datefield = 'accessdate = %s-%s-%s' %(year, month, day)
		title = gettitle(url)
		if not title:
			template = frontreftag + '[%s] {{dead link| date = %s %s }}</ref>' %(url, monthname, year)
			content = """\
			<h2>Template filler result</h2>
			%s
			<b>%s has been detected as a dead link (%s).  Please check <a href="http://web.archive.org">The Internet Archive</a> for old archives.</b>
			<br />
			<textarea>%s</textarea>
			""" %(subpagelink, url, gettitle(url, errorrep = True), template)
			printcontent(content)
			sys.exit()
		else:
			template = frontreftag + '{{cite web| url = %s | title = %s | %s }}</ref>' %(url, title, datefield)
		return template
	else:
		return frontreftag + '[%s %s]</ref>' %(url, title)


input_content = """\
<h2>Template filler</h2>
<br />
<form name="input" action="/~legoktm/cgi-bin/reflinks.py" method="get">

URL: <input type="text" name="url">

<br />
Do not use <code>{{cite web}}</code>: <input type="checkbox" name="temp"> <i>(Default True)</i>
<br /><br />
<input type="submit" value="Fill template">
</form>
<h2>Bookmarklet</h2>
Just drag the following link to your toolbar: <a href="javascript:location.href='http://toolserver.org/~legoktm/cgi-bin/reflinks.py?url='+document.location.href;" title="Template filler">Template filler</a>
"""

def printcontent(content):
	print monobook.header('Template filler')
	print monobook.body(content)
	print monobook.navbar(other = 'http://code.google.com/p/legobot/source/browse/trunk/toolserver/public_html/cgi-bin/reflinks.py|Source')
	print monobook.footer()

def main():
	form = cgi.FieldStorage()
	try:
		url = form["url"].value
		value = True
	except KeyError:
		value = False
	if value:
		try:
			temp = bool(form["temp"].value)
		except KeyError:
			temp = False
		template = createtemp(url, notemp = temp)
		content = """\
		<h2>Template filler result</h2>
		%s
		<textarea>%s</textarea>
		""" %(subpagelink, template)
	else:
		content = input_content
	printcontent(content)
	
	

	
if __name__ == "__main__":
	main()