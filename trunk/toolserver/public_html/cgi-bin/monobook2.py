#!usr/bin/python
# -*- coding: utf-8  -*-

__version__ = '$Id$'

#
#(C) 2009 Legoktm, MIT License
#
import monobook
class Page:
    def __init__(self, name, location, repmess = 'status'):
        self.name = name
        self.location = location
        self.repmess = repmess
    def top(self):
        """
        Returns the header with all JS and CSS.
        """
        head = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta http-equiv="Content-Style-Type" content="text/css" />
		<link rel="search" type="application/opensearchdescription+xml" href="/w/opensearch_desc.php" title="Wikipedia (en)" />
		<title>%s</title>
		<link rel="stylesheet" href="http://en.wikipedia.org/skins-1.5/monobook/main.css?207xx" type="text/css" media="screen" />
		<!--[if lt IE 5.5000]><link rel="stylesheet" href="http://en.wikipedia.org/skins-1.5/monobook/IE50Fixes.css?207xx" type="text/css" media="screen" /><![endif]-->
		<!--[if IE 5.5000]><link rel="stylesheet" href="http://en.wikipedia.org/skins-1.5/monobook/IE55Fixes.css?207xx" type="text/css" media="screen" /><![endif]-->
		<!--[if IE 6]><link rel="stylesheet" href="http://en.wikipedia.org/skins-1.5/monobook/IE60Fixes.css?207xx" type="text/css" media="screen" /><![endif]-->
		<!--[if IE 7]><link rel="stylesheet" href="http://en.wikipedia.org/skins-1.5/monobook/IE70Fixes.css?207xx" type="text/css" media="screen" /><![endif]-->
		<link rel="stylesheet" href="http://en.wikipedia.org/w/index.php?title=MediaWiki:Monobook.css&amp;usemsgcache=yes&amp;ctype=text%2Fcss&amp;smaxage=2678400&amp;action=raw&amp;maxage=2678400" type="text/css" />
		<link rel="stylesheet" href="http://en.wikipedia.org/w/index.php?title=-&amp;action=raw&amp;maxage=2678400&amp;gen=css" type="text/css" />
		<!--[if lt IE 7]><script type="text/javascript" src="http://en.wikipedia.org/skins-1.5/common/IEFixes.js?207xx"></script>
		<meta http-equiv="imagetoolbar" content="no" /><![endif]-->
        </head>
    """ %(self.title)
        bodystart = """
    <body class="mediawiki ltr ns-0 ns-subject page-Main_Page skin-monobook">
	<div id="globalWrapper">
		<div id="column-content">
	<div id="content">
		<a name="top" id="top"></a>
		<h1 id="firstHeading" class="firstHeading">%s</h1>
		<div id="bodyContent">
			<h3 id="siteSub">< <a href="/~legoktm/cgi-bin/index.py">Main Page</a></h3>
			<div id="contentSub"></div>
    """ %(self.title)

        return start+bodystart

    def body(self, content):
        """
        Returns the content surrounded by comments.
        """
        text = '<!-- Start Content -->'
        text += content
        text += '<!-- End Content -->\n</div>'
        return text
    def footer(self):
        """
        Returns the footer and navbar.
        """
        text = """
<div id="column-one">
	<div id="p-cactions" class="portlet">
		<h5>Views</h5>
		<div class="pBody">
			<ul>

				 <li id="ca-view" class="selected"><a href="%s" title="View the tool [c]" accesskey="c">Tool</a></li>
				 <li id="ca-source"><a href="%s?action=source" title="View the Python source [e]" accesskey="e">Python Source</a></li>
            </ul>
		</div>
	</div>
	<div class="portlet" id="p-logo">
		<a style="background-image: url(http://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Wikimedia_Community_Logo-Toolserver.svg/135px-Wikimedia_Community_Logo-Toolserver.svg.png);" href="/~legoktm/cgi-bin/index.py" title="Home"></a>
	</div>
	<div class='generated-sidebar portlet' id='p-navigation'>
		<h5>Navigation</h5>
		<div class='pBody'>
			<ul>
				<li id="n-mainpage"><a href="/~legoktm/cgi-bin/index.py" title="Visit the main page" accesskey="z">Main Page</a></li>
				<li id="n-bugtracker"><a href="http://code.google.com/p/legobot/issues/list" title="Google Code bug tracker">Bug tracker</a></li>
				<li id="n-subversion"><a href="http://code.google.com/p/legobot/source/browse#svn/trunk/toolserver" title="View Suversion repository at Google Code" accesskey="x">Subversion</a></li>
			</ul>
		</div>
    %s
	</div>
</div>
<table id="footer" style="text-align: left; clear:both;" width="100%"><tr><td>

<a href="http://tools.wikimedia.de/"><img src="http://tools.wikimedia.de/images/wikimedia-toolserver-button.png" alt="Toolserver project" /></a>
<a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
<a href="http://wikimediafoundation.org/wiki/Fundraising?s=cl-Wikipedia-free-mini-button.png"><img src="http://upload.wikimedia.org/wikipedia/meta/6/66/Wikipedia-free-mini-button.png" alt="Wikipedia... keep it free." /></a>
</td></tr></table>
</body>
</html>
        """ %(self.location, monobook.replagtable(repmess = self.repmess))
        return text