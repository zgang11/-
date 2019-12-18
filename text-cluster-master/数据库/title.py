# -*-coding:utf-8-*-
import sys
import importlib
import csv
import datetime
import time

importlib.reload(sys)

# 上面分别是修改解释器和编译器的编码格式

from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import requests
import socket





def getCommentCounts(newsurl):
    """
    根据newsurl来获取newsid
    :param newsurl:
    :return:newsid
    """
    requestURL = "https://comment.sina.com.cn/page/info?version=1&format=json&\
channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1\
&page_size=3&t_size=3&h_size=3"  # 注意这里传递参数的方法
    getCountRequestUrl = requestURL.format(re.search('doc-i(.+).shtml', newsurl).group(1))
    commentes = requests.get(getCountRequestUrl)
    commentes.close()
    try:
        jd = json.loads(commentes.text)
        return jd['result']['count']['total']
    except:
        time.sleep(4)


def getNewsDetail(newsurl):
    res = requests.get(newsurl)
    result = {}
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.content, features='lxml')
    result['title'] = soup.select('.main-title')[0].contents[0]
    print(result['title'])
    dt = soup.select('.date')[0].contents[0]
    result['dt'] = dt
    # result['dt'] =datetime.strptime(dt, '%Y年%m月%d日 %H:%M')
    result['newssource'] = soup.select('.source')[0].contents[0]
    result['article'] = ' '.join(p.text.encode('utf-8').decode('utf-8').strip() for p in soup.select('#article p')[:-1])
    result['editor'] = soup.select('.show_author')[0].text.lstrip('责任编辑：')
    result['commentsCount'] = getCommentCounts(newsurl)
    csv.writer(csv_obj).writerow(
        [result['title']])
    return json.dumps(result, ensure_ascii=False)


def parseListLinks(url):
    newsdetails = []
    res = requests.get(url)
    res.encoding = 'utf-8'
    jd = json.loads('{' + res.text.lstrip('try{feedCardJsonpCallback(').rstrip(');}catch(e){};') + '}}')
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails

socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
url = "https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page={}&encode=utf-8"
news_total = []
csv_obj = open('title2.csv', 'w', encoding='utf-8', newline='')
csv.writer(csv_obj).writerow(['title'])
for i in range(1, 30000):
    newsurl = url.format(i)
    # parseListLinks返回的是包含每个分页的新闻的信息的列表,列表中是字典
    newsary = parseListLinks(newsurl)
    # 用列表的extend方法加入新的部分，而不是用append
    news_total.extend(newsary)

for line in news_total:
    print(line)
