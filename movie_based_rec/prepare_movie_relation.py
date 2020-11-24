# -*- coding: utf-8 -*-

from functools import reduce
import numpy as np
import pandas as pd
import uuid
import datetime
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import common.common as common
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
import json
import common.schedule_util as sched_util


# 从数据库中获取全量的电影数据
def get_movie_data():
    df = pd.read_sql_query("select * from movie", common.get_connection())
    df_imp = df.drop(['ADD_TIME', 'enable', 'rat', 'id', 'name'], axis=1)
    return df, df_imp


# 获取维度上出现的频率统计数据
def get_dim_dict(df, dim_name):
    type_list = list(map(lambda x:x.split('|') ,df[dim_name]))
    type_list = [x for l in type_list for x in l]

    def reduce_func(x, y):
        for i in x:
            if i[0] == y[0][0]:
                x.remove(i)
                x.append((i[0], i[1] + 1))
                return x
        x.append(y[0])
        return x
    l = filter(lambda x: x is not None, map(lambda x:[(x, 1)], type_list))
    type_zip = reduce(reduce_func, list(l))
    type_dict = {}
    for i in type_zip:
        type_dict[i[0]] = i[1]
    return type_dict


# 获取各个频率统计字典对象
def get_typedict_actorsdict_directordict_traitdict():
    _, df = get_movie_data()
    type_dict = get_dim_dict(df, 'type')
    actors_dict = get_dim_dict(df, 'actors')
    director_dict = get_dim_dict(df, 'director')
    trait_dict = get_dim_dict(df, 'trait')
    return type_dict, actors_dict, director_dict, trait_dict


# 将原始数据转换为字典数据
def convert_to_dict_list(df_):
    _, actors_dict, director_dict, _ = get_typedict_actorsdict_directordict_traitdict()
    movie_dict_list = []
    for i in df_.index:
        movie_dict = {}
        # type
        for s_type in df_.iloc[i]['type'].split('|'):
            movie_dict[s_type] = 1
        # actors
        for s_actor in df_.iloc[i]['actors'].split('|'):
            if actors_dict[s_actor] < 2:
                movie_dict['other_actor'] = 1
            else:
                movie_dict[s_actor] = 1
        # regios
        movie_dict[df_.iloc[i]['region']] = 1
        # director
        for s_director in df_.iloc[i]['director'].split('|'):
            if director_dict[s_director] < 2:
                movie_dict['other_director'] = 1
            else:
                movie_dict[s_director] = 1
        # trait
        for s_trait in df_.iloc[i]['trait'].split('|'):
            movie_dict[s_trait] = 1
        movie_dict_list.append(movie_dict)
    return movie_dict_list


# 分别获取相似矩阵, 字典 -> 向量 转换器, 矩阵向量
def get_0similarity_matrix_1dict_vectorizer_2vector_matrix(movie_dict_list):
    v = DictVectorizer()
    X = v.fit_transform(movie_dict_list)
    item_similarity = pairwise_distances(X, metric='cosine')
    return item_similarity, v, X


# 测试函数
def test_similarity_matrix(item_similarity_matrix, movie_dict_list, vector_matrix, dict_vectorizer, original_df, compare_index):
    index = 0
    _max_index = 0
    _max = 1
    for i in item_similarity_matrix[compare_index]:
        if i < _max and i != 0:
            _max = i
            _max_index = index
        index += 1
    print(_max_index, _max)
    index_of_sim = _max_index

    print(original_df.iloc[index_of_sim])
    print(movie_dict_list[index_of_sim])
    df_106 = pd.DataFrame(data=vector_matrix.todense()[index_of_sim], columns=dict_vectorizer.feature_names_)
    df_0 = pd.DataFrame(data=vector_matrix.todense()[compare_index], columns=dict_vectorizer.feature_names_)
    df_diff = pd.concat([df_0, df_106], axis=0, ignore_index=True)
    df_diff = df_diff.T
    print(df_diff[(df_diff[0] != 0) | (df_diff[1] != 0)])


