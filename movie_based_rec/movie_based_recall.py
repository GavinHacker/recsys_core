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
from sklearn.datasets import dump_svmlight_file
from sklearn.preprocessing import OneHotEncoder
import pickle as pkl
from sklearn.metrics import roc_auc_score, mean_squared_error
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import LogisticRegression
import common.common as common
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
import common.schedule_util as sched_util


def get_comment_data():
    conn = common.get_connection()
    df_comment_new_data = pd.read_sql_query("select * from comment_new where newdata = 1 ", conn)
    df_comment_new_data_ldim = df_comment_new_data.loc[:, ['ID', 'MOVIEID', 'USERID']]
    return df_comment_new_data_ldim


def get_ibmovie_by_movieid(movieid, connection):
    sql = 'select DISTINCT recmovieid from ibmovie where movieid = \'%s\'' % movieid
    try:
        with connection.cursor() as cursor:
            cout = cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        connection.close()
    return None


def insert_or_update_recmovie(movieid, userid, srcmovieid, connection):
    _id = uuid.uuid4()
    time_now = datetime.datetime.now()
    q_sql = 'select id from recmovie where userid=\'%s\' and movieid=\'%s\'' % (userid, movieid)
    i_sql = 'insert into recmovie (id, userid, movieid, rectime, srcmovieid) values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (
    _id, userid, movieid, time_now, srcmovieid)
    exist_list = None
    try:
        with connection.cursor() as cursor:
            # print(q_sql)
            cout = cursor.execute(q_sql)
            exist_list = cursor.fetchall()
        if len(exist_list) > 0:
            with connection.cursor() as cursor:
                for item in exist_list:
                    u_sql = 'update recmovie set rectime=\'%s\' where id=\'%s\'' % (time_now, item[0])
                    cursor.execute(u_sql)
        else:
            with connection.cursor() as cursor:
                cursor.execute(i_sql)
    except Exception as e:
        print(e)
        connection.close()
    return None


def update_comment_new_data_flag(rid, connection):
    sql = 'update comment_new set newdata = 0 where id = \'%s\'' % rid
    try:
        with connection.cursor() as cursor:
            cout = cursor.execute(sql)
    except Exception as e:
        print(e)
        connection.close()


def exist_in_comment(movieid, userid, connection):
    sql = 'select id from comment_new where movieid = \'%s\' and userid = \'%s\'' % (movieid, userid)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            exist_list = cursor.fetchall()
        return len(exist_list) > 0
    except Exception as e:
        print(e)
        connection.close()
    return False


def func_main():
    print('start process movie based recall task:'+str(datetime.datetime.now()))
    start_time = datetime.datetime.now()

    conn = common.get_connection()
    df_comment_new_data_ldim = get_comment_data()
    conn = common.get_connection()
    for i in df_comment_new_data_ldim.index:
        print(df_comment_new_data_ldim.iloc[i]['MOVIEID'], df_comment_new_data_ldim.iloc[i]['USERID'])
        ibmovie_list = get_ibmovie_by_movieid(df_comment_new_data_ldim.iloc[i]['MOVIEID'], conn)
        for j in ibmovie_list:
            is_exist = exist_in_comment(j[0], df_comment_new_data_ldim.iloc[i]['USERID'], conn)
            if is_exist:
                print('exist in comment')
            else:
                insert_or_update_recmovie(j[0], df_comment_new_data_ldim.iloc[i]['USERID'],
                                          df_comment_new_data_ldim.iloc[i]['MOVIEID'], conn)
        #update_comment_new_data_flag(df_comment_new_data_ldim.iloc[i]['ID'], conn)
        conn.commit()

    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print('finish process movie based recall task:' + str(datetime.datetime.now()))


if __name__ == '__main__':
    sched_util.schedule_(60, func_main)