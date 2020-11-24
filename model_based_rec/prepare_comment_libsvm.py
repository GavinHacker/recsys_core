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
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
from sklearn.datasets import dump_svmlight_file
from sklearn.preprocessing import OneHotEncoder
import pickle as pkl
from sklearn import preprocessing
import common.config as cfg
import common.common as common
import common.schedule_util as sched_util


# 获取已经处理好的最新的CSV
def load_main_df_from_csv():
    conn = common.get_connection()
    csv_url = cfg.get_config_property('csv_last_url', conn)
    df = pd.read_csv(csv_url, sep='\t', encoding='utf-8')
    df = df.drop_duplicates()
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.drop_duplicates(['ID'])
    df = df.drop(['CONTENT'], axis=1)
    df = df.drop(['ADD_TIME_x', 'ADD_TIME_y'], axis=1)
    df = df.reset_index(drop=True)
    df_main = df.drop(['name', 'CREATOR','description','img','ID','NEWDATA'], axis=1)
    df_main = df_main.rename(columns = {'MOVIEID':'movieid'})
    df_main = df_main.drop(['enable'], axis=1)
    # datetime.datetime.strptime(df['TIME'][0],'%Y-%m-%d %H:%M:%S').year - 2000
    df_main = df_main.dropna(subset=['USERID','rcount']).reset_index(drop=True)

    def process_time(t):
        try:
            return datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S').year - 2000
        except Exception as e:
            print(e)

    df_main['TIME_DIS'] = df_main['TIME'].apply(lambda x: process_time(x))
    df_main = df_main.drop(['TIME'], axis=1)
    df_main = df_main.drop(['userid'], axis=1)
    return df_main


# 获取维度的频次类字典对象,如电影演员出现的频次
def get_dim_dict(df, dim_name):
    type_list = list(map(lambda x: x.split('|'), df[dim_name]))
    type_list = [x for l in type_list for x in l]

    def reduce_func(x, y):
        for i in x:
            if i[0] == y[0][0]:
                x.remove(i)
                x.append((i[0], i[1] + 1))
                return x
        x.append(y[0])
        return x

    l_ = list(filter(lambda x: x is not None, map(lambda x: [(x, 1)], type_list)))
    type_zip = reduce(reduce_func, l_)
    some_dict = {}
    for i in type_zip:
        some_dict[i[0]] = i[1]
    return some_dict


# 获取各个维度会使用到的,字典频次对象 type_dict, actors_dict, director_dict, trait_dict
def get_dicts():
    conn = common.get_connection()
    df_movie = pd.read_sql_query("select * from movie", conn)
    #type_dict = get_dim_dict(df_movie, 'type')
    actors_dict = get_dim_dict(df_movie, 'actors')
    director_dict = get_dim_dict(df_movie, 'director')
    #trait_dict = get_dim_dict(df_movie, 'trait')
    return None, actors_dict, director_dict, None


# 获取整个数据集的字典形式的数据结构（由DataFrame加工而来)
def get_dict_list(df_main, actors_dict, director_dict):
    invalid_data_list = []
    data_dict_list = []
    for i in df_main.index:
        if i % 1000 == 0:
            print('.')
        _dict = {}
        is_invalid = False
        # type
        for s_type in df_main.iloc[i]['type'].split('|'):
            _dict[s_type] = 1
        # actors
        for s_actor in df_main.iloc[i]['actors'].split('|'):
            if not s_actor in actors_dict:
                print('invalid data index is ' + str(i))
                invalid_data_list.append(i)
                is_invalid = True
                break
            if actors_dict[s_actor] < 2:
                _dict['other_actor'] = 1
            else:
                _dict[s_actor] = 1
        if is_invalid == True:
            continue
        # regios
        _dict[df_main.iloc[i]['region']] = 1
        # userid ...
        _dict[df_main.iloc[i]['USERID']] = 1
        _dict[str(df_main.iloc[i]['movieid'])] = 1
        _dict['rat'] = df_main.iloc[i]['rat']
        #_dict['rmax'] = df_main.iloc[i]['rmax']
        #_dict['rmin'] = df_main.iloc[i]['rmin']
        _dict['ravg'] = df_main.iloc[i]['ravg']
        #_dict['rcount'] = df_main.iloc[i]['rcount']
        #_dict['rsum'] = df_main.iloc[i]['rsum']
        _dict['rmedian'] = df_main.iloc[i]['rmedian']
        _dict['TIME_DIS'] = df_main.iloc[i]['TIME_DIS']
        #
        # director
        for s_director in df_main.iloc[i]['director'].split('|'):
            if director_dict[s_director] < 2:
                _dict['other_director'] = 1
            else:
                _dict[s_director] = 1
        # trait
        for s_trait in df_main.iloc[i]['trait'].split('|'):
            _dict[s_trait] = 1
        data_dict_list.append(_dict)
    print(invalid_data_list)
    print(len(data_dict_list))
    return data_dict_list

