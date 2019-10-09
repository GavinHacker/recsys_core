import logging
import random
import string
import requests
import time
from collections import deque
from urllib import parse
from bs4 import BeautifulSoup as beaut_soup
import pandas as pd
import re

#from settings import User_Agents,Agent_IP


class DoubanSpider(object):
    """豆瓣爬虫"""
    def __init__(self,form,Type,country,genres):
        # 基本的URL
        #self.base_url = 'https://movie.douban.com/tag/#/?sort=S&range=0,10&'
        self.base_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&'
        self.full_url = self.base_url + '{query_params}'
        # 从User-Agents中选择一个User-Agent
        #self.headers = {'User-Agent':random.choice(User_Agents)}
        self.headers = {'User-Agent': 'Mozilla/4.0'}
        #self.proxies = {'http':random.choice(Agent_IP)}
        # 可选参数 
        self.form_tag = form  # 影视形式
        self.type_tag = Type  # 类型
        self.countries_tag =  country # 地区
        self.genres_tag = genres #特色
        #默认参数
        self.sort = 'T'  # 排序方式,默认是T,表示热度
        self.range = 0, 10  # 评分范围

    def encode_query_data(self):
        """对输入信息进行编码处理"""
        
        if not (self.form_tag and self.type_tag and self.countries_tag and self.genres_tag):
            all_tags = ''
        else:
            all_tags = [self.form_tag, self.type_tag, self.countries_tag, self.genres_tag]
        query_param = {
            'sort': self.sort,
            'range': self.range,
            'tags': all_tags,
        }

        # string.printable:表示ASCII字符就不用编码了
        query_params = parse.urlencode(query_param, safe=string.printable)
        # 去除查询参数中无效的字符
        invalid_chars = ['(', ')', '[', ']', '+', '\'']
        for char in invalid_chars:
            if char in query_params:
                query_params = query_params.replace(char, '')
        # 把查询参数和base_url组合起来形成完整的url
        self.full_url = self.full_url.format(query_params=query_params) + '&start={start}'
        '''
        query_params = 'tags='+str(self.form_tag)+','+str(self.type_tag)+','+str(self.countries_tag)+','+\
            str(self.genres_tag)
        self.full_url = self.full_url.format(query_params=query_params) + '&start={start}'
        '''

    def download_movies(self, offset):
        """下载电影信息
        :param offset: 控制一次请求的影视数量
        :return resp:请求得到的响应体"""
        full_url = self.full_url.format(start=offset)
        print(full_url)
        resp = None
        try:
            #方法1.USER_AGENT配置,仿造浏览器访问 headers
            #方法2.伪造Cookie，解封豆瓣IP ,cookies = jar
            #jar = requests.cookies.RequestsCookieJar()  
            #jar.set('bid', 'ehjk9OLdwha', domain='.douban.com', path='/')
            #jar.set('11', '25678', domain='.douban.com', path='/')
            #方法3.使用代理IP proxies
            resp=requests.get(full_url,headers=self.headers)    #,proxies=self.proxies
        except Exception as e:
            print(resp)
            logging.error(e)
        return resp

    def get_movies(self, resp):
        """获取电影信息
        :param resp: 响应体
        :return movies:爬取到的电影信息"""
        if resp:
            if resp.status_code == 200:
                # 获取响应文件中的电影数据
                movies = dict(resp.json()).get('data')
                if movies:
                    # 获取到电影了,
                    return movies
                else:
                    # 响应结果中没有电影了!
                    # print('已超出范围!')
                    return None
            else:
                #关机
                import os
                print("poweroff")
                #os.system("poweroff")
        else:
            # 没有获取到电影信息
            return None

    def save_movies(self, movies):
        """把请求到的电影保存到csv文件中
        :param movies:提取到的电影信息
        """
        #判断爬取的网页是否为空
        if len(str(movies)) < 20 : 
            return False
        #分词
        words = re.findall(pattern=r'\d\.\d|\w+(?:[ ，\-：·！。\？\(\)]?\w*)*',string=str(movies))
        #提取信息，生成字典
        items = []
        flag = True
        for word in words:
            if word == 'cover': 
                item['directors'] = item['directors'][:-1]
                item['casts'] = item['casts'][:-1]
                items.append(item)
                key = None
                flag = True
            if flag: 
                item = {'directors':'','rate':0,'title':None,'casts':'','form':self.form_tag,\
                'Type':self.type_tag,'country':self.countries_tag,'genres':self.genres_tag,'subject':''}
                flag = False
            if word in item.keys(): key = word
            elif key != None: 
                if key in ['rate','title']:
                    item[key] = word
                    key = None
                else:
                    item[key] += word
                    item[key] += '|'
        #保存字典
        frame = pd.DataFrame.from_dict(items)
        frame.to_csv('./data/movie.csv',index=0,header=0,mode='a')  #不保留索引，不保留标题，追加写入
        return True


def main():
    """豆瓣电影爬虫程序入口"""
    form_tags = ['电影','电视剧','综艺','动画','纪录片','短片']
    Type_tags = ['剧情','喜剧','动作','爱情','科幻','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史',\
    '战争','西部','奇幻','冒险','灾难','武侠','情色'] 
    country_tags = ['中国大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度',\
    '泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
    genres_tags = ['经典','青春','文艺','搞笑','励志','魔幻','感人','女性','黑帮']
    
    
    for form in form_tags:
        if form != '电影':
            continue
        for Type in Type_tags:
            if Type != '战争':
                continue
            for country in country_tags: #country_tags[1:8]:
                for genres in genres_tags:
                    print(form,Type,country,genres)
                    # 1. 初始化工作,设置请求头等
                    spider = DoubanSpider(form=form,Type=Type,country=country,genres=genres)
                    # 2. 对信息进行编码处理,组合成有效的URL组合成有效的URL
                    spider.encode_query_data()
                    
                    offset = 0
                    flag = True
                    while flag:
                        # 3. 下载影视信息
                        reps = spider.download_movies(offset)
                        print(reps)
                        # 4.提取下载的信息
                        movies = spider.get_movies(reps)
                        # 5. 保存数据到csv文件
                        flag = spider.save_movies(movies)
                        print(offset,flag)
                        offset += 30
                        # 控制访问速度(访问太快会被封IP)
                        time.sleep(random.randint(4,8)) 
            time.sleep(random.randint(20,30))
        time.sleep(random.randint(40,50))

if __name__ == '__main__':
    main()