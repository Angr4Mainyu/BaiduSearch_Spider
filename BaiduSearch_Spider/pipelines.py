# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import urllib
from BaiduSearch_Spider.items import *
import copy


class BaidusearchSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class Pipeline_ToCSV(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        self.store_file = os.path.dirname(
            __file__) + '/data/{0}data/baidu_{1}.csv'
        self.cur_keyword = ""

    def process_item(self, item, spider):
        if isinstance(item, BaidunewsSpiderItem):
            return self.process_news_item(item, spider)
        elif isinstance(item, BaidusearchSpiderItem):
            return self.process_search_item(item, spider)

    def process_news_item(self, item, spider):
        if item['keyword'] != self.cur_keyword:  # 如果更换了关键词，就要打开另外一个文件中去读写
            if not os.path.exists((self.store_file).format("news", item['keyword'])):
                # 打开(创建)文件    
                # 不带newline的话输出总会有一个空行 加入encoding='utf-8-sig'就不会乱码了
                self.file = open((self.store_file).format(
                    "news", item['keyword']), 'a', newline='', encoding='utf-8-sig')
                # csv写法
                self.writer = csv.writer(self.file)
                # 记录当前榨取的关键词
                self.cur_keyword = item['keyword']
                # 加上第一行头部索引
                head_index = (u'title', u'platform', u'date',
                              u'time', u'brief', u'body', u'link')
                self.writer.writerow(head_index)
            elif self.cur_keyword == "":
                os.remove((self.store_file).format("news", item['keyword']))
                # 打开(创建)文件
                # 不带newline的话输出总会有一个空行 加入encoding='utf-8-sig'就不会乱码了
                self.file = open((self.store_file).format(
                    "news", item['keyword']), 'a', newline='', encoding='utf-8-sig')
                # csv写法
                self.writer = csv.writer(self.file)
                # 记录当前榨取的关键词
                self.cur_keyword = item['keyword']
            else:
                # 打开(创建)文件
                # 不带newline的话输出总会有一个空行 加入encoding='utf-8-sig'就不会乱码了
                self.file = open((self.store_file).format(
                    "news", item['keyword']), 'a', newline='', encoding='utf-8-sig')
                # csv写法
                self.writer = csv.writer(self.file)
                # 记录当前榨取的关键词
                self.cur_keyword = item['keyword']

        # 判断字段值不为空再写入文件
        if item['title'] != "":
            # 组成元组：
            # 将加密的link进行解密
            try:
                reallink = urllib.request.urlopen(
                    item['link'], timeout=1).geturl()
                item['link'] = reallink
            except:
                pass
            List = (item['title'], item['platform'], item['date'],
                    item['time'], item['brief'], item['body'], item['link'])
            self.writer.writerow(List)
        return item

    def process_search_item(self, item, spider):
        if item['keyword'] != self.cur_keyword:  # 如果更换了关键词，就要打开另外一个文件中取读写
            # 判断这个文件是否存在，如果不存在要加第一行索引
            if not os.path.exists((self.store_file).format("search", item['keyword'])):
                # 打开(创建)文件
                # 不带newline的话输出总会有一个空行 加入encoding='utf-8-sig'就不会乱码了
                self.file = open((self.store_file).format(
                    "search", item['keyword']), 'a', newline='', encoding='utf-8-sig')
                # csv写法
                self.writer = csv.writer(self.file)
                # 记录当前榨取的关键词
                self.cur_keyword = item['keyword']
                # 加上第一行头部索引
                head_index = (u'title', u'time', u'brief', u'link')
                self.writer.writerow(head_index)
            elif self.cur_keyword == "":
                os.remove((self.store_file).format("search", item['keyword']))
                # 打开(创建)文件
                # 不带newline的话输出总会有一个空行 加入encoding='utf-8-sig'就不会乱码了
                self.file = open((self.store_file).format(
                    "search", item['keyword']), 'a', newline='', encoding='utf-8-sig')
                # csv写法
                self.writer = csv.writer(self.file)
                # 记录当前榨取的关键词
                self.cur_keyword = item['keyword']
            else:
                # 打开(创建)文件
                # 不带newline的话输出总会有一个空行 加入encoding='utf-8-sig'就不会乱码了
                self.file = open((self.store_file).format(
                    "search", item['keyword']), 'a', newline='', encoding='utf-8-sig')
                # csv写法
                self.writer = csv.writer(self.file)
                # 记录当前榨取的关键词
                self.cur_keyword = item['keyword']

        # 判断字段值不为空再写入文件
        if item['title'] != "":
            # 组成元组：
            # 将加密的link进行解密
            if item['link'] != "":
                try:
                    reallink = urllib.request.urlopen(
                        item['link'], timeout=1).geturl()
                    item['link'] = reallink
                except:
                    pass
            List = (item['title'], item['time'], item['brief'], item['link'])
            self.writer.writerow(List)
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
