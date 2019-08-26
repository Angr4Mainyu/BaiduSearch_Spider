'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-07-07 01:33:36
@LastEditTime: 2019-08-26 10:18:42
@LastEditors: Please set LastEditors
'''
# -*- coding:utf-8 -*-import re
import random
import uuid
import urllib
from flask import Flask, session, request, render_template, Response, send_file, make_response
import csv
import shutil
import zipfile
import json
import os
import time
import datetime

app = Flask(__name__)
random.seed(uuid.getnode())
app.config['SECRET_KEY'] = str(random.random()*233)

upload_path = "BaiduSearch_Spider/keyword/"
filename = "keywords.csv"
# cur_keyword = "死亡"
cur_usr = 10000

def datetime_to_stamp(date_time):
    """
    将字符串日期格式转换为时间戳  2018-10-09 16:00:00==>1539100800
    :param date_time:
    :return:
    """
    # 字符类型的时间
    time_array = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def stamp_to_datetime(stamp):
    """
    将时间戳(1539100800)转换为 datetime2018-10-09 16:00:00格式并返回
    :param stamp:
    :return:
    """
    time_stamp_array = datetime.utcfromtimestamp(stamp)
    date_time = time_stamp_array.strftime("%Y-%m-%d %H:%M:%S")
    # 如果直接返回 date_time则为字符串格式2018-10-09 16:00:00
    date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    return date


@app.route('/')
def index():
    # session['username'] = 'www-data'
    if session == None:
        session['username'] = 'test-user'
    if 'userID' not in session:
        global cur_usr
        cur_usr += 1
        session['userID'] = str(cur_usr)
    print(session)
    return render_template("index.html", title="百度信息榨取")

# 多关键词文件查询页面
@app.route('/multi_keyword')
def multi_keyword():
    if session == None:
        session['username'] = 'test-user'
    if 'userID' not in session:
        global cur_usr
        cur_usr += 1
        session['userID'] = str(cur_usr)
    print(session)
    return render_template("multi_keyword.html", title="百度信息榨取")


# 读取csv并且输入为json
def read_csv(filename, spider='search'):
    csvfile = open(filename, encoding='utf-8-sig')
    if spider == 'search':
        header = ('title', 'time', 'brief', 'link')
    else:
        header = ('title', 'platform', 'date', 'time', 'brief', 'body', 'link')
    reader = csv.DictReader(csvfile, header)
    result = []
    for row in reader:
        result.append(json.dumps(row))
    return result


# 输入关键词搜索的爬虫
@app.route('/api/search_spider', methods=['GET', 'POST'])
def search_spider():
    keyword = request.args.get("keyword")
    cmd = 'scrapy crawl searchspider -a search="{}" -a keyword="{}"'.format(
        keyword, keyword)
    time_range = request.args.get("time")
    if time_range != "":
        time_range = time_range.split(' - ')
        cmd += ' -a beg_time={} -a end_time={}'.format(
            datetime_to_stamp(time_range[0]), datetime_to_stamp(time_range[1]))
    session['keyword'] = keyword
    session['type'] = 'search'
    print(cmd)
    os.popen(cmd)
    res = {
        'code': 0,
        'msg': '百度搜索爬虫启动!'
    }
    return Response(json.dumps(res), content_type='application/json')

# 打印结果的前20条供预览
@app.route('/api/get_result', methods=['GET'])
def get_result():
    keyword = session['keyword']
    spider_type = session['type']
    # 打印前20条
    result = read_csv('BaiduSearch_Spider/data/{}data/baidu_{}.csv'.format(
        spider_type, keyword.replace("|", " ")), spider_type)[1:21]
    data = '[' + ','.join(result) + ']'
    res = {
        'code': 0,
        'msg': 'success',
        'count': len(result),
        'data': json.loads(data)
    }
    return Response(json.dumps(res), content_type='application/json')


# 爬取新闻的接口
@app.route('/api/news_spider', methods=['GET', 'POST'])
def news_spider():
    keyword = request.args.get("keyword")
    cmd = 'scrapy crawl newsspider -a search="{}" -a keyword="{}"'.format(
        keyword, keyword)
    time_range = request.args.get("time")
    if time_range != "":
        time_range = time_range.split(' - ')
        cmd += ' -a beg_time={} -a end_time={}'.format(
            datetime_to_stamp(time_range[0]), datetime_to_stamp(time_range[1]))
    session['keyword'] = keyword
    session['type'] = 'news'
    print(cmd)
    os.popen(cmd)
    res = {
        'code': 0,
        'msg': '新闻搜索爬虫启动!'
    }
    return Response(json.dumps(res), content_type='application/json')

# 打包文件下载
@app.route('/api/download_files', methods=['GET', 'POST'])
def download_files():
    typ = request.args.get("type")
    if typ == "search":
        output_path = "BaiduSearch_Spider/data/searchdata/{}".format(session["userID"])
        file_name = 'baidu_search.csv'
    else:
        output_path = "BaiduSearch_Spider/data/newsdata/{}".format(session["userID"])
        file_name = 'baidu_news.csv'
    with zipfile.ZipFile('result.zip', 'w') as target:
        for i in os.walk(output_path):
            print(i)
            for n in i[2]:
                target.write(''.join((i[0], '/', n)), n)
        target.close()
    file_name = "result.zip"
    res = make_response(
        send_file("../" + file_name))
    res.headers['Content-Disposition'] = 'attachment; filename={}'.format(
        file_name)
    return res

 
@app.route('/api/download')
def download():
    typ = request.args.get("type")
    cur_keyword = session['keyword']
    if typ == "search":
        output_path = "../BaiduSearch_Spider/data/searchdata"
        file_name = 'baidu_{}.csv'.format(cur_keyword)
    else:
        output_path = "../BaiduSearch_Spider/data/newsdata"
        file_name = 'baidu_{}.csv'.format(cur_keyword)
    res = make_response(
        send_file(os.path.join(output_path, file_name)))
    res.headers['Content-Disposition'] = 'attachment; filename={}'.format(
        'result.csv')
    return res


# 检查进度
@app.route('/api/check_status', methods=['GET', 'POST'])
def check_status():
    typ = request.args.get("type")
    if typ == "search":
        output_path = "BaiduSearch_Spider/data/searchdata/{}".format(session["userID"])
    else:
        output_path = "BaiduSearch_Spider/data/newsdata/{}".format(session["userID"])
    count = len(os.listdir(output_path))
    res = {
        'count': count,
        'code': 0,
        'msg': 'success'
    }
    return Response(json.dumps(res), content_type='application/json')


# 从csv文件中读取关键词爬取
@app.route('/api/file_spider', methods=['GET', 'POST'])
def file_spider():
    # 获取关键词的总数量
    filename = "keywords_{}.csv".format(session['userID'])
    count = len(open(upload_path + filename, encoding='utf-8-sig').readlines()) - 1
    # 进行爬虫操作，由于文件比较大一般不可能等到爬完，所以新建一个线程进行爬取
    typ = request.args.get("type")
    if typ == "search":
        cmd = 'scrapy crawl searchspider -a user_id="{}"'.format(session['userID'])
        output_path = "BaiduSearch_Spider/data/searchdata/{}".format(session["userID"])
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            os.mkdir(output_path)
        else:
            os.mkdir(output_path)
    else:
        cmd = 'scrapy crawl newsspider -a user_id="{}"'.format(session['userID'])
        output_path = "BaiduSearch_Spider/data/newsdata/{}".format(session["userID"])
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            os.mkdir(output_path)
        else:
            os.mkdir(output_path)

    time_range = request.args.get("time")
    if time_range != "":
        time_range = time_range.split(' - ')
        cmd += ' -a beg_time={} -a end_time={}'.format(
            datetime_to_stamp(time_range[0]), datetime_to_stamp(time_range[1]))
    print(cmd)
    os.popen(cmd)
    res = {
        "count": count,
        "code": 0,
        'msg': 'success'
    }
    return Response(json.dumps(res), content_type='application/json')


# 文件上传接口
@app.route('/api/upload', methods=['GET', 'POST'])
def upload():
    # print(request)
    filename = "keywords_{}.csv".format(session['userID'])
    try:
        file = request.files['file']
        file.save(upload_path + filename)
        count = len(open(upload_path + filename, encoding='utf-8-sig').readlines()) - 1
        if count > 500:
            res = {
                'code' : 0,
                'msg' : '关键词过多,耗时会比较长</br>建议拆分成几个文件多次爬取'
            }
        else:
            res = {
                'code': 0,
                'msg': '上传成功' 
            }
    except:
        res = {
            'code': 1,
            'msg': '上传失败'
        }
    return Response(json.dumps(res), content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
