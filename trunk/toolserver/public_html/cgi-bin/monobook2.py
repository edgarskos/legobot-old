#!usr/bin/python
# -*- coding: utf-8  -*-
# (C) Legoktm 2008-2011, MIT License

__version__ = '$Id$'
import cgitb; cgitb.enable()
import os, cgi, urllib
#
#(C) 2009 Legoktm, MIT License
#
import monobook
class Page:
    def __init__(self, name, repmess = 'status'):
        try:
            self.qstring = dict(cgi.parse_qsl(os.environ['REQUEST_URI'].split('?')[1]))
        except IndexError:
            self.qstring = {}
        except KeyError:
            self.qstring = {}

        self.name = name
        try:
            self.location = os.environ['SCRIPT_FILENAME']
        except KeyError:
            self.location = ''
        try:
            self.urllocation = 'http://toolserver.org' + os.environ['SCRIPT_NAME']
        except KeyError:
            self.urllocation = ''
        self.repmess = repmess
    def getValue(self, name):
        try:
            return self.qstring[name]
        except:
            return ''
    def top(self):
        """
        Returns the header with all JS and CSS.
        """
        head = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
<head>
  <title>"""+self.name+"""</title>
  <link rel="stylesheet"           href="/~dispenser/resources/monobook.css" type="text/css" title="Monobook" />
  <!--link rel="alternate stylesheet" href="../resources/terminal.css" type="text/css" title="Terminal" />
  <link rel="alternate stylesheet" href="//wiki.ts.wikimedia.org/w/skins/chick/main.css" type="text/css" title="Chick" />
  <link rel="alternate stylesheet" href="//wiki.ts.wikimedia.org/w/skins/simple/main.css" type="text/css" title="Simple" /-->
  <link rel="stylesheet" href="/~dispenser/resources/common.css" type="text/css" />
	<!--[if lt IE 5.5000]><style type="text/css">@import "http://en.wikipedia.org/skins-1.5/monobook/IE50Fixes.css?116";</style><![endif]-->
	<!--[if IE 5.5000]><style type="text/css">@import "http://en.wikipedia.org/skins-1.5/monobook/IE55Fixes.css?116";</style><![endif]-->

	<!--[if IE 6]><style type="text/css">@import "http://en.wikipedia.org/skins-1.5/monobook/IE60Fixes.css?116";</style><![endif]-->
	<!--[if IE 7]><style type="text/css">@import "http://en.wikipedia.org/skins-1.5/monobook/IE70Fixes.css?116";</style><![endif]-->
	<!--[if lt IE 7]><script type="text/javascript" src="http://en.wikipedia.org/skins-1.5/common/IEFixes.js?116"></script>
	<meta http-equiv="imagetoolbar" content="no" /><![endif]-->
</head>


<body class="mediawiki ltr">
	<div id="globalWrapper">
		<div id="column-content">
	<div id="content">
		<a name="top" id="top"></a>
<h1 class="firstHeading">"""+self.name+"""</h1>

		<div id="bodyContent">
			<h3 id="siteSub"></h3>
			<div id="contentSub"></div>

    """

        return head

    def body(self, content):
        """
        Returns the content surrounded by comments.
        """
        text = '<!-- Start Content -->'
        if self.qstring.has_key('action'):
            if self.qstring['action'] == 'source':
                text += """
<div id="viewsourcetext">You can view and copy the source of this page:</div>
<textarea id="wpTextbox1" name="wpTextbox1" cols="80" rows="25" readonly="readonly">
"""+content.replace('<','&lt;').replace('>','&gt;')+"""
</textarea>
"""

            elif self.qstring['action'] == 'view':
                text += content
            else:
                self.qstring['action'] = 'view' #someone added a weird action
                text += content
        else: #default to action == view
            self.qstring['action'] = 'view'
            text += content
        text += """
<!-- tabs -->
<div id="p-cactions" class="portlet" style="top:-1.7em;left:0;">
  <div class="pBody">
    <ul>
    """
        if self.qstring['action'] == 'view':
            del self.qstring['action']
            text += """
<li class="selected"><a href=\""""+self.urllocation+"""\">Page</a></li>
<li><a href=\""""+self.urllocation+"""?action=source&"""+urllib.urlencode(self.qstring)+"""\">View source</a></li>
"""
        elif self.qstring['action'] == 'source':
            text += """
<li><a href=\""""+self.urllocation+"""\">Page</a></li>
<li class="selected"><a href=\""""+self.urllocation+"""?action=source&"""+urllib.urlencode(self.qstring)+"""\">View source</a></li>
"""
        text += """
      </ul>
  </div>
</div>
"""
        text += '<!-- End Content -->\n'
        return text
    def footer(self):
        """
        Returns the footer and navbar.
        """
        text = """
            <div class="visualClear"></div>
		</div>
	</div>
		</div>
<div id="column-one">
	<div class="portlet" id="p-logo">
		<a href="../view/Main_Page"></a>
	</div>

	<div class='portlet' id='p-personal'>
		<h5>Interaction</h5>
		<div class='pBody'>
			<ul>
				<li><a href="/~legoktm/cgi-bin/index.py">Main page</a></li>
                <li><a href="http://code.google.com/p/legobot/source/browse#svn/trunk/toolserver">Subversion</a></li>
                <li><a href="http://code.google.com/p/legobot/issues/list">Bug Tracker</a></li>

			</ul>

		</div>
	</div>
	<div class='portlet'>
		<h5>Tools</h5>
		<div class='pBody'>
			<ul>
				<li><a href="/~legoktm/cgi-bin/count.py">Edit Counter</a></li>
				<li><a href="/~legoktm/cgi-bin/reflinks.py">Template filler</a></li>
			</ul>
		</div>
        <h5>Status</h5>
        <div class='pStatus'>
            """+"""
	</div>

		</div>

<div class="visualClear"></div>
<div id="footer">
<a href="/" id="f-poweredbyico"><img src="/images/wikimedia-toolserver-button.png" alt="Powered by the Wikimedia Toolserver" title="About this server" width="88" height="31" /></a>
<a href="http://validator.w3.org/check?uri=referer" id="f-copyrightico"><img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Transitional" height="31" width="88" title="Validation dependent on wiki code" /></a>
Maintained by
<a href="http://en.wikipedia.org/wiki/User:Legoktm" class="extiw">Legoktm</a>
(<a href="http://en.wikipedia.org/wiki/User_talk:Legoktm" class="extiw">Talk</a>).
</div>

</div></body>
</html>"""
        return text
