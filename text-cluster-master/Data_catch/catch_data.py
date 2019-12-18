import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import json


def const_page_url():
    url_list = []


res = requests.get(
    'https://search.sina.com.cn/?q=%BD%B5%CE%C2%BD%B5%D1%A9&range=all&c=news&sort=rel&col=&source=&from=&country=&size=&time=&a=&page=3&pf=0&ps=0&dpc=1')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')
title = soup.select('.box-result')
print(soup)
csv_obj = open('data7.csv', 'w', encoding='utf-8', newline='')
csv.writer(csv_obj).writerow(['title', 'source', 'content', 'time'])
for item in title:
    h2 = item.select('h2')[0]
    a = h2.select('a')[0]
    print(a['href'])
    com = requests.get(a['href'])
    com.encoding = 'utf-8'
    com_soup = BeautifulSoup(com.text, 'html.parser')
    print(com_soup.select('.main-title'))
    if len(com_soup.select('.main-title')) == 0:
        main_title = ''
    else:
        main_title = com_soup.select('.main-title')[0].text
    # time = com_soup.select('.date')[0].text
    if len(com_soup.select('.date')) == 0:
        time = ''
    else:
        time = com_soup.select('.date')[0].text
    # source = com_soup.select('.source')[0].text
    if len(com_soup.select('.source')) == 0:
        source = '新浪网'
    else:
        source = com_soup.select('.source')[0].text
    content = com_soup.select('.article p')[1:-1]
    article = []
    print(content)
    for p in content:
        article.append(p.text.strip())
    csv.writer(csv_obj).writerow([main_title, source, article, time])
