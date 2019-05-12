import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import csv
import pandas 

# Set the URL you want to webscrape from
url = 'http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases'

# Connect to the URL
response = requests.get(url)
# Parse HTML and save to BeautifulSoup object¶
soup = bs(response.text, "html.parser")
li = soup.findAll('li','flex-item')
a=[i.find('a')for i in li]
name=[name.get_text(strip=True) for name in a]
img = ['http://www.agriculture.gov.au'+img.find('img')['src'] for img in a]
href=[href['href'] for href in a]
origin=[]
pest_type=[]
au_legal=[]
for i in href:
    x=i.split('/')
    if ''==x[-1]:del x[-1]
    if '/pests/' in i:
        pest_type.append(x[-1])
    else:pest_type.append('-')
    origin.append(x[-2])
    if '.au' in i:
        au_legal.append('Yes')
    else:au_legal.append('No')
        
        
for i in range(len((name))):
    if not 'http'in href[i]:
        href[i]="http://www.agriculture.gov.au"+href[i]
    urllib.request.urlretrieve(img[i],name[i]+'.jpg')
fields=["Disease Name","Image link","Page Origin","Origin","Pest Type","Legal in Australia"]
data = [name,img,href,origin,pest_type,au_legal,]

df = pandas.DataFrame({"Disease Name":name,"Image link":img,"Page Origin":href,"Origin":origin,"Pest Type":pest_type,"Legal in Australia":au_legal})
writer = pandas.ExcelWriter('diseases.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()

with open('diseases.csv', 'a', encoding='utf-8') as csv_file:
    writer=csv.writer(csv_file)
    writer.writerow(["Disease Name","Image link","Page Origin","Origin","Pest Type","Legal in Australia"])
    for i in range(len(name)):
        writer.writerow([name[i],img[i],href[i],origin[i],pest_type[i],au_legal[i]])
        
