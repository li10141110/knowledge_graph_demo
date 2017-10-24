# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-26 18:59:10 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-26 18:59:10 

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisCrawlSpider
from items import GeneralItem
import re


CODE_MATCHER = {"shmb": "SH", "szcn": "SZ", "szmb": "SZ", "szsme": "SZ"}

class Cninfo(RedisCrawlSpider):
    name = "Cninfo"
    redis_key = 'cninfo:start_urls'


    @staticmethod
    def clean_data(page):
        removeImg = re.compile('<img.*?>')
        replaceLine = re.compile('<tr>|<div>|</div>|<p>|</p>|\r|\n')
        replaceBR = re.compile('<br>|<br >|<br />')
        removeExtraTag = re.compile('<em>|</em>|<strong>|</strong>')
        page = re.sub(removeImg, "", page)
        page = re.sub(replaceLine, "", page)
        page = re.sub(replaceBR, "", page)
        page = re.sub(removeExtraTag, "", page)
        return page


    def parse(self, response):
        code = ''
        code_str = response.url.split('/')[-1][:-5]
        code_char = code_str[:-6]
        if code_char in CODE_MATCHER:
            code = CODE_MATCHER[code_char] + code_str[-6:]
        if not code: return 
        response = response.body.decode('gbk', 'ignore')
        response = self.clean_data(response)
        html = Selector(text=response)
        content = html.xpath('//td//text()').extract()
        if len(content) < 14:
            return 
        header = [i.encode('utf8').strip() for i in content[9:14]]
        content = [i.encode('utf8').strip() for i in content[14:]]
        if len(header) % 5!=0:
            return
        items = []
        for i in xrange(0, len(content), 10):
            item = GeneralItem()
            item['basic_info'] = dict(zip(header, content[i:i+5]))
            item['basic_info'].update({"代码": code})
            items.append(item)
        return items

