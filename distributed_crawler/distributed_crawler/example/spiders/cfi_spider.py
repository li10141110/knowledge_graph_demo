# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-26 18:58:50 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-26 18:58:50 

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisCrawlSpider
from items import GeneralItem

class Cfi(RedisCrawlSpider):
    name = "Cfi"
    redis_key = 'Cfi:start_urls'

    def parse(self, response):
        html = Selector(response)
        content = html.xpath('//td//text()').extract()
        if len(content) < 16:
            return 
        header = [i.encode('utf8').strip() for i in content[7:16]]
        content = [i.encode('utf8').strip() for i in content[16:]]
        if len(header) % 9!=0:
            return
        items = []
        for i in xrange(0, len(content), 9):
            item = GeneralItem()
            item['basic_info'] = dict(zip(header, content[i:i+10]))
            items.append(item)
        return items

