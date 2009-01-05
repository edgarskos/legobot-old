#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
&params;

    -namespace:n   Number or name of namespace to process. The parameter can be
                   more than one to add additional namespaces
# TODO
# TIP: use "%(dictname)s" % groupdict() a
#  better ref combining , combine urls and on ignoring a list of character (matching)
#  Seperate English from generic wikisyntax
#  Seperate enwiki sepefic
# steel stuff from 
# http://en.wikipedia.org/wiki/User:Polbot/source/Reffix.pl


# FIXME:
#  	http://en.wikipedia.org/w/index.php?title=London&diff=prev&oldid=253531178 (infobox)
# 	http://en.wikipedia.org/w/index.php?title=Hoover_Dam&diff=prev&oldid=253529821
# 	http://en.wikipedia.org/w/index.php?title=Global_Positioning_System&diff=prev&oldid=253529113 (why isn't the TITLE STILL CASED LIKE THAT?)
# FIXME:
# http://en.wikipedia.org/w/index.php?title=Rolls-Royce_RR300&diff=190562064&oldid=175311735
# http://www.nationaltrust.org/magazine/archives/arc_news_2007/010807.htm
# http://scholarworks.umass.edu/cgi/viewcontent.cgi?article=1186&context=theses
"""
__version__='$Id: selflink.py 4187 2007-09-03 11:37:19Z wikipedian $'
import re
try:
	import noreferences
except ImportError:
	noreferences = None

stndComments = (
		r"See http://en.wikipedia.org/wiki/Wikipedia:Footnotes for an explanation of how to generate footnotes using the<ref> and </ref> tags, and the template below.",
		r"See http://en.wikipedia.org/wiki/Wikipedia:Footnotes for an explanation of how to generate footnotes using the <references/)> tags",
		r"Categories",
#		r"Other languages",
)
familiesIWlist = {
		'wikipedia':	'w',
		'wiktionary':	'wikt',
		'wikinews': 	'n',
		'wikibooks':	'b',
		'wikiquote':	'q',
		'wikisource':	's',
		'wikiversity':	'v',
}
# NOT IMPLEMENTED
# Will change work/publisher cite news and |agancy="dictvalue"
agancies = {
	"AP": "Associated Press",
	"Associated Press": "Associated Press",

}
# "The" will be stripped if it exist
# So don't include Edge case e.g. "People" and "The People"
commonPublishers = (
"Associated Press",
"BBC News",
"BBC",
"Chicago Tribune",
"CNN",
"Daily Telegraph",
"Guardian",
"Huffington Post",
"International Herald Tribune",
"MTV",
"New York Times",
"NY Times",
"Observer",
"Seattle Times",
"Reuters",
"Rolling Stone",
"Wall Street Journal",
"Washington Post",

# VG Online sources
"IGN",
"GameStop",
"Electronic Gaming Monthly",
"Kotaku",
"Ars Technica",
"Joystiq",
"Tom's Hardware",
"Salon",
)

htmltags = (
# pairs
			"b", "i", "u", "font", "big", "small", "sub", "sup", "h1",
			"h2", "h3", "h4", "h5", "h6", "cite", "code", "em", "s", "span",
			"strike", "strong", "tt", "var", "div", "center",
			"blockquote", "ol", "ul", "dl", "table", "caption", "pre",
			"ruby", "rt" , "rb" , "rp",
# single
			"br", "p", "hr", "li", "dt", "dd",
# nest
			"table", "tr", "td", "th", "div", "blockquote", "ol", "ul",
			"dl", "font", "big", "small", "sub", "sup",
# table tags
			"td", "th", "tr",
)
htmlattrs = (
			"title", "align", "lang", "dir", "width", "height",
			"bgcolor", "clear", "noshade", 
			"cite", "size", "face", "color",
			"type", "start", "value", "compact",
			#/* For various lists, mostly deprecated but safe */
			"summary", "width", "border", "frame", "rules",
			"cellspacing", "cellpadding", "valign", "char",
			"charoff", "colgroup", "col", "span", "abbr", "axis",
			"headers", "scope", "rowspan", "colspan", 
			"id", "class", "name", "style" 
		)

# CSS HEX color values to named color convertion (selected)	
namedColors = {
	#  W3C Standard Color names
	'#00FFFF': 'cyan',		# same as aqua
	'#000000': 'black',
	'#0000FF': 'blue',
	'#FF00FF': 'magenta',	# same as Fuchsia
	'#808080': 'gray',
	'#008000': 'green',
	'#00FF00': 'lime',
	'#800000': 'maroon',
	'#000080': 'navy',
	'#808000': 'olive',
	'#800080': 'purple',
	'#FF0000': 'red',
	'#C0C0C0': 'silver',
	'#008080': 'teal',
	'#FFFFFF': 'white',
	'#FFFF00': 'yellow',
# HTML Color Names

	'#F0F8FF': 'AliceBlue',
	'#FAEBD7': 'AntiqueWhite',
	'#00FFFF': 'Aqua',
	'#7FFFD4': 'Aquamarine',
	'#F0FFFF': 'Azure',
	'#F5F5DC': 'Beige',
	'#FFE4C4': 'Bisque',
	'#000000': 'Black',
	'#FFEBCD': 'BlanchedAlmond',
	'#0000FF': 'Blue',
	'#8A2BE2': 'BlueViolet',
	'#A52A2A': 'Brown',
	'#DEB887': 'BurlyWood',
	'#5F9EA0': 'CadetBlue',
	'#7FFF00': 'Chartreuse',
	'#D2691E': 'Chocolate',
	'#FF7F50': 'Coral',
	'#6495ED': 'CornflowerBlue',
	'#FFF8DC': 'Cornsilk',
	'#DC143C': 'Crimson',
	'#00FFFF': 'Cyan',
	'#00008B': 'DarkBlue',
	'#008B8B': 'DarkCyan',
	'#B8860B': 'DarkGoldenRod',
	'#A9A9A9': 'DarkGray',
	'#A9A9A9': 'DarkGrey',
	'#006400': 'DarkGreen',
	'#BDB76B': 'DarkKhaki',
	'#8B008B': 'DarkMagenta',
	'#556B2F': 'DarkOliveGreen',
	'#FF8C00': 'Darkorange',
	'#9932CC': 'DarkOrchid',
	'#8B0000': 'DarkRed',
	'#E9967A': 'DarkSalmon',
	'#8FBC8F': 'DarkSeaGreen',
	'#483D8B': 'DarkSlateBlue',
	'#2F4F4F': 'DarkSlateGray',
	'#2F4F4F': 'DarkSlateGrey',
	'#00CED1': 'DarkTurquoise',
	'#9400D3': 'DarkViolet',
	'#FF1493': 'DeepPink',
	'#00BFFF': 'DeepSkyBlue',
	'#696969': 'DimGray',
	'#696969': 'DimGrey',
	'#1E90FF': 'DodgerBlue',
	'#B22222': 'FireBrick',
	'#FFFAF0': 'FloralWhite',
	'#228B22': 'ForestGreen',
	'#FF00FF': 'Fuchsia',
	'#DCDCDC': 'Gainsboro',
	'#F8F8FF': 'GhostWhite',
	'#FFD700': 'Gold',
	'#DAA520': 'GoldenRod',
	'#808080': 'Gray',
	'#808080': 'Grey',
	'#008000': 'Green',
	'#ADFF2F': 'GreenYellow',
	'#F0FFF0': 'HoneyDew',
	'#FF69B4': 'HotPink',
	'#CD5C5C': 'IndianRed ',
	'#4B0082': 'Indigo  ',
	'#FFFFF0': 'Ivory',
	'#F0E68C': 'Khaki',
	'#E6E6FA': 'Lavender',
	'#FFF0F5': 'LavenderBlush',
	'#7CFC00': 'LawnGreen',
	'#FFFACD': 'LemonChiffon',
	'#ADD8E6': 'LightBlue',
	'#F08080': 'LightCoral',
	'#E0FFFF': 'LightCyan',
	'#FAFAD2': 'LightGoldenRodYellow',
	'#D3D3D3': 'LightGray',
	'#D3D3D3': 'LightGrey',
	'#90EE90': 'LightGreen',
	'#FFB6C1': 'LightPink',
	'#FFA07A': 'LightSalmon',
	'#20B2AA': 'LightSeaGreen',
	'#87CEFA': 'LightSkyBlue',
	'#778899': 'LightSlateGray',
	'#778899': 'LightSlateGrey',
	'#B0C4DE': 'LightSteelBlue',
	'#FFFFE0': 'LightYellow',
	'#00FF00': 'Lime',
	'#32CD32': 'LimeGreen',
	'#FAF0E6': 'Linen',
	'#FF00FF': 'Magenta',
	'#800000': 'Maroon',
	'#66CDAA': 'MediumAquaMarine',
	'#0000CD': 'MediumBlue',
	'#BA55D3': 'MediumOrchid',
	'#9370D8': 'MediumPurple',
	'#3CB371': 'MediumSeaGreen',
	'#7B68EE': 'MediumSlateBlue',
	'#00FA9A': 'MediumSpringGreen',
	'#48D1CC': 'MediumTurquoise',
	'#C71585': 'MediumVioletRed',
	'#191970': 'MidnightBlue',
	'#F5FFFA': 'MintCream',
	'#FFE4E1': 'MistyRose',
	'#FFE4B5': 'Moccasin',
	'#FFDEAD': 'NavajoWhite',
	'#000080': 'Navy',
	'#FDF5E6': 'OldLace',
	'#808000': 'Olive',
	'#6B8E23': 'OliveDrab',
	'#FFA500': 'Orange',
	'#FF4500': 'OrangeRed',
	'#DA70D6': 'Orchid',
	'#EEE8AA': 'PaleGoldenRod',
	'#98FB98': 'PaleGreen',
	'#AFEEEE': 'PaleTurquoise',
	'#D87093': 'PaleVioletRed',
	'#FFEFD5': 'PapayaWhip',
	'#FFDAB9': 'PeachPuff',
	'#CD853F': 'Peru',
	'#FFC0CB': 'Pink',
	'#DDA0DD': 'Plum',
	'#B0E0E6': 'PowderBlue',
	'#800080': 'Purple',
	'#FF0000': 'Red',
	'#BC8F8F': 'RosyBrown',
	'#4169E1': 'RoyalBlue',
	'#8B4513': 'SaddleBrown',
	'#FA8072': 'Salmon',
	'#F4A460': 'SandyBrown',
	'#2E8B57': 'SeaGreen',
	'#FFF5EE': 'SeaShell',
	'#A0522D': 'Sienna',
	'#C0C0C0': 'Silver',
	'#87CEEB': 'SkyBlue',
	'#6A5ACD': 'SlateBlue',
	'#708090': 'SlateGray',
	'#708090': 'SlateGrey',
	'#FFFAFA': 'Snow',
	'#00FF7F': 'SpringGreen',
	'#4682B4': 'SteelBlue',
	'#D2B48C': 'Tan',
	'#008080': 'Teal',
	'#D8BFD8': 'Thistle',
	'#FF6347': 'Tomato',
	'#40E0D0': 'Turquoise',
	'#EE82EE': 'Violet',
	'#F5DEB3': 'Wheat',
	'#FFFFFF': 'White',
	'#F5F5F5': 'WhiteSmoke',
	'#FFFF00': 'Yellow',
	'#9ACD32': 'YellowGreen',

}
 
																														 
def fixStyle(text):
	pass

def getdateformat(text):
	"""
	ISO
	DMY
	MDY
	"""
	return 'DMY'


def fix(text):

	#
	## Hacks
	#
	text = text.replace('http://www.news.bbc.co.uk', 'http://news.bbc.co.uk')

# TODO: Fix accessyear/acessdate mismatch
	# Peer Reviewer script had for sometime time convert URL into the following bad form
	text = re.sub(r'\{\{[Cc]ite web\s*\|url=http://(?P<title>[^{|}]+)\s*\|title=(http://)?(?P=title)\s*(<!--[^<>]+-->)?\s*(\|format=(PDF|DOC))?(\|\s*accessdate *= *[^{|}]+)?\}\}', r'[http://\g<title>]', text)
	# a second time since we seem to hittings limits
	text = re.sub(r'\{\{[Cc]ite web\s*\|url=(http://[^{|}]+)\s*\|title=([^{=}]+<!--[^<=>/]+-->)(\|format=(PDF|DOC))?\}\}', r'[\1 \2]', text)

	# Following the collapse of MiB preference PDFbot converts to the new format when saving
	text = re.sub(r'\{\{(PDF(?:link)?\|[^{|}]+\|[\d\.]+)&nbsp;\[\[[^|]+\|([KMG])iB\]\]<!--[^<>]+-->\}\}', r'{{\1&nbsp;\2B}}', text)

	# EN MOS
	text = re.sub(r'([][.;,"\'] *) ((?:URL *)?([Aa]ccess|[Ll]ink access)e?d?( +on| +online)?|[Rr]etrie?ved?) +(?=\[\[|20\d\d-)', r'\1 Retrieved ', text)

	# deprecated date linking, remove in citations
	text =  re.sub(r'\[\[(\d+ (?:January|February|March|April|May|June|July|August|September|October|November|December))\]\],? \[\[(\d{4})\]\](?=[^<>]*</ref>)', r'\1 \2', text)
	text =  re.sub(r'\[\[((?:January|February|March|April|May|June|July|August|September|October|November|December) \d+)\]\],? \[\[(\d{4})\]\](?=[^<>]*</ref>)', r'\1, \2', text)

	# 
	## Templates
	#
#TODO
# unbold/unitlic publisher parameter
# convert title=blah blah (PDF)  to title= blah blah |format=PDF
# convert title={{xx icon}} blah  and {{xx icon}} {{cite web| to |language=dict[xx]
# ... something with [[Agence France-Presse]] ...
# language={{es icon}}
# [[PAGENAME#section|title]] -> [[#section|title]]


# r"(publisher|work)\s*=\s*(?P<sq>'{2,5})([^{|}']+)(?P=sq)", r'\1=\2', text)


	# Unlink PDF in format parameters
	text = re.sub(r'(?i)(\|\s*format\s*=\s*)\[\[(adobe|portable|document|file|format|pdf|\.|\s|\(|\)|\|)+\]\]', r'\1PDF', text)
	text = re.sub(r'(?i)(\|\s*format\s*=\s*)(\s*\.?(adobe|portable|document|file|format|pdf|\(|\)))+?(\s*[|}])', r'\1PDF\4', text)

	# Fix accessdate tags [[WP:AWB/FR#Fix accessdate tags]]
	text = re.sub(r'a[cs]*es*date(\s*=\s*)\[*(200\d)[/_\-](\d{2})[/_\-](\d{2})\]*', r'accessdate\1\2-\3-\4', text)
	text = re.sub(r'(\|\s*)a[cs]*es*mou*nthday(\s*=\s*)', r'\1accessmonthday\2', text)
	text = re.sub(r'(\|\s*)a[cs]*es*daymou*nth(\s*=\s*)', r'\1accessdaymonth\2', text)
	
	# Fix URLS lacking http://
	text = re.sub(r'(\|\s*url\s*=\s*)([0-9a-z.\-]+\.[a-z]{2,4}/[^][{|}:\s"]\s*[|}])', r'\1http://\2', text)

	# Fix pages=1 and page=20-44 and page=p. 22
	text = re.sub(r'(\{\{\s*(?:[Cc]ite (journal|news))[^{}]*\| *pages?\s*=\s*)(p[pg]?[. ]|pages?\b) *', r'\1', text)
	text = re.sub(r'(\{\{\s*(?:[Cc]ite |[Cc]itation)[^{}]*\| *)page( *=\s*[A-Z]?\d+\s*[{|}])', r'\1pages\2', text)
	text = re.sub(r'(\{\{\s*(?:[Cc]ite (?:journal|news|book)|[Cc]itation)[^{}]*\| *)pages( *=\s*[A-Z]?\d+\s*[{|}])', r'\1page\2', text)


	# Change infoboxes from trailing pipes (likely stems from  {{qif}} )
	p = re.compile(r'(\{\{[\w\s_]*[Ii]nfobox([^{}]*?\{\{[^{}]+\}\})*[^{}]*?[^{|}](= )?) *\| *\n ?(?=[\s\w]+=)', re.U)
	while p.search(text):
		text = p.sub(r'\1\n| ', text)



	#
	## HTML ## 
	#
	
	# Standardize tables
	text = re.sub(r'\n\|-+', r'\n|-', text)
	text = re.sub(r'\n\|-(?=\w)', r'\n|- ', text)
	text = re.sub(r'\n\|-[^][{}|<>\n]*(?=\n\|-)', r'', text)
	text = re.sub(r'(\n\{\|[^][{}|<>\n]*)\n+(?=[|!][^+\-{}\n]+\n)', r'\1\n|-\n', text)
	text = re.sub(r'\n\|-[^][{}|<>\n]*\n*(?=\n\|\})', r'', text)
	
	text = re.sub(r'(?i)((?:\n\{\||table|div)[^][{}<>|\n]*?) *align *= *"? *(left|right) *"?', r'\1 style="float:\2;" ', text)
	text = re.sub(r'(?i)((?:\n\{\||table)[^][{}<>|\n]*?) *align *= *"? *(center) *"?', r'\1 style="margin:auto;" ', text)
	text = re.sub(r'(?i)((?:div)[^][{}<>|\n]*?) *align *= *"? *(center) *"?', r'\1 class="center" ', text)
	text = re.sub(r'(?i)((?:\n\{\||table)[^][{}<>|\n]*?) *align *= *"? *(\w+) *"?', r'\1 ', text)
	# add # to bgcolor
	text = re.sub(r'(?i)\b(bgcolor *= *)(?P<q>"?)([A-Fa-f0-9]{6})\b(?P=q)', r'\1\2#\3\2', text)
	# add:
	# border="2" cellpadding="2" cellspacing="0" style="margin: 0 1em 0 0; background: #f9f9f9; border: 1px #aaa solid; border-collapse: collapse; font-size: 95%;"
	text = text.replace('border="2" cellpadding="4" cellspacing="0" style="margin: 1em 1em 1em 0; background: #f9f9f9; border: 1px #aaa solid; border-collapse: collapse; font-size: 95%;', ' class="wikitable')

	# <b> & <i> to ''' & ''
	text = re.sub(r"<b>([^{}<=>\n']*?)</b>", r"'''\1'''", text)
	text = re.sub(r"<i>([^{}<=>\n']*?)</i>", r"''\1''", text)

	# Fix br
	text = re.sub(r'(?i)(<br[^</>]*>)\n?</br>', r'\1', text)
	text = re.sub(r'(?i)<[/]?br([^{/}<>]*?)>', r'<br\1 />', text)
# Arrg! people are using this is templated tables as a way to visually align items! See [[Battle of Stalingrad]]
#	text = re.sub(r'(<br[\s/]*>|\n *\n *){4,}',	r'\n{{clear}}\n', text)
	text = re.sub(r'(?i)<br\s\S*clear\S*(all|both)\S*[\s/]*>', r'{{-}}', text)
	text = re.sub(r'<br\s\S*clear\S*(left|right)\S*[\s/]*>', r'{{clear\1}}', text)
	
	# Remove outdated comments
	for s in stndComments:
		text = re.sub(r'\n?<!--\s*%s\s*-->' % re.escape(s), '', text)

	for node in re.finditer(r'(<(?P<tag>\w+)(?= +)|\n\{\||(?<=\n)\|-)(?P<attr>[^][<>{}|\n]+(?(tag)>|\n))', text):
		tag = node.group('tag')
		attr = node.group('attr')
		if tag and tag.lower() not in htmltags:
			continue

		# HACKS
		attr = re.sub(r'border="2" cellpadding="4" cellspacing="0" style="margin: *1em 1em 1em 0; background: *#f9f9f9; border: *1px #aaa+ solid; *border-collapse: *collapse(; *font-size: *[89]\d%)?', r'class="wikitable" style="', attr)
		# Test cases
		# {| class="infobox" cellpadding="0" style="font-size: 90%; align=left; width:20%" 
		attr = re.sub(r'\b(\w{2,}) *= *(?P<q>["\']) *([^"\']+?) *(?P=q)(?![=|{}])', r'\1="\3"', attr)
		attr = re.sub(r'\b(\w{2,}) *= *([^][{}<>|="\'`:;\s]*[0-9a-zA-Z%._]+[^][{}<>|="\'\s]*)(?![^][{|}="\']+")', r'\1="\2"', attr)
		
		if '{|' in node.group(1):
			attr = re.sub(r'(col|row)span=("1"|1)(?=\D)', r'', attr)
			#attr = attr.replace('cellspacing="0"', 'style="border-collapse:collapse; "')
			if 'border=' not in attr:
				# See [[MediaWiki talk:Common.css# Wikitable borders without CSS]]
				attr = re.sub(r'class="wikitable([^"\'{|}]*)"( *border="?1"?)*', r'class="wikitable\1" border="1"', attr)
			if re.search('float: *right', attr) and 'toccolours' in attr and node.start() < 400:
				# floats right, and near the top, gotta be a infobox
				attr = re.sub(r'class="toc(colours|)', r'class="infobox', attr)
				attr = re.sub(r'float: *right;|margin[^:;=]*:[^:;=]+|border="1"', r'', attr)
			# border-collapse is not exactly the same but it's close enough
			#attr = re.sub(r' cellspacing="0"', r' style="border-collapse:collapse;"', attr)
		if 'class="wikitable' in attr:
			attr = re.sub(r'(?i) border="?([02-9])"?',   		r'', attr)
			attr = re.sub(r'(?i) cellspacing="?([0])"?',		r'', attr)
			attr = re.sub(r'(?i) cellpadding="?([2-4])"?',		r'', attr)
			attr = re.sub(r'(?i)margin: ?1em 1em 1em 0',		r'', attr)
			attr = re.sub(r'(?i)background: ?#f9f9f9',  		r'', attr)
			attr = re.sub(r'(?i)border: 1px #aaa solid',  		r'', attr)
			attr = re.sub(r'(?i)border-collapse: ?collapse',	r'', attr)
			#attr = re.sub(r'font-size: ?\.?9\d(%|em)',		r'', attr)

		# replace with CSS 
		attr = re.sub(r'(?i) align="(left|center|right|justify)"', 	r' style="text-align:\1;"', attr)
		attr = re.sub(r'(?i) bgcolor="([^"\']+?)"',	r' style="background-color:\1;"', attr)
		#attr = re.sub(r'(?i) border="?([1-9])"?',		r' style="border:\1px;"', attr)
		attr = re.sub(r'(?i) color="([^"\']+?)"',	r' style="color:\1;"', attr)
		attr = re.sub(r'(?i) clear="(left|right)"',	r' style="clear:\1;"', attr)
		attr = re.sub(r'(?i) clear=" *all *"',     	r' style="clear:both;"', attr)
		attr = re.sub(r'(?i) face="([^"\']+?)"',	r' style="font-family:\1;"', attr)
		attr = re.sub(r'(?i) height="([^"\']+?)"',	r' style="height:\1;"', attr)
		attr = re.sub(r'(?i) nowrap(="[^"]*"|(?= ))',	r' style="white-space:nowrap;"', attr)
		attr = re.sub(r'(?i) size="(\d+(em|%|px|pt))"',	r' style="font-size:\1;"', attr)
		attr = re.sub(r'(?i) valign="([^"]+?)"',	r' style="vertical-align:\1;"', attr)
		attr = re.sub(r'(?i) width="([^"\']+?)"',	r' style="width:\1;"', attr)

		# font size="#" render browser dependent
		fontSizeConvert = {'1':'0.8em','2':'0.9em','3':'1.2em','4':'1.4em','5':'1.9em','6':'2.4em','7':'3.7em'}
		for n in re.finditer(r' size="?([1-7])"?(?=\W)', attr):
			attr = attr.replace(n.group(),	r' style="font-size:%s;"'%fontSizeConvert[n.group(1)])
		
		# Remove all non approved attributes
		for m in re.finditer(r'\b(\w+)(="[^"\']+")', attr):
			if m.group(1).lower() not in htmlattrs:
				attr = attr.replace(m.group(), '')
			else:
				attr = attr.replace(m.group(), m.group(1).lower() + m.group(2))
		

		# put back in
		text = text.replace(node.group(), '%s%s'% (node.group(1).lower(), attr) )
	

	# Convert simple <font> to <span>
	# NOTE: <font>[[link|text]]</font> transforms to [[link|<font>text</font>]] by MW
	text = re.sub(r'(?i)(<font[^<>]*)> *\n?<font([^<>]*>)([^<>]*?</font> *\n?)</font>', r'\1\2\3', text)
	text = re.sub(r'(?i)<font(( +style="[^"]+")+)>(?!\[\[)([^<>]*?)(?<!\]\])</font>', r'<span\1>\3</span>', text)
	
	# merge style=
	while re.search(  r' style="([^"{|}=\n]+)"([^][!<>{|}\n]*?) style="', text):
		text = re.sub(r' style="([^"{|}=\n]+)"([^][!<>{|}\n]*?) style="', r'\2 style="\1; ', text)

	#
	## CSS ##
	#
	for styleMatch in re.finditer(r'(?<=\W)style *= *(?P<quote>["\'])([^][<>{}|=\n]+?)(?P=quote);*', text):
		styleText = styleMatch.group(2)
		styleText = re.sub(' *: *', ':', styleText)
		styleText = re.sub(r':([^:;]+)$', r':\1; ', styleText)
		styleText = re.sub(r' *;*(; *?)+( *)', r'\1\2', styleText)
		# Remove "float; ..."
		styleText = re.sub(r'(\A *|;)([^;:=]*:? *;)+', r'\1', styleText)

		styleText = re.sub(r'(background|color):([a-fA-F0-9]{3,6})', r'\1:#\2', styleText)
		if styleText.count('background') == 1:
			styleText = styleText.replace('background-color', 'background')

		# Assumed units
		styleText = re.sub(r'(width|height):(\d{2,});', r'\1:\2px;', styleText)
		styleText = re.sub(r'((?:background|border|border|color)(?:-color)?):([a-fA-F0-9]{3,6})(?=[ ;])', r'\1:#\2', styleText)

		# Fix units
		styleText = re.sub(r'\b(width|height|border|margin|padding):(\d{2,}|[1-9])(?=[; ])', r'\1:\2px;', styleText)
		styleText = re.sub(r'([ :]0)(em|%|px|pt)\b', r'\1', styleText)

		# IE color compatiblity
		styleText = re.sub(r'(?i)\bgrey\b', r'gray', styleText)
		styleText = re.sub(r'(?i)(dark|dim|light|lightslate|slate)gr[ae]y', r'\1grey', styleText)

		# Shorten CSS color values
		for m in re.finditer(r'#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?=[ ;!])', styleText):
			if m.group().upper() in namedColors:
				styleText = styleText.replace(m.group(), namedColors[m.group().upper()])
			elif re.search(r'(?i)#(00|11|22|33|44|55|66|77|99|aa|bb|cc|dd|ee|ff){3}', m.group().lower() ):
				styleText = styleText.replace(m.group(), re.sub(r'(?ui)#([0-9a-f])[0-9a-f]([0-9a-f])[0-9a-f]([0-9a-f])[0-9a-f]', r'#\1\2\3', m.group().lower() ))
			else:
				styleText = styleText.replace(m.group(), m.group().lower())

		# use mirroring
		styleText = re.sub(r'(margin|padding):(?P<v>[\-\.0-9]+[a-zA-z]+|0)( (?P=v))+;', r'\1:\2;', styleText)
		
		if re.sub(r'(?<=\S) (?=\S)', '', styleMatch.group(2)) != re.sub(r' ', '', styleText) and ';' in styleMatch.group():
			text=text.replace(styleMatch.group(), styleText.strip() and 'style="%s"'%styleText.strip() or '')



	#
	## Hyperlinking ##
	#
	
	# Remove url junk (tracking, referrers, client info)
	for i in range(0,9):
		text = re.sub(r'(http://[^][<>\s"|])(&client=firefox-a|&lt=)(?=[][<>\s"|&])', r'\1', text)


	# Use magic words instead
	text = text.replace('[{{SERVER}}{{localurl:', '[{{fullurl:')
	text = re.sub(r'\[http://(www\.toolserver\.org|toolserver\.org|tools\.wikimedia\.org|tools\.wikimedia\.de)/([^][<>"\s;?]*)\?? ([^]\n]+)\]', r'[[tools:\2|\3]]', text)
#	text = re.sub(r'\[http://en.wikipedia.org/w/index.php\?title=([^][<>"\s&=?]+)&?([^][<>"\s]*)', r'[{{fullurl:\1|\2}}', text)

	# convert (see http://...) into <http://...>, which is better handled by software
	text = re.sub(r'(?i)[(](?:see|) *(http://[^][<>"\s(|)]+[\w=/&])\s?[)]', r'<\1>', text)

	# From fixes.py
	# external link in double brackets
	text = re.sub(r'\[\[(?P<url>https?://[^\]]+?)\]\]',   r'[\g<url>]', text)
	# external link starting with double bracket
	text = re.sub(r'\[\[(?P<url>https?://.+?)\]',         r'[\g<url>]', text)
	# pipe in url (unlikely to go wrong)
	text = re.sub(r'\[(?P<url>https?://[^][<>\s"\|]+?\.(pdf|html?|php|aspx?|jsp)) *\| *(?P<label>[^\|\]]+?)\]', r'[\g<url> \g<label>]', text)


	# Commons fixes for URLs
	# TODO: remove domain name titles [http://example.com/aboutus.pdf example.com]
	# add [http://.... \n title] -> [$1 $2]
	# | url= http://www.statcan.ca/english/sdds/instrument/3901_Q2_V2_E.pdf]  (fx by removing the invalid [])
	text = re.sub(r'(http:/* *){2,}(?=[a-z0-9:.\-]+/)', 'http://', text)  # Silently correct http://http:/
	text = re.sub(r"(\[\w+://[^][<>\"\s]+?)''", r"\1 ''", text) # corrects [http://''title''] (nospaces) -> [http:// ''title'']

	# External to Interwiki
	# FIXME: http://sources.wikipedia.org/wiki/Bible%2C_English%2C_King_James%2C_Psalms#Chapter_72 
	#for m in re.finditer(ur'\[http://(?P<lang>\w+)\.(?P<family>\w+)\.org/wiki/(?!(?P=family):)([^{|}\[\]<>"\s?]+) +([^]\n]+)\]', text, re.I):
	for m in re.finditer(ur'\[http://([a-z0-9\-]+)\.(\w+)\.org/wiki/([^{|}\[\]<>"\s?]+) +([^]\n]+)\]', text):
		if m.group(1) == 'commons':
			iwPrefix = 'commons'
		elif m.group(1) == 'meta':
			iwPrefix = 'm'
		elif m.group(1) in familiesIWlist:
			# don't allow http://sources.wikipedia.org
			continue
		elif m.group(2) in familiesIWlist:
			iwPrefix = '%s:%s' % (familiesIWlist.get(m.group(2)), m.group(1))
		else:
			continue
		text = text.replace(m.group(0), '[[%s:%s|%s]]'% (iwPrefix, m.group(3), m.group(4)))

	#
	## Wikilinking ##
	#

	# Remove underscores from the links
	for m in re.finditer(r'\[\[([^<>\[\]|{}\n]+)\|([^][\n|]+)\]\]', text):
		wlink = m.group(1).replace('_', ' ')
		wlink = wlink.replace('# ', '#') # get ride of copy/paste space
		if '%' in wlink:
			try:
				import urllib
				wlink = unicode(urllib.unquote(wlink.encode('utf-8')), encoding='utf-8')
			except:
				pass
		text = text.replace(m.group(), '[['+wlink+'|'+m.group(2)+']]')
	
	#
	## References ##
	#
	text = re.sub(r'(?uis)<(/?)REF\b([^<>]*?)>', r'<\1ref\2>', text)
	text = re.sub(r'<ref +name(= *| *=)"', r'<ref name="', text)
	text = re.sub(r'(?i)<sup *>\s*\[(\w+://[^][<>"\s]+) *\]\s*</sup>', r'<ref>\1</ref>', text) # Fake reference (<sup>[url]</sup>)

	# Leaving out the http://
	text = re.sub(r'(?<=<ref>)\s*([a-z0-9\-\.]*?[a-z0-9\-]+\.[a-z\.]{2,6}/[^][<>\s"]+)\s*(?=</ref>)', r'http://\1', text)
	text = re.sub(r'(?<=<ref>)\s*\[?(?:http://)?([a-z0-9\-\.]*?[a-z0-9\-]+\.[a-z\.]{2,6}/[^][<>\s"|]+) +([^][{|}<>\n/]+?)\]?\s*(?=</ref>)', r'[http://\1 \2]', text)

	# TODO: Fix the below [ref] to <ref>[url]</ref> conversion 
	# FIXME: http://en.wikipedia.org/w/index.php?title=Naomi_Oreskes&oldid=206808331
	text = re.sub(r'(?is)<ref\s*>\s*(\[\w+://[^][<>"\s]+\s*\])\s*(\[\w+://[^][<>"\s]+\s*\])\s*</ref\s*>', r'<ref>\1</ref><ref>\2</ref>', text)
	# Bracket to reference conversion
	for i in range(0,8):
		text = re.sub(r'(?miu)(^[^*#;:= ]{1,4}.{4,}?)(?<!<ref>)(?<![*#]{3})(?<!PDFlink\|)(?<!PDF\|)(\s*)\[(http[s]?://[0-9a-z\-\.:]+/[^][<>\s"]{8,})\s*\](?!.*\s*</\s*ref\s*>)', r'\1<ref>\3</ref>\2', text)
	# remove invalid references
	text = re.sub(r'<ref></ref>', '', text)

	# [[WP:AWB/FR#Placement of [1] within punctuation]]
	# BUGS
	#  an [[anthelmintic]]<ref>''The Merck ... </ref>,
	# Tests:
	# independence."<ref name = "Stagg-1983"/>. 
	# "He said," <ref /> "She said."
	# previous estimates<ref />) a
	# 1999) <ref /><ref/>.
	# '''HIV/AIDS prevalence rate:<ref name=hpa/>'''<br/>  (puts space after ref)
	# item1, item2<ref />, item3
	# \n begin moved around:
	#   http://en.wikipedia.org/w/index.php?title=Economy_of_the_Republic_of_Ireland&diff=247400790&oldid=prev
	#	http://en.wikipedia.org/w/index.php?title=Jimmy_Wales&diff=next&oldid=250480032
	#	   }} \n</ref>\n*list
	# <ref  />\n, but would...

	# Only apply if pucuation infront is the dominate format
	if len(re.findall(r'[.,;:] *\s?<ref', text)) > len(re.findall(r'(?:</ref>|<ref [^</>]+/>) *\s?[.,;:]', text)):
		# Move punctuation left and space right but before \n
		text = re.sub(r'(?s)(?<=[\w")\]])( *)(\s?(?:<ref [^>]+?/> *\s??|<ref[^>]*?>[^>]*?</ref> *\s??)+)(\n?)([.,;:])(?![.,;:])(\s??)( *)', r'\4\2\1\6\5\3', text)
		# Move space to the right, if there's text to the right
		text = re.sub(r'(?s)(?<=[.,;:"])( +)((?:<ref [^>]+?/> *\s??|<ref[^>]*?>[^>]*?</ref> *\s??)+)(?=\s? *[^\s<>])', r'\2\1', text)
		# Remove duplicate punctuation
		text = re.sub(r'(?s)(?P<punc>[.,;:])(["]?(?:<ref [^>]+?/> *\s?|<ref[^>]*?>[^>]*?</ref> *\s?)+)(?P=punc)(?![.,;:])', r'\1\2', text)
		# Remove spaces between references
		text = re.sub(r'(</ref>|<ref [^>]+?/>) +(<ref)', r'\1\2', text)
		# Add two space if none, reduce to two if more
		# trim or add whitespace after <ref />
		text = re.sub(r'(</ref>|<ref [^>]+?/>)()((\'{2,5}|)[\w"(\[])', r'\1 \3', text)
		text = re.sub(r'(</ref>|<ref [^>]+?/>)( {3,})([\w(\[])', r'\1  \3', text)

	# Merge duplicate refs
	for m in re.finditer(r'(?si)(<ref>)(.*?)(</ref>)', text):
	# FIXME: don't use the from:
	#	The Empire State Building is located  
	# Also search author= 
		if text.count(m.group()) <= 1:
			# Skip single references 
			continue
		refname = 'ref'
		for p in (r'\|\s*last\s*=(\w+)',
				r'(?s).*\w+://[a-z0-9\-\.]*?([a-z0-9\-]+)\.[a-z\.]{2,6}[ /|=!].*',
				r'(?s)^(?:\[\[[^][]+\|)?((?<![{])(?<=\W)\w+)[,. ].*?(\d{2,4}\b)',):
			match = re.search(p, re.sub(r'accessdate\s*=[^{|}]*|Retrieved [\s\w\[\],]+', ' ', m.group(2)) , re.U)
			if match:
				refname = match.group(1)
				break
		else:
			# get the longest word (should be longest Capitlized word)
			for n in re.split(r'[^A-Za-z]+', re.sub(r'\|[^{|}=]+=', ' ', m.group(2) )):
				if len(n) > len(refname):
					refname = n
		# remove digits so we don't get "rescue007" + "1"
		refname = refname.strip('\t\r\n 0123456789').lower()
		
		for p in (r'\|\s*(?:pages|page|p|pp)\s*=\s*(\d+)', 
				r'\b(?:pages|page|p|pp|pg)[.:= ]*(\d{1,4})\b[\w\s\.\-<&\]]*', 
				r'\|\s*year\s*=\s*(\d{4})', 
				r'\b(19\d\d|200[0-7])\b',
				r'\b([mclxvi]*[clxvi]{2,6})(?:\b|\.)' ):
			match = re.search(p, re.sub(r'accessdate\s*=[^{|}]*|Retrieved [\s\w\[\],]+', ' ', m.group(2)) )
			if match and refname+match.group(1) not in text:
				refname = refname+match.group(1)
				break
		else:
			i = 1
			while refname+str(i) in text:	i+=1
			else: refname += str(i)
		if len(m.group(2)) > len(refname) * 1.4:
			text = text.replace(m.group(), '<ref name="%s">%s</ref>' % (refname, m.group(2)), 1)
			text = text.replace(m.group(), '<ref name="%s"/>' % refname)

	# remove <refernces /> wrapper
	# Adapted from AWB
	m = re.search(r'(?i)(<(span|div)( class="(references-small|small|references-2column)"|)>\s*){1,2}\s*<references[\s]?/>(\s*</(span|div)>){1,2}', text)
	if m and m.group().count('<div') == m.group().count('</div'):
		cols = re.search(r'((?!-)column-count|-moz-column-count):\s*?(\d+)', m.group())
		if "references-2column" in m.group():
			text = text.replace(m.group(), '{{reflist|2}}')
		elif cols:
			text = text.replace(m.group(), '{{reflist|%s}}' % cols.group(2))
		else:
			text = text.replace(m.group(), '{{reflist}}')

	# If more than 30 refs, make sure the reference section is multi column
	if text.count('</ref>') > 30:
		text = re.sub(r'(?is)(=\s+(<!--.*?-->)*\s*)(<references />|\{\{reflist\|?3?\}\})', r'\1{{reflist|colwidth=30em}}', text)
	elif text.count('</ref>') < 5:
		text = re.sub(r'(?is)(=\s+)\{\{reflist\|(\d+|colwidth=\d+\w+)\}\}', r'\1{{reflist}}', text)
	
	if noreferences:
		norefbot = noreferences.NoReferencesBot(None)
		if norefbot.lacksReferences(text, verbose=False):
			text = norefbot.addReferences(text)
	# change image: to file:
	text = re.sub(r'\[\[Image:)', r'[[File:', text)
	return text
def test():
	tests = (
"""
see,  <ref  /> after,\t<ref  > class,
<ref />
sdf her
<ref  />
<ref  />
,  \t but would...
""",
	)