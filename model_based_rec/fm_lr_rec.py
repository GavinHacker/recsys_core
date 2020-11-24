# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
import pymysql.cursors
from functools import reduce
import numpy as np
import pandas as pd
import uuid
import datetime
#from pyfm import pylibfm
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import pairwise_distances
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
from sklearn.datasets import dump_svmlight_file
from sklearn.preprocessing import OneHotEncoder
import pickle as pkl
from sklearn.metrics import roc_auc_score, mean_squared_error
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import LogisticRegression
import pickle as pkl
import subprocess
import tempfile
import os
import common.config as cfg
import common.common as common
import common.schedule_util as sched_util


# 使用命令行运行FM模型调用
def run(cmd):

    conn = common.get_connection()
    base_dir = cfg.get_config_property('dir_base_url', conn)
    temp_dir = base_dir + os.sep + 'tmp' + os.sep
    out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000 * 1000)
    final_temp_dir = temp_dir + os.sep
    cmd = cmd.split(' ')
    try:
        fileno = out_temp.fileno()
        p = subprocess.Popen(cmd, shell=False, cwd=final_temp_dir, stdout=fileno,
                             stderr=fileno, universal_newlines=True)
        p.wait(1000000000000)
        out_temp.seek(0)
        print(out_temp.read().decode('utf8', 'replace'))
    except Exception as e:
        raise RuntimeError('run error: %s' % str(e))
    finally:
        if out_temp:
            out_temp.close()

# FM模型使用函数, 输入训练集的file: train_file, 要预测的数据的file: test_file
def fm(train_file, test_file, classification=True, rank=10, n_iter=150):
    conn = common.get_connection()
    libfm = cfg.get_config_property('lib_fm_path', conn)
    task = 'c' if classification else 'r'
    base_dir = cfg.get_config_property('dir_base_url', conn)
    cmd_ = '%s -task %s -method mcmc -train %s -test %s -iter %s -dim \'1,1,%s\' -out %soutput_.libfm' % (libfm, task, train_file, test_file, n_iter, rank, base_dir)
    #console_output = !$LIBFM_PATH -task $task -method als -regular '0,0,10' -train $train_file -test $test_file -iter $n_iter -dim '1,1,$rank' -save_model recsysmode.fm -out output_.libfm
    #console_output = !$LIBFM_PATH -task $task -method sgd -train $train_file -test $test_file -iter $n_iter -dim '1,1,$rank' -save_model recsysmode.fm -out output_.libfm
    print(libfm)
    console_output = run(cmd_)
    print(console_output)
    libfm_predict = pd.read_csv('%soutput_.libfm' % base_dir, header=None).values.flatten()
    return libfm_predict


# 测试FM
def test_fm_by_test_data(train_file, test_file):

    conn = common.get_connection()
    libfm_predict = fm(train_file, test_file, classification=False)

    libfm_predict_series = pd.Series(libfm_predict)
    libfm_predict_series_int = libfm_predict_series.apply(lambda x:int(x))

    _, y = get_data(test_file)

    print('MSE(to int):' + str(mean_squared_error(y, libfm_predict_series_int.tolist())))
    print('MSE(origin):' + str(mean_squared_error(y, libfm_predict_series.tolist())))


# 从路径中获取libsvm数据, 返回X矩阵和 y矩阵
def get_data(path):
    data = load_svmlight_file(path)
    return data[0], data[1]


# 获取 由 相似度矩阵得来的 推荐电影集合
def get_recmovie_by_movie_based():
    conn = common.get_connection()
    sql = 'select * from recmovie left join movie on movie.id=recmovie.movieid left join userproex_new on userproex_new.userid=recmovie.userid'
    df_data = pd.read_sql_query(sql, conn)
    #df_data = df_data.drop([0], axis=1)
    #df_data = df_data.rename(columns = {'userid':'USERID'})
    #df_data['USERID'].fillna(0)
    print(df_data.columns)
    df_data = df_data.loc[:,~df_data.columns.duplicated()]
    #print(df_data.shape)
    df_data = df_data.rename(columns = {'userid':'USERID'})
    df_data['TIME_DIS'] = np.zeros(df_data.shape[0])
    df_data = df_data.fillna(0)
    return df_data


# 获取保存的对象, 1 演员出现频次字典对象 2 导演出现频次字典对象 3 将训练数据由字典到vector进行向量化的时候保存的处理器 4 scaler处理器
def get_saved_actors_dict_director_dict_vectorizer():
    conn = common.get_connection()
    dict2vec_url = cfg.get_config_property('dict2vec', conn)
    actors_dict_url = cfg.get_config_property('actors_dict', conn)
    director_dict_url = cfg.get_config_property('director_dict', conn)
    scaler_url = cfg.get_config_property('scaler', conn)

    with open(dict2vec_url, 'rb') as f:
        v_from_pkl = pkl.load(f)

    with open(actors_dict_url, 'rb') as f:
        actors_dict = pkl.load(f)

    with open(director_dict_url, 'rb') as f:
        director_dict = pkl.load(f)

    with open(scaler_url, 'rb') as f:
        scaler = pkl.load(f)

    return actors_dict, director_dict, v_from_pkl, scaler


