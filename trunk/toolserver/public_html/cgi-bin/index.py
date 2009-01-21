#!/usr/bin/env python
#
# (C) Legoktm 2008-2009, MIT License
# 
import cgitb; cgitb.enable()
import monobook
content = """\
<h1>Bots running here</h1>
<ul>
<li><a href="http://en.wikipedia.org/wiki/User:Legobot">Legobot</a></li>
<li><a href="http://en.wikipedia.org/wiki/User:ArticleAlertbot">ArticleAlertbot</a></li>
</ul>
<h1>Tools</h1>
<ul>
<li><a href="http://toolserver.org/~legoktm/count.html">Raw edit counter</a></li>
<li><a href="http://toolserver.org/~legoktm/alertbot.html">Alertbot status</a></li>
</ul>
"""

print monobook.header('~legoktm')
print monobook.body(content)
print monobook.navbar()
print monobook.footer()