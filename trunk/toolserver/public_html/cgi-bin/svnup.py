#!/usr/bin/python
import cgitb; cgitb.enable()
import cgi, sys
from commands import getoutput
sys.path.append('/home/legoktm')

import monobook

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
	return monobook.header('SVN Updater') + monobook.body(content) + monobook.navbar() + monobook.footer()
form = cgi.FieldStorage()
try:
	username = form["username"].value
	value = True
except:
	value = False
if value:
	code = form["code"].value
	import passcode
	if code == passcode.code:
		#remove the pass code
		passcode = ''
		run = True
		execute = getoutput('cd /home/legoktm; svn up')
		content = """\
		<h2>Result</h2><br />
		%s
		""" %(execute)
		print fullcontent(content)
	else:
		content = """\
		<h2>Error</h2>
		Incorrect Password.
		"""
		print fullcontent(content)
		sys.exit()
else:
	print fullcontent(input_content)