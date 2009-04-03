#!usr/bin/python
import cgitb; cgitb.enable()
import BeautifulSoup as BS, monobook
import urllib, cgi, re, sys
sys.path.append('/home/legoktm')
print "Content-Type: text/html\n"


input_content = """\
<h2>Template filler</h2>
<br />
<form name="input" action="/~legoktm/cgi-bin/isbndb.py" method="get">

URL: <input type="text" name="isbn">

<br />
<input type="submit" value="Generate {{cite book}}">
</form>
"""
subpagelink = '<div id="contentSub"><span class="subpages">&lt; <a href="http://toolserver.org/~legoktm/cgi-bin/isbndb.py" title="isbndb.py">Template filler</a></span></div>'


def cite_web(data):
	isbn = data.isbndb.booklist.bookdata['isbn']
	title = re.findall('<title>(.*?)</title>', str(data.isbndb.booklist.bookdata.title))[0]
	try:
		authors = re.findall('<authorstext>(.*?)</authorstext>', str(data.isbndb.booklist.bookdata.authorstext))[0]
	except:
		authors = None
	if authors:
		authors = authors.split(' and')[0]
		split = authors.split(' ')
		if len(split) == 3:
			last = split[2]
			first = split[0]
		elif len(split) == 2:
			last = split[1]
			first = split[0]
		else: #wtf...
			authors = False
	
	list = ['|isbn=' + str(isbn), '|title=' + title]
	if authors:
		list.append('|last=' + last)
		list.append('|first=' + first)
	template = '{{cite web'
	for i in list:
		template += i
	template += '}}'
	return template
def main():
	import passcode
	key = passcode.code
	del passcode
	url = 'http://isbndb.com/api/books.xml?access_key=%s&index1=isbn&value1=%s'
	form = cgi.FieldStorage()
	try:
		isbn = form['isbn'].value
		value = True
	except KeyError:
		value = False
	if not value:
		printcontent(input_content)
		sys.exit()
	open = urllib.urlopen(url %(key, isbn))
	text = open.read()
	open.close()
	template = cite_web(BS.BeautifulStoneSoup(text))
	content = """\
	<h2>{{cite book}}</h2>
	%s
	<textarea>%s</textarea>
	""" %(subpagelink, template)
	printcontent(content)
	del key
def printcontent(content):
	return monobook.all('{{cite book}}',content,other = 'http://code.google.com/p/legobot/source/browse/trunk/toolserver/public_html/cgi-bin/isbndb.py|Source')