# 插入一个movie based数据
def insert_one_ibmovie(id_,
                       movieid,
                       recmovieid,
                       recmovierat,
                       simrat,
                       time,
                       enable, connection):

    exist_sql = 'select count(*) as cnt from ibmovie where movieid = \'%s\' and recmovieid = \'%s\'' % (movieid, recmovieid)
    try:
        with connection.cursor() as cursor:
            cursor.execute(exist_sql)
            r = cursor.fetchone()
            if r is not None and r[0] > 1:
                print('exist ibmovie data, movieid:' + movieid + " recmovieid:" + recmovieid)
                return
    except Exception as e:
        print('exception:' + str(e))
        try:
            connection.close()
        except Exception as e:
            print(e)
            pass
    print('insert one recmovie, movieid:' + movieid + "recmovieid:" + recmovieid)
    sql = 'insert into ibmovie (id, movieid, recmovieid, recmovierat, simrat, time, enable) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (id_, movieid, recmovieid, recmovierat, simrat, time, enable)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    except Exception as e:
        print('exception:' + str(e))
        try:
            connection.close()
        except Exception as e:
            print(e)
            pass


# 根据某电影ID, 查询ibmovie表中,关于某电影已经存在的相似电影数量
def get_recmovie_cnt_by_movieid(movieid, connection):
    sql = 'select count(*) from ibmovie group by movieid having movieid=\'%s\'' % movieid
    try:
        with connection.cursor() as cursor:
            cout = cursor.execute(sql)
            if cout == 0:
                return 0
            return cursor.fetchone()[0]
    except Exception as e:
        print('exception@get_recmovie_by_movieid:' + str(e))
        try:
            connection.cursor().close()
            connection.close()
            print('closed')
        except Exception as e1:
            print('exception1@get_recmovie_by_movieid:' + str(e1))
        connection = common.get_connection()


# 处理全量数据（初始化数据)入口函数; 一般此函数应是初始化时执行,如果数据库中,ibmovie表已经是初始化好的,本函数不用二次执行
def process_offline_compute_by_cosdis(rec_per_num, item_similarity, df_sim, df_orgin):
    rec_per_num += 1
    connection = common.get_connection()
    for i in range(0, item_similarity.shape[0]):
        # 获取与i相似度rec_per_num个数量的电影, 并插入到ibmovie中
        df_sim_p = df_sim.nsmallest(rec_per_num, i)
        df_sim_p = df_sim_p[i]
        movie_id = df_orgin.iloc[i]['id']
        recmovie_cnt = get_recmovie_cnt_by_movieid(movie_id, connection)
        if recmovie_cnt == 200:
            print('pass...')
            continue
        print('new...')
        time_now = datetime.datetime.now()
        for rec_movie_item in df_sim_p.to_dict().items():
            if rec_movie_item[0] != i:
                rec_movie_index = rec_movie_item[0]
                rec_movie_sim = rec_movie_item[1]
                rec_movie_id = df_orgin.iloc[rec_movie_index]['id']
                rec_movie_rat = df_orgin.iloc[rec_movie_index]['rat']
                insert_one_ibmovie(id_=uuid.uuid4(), movieid=movie_id, recmovieid=rec_movie_id,
                                   recmovierat=rec_movie_rat, simrat=rec_movie_sim, time=time_now, enable='1',
                                   connection=connection)
        connection.commit()


# 增量处理 当电影数据增加的时候 扫描mqlog表, 查询logtype为m的数据, 得到增量的电影, 然后调用处理函数（process_func）
def process_by_movie_change_log(process_func, sim_matrix, df_origin):
    connection = common.get_connection()
    sql = 'select * from mqlog where logtype = \'m\' and pulled = 0 limit 0,10'
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        while True:
            r = cursor.fetchone()
            if r is None:
                break
            message = json.loads(r[2])
            movieid = message['movieid']
            print('process movie\'s id is:' + movieid)
            process_func(movieid, sim_matrix, df_origin)
            with connection.cursor() as cursor4update:
                update_sql = 'update mqlog set pulled=1 where id=\'%s\'' % r[0]
                cursor4update.execute(update_sql)
        connection.commit()
    except Exception as e:
        print(e)
        connection.close()
    connection.close()


