#!usr/bin/python
#
# (C) Legoktm 2008-2011, MIT License
# 
import re, sys, os
import urllib, string
import shlex
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pylegoktm')
import wikipedia, pagegenerators, catlib
import legoktm
#page = raw_input('What page? ')
def doarticle(page):
	key = "4ZK9WURM"
	try:
		wikitext = page.get()
	except wikipedia.IsRedirectPage:
		print 'Skipping %s as it is a redirect' %str(page)
		return
	state0 = wikitext
	import urllib
	m=re.findall(r'\<ref\>ISBN(:| )(.*)\</ref\>', wikitext)
	if len(m) == 0:
		print 'No changes needed in %s' %str(page)
		return
	else:
		print 'Checking %s' %str(page)
	print m
	try:
		m=string.join(m,'')
		m=m[1:]
	except TypeError:
		m=m[0][1]
	isbn = m
	f = urllib.urlopen("http://isbndb.com/api/books.xml?access_key="+key+"&results=authors&index1=isbn&value1=" + m)
	s = f.read()
	f.close()
	print s
	realisbn = re.findall(r'<BookData (.*) isbn="(.*)" (.*)">', s)
	try:
		realisbn=string.join(realisbn,'')
		realisbn=realisbn[1:]
	except TypeError:
		realisbn=realisbn[0][1]
	print 'The official ISBN is: ' +realisbn
	
	title=re.findall(r'\<Title\>(.*)\</Title\>', s)
	try:
		title=string.join(title,'')
	except TypeError:
		title=title[0][1]
	print 'Title is: ' + title
	auth=re.findall(r'\<Person person_id="(.*)"\>(.*)\</Person\>', s)
	print auth
	if len(auth) == 1:
		auth=auth[0][1]
	elif len(auth) == 2:
		auth=auth[0][0]
		auth2=auth[0][1]
	elif len(auth) >= 3:
		print 'Too many authors... skipping'
		return
	authsplit = re.split(',', auth)
	last = authsplit[0]
	first = authsplit[1]
	pubinfo=re.findall(r'\<PublisherText publisher_id="(.*)"\>(.*)</PublisherText\>', s)
	print pubinfo[0][0]
	a = urllib.urlopen("http://isbndb.com/api/publishers.xml?access_key="+key+"&results=details&index1=publisher_id&value1=" + pubinfo[0][0])
	a1=a.read()
	a.close()
	a=a1
	print a
	pub=re.findall(r'\<Name\>(.*)\</Name\>', a)
	print pub[0]
	loc=re.findall(r'\<Details location="(.*)\((.*)\)" /\>', a)
	print loc[0][0]
	temp = u'<ref name="'+title+'">{{cite book |title= '+title+'|last= '+last+'|first= '+first+'|isbn= '+realisbn+'|publisher='+pub[0]+'|location='+loc[0][0]+'}} <!--ISBN Converted by Bot --></ref>'
	wikitext = re.sub('\<ref\>ISBN(:| )(.*)\</ref\>', temp, wikitext)
	wikipedia.showDiff(state0, wikitext)
	try:
		prompt = raw_input('Would you like to accept the changes? [y][n][q] ')
	except KeyboardInterrupt:
		print '\n'
		wikipedia.stopme()
		sys.exit()
	if prompt == 'y':
		page.put(wikitext, 'Fixing raw ISBN')
		done = True
	elif prompt == 'n':
		return False
	elif prompt == 'q':
		wikipedia.stopme()
		sys.exit()
	else:
		print 'Error: Invalid choice, skipping %s' %(str(page))
	return done
site = wikipedia.getSite()
cat = catlib.Category(site, 'Books')
#gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)
page=wikipedia.Page(site, 'User:Legoktm/Bot')
doarticle(page)
for page in gen:
	doarticle(page)
