# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2016-07-20 18:59:50 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2016-07-20 18:59:50 

import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/distributed_crawler/example')

import redis
import os
import argparse
import json
from distributed_crawler.example import url_settings
from spiders.cfi_spider import Cfi
from spiders.cninfo_spider import Cninfo
from spiders.notice_spider import Notice
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings


CODE_MATCHER = {"SH": "shmb", "SZ300": "szcn", "SZ000": "szmb", "SZ002": "szsme"}
SPIDER_MATCHER = {"cfi": Cfi, "cninfo": Cninfo, "notice": Notice}

def generateStartUrls(host, input):
    # f = open(input, 'r')
    # category = f.readlines()
    # category = [c.strip() for c in category]
    # self.start_urls = ['http://verify.baidu.com/']
    # start_urls = ['http://www.baidu.com/s?wd=' +
    #               item for item in category]

    # basic informaiton: 70 pages in total, by 23 August, 2017
    start_urls = [url_settings.CFI_COMPANY%(str(i)) for i in xrange(1,70)]
    r = redis.Redis(host=host, port=6379)
    for i in start_urls:
        r.lpush('Cfi:start_urls', i)
    with open(input, 'r') as f:
        for line in f:
            js = json.loads(line.strip())
            code = js['basic_info'][u'代码']
            if code: 
                # notice information
                notice_url = url_settings.NOTICE_INFO_URL%(code.lower())
                # management information
                code = _match_code(code)
                management_url = url_settings.CNINFO_MANAGEMENT%(code)
            r.lpush('cninfo:start_urls', management_url)  
            r.lpush('noticeinfo:start_urls', notice_url)            


def _match_code(code):
    slice1 = code[:2]
    if slice1 in CODE_MATCHER:
        return CODE_MATCHER[slice1] + code[2:]
    slice2 = code[:5]
    if slice2 in CODE_MATCHER:
        return CODE_MATCHER[slice2] + code[2:]


def changeSettings(host):
    path = os.getcwd()
    os.chdir(path + '/distributed_crawler/example/')
    f = open('settings.py', 'r')
    lines = f.readlines()
    if not lines[-1].startswith("REDIS_URL = "):
        f = open('settings.py', 'a')
        f.write("REDIS_URL = 'redis://" + host + ":6379'")


def runSpider(host, spider):
    spiders = spider.split(',')
    changeSettings(host)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    for i in spiders:
        runner.crawl(SPIDER_MATCHER[i.lower()])

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    # os.chdir(os.path.dirname(os.getcwd()))
    # os.system('scrapy crawl ' + spider)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', action='store', dest='host', default='localhost',
                        help='The host address for Redis, default is localhost')
    parser.add_argument('-input', action='store', dest='input', default='medicine_114_basic.json',
                        help='The file listing items you want to crawl')
    parser.add_argument('-spider', action='store', dest='spider', default='cfi,cninfo,notice',
                        help='The spider to run. You can run multiple spiders together, just use "," to concat. Default is cfi,cninfo,notice')
    parser.add_argument('-master', action='store', dest='master', default='0',
                        help='This defines master machine. By defalut(master=0),it is slave. Otherwise(master=1), it is the master where Redis is configured')
    args = parser.parse_args()
    if args.master == '1':
        generateStartUrls(args.host, args.input)
    if (args.master and not args.host) or (args.host and not args.master):
        print 'If master, identify the host address and input file. See python runSpider.py -h'
    runSpider(args.host, args.spider)
