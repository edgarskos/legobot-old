#!usr/bin/env python
import time, sys, os, re
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
log = open('/home/legoktm/alertbot/AlertsBatch.log', 'r')
logtext = log.read()
log.close()
rs = re.findall('(.*)-(.*)-(.*) (.*),(.*) \[main\] INFO - Batch job completed; exit code 0', logtext)[0]
runstamptext = months[str(int(rs[1]))]+' '+rs[2]+ ', '+rs[0]+' at '+rs[3]+':'+rs[4]

def finderrors(logtext):
	if re.search(r'\[main\] ERROR - (.*)at', logtext):
		error = re.findall('\[main\] ERROR - (.*)at', logtext)
		return str(error[0]) + '...'
	else:
		return 'No error occurred.'
errors = finderrors(logtext)
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
<li>%s</li>
</ul>
<h2>Statistics</h2>
<ul>
<li>%s</li>
<li>%s</li>
<li>%s</li>
</ul>
<small>Report generated at %s</small>
""" %(runstamptext, errors, subscript, write, skip, stamp)

#content to be put in the page
title = monobook.header('Alertbot status')
body = monobook.body(content)
navbar = monobook.navbar('status at run')
footer = monobook.footer()
fullcontent = str(title)+str(body)+str(navbar)+str(footer)
print fullcontent
htmlpage = open('/home/legoktm/public_html/alertbot.html', 'w')
htmlpage.write(fullcontent)
htmlpage.close()