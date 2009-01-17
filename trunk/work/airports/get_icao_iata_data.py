from urllib import FancyURLopener
import urllib

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
 
fileFromWiki = open('C:\\DEV\\work\\data.x-plane.com\\work\\wiki_icao.html', 'w')

myopener = MyOpener()

postfix = [chr(i) for i in range(65,91)]
for strPost in postfix:
    page = myopener.open('http://en.wikipedia.org/wiki/List_of_airports_by_ICAO_code:_'+strPost)
    fileFromWiki.write(page.read())
    
print "The end"