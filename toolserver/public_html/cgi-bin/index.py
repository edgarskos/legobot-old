#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# (C) Legoktm 2008-2011, MIT License
# 
import cgitb; cgitb.enable()
import monobook2
content = """\
<h1>Bots running here</h1>
<ul>
<li><a href="http://en.wikipedia.org/wiki/User:Legobot">Legobot</a></li>
<li><a href="http://en.wikipedia.org/wiki/User:Legobot II">Legobot II</a></li>
<li><a href="http://en.wikipedia.org/wiki/User:Legobot III">Legobot III</a></li>
<li><i><a href="http://en.wikipedia.org/wiki/User:ArticleAlertbot">ArticleAlertbot</a> -- <i>Inactive</i></li>
</ul>
<h1>Tools</h1>
<ul>
<li><a href="http://toolserver.org/~legoktm/cgi-bin/count.py">Raw edit counter</a></li>
<li><a href="http://toolserver.org/~legoktm/alertbot.html">Alertbot status</a></li>
<li><a href="http://toolserver.org/~legoktm/cgi-bin/reflinks.py">Template filler</a></li>
</ul>
<!--<h2>Beta Tools</h2>
<ul>
</ul>-->
"""
page = monobook2.Page('~legoktm','/~legoktm/cgi-bin/index.py')
print page.top()
print page.body(content)
print page.footer()
#print monobook.header('~legoktm')
#print monobook.body(content)
#print monobook.navbar()
#print monobook.footer()