# 把一个dataframe转换成为row为字典形式的list, 每个row是一个字典, 其中包含了所有维度作为key
def convert_dataframe_2_dict_list(df_main, actors_dict, director_dict):
    data_dict_list = []
    for i in df_main.index:
        _dict = {}
        is_invalid = False
        # type
        for s_type in df_main.iloc[i]['type'].split('|'):
            _dict[s_type] = 1
        # actors
        for s_actor in df_main.iloc[i]['actors'].split('|'):
            if not s_actor in actors_dict:
                print('invalid data index is ' + str(i))
                is_invalid = True
                break
            if actors_dict[s_actor] < 2:
                _dict['other_actor'] = 1
            else:
                _dict[s_actor] = 1
        if is_invalid == True:
            continue;
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
    return data_dict_list


# 更推荐表（recmovie表）中的FM模型打分和LR模型打分
def update_recmovie_rat(id, rat, connection, model_type):
    rat_field = None
    if model_type == 'LR':
        rat_field = 'recmovie.lrrat'
    elif model_type == 'FM':
        rat_field = 'recmovie.fmrat'

    sql = 'update recmovie set %s = %s,rectime=\'%s\' where id = \'%s\'' % (rat_field, rat, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id)
    print(sql)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    except:
        connection.close()


# 更新recmove表中的FM评分
def update_fm_rat(df_data, libfm_predict_final):
    conn = common.get_connection()
    index_ = 0
    for r in libfm_predict_final:
        r_temp = str(r)
        try:
            r_temp = str(r)[0:1]
        except Exception as e:
            print("Update FM rat exception")
            print(e)
        update_recmovie_rat(df_data.iloc[index_]['id'], r_temp, conn, 'FM')
        index_ += 1


# 更新recmove表中的LF模型给出的推荐评分
def update_lr_rat(df_data, lr_predict_final):
    conn = common.get_connection()
    index_ = 0
    for r in lr_predict_final:
        update_recmovie_rat(df_data.iloc[index_]['id'], r[1], conn, 'LR')
        index_ += 1


# 处理任务入口函数
def process_task():
    _conn = common.get_connection()
    # update_recmovie_rat('1', '1', _conn, 'FM')
    # os._exit(0)
    train_file_scaling = cfg.get_config_property('train_file_fm_url', _conn)
    test_file_scaling = cfg.get_config_property('test_file_fm_url', _conn)
    # test_fm_by_test_data(train_file_scaling, test_file_scaling)
    df_data = get_recmovie_by_movie_based()
    actor_dict_data, director_dict_data, vectorizer, scaler = get_saved_actors_dict_director_dict_vectorizer()
    dict_list = convert_dataframe_2_dict_list(df_data, actor_dict_data, director_dict_data)
    X_predict = vectorizer.transform(dict_list)
    predict_file_ = cfg.get_config_property('dir_base_url', _conn) + 'X_predict.txt'

    # FM PART
    # 把 X_predict 处理成libsvm格式,供libfm使用
    dump_svmlight_file(scaler.transform(X_predict), np.zeros(X_predict.shape[0]), predict_file_)
    libfm_predict_final = fm(train_file_scaling, predict_file_, classification=False)
    update_fm_rat(df_data, libfm_predict_final)

    # LR PART
    train_file_lr_path = cfg.get_config_property('train_file_lr_url', _conn)
    test_file_lr_path = cfg.get_config_property('test_file_lr_url', _conn)

    train_X_lr, train_y = get_data(train_file_lr_path)
    # test_X_lr, test_y = get_data(test_file_lr_path)
    print(train_X_lr.shape)

    lr = LogisticRegression(C=0.1, penalty='l2')
    lr.fit(train_X_lr, train_y)

    # test_predict = vectorizer.transform([{'尼泊尔': 1},
    #                                      {'赵本山': 1, '赵薇': 1, '张曼玉': 1, 'rat': '8.0',
    #                                                   'ravg': 3.85714,
    #                                                   'rcount': 7.0,
    #                                                   'rmax': 5.0,
    #                                                   'rmedian': 4.0,
    #                                                   'rmin': 2.0,
    #                                                   'rsum': 27.0},
    #                                      {'克里斯·派恩': 1, '扎克瑞·昆图': 1, '佐伊·索尔达娜': 1,'西蒙·佩吉':1, '安东·叶利钦':1, '林诣彬':1 ,
    #                                                  '美国':1,
    #                                                   'rat': '8.0',
    #                                                   'ravg': 3.85714,
    #                                                   'rcount': 7.0,
    #                                                   'rmax': 5.0,
    #                                                   'rmedian': 4.0,
    #                                                   'rmin': 2.0,
    #                                                   'rsum': 27.0}])
    # print(lr.predict_proba(test_predict))

    lr_predict_final = lr.predict_proba(X_predict)
    update_lr_rat(df_data, lr_predict_final.tolist())
    print(lr.classes_)


if __name__ == '__main__':
    sched_util.schedule_(10*60*1000, task_func=process_task)