# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-26 18:59:35 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-26 18:59:35 

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisCrawlSpider
from items import GeneralItem
from url_settings import NOTICE_INFO_PREFIX
from scrapy.http import Request
import re



class Notice(RedisCrawlSpider):
    name = "Notice"
    redis_key = 'noticeinfo:start_urls'


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
        code_str = response.url.split('=', 1)[1].upper()
        response = response.body.decode('gbk', 'ignore')
        html = Selector(text=response)
        res = html.xpath('//table[@class="body_table"]/tbody/tr')
        for td in res:
            item = dict()
            item['title'] = td.xpath('th/a/text()').extract_first().encode('utf8').strip()
            item['notice_type'] = td.xpath('td[1]/text()').extract_first().encode('utf8').strip()
            item['date'] = td.xpath('td[2]/text()').extract_first().encode('utf8').strip()
            item['url'] = NOTICE_INFO_PREFIX % (td.xpath('th/a/@href').extract_first()).encode('utf8').strip()
            item['code'] = code_str
            yield Request(url=item['url'], meta={'meta': item}, callback=self.secondary_parse)


    def secondary_parse(self, response):
        meta = response.meta['meta']
        response = response.body.decode('gbk', 'ignore')
        html = Selector(text=response)
        notice = html.xpath('//div[@id="content"]/pre/text()').extract_first()
        if notice:
            meta['text'] = notice.encode('utf8').strip()
            meta['source'] = '公告'
            item = GeneralItem()
            item['basic_info'] = meta
        return item

