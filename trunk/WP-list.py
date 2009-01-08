#!usr/bin/python
import os, sys, re
sys.path.append(os.environ['HOME'] + '/pyenwiki')
import wikipedia, catlib, pagegenerators
def unicodify(text):
    if not isinstance(text, unicode):
        return text.decode('utf-8')
    return text
def delink(link):
	link = re.compile(r'\[\[(.*?)\]\]', re.IGNORECASE).sub(r'\1', link)
	return link
site = wikipedia.getSite()
def createlist(cat, wpproj, raw = False):
	category = catlib.Category(site, cat)
	gen = pagegenerators.CategorizedPageGenerator(category, recurse=True)
	wikitext = ''
	wikitext2 = ''
	for page in gen:
		wikitext = wikitext+'\n*'+str(page)
		link = delink(str(page))
		print link
		wikitext2 = wikitext2+'\n'+link
	wikitext = unicodify(wikitext)
	page = wikipedia.Page(site, wpproj + '/Articles')
	page.put(wikitext, 'Updating watchlist (Trial BRFA)')

	wikitext2 = '<pre>\n' + wikitext2 + '\n</pre>'
	wikitext2 = unicodify(wikitext2)
	if raw == True:
		page = wikipedia.Page(site, wpproj + '/Articles/raw')
		page.put(wikitext2, 'Updating raw watchlist (Trial BRFA)')

createlist('Canadian football', 'Wikipedia:WikiProject Canadian football', raw = True)
# Define some namespaces
ARTICLE = 0
ARTICLE_TALK = 1
USER = 2
USER_TALK = 3
WIKIPEDIA = 4
WIKIPEDIA_TALK = 5
IMAGE = 6
IMAGE_TALK = 7
TEMPLATE = 10
TEMPLATE_TALK = 11
CATEGORY = 14
CATEGORY_TALK = 15
PORTAL = 100
PORTAL_TALK = 101
def watchbot(projtemp, project, count = True):
	# a list for all articles
    articles = []
    # a list for all article talk pages
    articlesTalk = []
    # a list for all Wikipedia pages
    wikis = []
    # a list for all Wikipedia talk pages
    wikisTalk = []
    # a list for all templates
    templates = []
    # a list for all template talk pages
    templatesTalk = []
    # a list for all categories
    categories = []
    # a list for all category talk pages
    categoriesTalk = []
    # a list for all images
    images = []
    # a list for all image talk pages
    imagesTalk = []
    # a list for all portals
    portals = []
    # a list for all portal talk pages
    portalsTalk = []
	#null wikitext so it is blank pre
	wikitext = ''
	temp = wikipedia.Page(site, 'Template:' + projtemp)
	gen = pagegenerators.ReferringPageGenerator(temp, onlyTemplateInclusion = True)
	for page in gen:
		if page.namespace() == 0:
			articles.append(page)
		if page.namespace() == 1:
			articlesTalk.append(page)
			return
		if page.namespace() == 4:
			wikis.append(page)
		if page.namespace() == 5:
			wikisTalk.append(page)
			return
		if page.namespace() == 6:
			images.append(page)
		if page.namespace() == 7:
			imagesTalk.append(page)
			return
		if page.namespace() == 10:
			templates.append(page)
		if page.namespace() == 11:
			templatesTalk.append(page)
			return
		if page.namespace() == 14:
			categories.append(page)
		if page.namespace() == 15:
			categoriesTalk.append(page)
			return
		if page.namespace() == 100:
			portals.append(page)
		if page.namespace() == 101:
			portalsTalk.append(page)
			return
		else:
			return
		wikitext += '[[%s]] ([[%s]])\n' %(page, page.toggleTalkPage())
	putpage = wikipedia.Page(site, project + '/Articles')
	wikipedia.showDiff(putpage.get(), wikitext)