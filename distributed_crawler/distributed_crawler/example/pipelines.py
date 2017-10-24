# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2016-07-20 18:59:50 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2016-07-20 18:59:50 

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import json

class ExamplePipeline(object):
    def __init__(self):
        self.file = open('items.json', 'w')
    def process_item(self, item, spider):
        #item["crawled"] = datetime.utcnow()
        #item["spider"] = spider.name
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
