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


def set_config_property(content, type_, conn):
    sql = 'update config set content = \'%s\' where type = \'%s\'' % (content, type_)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()


if __name__ == '__main__':
    print(get_config_property('csv_last_url'))

