#!usr/bin/python
import os, sys
CONFIG = os.environ['PWD'] + '/userconfig.py'
#if os.path.isfile(CONFIG):
#	sys.exit('Your user-config.py already exists.')
file = open(CONFIG, 'w')
content = '#!usr/bin/python\n\"\"\"Username to login/edit/query with\"\"\"'
username = raw_input('Username to login/edit/query with: ')
content += '\nusername = \'%s\'' %(username)
commons = raw_input('Wikimedia Commons username, blank if none ')
if len(commons) == 0:
	commons = False
content += '\n\"\"\"Wikimedia Commons username (False if none)\"\"\"\ncommons = \'' + str(commons) + '\''
content += '\n\"\"\"Not necessary, but won\'t prompt you for password\"\"\"\n#password = \'\''
quitonmess = raw_input('Quit when finding new messages? [t]rue, [f]alse: ')
if quitonmess.lower() == ('t' or 'true'):
	mess = True
else:
	mess = False
content += '\n\"\"\"Quit when finding new messages?\"\"\"\nquitonmess = ' + str(mess)
wiki = raw_input("""Wiki to query... in format of 'xx.project' """)
content += '\n\"\"\" Wiki to query... in format of \'xx.project\' \"\"\"\nwiki = \'%s\'' %(wiki)
content += '\n\"\"\"API path for the wiki, where %s is the wiki above\"\"\"\napipath = \'http://%s.org/w/api.php\''
file.write(content)
file.close()