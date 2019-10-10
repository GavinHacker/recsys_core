# coding=utf-8
import urllib
import os
import pymysql


def get_connection():
    return pymysql.connect(host='x.x.x.x',
                               user='root',
                               password='root',
                               db='r',
                               port=3306,
                               charset ='utf8',
                               use_unicode=True)


def save_img(img_url, file_name, file_path='book\img'):
    # 保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        if not os.path.exists(file_path):
            print 'folder', file_path, 'not exist，recreate'
            # os.mkdir(file_path)
            os.makedirs(file_path)
        # 获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        # 拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
        # 下载图片，并保存到文件夹中
        urllib.urlretrieve(img_url, filename=filename)
    except IOError as e:
        print 'file process error',e
    except Exception as e:
        print 'error ：',e


def process_all_img_url(process_func):
    connection = get_connection()
    sql = 'select id, img from movie'
    base_path = 'http://x.com/x/p/'
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            while True:
                try:
                    r = cursor.fetchone()
                    if r is None:
                        break
                    file_name = r[0]
                    file_url = r[1]
                    process_func(file_url, file_name)
                    conn2 = get_connection()
                    with conn2.cursor() as cursor4update:
                        new_img_url = base_path + file_name + os.path.splitext(file_url)[1]
                        update_sql = 'update m set img=\'%s\' where id=\'%s\'' % (new_img_url, file_name)
                        cursor4update.execute(update_sql)
                        conn2.commit()
                    conn2.close()
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
        connection.close()
    connection.close()


if __name__ == '__main__':
    # img_url = 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2317864927.jpg'
    # url_part_list = img_url.split('/')
    # url_part_list.reverse()
    # print(url_part_list[0]);
    # save_img(img_url, url_part_list[0])
    process_all_img_url(save_img)
