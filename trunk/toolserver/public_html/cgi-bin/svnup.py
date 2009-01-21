#!/usr/bin/python
import cgitb; cgitb.enable()
import cgi, sys
import commands

import monobook

content = """\
	<h2>Run subversion update</h2>
<form name="input" action="/~legoktm/cgi-bin/svnup.py" method="get">

Username: <input type="text" name="username">

<br />
Passcode: <input type="text" name="code"> <i>Ask Legoktm</i>
<br />
<input type="submit" value="Run">
</form>
"""

print monobook.header('SVN Updater')
print monobook.body(content)
print monobook.navbar()
print monobook.footer()