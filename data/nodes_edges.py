# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-29 17:08:03 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-29 18:58:13 

import redis
import json
from collections import defaultdict
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')


r = redis.Redis(
    host='localhost',
    port=6379, 
    password='')

# comp_id : code
comp_dict = defaultdict(str)
pers_dict = defaultdict(str) # use this dict to avoid duplicate person records

edges = set()
edge_str = "%s\t%s\tisManagedBy\t%s\t%s\t%s\n"
edge_header = ":START_ID\t:END_ID\t:TYPE\tcreate_time\tupdate_time\ttitle\t\n"
comp_header = ":ID\t:LABEL\tcreate_time\tupdate_time\tindustry\t"
pers_header = ":ID\t:LABEL\tcreate_time\tupdate_time\t"

company_attr = {u"法人代表": "legal_entity", u"公司名称": "company_name", u"证券简称": "security_short_name", u"公司注册地址邮箱": "zipcode", u"首次注册登记地点": "first_register_addr", u"代码": "code", u"公司注册地址": "company_address", u"企业法人营业执照注册号": "register_number", u"行业": "industry", u"总经理": "manager"}
person_attr = {u"出生年份": "birth", u"性别": "sex", u"姓名": "name", u"学历":"education"}
edge_attr = {u"职务": "title"}


dt = str(datetime.now())[:19]

def _transform_header(header, refer):
    for i,v in enumerate(header):
        header[i] = refer.get(v, v)
    return "\t".join(header) + "\n"


def write_company_nodes(key, fname):
    if not r.exists(key):
        print("%s"%("not exists!"))
        return 
    litems = r.llen(key)
    items = r.lrange(key, 0, litems)
    with open(fname, 'w') as fw:
        for index,item in enumerate(items):
            js = json.loads(item)
            js = js['basic_info']
            # write header
            if index==0: 
                fw.write("%s%s"%(comp_header, _transform_header(js.keys(), company_attr)))
            # write content
            fw.write("comp%s\tCompany\t%s\t%s\t医药\t%s\n"%(index, dt, dt, '\t'.join(js.values())))
            # update comp_dict
            comp_dict[js[u'代码']] = "comp%s"%index
            index += 1
               
        
def write_person_nodes(key, fname):
    if not r.exists(key):
        print("%s"%("not exists!"))
        return 
    litems = r.llen(key)
    items = r.lrange(key, 0, litems)
    with open(fname, 'w') as fw:
        for index,item in enumerate(items):
            js = json.loads(item)
            js = js['basic_info']
            # write header
            if index==0: 
                keys = js.keys()
                keys.remove(u'代码')
                keys.remove(u'职务')
                fw.write("%s%s"%(pers_header, _transform_header(keys, person_attr)))
            # write content
            code = js[u'代码'][2:]
            pos = js[(u'职务')]
            js.pop(u'代码')
            js.pop(u'职务')
            # identify person by birth, name, and sex
            unique_key = "%s%s%s"%(js[u'出生年份'], js[u'姓名'], js[u'性别'])
            if unique_key in pers_dict:
                edges.add(edge_str%(comp_dict[code], dt, dt, pers_dict[unique_key], pos))
            else:
                pers_dict[unique_key] = "pers%s"%index
                fw.write("pers%s\tPerson\t%s\t%s\t%s\n"%(index, dt, dt, '\t'.join(js.values())))
                # update edges
                edges.add(edge_str%(comp_dict[code], "pers%s"%(index), dt, dt, pos))
                index += 1
    
    
def write_edges(data, header, fname):    
    with open(fname, 'w') as fw:
        fw.write(header)
        fw.writelines(data)
        

write_company_nodes('Cfi:items', 'company_node.txt')
write_person_nodes('Cninfo:items', 'person_node.txt')
write_edges(edges, edge_header, 'management_edge.txt')