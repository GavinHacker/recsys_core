# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors

def get_connection():
    return pymysql.connect(host='x.x.x.x',
                               user='root',
                               password='x#$_db',
                               db='recsys',
                               port=3306,
                               charset ='utf8',
                               use_unicode=True)