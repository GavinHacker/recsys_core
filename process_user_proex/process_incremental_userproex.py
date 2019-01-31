# -*- coding: utf-8 -*-
import common.common as common
import numpy as np
import datetime
import json
import common.schedule_util as sched_util
import math


# 全量处理userproex, 处理中位数字段
def get_user_list_in_comment(is_all_or_sample, process_func, insert_or_update_func):
    connection = common.get_connection()
    if is_all_or_sample:
        sql = 'select DISTINCT userid from comment_new where userid is not null and userid in (select userid from userproex_new where rmedian=0)'
    else:
        sql = 'select DISTINCT userid from comment_new where userid is not null and userid in (select userid from userproex_new where rmedian=0) limit 0,10'

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        process_size = 0
        while True:
            r = cursor.fetchone()
            if r is None:
                break
            process_func(r[0], insert_or_update_func, connection)
            process_size += 1
            if process_size >= 1000:
                connection.commit()
                process_size = 0
        connection.commit()
    except Exception as e:
        print(e)
        connection.close()
    connection.close()


# 插入或更新一条userproex数据
def insert_or_update_one_userproex(userid, rmax, rmin, ravg, rmedium, rcount, rsum):
    print('insert_or_update_one_userproex start')
    is_insert = True
    connection = common.get_connection()
    try:
        sql = 'select count(*) from userproex_new where userid=\'%s\'' % userid
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        res_cnt = cursor.fetchall()[0][0]
        if res_cnt > 0:
            is_insert = False
    except Exception as e:
        print('query for exist info error'+str(e))

    if is_insert:
        sql = 'insert into userproex_new(userid, rmax, rmin, ravg, rcount, rsum, rmedian) values(\'%s\', %s, %s, %s, %s, %s, %s)' % (userid, rmax, rmin, ravg, rcount, rsum, rmedium)
    else:
        sql = 'update userproex_new set rmax=%s, rmin=%s, ravg=%s, rmedian=%s, rcount=%s, rsum=%s where userid=\'%s\'' % (rmax, rmin, ravg, rmedium, rcount, rsum, userid)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        print(('insert userid:' if is_insert else 'update userid:') + str(userid) + ' success.')
    except Exception as e:
        print(e)
        connection.close()
    connection.close()


# 更新userproex数据的median字段
def update_one_userproex_4_median(userid, rmedian, connection):
    print('insert_or_update_one_userproex_4_median start')
    not_exist = True
    try:
        sql = 'select count(*) from userproex_new where userid=\'%s\'' % userid
        with connection.cursor() as cursor:
            cursor.execute(sql)
        res_cnt = cursor.fetchall()[0][0]
        if res_cnt > 0:
            not_exist = False
    except Exception as e:
        print('query for exist info error'+str(e))

    # 函数的调用场景或数据异常
    if not_exist:
        print('异常数据'+str(userid))
        return
    else:
        sql = 'update userproex_new set rmedian=%s where userid=\'%s\'' % (rmedian, userid)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print('update userproex median (userid:' + str(userid) + ') success.')
    except Exception as e:
        print(e)
        connection.close()


# 对于每一个用户, 处理userproex数据
def process_per_user(userid, insert_or_update_func):
    connection = common.get_connection()

    rmedian = 0
    rmax = 0
    rmin = 0
    ravg = 0
    rcount = 0
    rsum = 0

    sql = 'select rating from comment_new where userid=\'%s\'' % userid
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        rlist = cursor.fetchall()
        rmedian = np.median(np.array(list(map(lambda x:x[0], rlist))).astype(float))
    except Exception as e:
        print(e)
        connection.close()

    sql = 'select max(rating) as rmax, min(rating) as rmin, avg(rating) as ravg, count(rating) as rcount, sum(rating) as rsum from comment_new where userid=\'%s\'' % userid
    try:
        count = 0
        with connection.cursor() as cursor:
            count = cursor.execute(sql)
        if count > 0:
            r = cursor.fetchone()
            rmax, rmin, ravg, rcount, rsum = r[0], r[1], r[2], r[3], r[4]
    except Exception as e:
        print(e)
        connection.close()

    if rmax is None:
        rmax = 0
    if rmin is None:
        rmin = 0
    if ravg is None:
        ravg = 0
    if rcount is None:
        rcount = 0
    if rsum is None:
        rsum = 0
    if math.isnan(rmedian):
        rmedian = 0

    insert_or_update_func(userid=userid, rmax=rmax, rmin=rmin, ravg=ravg, rmedium=rmedian, rcount=rcount, rsum=rsum)
    connection.close()


# 对于每一个用户, 处理userproex数据, 但只处理median，由于max,min等都有内置函数，所以全量时直接sql处理（参考SQL文件）
def process_per_user_median(userid, insert_or_update_func, connection):
    rmedian = 0
    sql = 'select rating from comment_new where userid=\'%s\'' % userid
    try:
        with connection.cursor() as cursor:
            count = cursor.execute(sql)
        rlist = cursor.fetchall()
        rmedian = np.median(np.array(list(map(lambda x:x[0], rlist))).astype(float))
    except Exception as e:
        print(e)
        connection.close()
    if math.isnan(rmedian):
        rmedian = 0
    insert_or_update_func(userid=userid, rmedian=rmedian, connection=connection)


def get_user_list_in_log(process_func, insert_or_update_func):
    connection = common.get_connection()
    sql = 'select * from mqlog where logtype = \'u\' and pulled = 0 limit 0,10'

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        while True:
            r = cursor.fetchone()
            if r is None:
                break
            message = json.loads(r[2])
            userid = message['userid']
            print('process user\'s id is:' + userid)
            process_func(userid, insert_or_update_func)
            with connection.cursor() as cursor4update:
                update_sql = 'update mqlog set pulled=1 where id=\'%s\'' % r[0]
                cursor4update.execute(update_sql)
        connection.commit()
    except Exception as e:
        print(e)
        connection.close()
    connection.close()


def process_task():
    print('start process userproex task:'+str(datetime.datetime.now()))
    start_time = datetime.datetime.now()

    # get_user_list_in_comment(True, process_per_user_median, update_one_userproex_4_median)
    get_user_list_in_log(process_per_user, insert_or_update_one_userproex)

    end_time = datetime.datetime.now()
    print(end_time - start_time)
    print('finish process userproex task:' + str(datetime.datetime.now()))


if __name__ == '__main__':
    sched_util.schedule_(10, task_func=process_task)
