#!/usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008-2009, MIT License
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
		EditMsg = "Robot: Tagging {{Football|Iran=yes}}"
		wikipedia.setAction(EditMsg)
		try:
			wikitext = page.get()
		except wikipedia.NoPage:
			page.put("{{Football|Iran=yes}}")
			return
		except wikipedia.IsRedirectPage:
			return
		if re.search('Iran=yes',wikitext,re.I):
			print "Skipping " + str(page)
			return
		# Fix Casing (Reduces the number of possible expressions)
		wikitext = re.compile(r'\{\{\s*(template:|)football', re.IGNORECASE).sub(r'{{Football', wikitext)
		# Common fixes
		wikitext = commonfixes.fix(wikitext)
		# State point.  Count any changes as needing an update if they're after this line
		state0 = wikitext
 
		# Add |Iran=yes
		wikitext = re.compile(r'\{\{\s*football(.*?)\}\}', re.IGNORECASE).sub(r'{{Football\1|Iran=yes}}', wikitext)
 
		wikipedia.showDiff(page.get(), wikitext)
 
		if (wikitext != state0):
			try:
				wikipedia.output(u'WRITE:	Adding %s bytes.' % str(len(wikitext)-len(state0)))
				page.put(wikitext)	
			except:
				wikipedia.output(u'ERROR:	Except raised while writing.')
 
def dogen(gen):
	for page in gen:
		if not page.isTalkPage():
	        	page = page.toggleTalkPage()
		process_article(page)
 
def docat(cat2):
	site  = wikipedia.getSite()
	cat = catlib.Category(site, cat2)
	gen = pagegenerators.CategorizedPageGenerator(cat)
	dogen(gen)
	wikipedia.output(u'\nFinished with Category:' + cat2 + '.\n')
 
 
def main():
 
	docat("Defunct Iranian football clubs")
	docat("Esteghlal FC")
	docat("Esteghlal FC players")
	docat("Esteghlal F.C. seasons")
	docat("Persepolis F.C.")
	docat("Persepolis F.C. managers")
	docat("Persepolis F.C. non-playing staff")
	docat("Persepolis F.C. players")
	docat("Persepolis F.C. seasons")
	docat("Persepolis F.C. templates")
	docat("Sepahan F.C.")
	docat("Sepahan players")
	docat("Sepahan F.C. managers")
	docat("Sepahan F.C. seasons")
	docat("Sepahan F.C. templates")
	docat("Iran football club stubs")
	docat("Iranian football competitions")
	docat("Defunct Iranian football competitions")
	docat("Expatriate footballers in Iran")
	docat("Iranian footballers")
	docat("Iran international footballers")
	docat("Iranian expatriate footballers")
	docat("Olympic footballers of Iran")
	docat("Iranian football biography stubs")
	docat("Footballers in Iran by club")
	docat("Aboomoslem players")
	docat("Bargh Shiraz players")
	docat("Damash Gilan players")
	docat("Esteghlal Ahvaz players")
	docat("Esteghlal FC players")
	docat("Fajr Sepasi players")
	docat("Foolad FC players")
	docat("Malavan players")
	docat("Mes Kerman players")
	docat("Pas players")
	docat("Paykan players")
	docat("Pegah Gilan players")
	docat("Persepolis F.C. players")
	docat("Rah Ahan players")
	docat("Saba Battery players")
	docat("Saipa players")
	docat("Sepahan players")
	docat("Shirin Faraz Kermanshah players")
	docat("Zob Ahan players")
	docat("IPL Club Templates")
	docat("Iranian football managers")
	docat("Football managers in Iran")
	docat("Football managers in Iran by club")
	docat("Persepolis F.C. managers")
	docat("Sepahan F.C. managers")
	docat("Non-Iranian football managers in Iran")
	docat("Iran national football team")
	docat("Iran international footballers")
	docat("Iran national football team managers")
	docat("Iran national football team templates")
	docat("Iranian football referees")
	docat("Iranian football squad templates")
	docat("Iran national football team templates")
	docat("Football venues in Iran")
	docat("Women's football in Iran")
	docat("Iran football (soccer) templates")
	docat("Iran football (soccer) club templates")
	docat("Persepolis F.C. templates")
	docat("Sepahan F.C. templates")
 
 
if __name__ == "__main__":
	try:
		main()
	finally:
		wikipedia.stopme()
