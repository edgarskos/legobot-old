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
page = monobook2.Page('SVN Updater', '/~legoktm/cgi-bin/svnup.py')

def fullcontent(content):
    global page
    print page.top()
    print page.body(content)
    print page.footer()

username = page.getValue('username')
if username:
    code = page.getValue('code')
    import passcode
    if code == passcode.code:
        #remove the pass code
        passcode = ''
        del passcode
        run = True
        execute = getoutput('svn up /home/legoktm')
        execute2 = getoutput('svn up /home/legoktm/pythonwikibot')
        execute1 = getoutput('cd /home/legoktm/pythonwikibot/wiki; python generate_docs.py')
#        newcont = execute.replace('.py','.py<br />')
        newcont = execute.replace('\n','<br />')
        newcont1 = execute1.replace('\n','<br />')
        newcont2 = execute2.replace('\n','<br />')
        content = """\
        <h2>Result</h2><br />
        %s
        """ %(newcont+'\n'+newcont1+'\n'+newcont2)
        fullcontent(content)
    else:
        content = """\
        <h2>Error</h2>
        Incorrect Password.
        """
        fullcontent(content)
        sys.exit()
else:
    fullcontent(input_content)
