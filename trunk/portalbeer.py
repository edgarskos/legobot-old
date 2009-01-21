#!usr/bin/python
#
# (C) Legoktm 2008-2009, MIT License
# 
import sys, os, re
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')

import wikipedia as wiki


site = wiki.getSite()
page = 'Portal:Beer/Selected picture/'

#get page list
pages = []
num = 0
content = """\
{{Selected picture
| image   = 
| size    = 
| caption = 
| text    = 
| credit  = 
| link    = 
}}
"""
while num <=50:
	num +=1
	pages.append(wiki.Page(site,page + str(num)))
#for page in pages:
#	print page
#	wiki.showDiff(page.get(), content)
#	page.put(content, 'Updating per [[WP:BOTREQ]]')

raw_content = """\
{{Selected picture
| image   = 
| size    = 
| caption = 
| text    = 
| credit  = 
| link    = 
}}

[[Category:Wine Portal]]
"""


pagewine = 'Portal:Wine/Selected picture/'
pages1 = []
num = 0
while num <50:
	num +=1
	pages1.append(wiki.Page(site,pagewine + str(num)))
for page in pages1:
	print page
	try:
		wikitext = page.get()
		newtext = re.sub('Portal:Wine/Selected picture/Layout','Selected picture', wikitext)
		wiki.showDiff(wikitext, newtext)
		page.put(newtext, 'Updating per [[WP:BOTREQ]]')
	except wiki.NoPage:
		page.put(raw_content, 'Updating per [[WP:BOTREQ]]')