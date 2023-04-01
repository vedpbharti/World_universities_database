from __future__ import unicode_literals
from __future__ import division
import urllib2 as url
from bs4 import BeautifulSoup as bs
import re
import os
import requests
import json
import sys
from unidecode import unidecode
import codecs
import csv


input = open('unis.json')
unisj = json.load(input)
input.close()
unisl = []

for item in unisj:
    unisl.append(re.sub('[^A-Za-z0-9.]+', ' ', unidecode(item['name'])))

os.chdir('C:/Projects/Code')
reload(sys)
sys.setdefaultencoding('utf8')

orig_stdout = sys.stdout
f = open('crawllabels.txt', 'w')
sys.stdout = f


d = {}

# read a text file with wikipedia universities url
'''
f = open('university_url_1.txt', 'r')
links = f.readlines()
'''
links = unisl

failed = []
outlist = []
notablist = []

wikirows = ['Type', 'Established', 'Budget', 'Academic staff', 'Administrative Staff', 'Endowment', 'Students', 'Undergraduates', 'Postgraduates', 'Location', 'Affiliation']

# Extract data
for link in links:
    unidict = {'Name': link,'Type':'NA', 'Established':'NA', 'Budget':'NA', 'Academic staff':'NA', 'Administrative Staff':'NA', 'Endowment':'NA', 'Students':'NA', 'Undergraduates':'NA', 'Postgraduates':'NA', 'Location':'NA', 'Affiliation':'NA'}
    try:
        page = bs(url.urlopen('https://en.wikipedia.org/wiki/' + link), 'html.parser')
        infotable = page.find('table', attrs={'class':'infobox vcard'})
        try:  
            rows = [row for row in infotable.findAll('tr')]
            for rownumber, row in enumerate(rows):
                x =  row.get_text()
                ans = x.split('\n') 
                if ans[1] in wikirows:
                    unidict[ans[1]] = ans[2] 
                # get the Academic staff which is at index 2  					
                if ans[2] in wikirows:
                    unidict[ans[2]] = ans[4]	
        except AttributeError:
            print "No table for " + link
            j += 1
            notablist.append(link)
	   
    except url.HTTPError:
        print str(link) + ' not found on Wikipedia'
        failed.append(link)
        l += 1

    outlist.append(unidict)

print str(len(links)) + " universities tried"
print str(l) + " universities had no wikipedia entry"
print str(j) + " universities had a wikipedia entry but no info table"

sys.stdout = orig_stdout
f.close()

print "writing failed list..."
with open('failed.txt', 'w') as outfile:
    outfile.write(str(l) + " universities had no wikipedia entry\n")
    outfile.write(str(len(links)) + " universities recorded\n")
    outfile.write("failed unis below\n")
    for uni in failed:
        outfile.write(uni + "\n")
    outfile.write("unis with no table below\n")
    for uni in notablist:
        outfile.write(uni + "\n")
    outfile.close()

unisl = outlist

print "writing csv..."
with codecs.open('unidic.csv', encoding='utf-8', mode='w+') as csvout:
