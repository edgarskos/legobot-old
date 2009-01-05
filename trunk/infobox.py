#!usr/bin/python
import re, os
import wikipedia
import commonfixes #dispenser's common fixes
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pywikipedia')
import legoktm
import wikipedia, pagegenerators, catlib
def doinfobox(page)
	try:
		wikitext = page.get()
	except wikipedia.NoPage:
		return
	except wikipedia.IsRedirectPage:
		return
	wikitext = re.compile(r'\{\{\s*(template:|)football', re.IGNORECASE).sub(r'{{Football', wikitext)


def yearfix(wikitext):
	#Fix years
	if re.search('| years =(.*?)<br />',wikitext,re.I):
		wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years1 = \1\n|years =\2', wikitext)
		if re.search('| years =(.*?)<br />',wikitext,re.I):
			wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years2 = \1\n|years =\2', wikitext)
			if re.search('| years =(.*?)<br />',wikitext,re.I):
				wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years3 = \1\n|years =\2', wikitext)
					if re.search('| years =(.*?)<br />',wikitext,re.I):
						wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years4 = \1\n|years =\2', wikitext)
						if re.search('| years =(.*?)<br />',wikitext,re.I):
							wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years5 = \1\n|years =\2', wikitext)
							if re.search('| years =(.*?)<br />',wikitext,re.I):
								wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years6 = \1\n|years =\2', wikitext)
								if re.search('| years =(.*?)<br />',wikitext,re.I):
									wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years6 = \1\n|years =\2', wikitext)
									if re.search('| years =(.*?)<br />',wikitext,re.I):
										wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years7 = \1\n|years =\2', wikitext)
										if re.search('| years =(.*?)<br />',wikitext,re.I):
											wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years7 = \1\n|years =\2', wikitext)
											if re.search('| years =(.*?)<br />',wikitext,re.I):
												wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years8 = \1\n|years =\2', wikitext)
												if re.search('| years =(.*?)<br />',wikitext,re.I):
													wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years9 = \1\n|years =\2', wikitext)
														if re.search('| years =(.*?)<br />',wikitext,re.I):
															wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years10 = \1\n|years =\2', wikitext)
															if re.search('| years =(.*?)<br />',wikitext,re.I):
																	wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years10 = \1\n|years =\2', wikitext)
																	if re.search('| years =(.*?)<br />',wikitext,re.I):
																		wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years11 = \1\n|years =\2', wikitext)
																		if re.search('| years =(.*?)<br />',wikitext,re.I):
																			wikitext = re.compile(r'| years =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| years12 = \1\n|years =\2', wikitext)
	return wikitext
def clubfix(wikitext):
	#Fix all clubs
	if re.search('| clubs=\'\'\'Total\'\'\'',wikitext,re.I):
		wikitext = re.compile(r'| clubs=\'\'\'Total\'\'\'', re.IGNORECASE).sub(r'', wikitext)
	#Get rid of the '''Total''' first
	if re.search('| clubs =(.*?)<br />',wikitext,re.I):
		wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs1 = \1\n|clubs =\2', wikitext)
		if re.search('| clubs =(.*?)<br />',wikitext,re.I):
			wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs2 = \1\n|clubs =\2', wikitext)
			if re.search('| clubs =(.*?)<br />',wikitext,re.I):
				wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs3 = \1\n|clubs =\2', wikitext)
					if re.search('| clubs =(.*?)<br />',wikitext,re.I):
						wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs4 = \1\n|clubs =\2', wikitext)
						if re.search('| clubs =(.*?)<br />',wikitext,re.I):
							wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs5 = \1\n|clubs =\2', wikitext)
							if re.search('| clubs =(.*?)<br />',wikitext,re.I):
								wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs6 = \1\n|clubs =\2', wikitext)
								if re.search('| clubs =(.*?)<br />',wikitext,re.I):
									wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs6 = \1\n|clubs =\2', wikitext)
									if re.search('| clubs =(.*?)<br />',wikitext,re.I):
										wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs7 = \1\n|clubs =\2', wikitext)
										if re.search('| clubs =(.*?)<br />',wikitext,re.I):
											wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs7 = \1\n|clubs =\2', wikitext)
											if re.search('| clubs =(.*?)<br />',wikitext,re.I):
												wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs8 = \1\n|clubs =\2', wikitext)
												if re.search('| clubs =(.*?)<br />',wikitext,re.I):
													wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs9 = \1\n|clubs =\2', wikitext)
														if re.search('| clubs =(.*?)<br />',wikitext,re.I):
															wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs10 = \1\n|clubs =\2', wikitext)
															if re.search('| clubs =(.*?)<br />',wikitext,re.I):
																	wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs10 = \1\n|clubs =\2', wikitext)
																	if re.search('| clubs =(.*?)<br />',wikitext,re.I):
																		wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs11 = \1\n|clubs =\2', wikitext)
																		if re.search('| clubs =(.*?)<br />',wikitext,re.I):
																			wikitext = re.compile(r'| clubs =(.*?)<br />(.*?)| clubs', re.IGNORECASE).sub(r'| clubs12 = \1\n|clubs =\2', wikitext)

	return wikitext
def capsgoals(wikitext):
	#Fix the 'caps(goals)' parameter
	if re.search('| caps(goals) = (.*?)<br />\'\'\'(.*?)\'\'\'',wikitext,re.I):
		wikitext = re.compile(r'| caps(goals) = (.*?)<br />\'\'\'(.*?)\'\'\'', re.IGNORECASE).sub(r'| caps(goals) = \1\n| totalcaps(goals) = \'\'\'\2\'\'\'', wikitext)
	if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
		wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)1 = \1\n|caps(goals) =\2', wikitext)
		if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
			wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)2 = \1\n|caps(goals) =\2', wikitext)
			if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
				wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)3 = \1\n|caps(goals) =\2', wikitext)
					if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
						wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)4 = \1\n|caps(goals) =\2', wikitext)
						if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
							wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)5 = \1\n|caps(goals) =\2', wikitext)
							if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
								wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)6 = \1\n|caps(goals) =\2', wikitext)
								if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
									wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)6 = \1\n|caps(goals) =\2', wikitext)
									if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
										wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)7 = \1\n|caps(goals) =\2', wikitext)
										if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
											wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)7 = \1\n|caps(goals) =\2', wikitext)
											if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
												wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)8 = \1\n|caps(goals) =\2', wikitext)
												if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
													wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)9 = \1\n|caps(goals) =\2', wikitext)
														if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
															wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)10 = \1\n|caps(goals) =\2', wikitext)
															if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
																	wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)10 = \1\n|caps(goals) =\2', wikitext)
																	if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
																		wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)11 = \1\n|caps(goals) =\2', wikitext)
																		if re.search('| caps(goals) =(.*?)<br />',wikitext,re.I):
																			wikitext = re.compile(r'| caps(goals) =(.*?)<br />(.*?)| caps(goals)', re.IGNORECASE).sub(r'| caps(goals)12 = \1\n|caps(goals) =\2', wikitext)
	return wikitext
