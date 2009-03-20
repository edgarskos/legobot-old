#!usr/bin/python
import re, time, sys, os
sys.path.append(os.environ['HOME'] + '/pywiki')
from pywikibot import wiki, pagegen, timedate
wiki.setUser('Legobot')

def main():
	gen = pagegen.transclude(wiki.Page('Template:WikiProject Fungi'))
	table = ''
	for page in gen:
		table += do_page(page)
	putpage = wiki.Page('User:Legoktm/Bot')
	newcontent = '{| class="wikitable sortable" style="text-align: left;"\n|-\n! Article name\n! Size (bytes)\n! Rating\n! Last modified\n! # Incoming links\n' + table + '\n|}'
	putpage.put(newcontent, 'Testing bot')
def do_page(page):
	talk_page = page
	main_page = page.toggletalk()
	print 'Doing ' + main_page.title()
	lastedit = timedate.convertts(main_page.lastedit()['timestamp'])
	try:
		clas = wiki.parseTemplate(talk_page.get())['class']
	except KeyError:
		clas = ''
	if clas == 'GA':
		clas = '{{GA-inline}}'
	elif clas == 'FA':
		clas = '{{FA-inline}}'
	else:
		clas = clas.title()
	try:
		tablerow = '|-\n|| %s || %s || %s || %s || %s\n' %(main_page.aslink(), str(len(main_page.get())), clas, lastedit, str(len(pagegen.whatlinkshere(main_page))))
	except wiki.IsRedirectPage:
		return ''
	print tablerow,
	return tablerow

if __name__ == '__main__':
	main()