def get_min_sim_movie_by_movieid(movieid):
    connection = common.get_connection()
    sql = 'select id,simrat,convert(simrat , DECIMAL(5,5)) as simrat_5 from ibmovie where movieid = \'%s\' order by convert(simrat , DECIMAL(5,5)) desc limit 0,10' % movieid
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)

        r = cursor.fetchone()
        if r is None:
            return None
        return r
    except Exception as e:
        print(e)
        connection.close()
    connection.close()


# 处理每一个增量的电影, 在相似度矩阵中查找到关于新电影 的相似电影集合, 插入到ibmoive中
def process_per_movie(movieid, sim_matrix, df_origin, rec_per_num=201):
    df_sim_matrix = pd.DataFrame(data=sim_matrix)
    print(df_sim_matrix.shape)
    connection = common.get_connection()
    time_now = datetime.datetime.now()
    for i in range(0, sim_matrix.shape[0]):
        if df_origin.iloc[i]['id'] == movieid:
            print(df_origin.iloc[i])
            df_sim_p_self = df_sim_matrix.nsmallest(rec_per_num, i)
            df_sim_p_self = df_sim_p_self[i]
            for rec_movie_item in df_sim_p_self.to_dict().items():
                if rec_movie_item[0] != i:
                    rec_movie_index = rec_movie_item[0]
                    rec_movie_dis = rec_movie_item[1]
                    rec_movie_id = df_origin.iloc[rec_movie_index]['id']
                    rec_movie_rat = df_origin.iloc[rec_movie_index]['rat']
                    insert_one_ibmovie(id_=uuid.uuid4(), movieid=movieid, recmovieid=rec_movie_id,
                                       recmovierat=rec_movie_rat, simrat=rec_movie_dis, time=time_now, enable='1',
                                       connection=connection)

            df_sim_p = df_sim_matrix[i]
            sim_item_list = df_sim_p.to_dict().items()
            sim_item_list_new = list(filter(lambda x: True if float(x[1]) < 0.80482 else False, sim_item_list))
            for sim_movie_item in sim_item_list_new:
                if sim_movie_item[0] != i:
                    sim_movie_index = sim_movie_item[0]
                    sim_movie_dis = sim_movie_item[1]
                    sime_movie_id = df_origin.iloc[sim_movie_index]['id']
                    sim_movie_rat = df_origin.iloc[sim_movie_index]['rat']

                    min_sim_movie4self = get_min_sim_movie_by_movieid(sime_movie_id)
                    print(min_sim_movie4self)
                    print(sim_movie_dis)
                    if sim_movie_dis < min_sim_movie4self[2]:
                        print('insert as recmovie...')
                        insert_one_ibmovie(id_=uuid.uuid4(), movieid=sime_movie_id, recmovieid=movieid,
                                           recmovierat=sim_movie_rat, simrat=sim_movie_dis, time=time_now, enable='1',
                                           connection=connection)


# 处理主函数
def process_task():
    print('start process movie similarity task:'+str(datetime.datetime.now()))
    start_time = datetime.datetime.now()
    df_origin, df_simple = get_movie_data()
    movie_dict_list = convert_to_dict_list(df_simple)
    # 得到相似度矩阵
    similarity_matrix, dict_vectorizer, vector_matrix = get_0similarity_matrix_1dict_vectorizer_2vector_matrix(movie_dict_list)
    # 处理mqlog的消息日志, 如果出现新的电影, 则执行相似电影的计算插入到ibmoive表中
    process_by_movie_change_log(process_per_movie, similarity_matrix, df_origin)
    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print('finish process movie similarity task:' + str(datetime.datetime.now()))


if __name__ == '__main__':
    sched_util.schedule_(10, task_func=process_task)