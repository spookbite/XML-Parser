
import re
import os
import sys
import pathlib
import pandas as pd
from xml.dom import minidom

year = 2013

dir1 = '/Volumes/Untitled/PatentSimilarity/Assignment/'
dest = '/Volumes/Untitled/PatentSimilarity/Extracted-Application/'
p = pathlib.Path(dest)
if not p.is_dir():
    p.mkdir(parents=True)

dir2 = 'F:\Patent-textdata2013'

related = []
field = []
background = []
brief = []
abstract = []
detail = []
doc_id = []

ct = 0

files = os.listdir(dir2)
print(year, len(files))

for file1 in files:

    if file1.endswith('.zip'):
        continue

    xmlfile = file1
    ct += 1

    if file1.endswith('.zip'):
        continue

    file = open(xmlfile)
    filestring = file.read()
    xmlstrings = filestring.split('<?xml')
    napps = len(xmlstrings)

    for i in xmlstrings:
        # print(len(i))
        if len(i) == 0:
            print(i)
            continue
        xml = str('<?xml' + i)

        doc = minidom.parseString(str(xml))

        # xml = xml.replace('&lsqb;', '')
        xml = xml.replace('\n', '')

        try:
            di = doc.getElementsByTagName("publication-reference")[0]
            d = di.getElementsByTagName("document-id")[0]
            doc_no = d.getElementsByTagName("doc-number")[0].firstChild.data
        except:
            doc_no = 'NF'

        try:    
            abst =doc.getElementsByTagName("abstract")
            
            for text in abst:
                absr = text.getElementsByTagName("p")[0].firstChild.data
        except:
            absr = 'NF'
            
    
        description = doc.getElementsByTagName("description")
        
        for text in description:
            try:
                rel = text.getElementsByTagName("p")[0].firstChild.data
            except:
                rel = 'NF'
            try:
                fiel = text.getElementsByTagName("p")[1].firstChild.data
            except:
                fiel = 'NF'
            try:
                back = text.getElementsByTagName("p")[2].firstChild.data
            except:
                back = 'NF'
            try:
                brie = text.getElementsByTagName("p")[3].firstChild.data
            except:
                brie = 'NF'
            try:
                detai = text.getElementsByTagName("p")[4].firstChild.data
            except:
                detai = 'NF'
                
        
        related.append(rel)
        brief.append(brie)
        field.append(fiel)
        background.append(back)
        abstract.append(absr)
        detail.append(detai)
        doc_id.append(doc_no)
        
    if ct%2 == 0:
        print('\tCompleted {} files'.format(ct, len(dir2)))

df = pd.DataFrame()
df['doc-no'] = doc_id
df['abstract'] = abstract
df['related'] = related
df['brief'] = brief
df['field'] = field
df['background'] = background
df['details'] = detail

df.to_csv(str(year) + '.csv', index=False)
print('\tExtracted {} rows for year {}'.format(len(df), year))