csv_url_cache = None


# 处理主函数
def process_task():
    global csv_url_cache
    start_time = datetime.datetime.now()
    print('start process comment to libsvm task:'+str(datetime.datetime.now()))

    conn = common.get_connection()
    csv_url = cfg.get_config_property('csv_last_url', conn)
    if csv_url_cache is None:
        csv_url_cache = csv_url
    elif csv_url_cache == csv_url:
        print('there is no new comment csv...')
        return
    # 从csv文件加载数据集
    data_frame_main = load_main_df_from_csv()
    conn = common.get_connection()
    # 加载字典频次对象
    _, actors_dict_, director_dict_, _ = get_dicts()
    actors_dict_save_url = cfg.get_config_property('actors_dict', conn)
    director_dict_save_url = cfg.get_config_property('director_dict', conn)
    with open(actors_dict_save_url, 'wb') as f:
        pkl.dump(actors_dict_, f)
    with open(director_dict_save_url, 'wb') as f:
        pkl.dump(director_dict_, f)

    train_y = data_frame_main['RATING']
    data_frame_main = data_frame_main.drop(['RATING'], axis=1)
    # 获取整体数据集的字典形式数据
    dict_data_list = get_dict_list(data_frame_main, actors_dict_, director_dict_)

    # 把字典形式的数据做向量化
    v = DictVectorizer()
    train_X = v.fit_transform(dict_data_list)

    train_X_ = train_X[0:280000]
    train_y_ = train_y[:280000]
    test_X_ = train_X[280000:]
    test_y_ = train_y[280000:]

    print(train_X_.shape)

    # 对于逻辑回归的训练集和测试集数据处理, 评分大于3为用户喜爱电影
    train_y_lr_ = train_y_.apply(lambda x: 1 if int(x) > 3 else 0)
    test_y_lr_ = test_y_.apply(lambda x: 1 if int(x) > 3 else 0)

    # 最大最小值归一化
    scaler = preprocessing.MaxAbsScaler()
    scaler.fit(train_X)
    train_X_scaling = scaler.transform(train_X_)
    test_X_scaling = scaler.transform(test_X_)

    train_X_lr = train_X_   # no scale
    test_X_lr = test_X_     # no scale

    time_now_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    train_file_fm_base_url = cfg.get_config_property('train_file_fm_t_url', conn)
    test_file_fm_base_url = cfg.get_config_property('test_file_fm_t_url', conn)
    train_file_fm = train_file_fm_base_url % time_now_str
    test_file_fm = test_file_fm_base_url % time_now_str

    # 转换为libsvm格式数据
    dump_svmlight_file(train_X_scaling, train_y_, train_file_fm)
    dump_svmlight_file(test_X_scaling, test_y_, test_file_fm)

    train_file_lr_base_url = cfg.get_config_property('train_file_lr_t_url', conn)
    test_file_lr_base_url = cfg.get_config_property('test_file_lr_t_url', conn)
    train_file_lr = train_file_lr_base_url % time_now_str
    test_file_lr = test_file_lr_base_url % time_now_str

    # 转换为libsvm格式数据
    dump_svmlight_file(train_X_lr, train_y_lr_, train_file_lr)
    dump_svmlight_file(test_X_lr, test_y_lr_, test_file_lr)

    cfg.set_config_property(train_file_fm, 'train_file_fm_url', conn)
    cfg.set_config_property(test_file_fm, 'test_file_fm_url', conn)
    cfg.set_config_property(train_file_lr, 'train_file_lr_url', conn)
    cfg.set_config_property(test_file_lr, 'test_file_lr_url', conn)

    dict2vec_save_url = cfg.get_config_property('dict2vec', conn)
    with open(dict2vec_save_url, 'wb') as f:
        pkl.dump(v, f)

    scaler_save_url = cfg.get_config_property('scaler', conn)
    with open(scaler_save_url, 'wb') as f:
        pkl.dump(scaler, f)

    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print('finish process comment to libsvm task:' + str(datetime.datetime.now()))


if __name__ == '__main__':
    sched_util.schedule_(60, process_task)



