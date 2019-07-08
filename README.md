# 使用Scrapy爬虫框架
对百度搜索和百度旗下相关搜索进行关键词爬取

爬取的主要内容包括：标题 时间 平台 作者 时间 简介 正文 链接

使用的时候注意要修改关键词和起始爬虫的URL

## 使用方式

```shell
scrapy crawl searchspider -a search=xxxx -a keyword=xxxx
```

或者

```shell
scrapy crawl baiduspider -a search=xxxx -a keyword=xxxx
```