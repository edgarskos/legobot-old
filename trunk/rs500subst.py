#!/usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008, MIT License
# 
 
import re, sys, time
import os
import commonfixes #dispenser's common fixes
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')
import legoktm
import wikipedia, pagegenerators, catlib
# Define global constants
readDelay  = 20	# seconds
writeDelay = 60 # seconds
 
 
def process_article(page):
		EditMsg = "Robot: Substituting {{[[Template:RS500|RS500]]}} and common fixes"
		wikipedia.setAction(EditMsg)
		try:
			wikitext = page.get()
		except wikipedia.NoPage:
			return
		except wikipedia.IsRedirectPage:
			return
		# Fix Casing (Reduces the number of possible expressions)
		# Common fixes
#		wikitext = commonfixes.fix(wikitext)
		# State point.  Count any changes as needing an update if they're after this line
		state0 = wikitext
 
		# Add |Iran=yes
		wikitext = re.compile(r'\{\{\s*rs500(.*?)\}\}', re.IGNORECASE).sub(r'{{subst:RS500\1}}', wikitext)
 
		wikipedia.showDiff(page.get(), wikitext)
		if (wikitext != state0):
			try:
				wikipedia.output(u'WRITE:	Adding %s bytes.' % str(len(wikitext)-len(page.get())))
#				print 'Waiting 2.5 seconds'
#				time.sleep(2.5)
				page.put(wikitext)	
			except TypeError:
				print 'Skipping TypeError'
				return

 
site  = wikipedia.getSite()
transclusionPage = wikipedia.Page(wikipedia.getSite(), 'Template:RS500')
gen = pagegenerators.ReferringPageGenerator(transclusionPage, onlyTemplateInclusion = True)
for page in gen:
	process_article(page)
wikipedia.stopme()