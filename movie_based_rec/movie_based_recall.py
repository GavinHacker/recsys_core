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


# 获取新的电影评分数据,即用户对某个电影作出的新的评论打分
def get_comment_data():
    conn = common.get_connection()
    df_comment_new_data = pd.read_sql_query("select * from comment_new where newdata = 1 ", conn)
    df_comment_new_data_ldim = df_comment_new_data.loc[:, ['ID', 'MOVIEID', 'USERID']]
    return df_comment_new_data_ldim


# 根据电影id, 到ibmovie表中, 获取所有与该电影相似的电影
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


# 将推荐的电影插入或更新到recmovie表（当推荐的电影已经存在于recmovie, 执行更新, 如果不存在 则执行插入）
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


# 更新newdata字段, 即对于新的评分数据做已读处理,不会二次处理
def update_comment_new_data_flag(rid, connection):
    sql = 'update comment_new set newdata = 0 where id = \'%s\'' % rid
    try:
        with connection.cursor() as cursor:
            cout = cursor.execute(sql)
    except Exception as e:
        print(e)
        connection.close()


# 判断某个用户是不是对于某个电影已经有了评分
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


# 处理主函数
def func_main():
    print('start process movie based recall task:'+str(datetime.datetime.now()))
    start_time = datetime.datetime.now()

    conn = common.get_connection()
    # 获取增量的评论评分数据
    df_comment_new_data_ldim = get_comment_data()
    conn = common.get_connection()
    # 遍历评分数据
    for i in df_comment_new_data_ldim.index:
        print(df_comment_new_data_ldim.iloc[i]['MOVIEID'], df_comment_new_data_ldim.iloc[i]['USERID'])
        # 从相似推荐中找到相似的电影
        ibmovie_list = get_ibmovie_by_movieid(df_comment_new_data_ldim.iloc[i]['MOVIEID'], conn)
        for j in ibmovie_list:
            is_exist = exist_in_comment(j[0], df_comment_new_data_ldim.iloc[i]['USERID'], conn)
            # 如果推荐的电影,该用户已经评分过（看过, 则不推荐
            # 否则, 插入到recmove表中（recmove表的插入也有存在判断,如果存在,则更新）
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
    sched_util.schedule_(10*60*1000, func_main)