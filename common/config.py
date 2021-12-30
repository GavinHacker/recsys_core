# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
import pymysql.cursors
from functools import reduce
import numpy as np
import pandas as pd
import uuid
import datetime
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import json

# 获取数据库中,config表的配置项, type为配置项的key, 比如获取csv_last_url,则值为/usr/local/recsys_core/data/comment_origin_data_2019-01-01-01-01-01.csv
def get_config_property(type_, conn):
    sql = 'select * from config where type = \'%s\'' % type_
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            r = cur.fetchone()
            if r is not None:
                return r[2]
        return None
    except Exception as e:
        print(e)
        conn.close()

# 与get_config_property对应, 为设置配置项函数
def set_config_property(content, type_, conn):
    sql = 'update config set content = \'%s\' where type = \'%s\'' % (content, type_)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()

# 测试
if __name__ == '__main__':
    print(get_config_property('csv_last_url'))

