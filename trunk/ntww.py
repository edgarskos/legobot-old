import sys, os
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')
import wikipedia, pagegenerators
def getfrommeta():
	meta = wikipedia.getSite(code = 'meta', fam = 'meta')
    wp = wikipedia.getSite(code = 'en', fam = 'wikipedia')
	mtemp = wikipedia.Page(meta, 'Template:Wikivoices subscription')
	mtemptext = mtemp.get()
	wptemp = wikipedia.Page(wp, 'Template:Wikivoices subscription')
	wikipedia.showDiff(mtemptext, wptemp.get())
	if mtemptext != wptemp.get()
		get = True
		wptemp.put(mtemptext, "Updating NTWW from content from [[m:Template:Wikivoices subscription]]")
	else:
		get = False
	return get
def subscribers():
	message = """\n==New [[m:Wikivoices|Wikivoices]] episode==\n
	See [[m:Wikivoices|Wikivoices]] for the latest episode.\n
	See what the next skypecast might be about [[m:Wikivoices#Our next Skypecast|here]], and sign up [[m:Wikivoices#Participants|here]].
	<small>This message was delivered to you because you were listed [[Wikipedia:NotTheWikipediaWeekly/Subscription|here]].\n
	If you wish to stop receiving these messages, simply remove your name from the list. ~~~~ </small>
	"""
	wp = wikipedia.getSite(code = 'en', fam = 'wikipedia')
	page = wikipedia.Page(wp, 'Wikipedia:Wikivoices/Subscription')
	gen = pagegenerators.LinkedPageGenerator(page)
	for page in gen:
		if not page.isTalkPage():
			return
		else:
			text = page.get()
			text = text + message
			page.put(text, '[[m:Wikivoices|Wikivoices]] delivery', minorEdit=False)
			x = x + 1
	return x
if __name__ == "__main__":
	try:
		get = getfrommeta()
		if get == True:
			x = 0
			num = subscribers()
			print "Messages were sent out to %s people" %(num)
	finally:
		wikipedia.stopme()