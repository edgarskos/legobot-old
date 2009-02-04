#!usr/bin/python
import pywiki, apinew
params = {
	'action':'query',
	'prop':'revisions',
	'titles':'API',
	'rvprop':'content',
}


page = 'User:Legoktm'

x=apinew.login('Legoktm')

#print x
