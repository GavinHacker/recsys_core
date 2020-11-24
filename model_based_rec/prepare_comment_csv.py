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
import common.common as common
import common.config as cfg
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
import common.schedule_util as sched_util


# 处理mqlog中记录的新的电影评分, 通过sql读取mqlog中类型为c的电影评分动作, 查询出相关的用户\电影\评分信息, 然后追加到训练集的csv上（训练集的csv会变大)
def process_comment_by_log(process_func):
    connection = common.get_connection()
    sql = 'select * from mqlog where logtype = \'c\' and pulled = 0 limit 0, 1000'
    try:
        comment_id_list = []
        movie_id_list = []
        user_id_list = []
        message_id_list = []
        with connection.cursor() as cursor:
            cursor.execute(sql)
            while True:
                r = cursor.fetchone()
                if r is None:
                    break
                message = json.loads(r[2])
                comment_id = message['id']
                comment_id_list.append(comment_id)
                movie_id = message['movieid']
                movie_id_list.append(movie_id)
                user_id = message['userid']
                user_id_list.append(user_id)
                message_id_list.append(r[0])
        print('process comment\'s id collection is:' + str(comment_id_list))
        if len(comment_id_list) == 0 or len(movie_id_list) == 0 or len(user_id_list) == 0:
            print('No new available comment')
            return
        process_func(comment_id_list, movie_id_list, user_id_list, connection)
        # 把mqlog表的pulled表标记为1, 即处理过此消息,不再二次处理
        with connection.cursor() as cursor4update:
            for id_ in message_id_list:
                update_sql = 'update mqlog set pulled=1 where id=\'%s\'' % id_
                cursor4update.execute(update_sql)
        connection.commit()
    except Exception as e:
        print(e)
        connection.close()
    connection.close()


# 处理新的电影评分的具体处理函数,作为回调函数被传递使用
def process_new_comment_collection(comment_list, movie_list, user_list, conn):
    exp_comment = '(\'' + reduce(lambda x, y: x+'\',\''+y, comment_list) + '\')'
    c_sql = 'select * from comment_new where id in ' + exp_comment
    print(c_sql)
    exp_movie = '(\'' + reduce(lambda x, y: x+'\',\''+y, movie_list) + '\')'
    m_sql = 'select * from movie where id in ' + exp_movie
    print(m_sql)
    exp_user = '(\'' + reduce(lambda x, y: x+'\',\''+y, user_list) + '\')'
    u_sql = "select * from userproex_new where userid in " + exp_user
    print(u_sql)
    df_incremental = pd.read_sql_query(c_sql, conn)
    df_movie = pd.read_sql_query(m_sql, conn)
    df_user_pro = pd.read_sql_query(u_sql, conn)
    df_data = pd.merge(df_incremental, df_movie, left_on=['MOVIEID'], right_on=['id'])
    df_data = pd.merge(df_data, df_user_pro, left_on=['USERID'], right_on=['userid'])
    df_origin = pd.read_csv(cfg.get_config_property('csv_last_url', conn), sep='\t', encoding='utf-8')
    df_all = df_origin.append(df_data)
    time_now_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    new_csv_url = cfg.get_config_property('csv_base_url', conn) % time_now_str
    df_all.to_csv(new_csv_url, sep='\t', encoding='utf-8')
    cfg.set_config_property(new_csv_url, 'csv_last_url', conn)


# 定时任务处理入口函数
def process_task():
    start_time = datetime.datetime.now()
    print('start process comment csv task:'+str(datetime.datetime.now()))

    process_comment_by_log(process_new_comment_collection)

    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print('finish process comment csv task:' + str(datetime.datetime.now()))


if __name__ == '__main__':
    sched_util.schedule_(60, process_task)


