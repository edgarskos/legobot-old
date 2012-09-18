#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Reame: TODO
"""
#
# (C) Compwhizii, 2008
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#
 
import wikipedia, pagegenerators, catlib
import re
 
def main():
    site = wikipedia.getSite()
    roadnumber = 419
    loopsat = True
 
    for arg in wikipedia.handleArgs():
        if arg.startswith('-road'):
            if len(arg) == 5:
                roadnumber = int(wikipedia.input('What road do you want to start at?'))
            elif len(arg) > 5:
                roadnumber = int(arg[6:])
 
    while loopsat == True:
        if roadnumber >= 1000:
            return
        listpage = wikipedia.Page(site, "List of highways numbered %s" % str(roadnumber))
        if listpage.exists() == True:
            wikipedia.setAction("Robot: Making redirects for Wikiproject U.S. Roads")
            wikipedia.output(">List of highways numbered %s exists" % str(roadnumber))
            rd = "#REDIRECT [[List of highways numbered %s]]" % str(roadnumber)
            p1 = wikipedia.Page(site, "Route %s" % str(roadnumber))
            p2 = wikipedia.Page(site, "Highway %s" % str(roadnumber))
            p3 = wikipedia.Page(site, "State Route %s" % str(roadnumber))
            p4 = wikipedia.Page(site, "State Highway %s" % str(roadnumber))
            p5 = wikipedia.Page(site, "State Road %s" % str(roadnumber))
            p6 = wikipedia.Page(site, "SR_%s" % str(roadnumber))
            p7 = wikipedia.Page(site, "SH_%s" % str(roadnumber))
            p8 = wikipedia.Page(site, "SR-%s" % str(roadnumber))
            p9 = wikipedia.Page(site, "SH-%s" % str(roadnumber))
            p10 = wikipedia.Page(site, "Federal Highway %s" % str(roadnumber))
            p11 = wikipedia.Page(site, "National Highway %s" % str(roadnumber))
            p12 = wikipedia.Page(site, "Federal Road %s" % str(roadnumber))
            p13 = wikipedia.Page(site, "National Road %s" % str(roadnumber))
            p14 = wikipedia.Page(site, "Federal Route %s" % str(roadnumber))
            p15 = wikipedia.Page(site, "National Route %s" % str(roadnumber))
            p16 = wikipedia.Page(site, "SR%s" % str(roadnumber))
            p17 = wikipedia.Page(site, "SH%s" % str(roadnumber))
            pagelist = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17]
 
            for i in pagelist:
                if i.exists() == False:
                    wikipedia.output(">>Creating %s" % i.title() )
                    i.put(rd)
                else:
                    wikipedia.output(">>%s exists" % i.title() )
        else:
            wikipedia.output(">List of highways numbered %s does not exist" % str(roadnumber))
        #End Of Loop
        roadnumber = roadnumber + 1
    wikipedia.output("Done!")
 
if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()