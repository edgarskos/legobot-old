#!usr/bin/env python
import time, sys, os, re
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
sys.path.append(os.environ['HOME'] + '/alertbot')
log = open("AlertsBatch.log", "r")
logtext = log.read()
log.close()

content = """<h2>Last run</h2>
<ul>
<li>Alertbot last ran at %s</li>
</ul>
<h3>Errors</h3>
<ul>

"""
header = monobook.header('Alertbot Status')
body = monobook.body(content)