# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-26 19:01:26 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-26 19:01:26 

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
info_path = '/Users/xushuang/sf/kb/distributed_crawler/example-project/items.json'


def get_industry_firms(input):
    f = open(input, 'r')
    industry_firms = set([line.strip() for line in f])
    return list(industry_firms)


def handle_firm_basic(input, output):
    industry_firms = get_industry_firms(input)
    count = 0
    fw = open(output, 'w')
    with open(info_path, 'r') as f:
        for line in f:
            js = json.loads(line.strip())
            firm = js['basic_info'][u'代码']
            for i in industry_firms:
                firm = firm.encode('utf8')
                if i[2:]==firm:
                    print i
                    js['basic_info'][u'代码'] = i
                    count += 1
                    fw.write(json.dumps(js, ensure_ascii=False))
                    fw.write('\n')
                    break           
    print count



medicine = '/Users/xushuang/sf/kb/distributed_crawler/medicine_168_basic.json'
medicine_list = '/Users/xushuang/sf/kb/distributed_crawler/medicine_company_list.txt'

handle_firm_basic(medicine_list, medicine)