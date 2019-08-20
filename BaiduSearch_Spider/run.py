import os
if __name__=="__main__":
    keyword = "北京大学 学生死亡"
    #keyword = ""
    #os.system(
    #    "scrapy crawl searchspider")

    os.system(
        "scrapy crawl newsspider".format(keyword, keyword))
