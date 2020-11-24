# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors

# 连接数据库函数,host 代表数据库 ip, user代表数据库用户名, password代表数据库密码, port为端口
def get_connection():
    return pymysql.connect(host='x.x.x.x',
                               user='root',
                               password='demo12DB',
                               db='recsys',
                               port=3306,
                               charset ='utf8',
                               use_unicode=True)
