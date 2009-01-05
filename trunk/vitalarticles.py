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
# (C) Legoktm 2008
# 

import re, sys, time, os
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')
import wikipedia, pagegenerators, catlib
import legoktm
# Define global constants
readDelay  = 20	# seconds
writeDelay = 60 # seconds

def unicodify(text):
	return text.encode('utf-8')
def process_article(page, mainpage, edittedtext):
		print 'in proc art func'
		try:
			edittedtext = edittedtext.encode('utf-8')
		except UnicodeDecodeError:
			print 'exccept ude'
		#print edittedtext
		#Check what class it is, starting at the highest
		pagetext = page.get()
		if re.search('class=FA',pagetext,re.I):
			if not re.search('class=fail',pagetext,re.I):
				pagename = str(page)
				pgclass = ['FA', 'FA']
		elif re.search('class=A',pagetext,re.I):
			pagename = str(page)
			pgclass = ['A', 'A-icon']
		elif re.search('class=GA',pagetext,re.I):
			pagename = str(page)
			pgclass = ['GA', 'GAicon']
		elif re.search('class=B',pagetext,re.I):
			pagename = str(page)
			pgclass = ['B', 'B-icon']
		elif re.search('class=C',pagetext,re.I):
			pagename = str(page)
			pgclass = ['C', 'C-icon']
		elif re.search('class=stub',pagetext,re.I):
			pagename = str(page)
			pgclass = ['Stub', 'Stub-icon']
		elif re.search('class=start',pagetext,re.I):
			pagename = str(page)
			pgclass = ['Start', 'Start-icon']			

		else:
			print "No class assigned."
			return
		print str(mainpage) + " has a class of " + str(pgclass[0])
		pgtemp = str(pgclass[1])
		pgtempl = legoktm.templink(pgtemp)
		mainpage = str(mainpage)
		mpdlink = legoktm.delink(mainpage)
		#Check for FGANs, FFAs, and FFACs
		ffac=re.findall('action(.*)=FAC', pagetext)
		try:
			ffac= ffac[0]
			if re.search('currentstatus=FGAN',pagetext,re.I):
				pgclassother = ['FGAN','{{NoGA-icon}}']			
			elif re.search('currentstatus=FFA',pagetext,re.I):
				pgclassother = ['FFA', '{{NoFA}}']	
			elif re.search('action%sresult=not promoted' %(ffac),pagetext,re.I):
				pgclassother = ['FFAC', '{{FAC-icon}}']
			else:
				pgclassother = ['','']
		except IndexError:
			pgclassother = ['','']
		pgaltclass = pgclassother[1]
		if pgclassother[0] != '':
			print '%s has a action of %s' %(mainpage, pgclassother[0])
		else:
			print '%s has no other actions' %(mainpage)
		# Fix Casing (Reduces the number of possible expressions)
		vapage = wikipedia.Page(wikipedia.getSite(), 'Wikipedia:Vital articles')
		wikitext = edittedtext
#		print edittedtext
		find = '\{\{%s\}\} \[\[%s\]\]' %(pgtemp, mpdlink)
		shouldfind = u'{{%s}} [[%s]]' %(pgtemp, mpdlink)
		print find
#		print wikitext
		m=re.findall(find, wikitext)
		try:
			print m[0]
			if m[0] == shouldfind:
				print '[[WP:VA]] does not need updating for %s' %mainpage
				return wikitext
		except IndexError:
			print 'Not found, updating [[WP:VA]]'
		"""Following checks if the article is bolded"""
		boldcheck=re.findall('\'\'\'\[\[%s\]\]\'\'\'' %(mpdlink), wikitext)
		try:
			print boldcheck[0]
			bold=True
		except IndexError:
			print 'Not found'
			bold=False
		"""Done checking for bolding"""
		"""Check for howmany # signs, only checks for 3"""
		numcheck1=re.findall('\n(.*) (.*)\[\[%s\]\]' %(mpdlink), wikitext)
		numcheck=numcheck1[0][0]
		print numcheck
		find2= '(\{\{(.*)\}\}|) \[\[%s\]\]' %(mpdlink)
		if bold==True:
			find3= '%s(.*)\'\'\'\[\[%s\]\]\'\'\'' %(numcheck, mpdlink)
			rep= '%s %s{{%s}} \'\'\'[[%s]]\'\'\'' %(numcheck, pgaltclass, pgtemp, mpdlink)
		else:
			find3= '%s(.*)\[\[%s\]\]' %(numcheck, mpdlink)
			rep= '%s %s{{%s}} [[%s]]' %(numcheck, pgaltclass, pgtemp, mpdlink)
		try:
			wikitext = wikitext.encode('utf-8')
		except UnicodeDecodeError:
			print 'ude'
		wikitext = re.sub(find3, rep, wikitext)
		wikitext = re.sub(find2, shouldfind, wikitext)
#		wikipedia.output(u'WRITE:	Adding %s bytes.' % str(len(wikitext)-len(state0)))
#		vapage.put(wikitext, 'Updating rating for %s to %s' %(mainpage, pgtemp))	
		return unicodify(wikitext)				

def dp(page, text):
#	text = text.encode('utf-8')
#	print text
	print 'in dp func'
	site = wikipedia.getSite()
	page = wikipedia.Page(site, page)
#	time.sleep(30) #Wait so we don't lag servers to much
	if not page.isTalkPage():
		mainpage = page
		page = page.toggleTalkPage()
	newtext = process_article(page, mainpage, text)
	try:
		return unicodify(newtext)
	except UnicodeDecodeError:
		return newtext
