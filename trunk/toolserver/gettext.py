#
# (C) Legoktm 2008-2011, MIT License
# 
import urllib
data = urllib.urlencode({"wiki" : "en.wikipedia.org", "title" : "Main Page"})
f= urllib.urlopen("http://toolserver.org/~daniel/WikiSense/WikiProxy.php", data)
s=f.read()
f.close()
print s
