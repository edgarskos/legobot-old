#!usr/bin/python
#-*- coding:utf-8 -*-
__version__ = '$Id$'
import re, time, sys, os
sys.path.append(os.environ['HOME'] + '/pywiki')
from pywikibot import wiki, pagegen, timedate
wiki.setUser('Legobot')

def do_project(page, putpage):
	gen = pagegen.transclude(wiki.Page('Template:' + page))
	table = ''
	for page in gen:
		try:
			table += do_page(page)
		except:
			table += ''
	putpage1 = wiki.Page(putpage)
	newcontent = '{| class="wikitable sortable" style="text-align: left;"\n|-\n! Article name\n! Size (bytes)\n! Rating\n! Last modified\n! # Incoming links\n' + table + '\n|}'
	putpage1.put(newcontent, 'Bot: Updating article list')
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
	list = pagegen.whatlinkshere(main_page)
	num=0
	for i in list:
		num+=1
	try:
		tablerow = '|-\n|| %s || %s || %s || %s || %s\n' %(main_page.aslink(), str(len(main_page.get())), clas, lastedit, str(num))
	except wiki.IsRedirectPage:
		return ''
	except UnicodeEncodeError:
		return ''
	except UnicodeDecodeError:
		return ''
	print tablerow,
	return tablerow
def main():
	do_project('WikiProject Fungi','Wikipedia:WikiProject Fungi/fungus articles by size')
	do_project('WikiProject Egypt','Wikipedia:WikiProject_Egypt/Articles_by_size')

if __name__ == '__main__':
	main()