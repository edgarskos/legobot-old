#!usr/bin/env python
#
# (C) Legoktm 2008-2009, MIT License
# 
import time, sys, os, re
from commands import getoutput
sys.path.append('/home/legoktm/public_html/cgi-bin/')
import monobook
cur = time.localtime()
months = {
'1':'January',
'2':'February',
'3':'March',
'4':'April',
'5':'May',
'6':'June',
'7':'July',
'8':'August',
'9':'September',
'10':'October',
'11':'November',
'12':'December',
}
#num = cur[1]
month = months[str(cur[1])]
year = cur[0]
day = cur[2]
hour = cur[3]
min = cur[4]
sec = cur[5]
stamp = month+' '+str(day)+ ', '+str(year)+' at '+str(hour)+':'+str(min)+':'+str(sec)
#this is what actually runs it
logtext = getoutput('./alertbot/run org.toolserver.alertbot.AlertsBatch')
rs = re.findall('(.*)-(.*)-(.*) (.*),(.*) \[main\] INFO - Batch job completed; exit code (0|1)', logtext)[0]
runstamptext = months[str(int(rs[1]))]+' '+rs[2]+ ', '+rs[0]+' at '+rs[3]+':'+rs[4]

def finderrors(logtext):
	errorcontent = ''
	errors = re.findall('ERROR(.*?)\n', logtext)
	error2 = re.findall('at com(.*?)\n', logtext)
	error3 = re.findall('at org(.*?)\n', logtext)
	for error in errors:
		errorcontent += '<li>ERROR%s...</li>\n' %error
	for error in error2:
		errorcontent += '<li>at com%s</li>\n' %error
	for error in error3:
		errorcontent += '<li>at org%s</li>\n' %error
	if len(errorcontent) == 0:
		return '<li>No error occurred.</li>'
	else:
		return errorcontent

errors = finderrors(logtext)
def probreport(logtext):
	list = re.findall('WARN - problem report generated for (.*?)\n', logtext)
	content =''
	for i in list:
		content += '<li><a href="http://en.wikipedia.org/wiki/Wikipedia:%s/Article alerts">Wikipedia:%s/Article alerts</a></li>' %(i, i)
	if len(content) == 0:
		return '<li>No problem reports generated</li>'
	else:
		return content
probreb = probreport(logtext)
numofsubscrip=re.findall(' \[main\] INFO - (.*) subscriptions read from Category:ArticleAlertbot subscriptions', logtext)
subscript = numofsubscrip[0] + ' subscriptions were read from [[Category:ArticleAlertbot subscriptions]].'
writenum = re.findall('\[main\] INFO - WRITE:', logtext)
write = str(len(writenum)) + ' edits were made during the last run.'
skipnum = re.findall('\[main\] INFO - Job is cached, skipping: REPLACE:', logtext)
skip = str(len(skipnum)) + ' reports were cached and not updated.'
content = """<h2>Last run</h2>
<ul>
<li>Alertbot last ran at %s</li>
</ul>
<h3>Error(s)</h3>
<ul>
%s
</ul>
<h3>Problem Report(s)</h3>
<ul>
%s
</ul>
<h2>Statistics</h2>
<ul>
<li>%s</li>
<li>%s</li>
<li>%s</li>
</ul>
<small>Report generated at %s</small>
""" %(runstamptext, errors, probrep, subscript, write, skip, stamp)

#content to be put in the page
title = monobook.header('Alertbot status')
body = monobook.body(content)
navbar = monobook.navbar()
footer = monobook.footer()
fullcontent = str(title)+str(body)+str(navbar)+str(footer)
print 'Editing http://toolserver.org/~legoktm/alertbot.html'
print fullcontent
htmlpage = open('/home/legoktm/public_html/alertbot.html', 'w')
htmlpage.write(fullcontent)
htmlpage.close()