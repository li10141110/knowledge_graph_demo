# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2016-07-20 18:59:50 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2016-07-20 18:59:50 

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from example.items import SearchItem
from example.spiders import sendmail
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
import time
import socket
import fcntl
import struct
import urllib
import re
import itertools


class Search(RedisCrawlSpider):
    name = "Search"
    redis_key = 'Search:start_urls'
    start_time = time.time()

    @staticmethod
    def get_local_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        inet = fcntl.ioctl(s.fileno(), 0x8915,
                           struct.pack('256s', ifname[:15]))
        ret = socket.inet_ntoa(inet[20:24])
        return ret

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
        global start_time
        html = Selector(response)
        # base_url = 'http://www.qichacha.com'
        # page = html.xpath('//table[@class="m_srchList"]//td/a/@href').extract()
        page = html.xpath('//div[@class="col-xs-10 search_repadding2 f18"]/a/@href').extract()
        if len(page) > 0:
            secondary_url = page[0]
            item = dict()
            item['secondary_url'] = secondary_url
            yield Request(url=item['secondary_url'], meta={'item_1': item}, callback=self.tianyancha_parse)


    def tianyancha_parse(self, response):
        html = Selector(response)
        item = SearchItem()
        keys = html.xpath('//div[@class="c8"]/text()').extract()
        values = html.xpath('//div[@class="c8"]/span//text()').extract()
        if values:
            values = values[1:]
        for i in range(0,len(keys)):
            print keys[i],values[i]
        # if len(keys) != len(values):
        #     return
        basic_info = dict(zip(keys, values))
        # item['basic_info'] = basic_info
        more_info = html.xpath('//tr//td/text()').extract()
        print 'more_info'
        print more_info
        print '='*50, len(more_info)
        if len(more_info) % 2 == 0:
            item['more_info'] = dict(itertools.izip_longest(*[iter(more_info)] * 2, fillvalue=""))
        print item.keys()
        return item
    # def parse(self, response):
    #     global start_time
    #     html = Selector(response)
    #     base_url = 'http://www.baidu.com'
    #     # print self.get_local_ip('eth0')
    #     current_time = time.time()
    #     if response.url.startswith('http://verify.baidu.com/') and (current_time - start_time) > 600:
    #         sendmail.sendmail('Crawler: slave vm failure!', self.get_local_ip(
    #             'eth0'), 'brucewen@wezhuiyi.com', time.time())
    #     page = html.xpath('//div[@class="result c-container "]').extract()
    #     test = html.xpath(
    #         '//div[@class="result c-container "]/h3/a/text()').extract()
    #     relatedPage = html.xpath(
    #         '//div[@id="rs"]/table/tr/th/a/text()').extract()
    #     relatedQuery = '\t'.join(relatedPage)
    #     nextPageUrl = html.xpath(
    #         '//div[@id="page"]/a[@class="n"]/@href').extract()
    #     nextPageText = html.xpath(
    #         '//div[@id="page"]/a[@class="n"]/text()').extract()
    #     query = response.url.split('&')[0]
    #     query = query.split('wd=')[-1]
    #     query = urllib.unquote(query).encode('utf8')
    #     items = []
    #     for i in range(0, len(page)):
    #         if '贴吧' in test[i].encode('utf8'):
    #             item = dict()
    #             secondUrl = html.xpath(
    #                 '//div[@class="result c-container "]/h3/a/@href').extract_first()
    #             item['url'] = secondUrl
    #             item['query'] = query
    #             yield Request(url=item['url'], meta={'item_1': item}, callback=self.tieba_parse)
    #         elif '知道' in test[i].encode('utf8'):
    #             item = dict()
    #             secondUrl = html.xpath(
    #                 '//div[@class="result c-container "]/h3/a/@href').extract_first()
    #             item['url'] = secondUrl.encode('utf8')
    #             item['query'] = query
    #             yield Request(url=secondUrl, meta={'item_1': item}, callback=self.zhidao_parse)
    #         else:
    #             replaceTags = re.compile("<.*?>", re.S)
    #             replaceLine = re.compile('\r|\n|\t')
    #             page[i] = replaceTags.sub("", page[i])
    #             page[i] = replaceLine.sub("", page[i])
    #             item = SearchItem()
    #             item['abstract'] = page[i].encode('utf8')
    #             item['url'] = response.url.encode('utf8')
    #             item['query'] = query
    #             item['relatedQuery'] = relatedQuery.encode('utf8')
    #             yield item
    #         # items.append(item)
    #     # yield items
    #     if nextPageText and '下一页' in nextPageText[-1].encode('utf8'):
    #         nextPage = base_url + nextPageUrl[-1].encode('utf8')
    #         yield Request(url=nextPage, callback=self.parse)

    def tieba_parse(self, response):
        '''
        Get every post content
        '''
        item_1 = response.meta['item_1']
        response = response  # .body
        # response = self.clean_data(response)
        html = Selector(response)
        page = html.xpath(
            '//div[starts-with(@id,"post_content_")]/text()').extract()  # .encode('utf8')
        page = [p.strip() for p in page]
        item = SearchItem()
        item['query'] = item_1['query'].encode('utf8')
        item['url'] = item_1['url'].encode('utf8')
        item['abstract'] = "##".join(page).encode('utf8')
        return item

    def zhidao_parse(self, response):
        item_1 = response.meta['item_1']
        response = response.body.decode('gbk', 'ignore')
        response = self.clean_data(response)
        html = Selector(text=response)
        ques = html.xpath('//pre[@accuse="qContent"]/span').extract_first()
        # 普通回答
        ans = html.xpath('//div[@accuse="aContent"]/span/text()').extract()
        # 专业回答
        ans_quality = html.xpath(
            '//div[@class="quality-content-detail content"]/text()').extract()
        # 提问者采纳
        ans_best = html.xpath('//pre[@accuse="aContent"]/text()').extract()
        # print "Q", ques
        # print ans
        items = []
        item = SearchItem()
        item['query'] = item_1['query'].encode('utf8')
        item['url'] = item_1['url'].encode('utf8')
        ans.extend(ans_quality)
        ans.extend(ans_best)
        item['abstract'] = "##".join(ans)
        items.append(item)
        return items
