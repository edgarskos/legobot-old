#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
This script is a clone of [[en:User:SmackBot]]
Syntax: python datebot.py [pagegenerator option]

Pagegenerator options:

-file:       Update pages listed in a text file.
-ref:        Update pages transcluding from a given page.
-cat:        Update pages from the given category.
-links:      Update pages linked from a given page.
-page:       Update that page.

"""

#
# (C) Legoktm 2008-2009, MIT License
# 

import re, sys, time
import os
sys.path.append('/home/legoktm/legobot2')
import wikipedia, pagegenerators, catlib

# Define global constants
readDelay  = 20	# seconds
writeDelay = 60 # seconds

def checktalk():
	page = wikipedia.Page('User:Legobot II/Stop')
	try:
		wikitext = page.get()
	except:
		sys.exit()
	if wikitext.lower() != 'run':
		sys.exit()
def process_article(page):
		wikitext = state1 = page.get()
		
		# Fix Casing (Reduces the number of possible expressions)
		wikitext = re.compile(r'\{\{\s*(template:|)fact', re.IGNORECASE).sub(r'{{Fact', wikitext)
		# Fix some redirects
		if not re.search('cnote', wikitext, re.I):
			wikitext = re.compile(r'\{\{\s*(template:|)cn', re.IGNORECASE).sub(r'{{Fact', wikitext)
		wikitext = re.compile(r'\{\{\s*(template:|)citation needed', re.IGNORECASE).sub(r'{{Fact', wikitext)
		wikitext = re.compile(r'\{\{\s*(template:|)proveit', re.IGNORECASE).sub(r'{{Fact', wikitext)
		wikitext = re.compile(r'\{\{\s*(template:|)sourceme', re.IGNORECASE).sub(r'{{Fact', wikitext)
		wikitext = re.compile(r'\{\{\s*(template:|)fct', re.IGNORECASE).sub(r'{{Fact', wikitext)
		# State point.  Count any changes as needing an update if they're after this line
		state0 = wikitext
		
		# Date the tags
		wikitext = re.compile(r'\{\{\s*fact\}\}', re.IGNORECASE).sub(r'{{Fact|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*wikify\}\}', re.IGNORECASE).sub(r'{{Wikify|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*orphan\}\}', re.IGNORECASE).sub(r'{{Orphan|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*uncategorized\}\}', re.IGNORECASE).sub(r'{{Uncategorized|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*uncatstub\}\}', re.IGNORECASE).sub(r'{{Uncatstub|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*cleanup\}\}', re.IGNORECASE).sub(r'{{Cleanup|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*unreferenced\}\}', re.IGNORECASE).sub(r'{{Unreferenced|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*importance\}\}', re.IGNORECASE).sub(r'{{importance|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*Expand\}\}', re.IGNORECASE).sub(r'{{Expand|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
#		wikitext = re.compile(r'\{\{\s*merge(.*?)\}\}', re.IGNORECASE).sub(r'{{Merge\\1|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*copyedit\}\}', re.IGNORECASE).sub(r'{{Copyedit|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		wikitext = re.compile(r'\{\{\s*refimprove\}\}', re.IGNORECASE).sub(r'{{Refimprove|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
		EditMsg = "Date maintenance tags"
		if page.get() != state0:
			EditMsg = EditMsg + " and general fixes"
		
		
		wikipedia.setAction(EditMsg)
	
		# If the text has changed at all since the state point, upload it
		if (wikitext != state0):
			try:
				print 'Editing ' + str(page)
				wikipedia.output(u'WRITE:	Adding %s bytes.' % str(len(wikitext)-len(state0)))
#				wikipedia.showDiff(state1, wikitext)
				page.put(wikitext)
			except KeyboardInterrupt:
				wikipedia.stopme()
				quit()
			except:
				print 'ERROR:	Except raised while writing.'
		else:
			print 'Skipping ' + str(page)
def docat(cat2):
	site  = wikipedia.getSite()
	cat = catlib.Category(site, cat2)
	gen = pagegenerators.CategorizedPageGenerator(cat)
	for page in gen:
		if page.namespace() != 2 or page.namespace() != 3 or page.namespace() != 14:
			process_article(page)
			checktalk()
		else:
			print 'Skipping %s because it is not in the mainspace' %(str(page))
	print 'Done with Category:%s' %(cat2)
def main():
	docat("Articles with unsourced statements")
	docat("Articles that need to be wikified")
	docat("Orphaned articles")
	docat("Category needed")
	docat("Uncategorized stubs")
	docat("Wikipedia cleanup")
	docat("Articles lacking sources")
	docat("Articles to be expanded")
	docat("Articles with topics of unclear notability")
	docat("Articles to be merged")
	docat("Wikipedia articles needing copy edit")
	docat("Articles needing additional references")
	
	wikipedia.output(u'\nOperation Complete.\n')

if __name__ == "__main__":
	try:
		main()
	finally:
		wikipedia.stopme()