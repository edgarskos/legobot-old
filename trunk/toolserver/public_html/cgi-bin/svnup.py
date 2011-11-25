#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# (C) Legoktm 2008-2011, MIT License
# 
import cgitb; cgitb.enable()
import cgi, sys, re
from commands import getoutput
sys.path.append('/home/legoktm')

__version__ = '$Id$'
import monobook2

input_content = """\
    <h2>Run subversion update</h2>
<form name="input" action="/~legoktm/cgi-bin/svnup.py" method="get">

Username: <input type="text" name="username">

<br />
Passcode: <input type="password" name="code"> <i>(Ask Legoktm)</i>
<br />
<input type="submit" value="Run">
</form>
"""

def fullcontent(content):
    page = monobook2.Page('SVN Updater', '/~legoktm/cgi-bin/svnup.py')
    print page.top()
    print page.body(content)
    print page.footer()

def main()"
	username = page.getValue('username')
	if username:
		code = page.getValue('code')
		import passcode
		if code == passcode.code:
			#remove the pass code
			passcode = ''
			del passcode
			run = True
			execute = getoutput('svn up /home/legoktm') + '\n'
			execute += getoutput('svn up /home/legoktm/pythonwikibot') + '\n'
			execute += getoutput('cd /home/legoktm/pythonwikibot/wiki; python generate_docs.py') + '\n'
			newcont = execute.replace('\n','<br />')
			content = """\
			<h2>Result</h2><br />
			%s
			""" %(newcont)
			fullcontent(content)
		else:
			content = """\
			<h2>Error</h2>
			Incorrect Password.
			"""
			fullcontent(content)
			sys.exit(1)
	else:
		fullcontent(input_content)

if __name__ == "__main__":
	main()
