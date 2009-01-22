#!/usr/bin/python
#
# (C) Legoktm 2008-2009, MIT License
# 
import cgitb; cgitb.enable()
import cgi, sys, urllib2, re, time
import monobook
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

def gettitle(url):
	try:
		check = urllib2.urlopen(url)
		error = False
		text = check.read()
		try:
			title = re.findall('<title>(.*?)</title>', text)[0]
		except IndexError: #means that it couldn't find a title
			#check for any level 1 headers, and then level 2 headers
			try:
				title = re.findall('<h1>(.*?)</h1>', text)[0]
				title = deahref(title)
			except IndexError:
				try:
					title = re.findall('<h2>(.*?)</h2>', text)[0]
					title = deahref(title)
				except IndexError:
					title = False
		return title
	except urllib2.HTTPError, e:
		error = e
		print error
#		sys.exit()
#		title = internetarch(url)

	
def deahref(text):
	text = re.findall('<a(.*?)>(.*?)</a>', text)
	try:
		return text[0][1]
	except IndexError:
		return text

def internetarch(url):
	check = urllib2.urlopen('http://web.archive.org/' + url)
	
def createtemp(url, notemp = False):
	url = url.replace(' ', '_')
	if not notemp:
		cur = time.localtime()
		month = months[str(cur[1])]
		year = cur[0]
		day = cur[2]
		datefield = 'accessdate = %s-%s-%s' %(year, month, day)
		template = '{{cite web| url = %s | title = %s | %s }}' %(url, gettitle(url), datefield)
		return template
	else:
		return '[%s %s]' %(url, gettitle(url))


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
"""

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
		<textarea>%s</textarea>
		""" %(template)
	else:
		content = input_content
	print monobook.header('Template filler')
	print monobook.body(content)
	print monobook.navbar(other = 'http://code.google.com/p/legobot/source/browse/trunk/toolserver/public_html/cgi-bin/reflinks.py|Source')
	print monobook.footer()
	
if __name__ == "__main__":
	main()