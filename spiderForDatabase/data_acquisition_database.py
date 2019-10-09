#coding:utf-8

import requests
import time
from bs4 import BeautifulSoup
import pymysql
import re
import pandas as pd
import random
import csv
from pyquery import PyQuery as pq

def get_info(index,_id):
    movie_info = []
    url = 'https://movie.douban.com/subject/' + _id
    #     url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&start=0'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    proxies_1 = {
        'http': ip_list[random.randint(2, 59)]          #proxies_1 = {'http':'27.8.29.86:808'}
    }

    time.sleep(round(random.uniform(1, 2), 2))

    info_html = requests.get(url, headers=headers, proxies=proxies_1)  # 请求
    content = info_html.text  # 获取内容

    soup = BeautifulSoup(content,'html.parser')

    #img
    #img = soup.find('div', attrs={'class': 'subject clearfix'})
    img2 = soup.find('img', attrs={'rel': 'v:image'}).attrs
    img_path = img2['src']

    #简介
    related = soup.find('div',attrs={'class':'related-info'})
    #intro = related.find('span',attrs={'class':''}).next   #property="v:summary"
    intro = related.find('span', attrs={'class':'','property':'v:summary'}).text
    intro = intro.replace(' ','')
    intro = intro.replace('\n', '')

    single_info =[]
    single_info.append(index)
    single_info.append(_id)
    single_info.append(img_path)
    single_info.append(intro)
    movie_info.append(single_info)
    return movie_info

# ip代理池
f = open("IPPond.txt","r")
ip_list = []
for i in f.readlines():
    ip_list.append(i.split('\n')[0])
f.close()


# 数据库链接
db = pymysql.connect(host='rm-2zeqqm6994abi7b6dqo.mysql.rds.aliyuncs.com',
                     port=3306,
                     user='noone',
                     password='Huawei12#$')

cursor = db.cursor()
# recsys数据库
cursor.execute('use recsys')
#cursor.execute('SELECT id FROM movie')
cursor.execute('SELECT id FROM movie where description is null or description = ""')
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

#起点
_start = 1602
#爬虫序号
index = 0

for _id in data:
    index = index + 1
    if index > _start:
        try:
            mov_cont = get_info(index,_id[0])

            file_add = "/Users/mayday/Downloads/spider/rec.csv"

            with open(file_add, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(mov_cont)

            print(index)
        except BaseException as ce:
            print('Acquire exception:', ce)

# 关闭数据库连接
db.close()
