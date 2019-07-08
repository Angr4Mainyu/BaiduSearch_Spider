import re
import random
import uuid
import urllib
from flask import Flask, session, request, render_template, Response, send_file, make_response
import csv
import json
import os

app = Flask(__name__)
random.seed(uuid.getnode())
app.config['SECRET_KEY'] = str(random.random()*233)
app.debug = True


@app.route('/')
def index():
    session['username'] = 'www-data'
    return render_template("index.html")


# 读取csv并且输入为json
def read_csv(filename):
    csvfile = open(filename)
    # header = ('title','platform','date','time','brief','body','link')
    header = ('number', 'title', 'time', 'brief', 'link')
    reader = csv.DictReader(csvfile, header)
    result = []
    for row in reader:
        result.append(json.dumps(row))
    return result


@app.route('/api/spider', methods=['GET', 'POST'])
def spider():
    keyword = request.args.get("keyword")
    os.system(
        "scrapy crawl searchspider -a search={} -a keyword={}".format(keyword, keyword))
    # 打印前10条
    result = read_csv('BaiduSearch_Spider\data\\baidusearch_test.csv')[:20]
    data = '[' + ','.join(result) + ']'
    res = {
        'code': 0,
        'msg': 'success',
        'count': len(result),
        'data': json.loads(data)
    }
    return Response(json.dumps(res), content_type='application/json')


@app.route('/api/download')
def download():
    res = make_response(send_file('..\\BaiduSearch_Spider\data\\baidusearch_test.csv'))
    res.headers['Content-Disposition'] = 'attachment; filename={}'.format('result.csv')
    return res

if __name__ == '__main__':
    app.run()
