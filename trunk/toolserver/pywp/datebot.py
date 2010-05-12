#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
This script is a clone of [[en:User:SmackBot]]
Syntax: python datebot.py
"""

#
# (C) Legoktm 2008-2009, MIT License
# 
__version__ = '$Id$'
import re, sys, time
import os
sys.path.append(os.environ['HOME'] + '/legobot2')
import wikipedia as wiki
import pagegenerators as pagegen
import catlib
import timedate
# Define global constants
readDelay  = 20	# seconds
writeDelay = 60 # seconds
logfile = "datebot-errors.log"
site=wiki.getSite()

def checktalk():
	page = wiki.Page(site,'User:Legobot II/Stop')
	try:
		wikitext = page.get()
	except:
		sys.exit("Error: Cannot acess stop page")
	if wikitext.lower() != 'run':
		sys.exit("Error: Runpage disabled")
def log_error(page,disp_only=False):
	"""
	Logging an error on a page due to any reason
	page should be the wiki.Page object
	disp_only should be true when only wanting to view the list, not add anything to it.
		Then page should be just set to 0 (ex use: log_error(page=0,disp_only=True) )
	"""
	if not disp_only:
		print 'Logging error on ' + page.title()
		try:
			f1 = open(logfile, 'r')
			old = f1.read()
			f1.close()
		except IOError:
			old = ""
		new = old + '\n' + page.title()
		f2 = open(logfile, 'w')
		f2.write(new)
		f2.close()
	else:
		try:
			f1 = open(logfile, 'r')
			txt = f1.read()
			f1.close()
		except IOError:
			txt = "Log is non-existent."	
		print txt
def process_article(page):
	month_name = timedate.monthname(timedate.currentmonth())
	year = str(timedate.currentyear())
	try:
		wikitext = state1 = page.get()
	except wiki.IsRedirectPage:
		log_error(page)
		return
	# Fix Casing (Reduces the number of possible expressions)
	wikitext = re.compile(r'\{\{\s*(template:|)fact', re.IGNORECASE).sub(r'{{Fact', wikitext)
	# Fix some redirects
	wikitext = re.compile(r'\{\{\s*(template:|)cn\}\}', re.IGNORECASE).sub(r'{{Fact}}', wikitext)
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
#	wikitext = re.compile(r'\{\{\s*merge(.*?)\}\}', re.IGNORECASE).sub(r'{{Merge\\1|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
	wikitext = re.compile(r'\{\{\s*copyedit\}\}', re.IGNORECASE).sub(r'{{Copyedit|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
	wikitext = re.compile(r'\{\{\s*refimprove\}\}', re.IGNORECASE).sub(r'{{Refimprove|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
	wikitext = re.compile(r'\{\{\s*primary sources\}\}', re.IGNORECASE).sub(r'{{Primary sources|date={{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}}}}', wikitext)
	wikitext = wikitext.replace('{{subst:CURRENTMONTHNAME}}', month_name)
	wikitext = wikitext.replace('{{subst:CURRENTYEAR}}', year)
	EditMsg = "[[WP:BOT|BOT]]: Date maintenance tags"
	if state1 != state0:
		EditMsg = EditMsg + " and general fixes"
	# If the text has changed at all since the state point, upload it
	if wikitext != state0:
		print 'Editing ' + page.title()
		print 'WRITE:	Adding %s bytes.' % str(len(wikitext)-len(state1))
		try:
			page.put(wikitext, EditMsg)
		except:
			log_error(page)
#		except KeyboardInterrupt:
#			quit()
#		except:
#			print 'ERROR:	Except raised while writing.'
	else:
		print 'Skipping ' + page.title() + ' due to no changes made after state point.'
		log_error(page)
def docat(cat2):
	pg = wiki.Page(site,cat2)
	print pg
	print type(pg)
	category = catlib.Category(site, cat2)
	print 'Fetching Category:' + cat2
 	gen = pagegen.CategorizedPageGenerator(category)
	for page in gen:
		if page.namespace() == 0:
			try:
				process_article(page)
			except UnicodeEncodeError:
				log_error(page)
				pass
			checktalk()
		else:
			print 'Skipping %s because it is not in the mainspace' %(page.title())
			log_error(page)
	print 'Done with Category:%s' %(cat2)
def main():
	docat(u"Articles with unsourced statements")
	docat(u"Articles that need to be wikified")
	docat(u"Orphaned articles")
	docat(u"Category needed")
	docat(u"Uncategorized stubs")
	docat(u"Wikipedia cleanup")
	docat(u"Articles lacking sources")
	docat(u"Articles to be expanded")
	docat(u"Articles with topics of unclear notability")
#	docat(u"Articles to be merged")
	docat(u"Wikipedia articles needing copy edit")
	docat(u"Articles needing additional references")
	docat(u"Articles lacking reliable references")
	print 'Done'
	
if __name__ == "__main__":
	main() #run it
	log_error(page=0,disp_only=True) #view error log
