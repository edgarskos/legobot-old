#!usr/bin/python
#
# (C) Legoktm 2008-2011, MIT License
# 
import re, os, sys
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')
import wikipedia
def createredir(origname):
	site = wikipedia.getSite()
	redircontent = re.sub('OH', 'Ohio', origname)
	redircontent = '#REDIRECT [[%s]]' %(redircontent)
	page = wikipedia.Page(site, origname)
	print page
	wikipedia.showDiff('', redircontent)
	page.put(redircontent, 'Creating redirect per [[WP:BOTREQ#Need_some_redlinks_to_become_redirects|BOTREQ]]')


createredir("German Township, Montgomery County, OH")
wikipedia.stopme()
