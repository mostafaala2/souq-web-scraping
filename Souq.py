
import requests 
import urllib.request
import time
from PIL import Image
from bs4 import BeautifulSoup
import json
import csv
from io import BytesIO
10
filecsv = open('SouqDataapple.csv', 'w',encoding='utf8')
# Set the URL you want to webscrape from
#xyz
url = 'https://egypt.souq.com/eg-en/samsung/p/?section=2&page='

csv_columns = ['name','EAN-13','Item EAN','Brand','Type','price','Size','descreption','img']
writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
writer.writeheader()
prod = 2
for page in range(10):
    print('---', page, '---')
    r = requests.get(url + str(page))
    soup = BeautifulSoup(r.content, "html.parser")
    ancher=soup.find_all('div',{'class' : 'column column-block block-grid-large single-item'})

    for pt in  ancher:        
            
        a_tag = pt.find('a', href=True)
        href = a_tag['href'] # get the href attribute
        name=pt.find('h6', {'class' : 'title itemTitle'})
        itemPrice=pt.find('span', {'class' : 'itemPrice'})
        img=pt.find('img', {'class' : 'img-size-medium'})

        #descreption page
        imgpage = requests.get(href)
        soup_img = BeautifulSoup(imgpage.content, "html.parser")

        #image
        ancher_img=soup_img.find('div',{'class': 'vip-item-img-container'})
        xl_img=ancher_img.find('img', src=True)
        src = xl_img['src']
        #descreption

        ancher_info = soup_img.find('ul', {'class': 'grouped-list product-grouped-list'})



        det = ancher_info.find('div', {'id': 'specs-full'})
        dictionary_of_info = {'Brand': '--',
                              'Type': '--',
                              'EAN-13': '00000',
                              'Item EAN': '00000'}
        if det != None:
            dd = [tag.get_text() for tag in det.find_all("dd")]
            dt = [tag.get_text().strip() for tag in det.find_all("dt")]
            dictionary_of_info = dict(zip(dt, dd))




        ancher_desc = soup_img.find('div', {'class': 'vip-product-info'})
        Size = ancher_desc.find('div', {'class': 'item-connection text-center active'})
        descreption = ancher_desc.find('p', {'class': 'DarkGrey'})
        s = ' '
        EAN = ''
        Type = ''
        if 'EAN-13' in dictionary_of_info:
            EAN = dictionary_of_info['EAN-13']
        else :
            EAN = '1'


        if  'Type' in dictionary_of_info :
            Type= dictionary_of_info['Type']
        else :
            Type = 'none'



        Brand= dictionary_of_info['Brand'],
        Item_EAN= dictionary_of_info['Item EAN'],

        if Size != None:
            s = Size.text.replace('', '').strip('\r\n')

        writer.writerow(
            {'name': name.text.replace('', '').strip('\r\n'), 'price': itemPrice.text, 'Size': s,
             'descreption': descreption.text.replace(' ', '').strip('\r\n'), 'img': str(prod)+".jpg",
             'EAN-13': EAN, 'Brand': Brand[0], 'Item EAN': Item_EAN[0],
             'Type': Type})
        # urllib.request.urlretrieve(img.get('src'), itemPrice.text+".jpg")----
        urllib.request.urlretrieve(src, str(prod) + ".jpg")
        prod = prod + 1
        print(prod)
filecsv.close()
