
# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-29 17:08:03 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-29 18:58:13 


from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

company_attr = {u"法人代表": "legal_entity", u"公司名称": "company_name", u"证券简称": "security_short_name", u"公司注册地址邮箱": "zipcode", u"首次注册登记地点": "first_register_addr", u"代码": "code", u"公司注册地址": "company_address", u"企业法人营业执照注册号": "register_number", u"行业": "industry", u"总经理": "manager"}
person_attr = {u"出生年份": "birth", u"性别": "sex", u"姓名": "name", u"学历":"education"}
edge_attr = {u"职务": "position"}

company_attr = dict(zip(company_attr.values(), company_attr.keys()))
person_attr = dict(zip(person_attr.values(), person_attr.keys()))
edge_attr = dict(zip(edge_attr.values(), edge_attr.keys()))


dt = str(datetime.now())[:19]

def read_nodes(frname, fwname, refer, write_mode='w'):
    with open(frname, 'r') as fr, open(fwname, write_mode) as fw:
        header = fr.readline().strip()
        header = header.split('\t')[4:]
        for i,h in enumerate(header):
            header[i] = refer.get(h,h)
        if write_mode=='w':
            fw.write("subj\tpred\tobj\ttype\tcreate_time\tupdate_time\n")
        for line in fr:
            parts = line.strip().split('\t')
            subj = parts[0]
            for i,p in enumerate(parts[4:]):
                fw.write("%s\t%s\t%s\tproperty\t%s\t%s\n"%(subj, header[i], p, dt, dt))


def read_edges(frname, fwmang, fwspo, refer, write_mode='a'):
    with open(frname, 'r') as fr, open(fwmang, 'w') as fw, open(fwspo, write_mode) as spo:
        header = fr.readline().strip()
        header = header.split('\t')[5:]
        for i,h in enumerate(header):
            header[i] = refer.get(h,h)
        if write_mode=='w':
            fw.write("subj\tpred\tobj\ttype\tcreate_time\tupdate_time\n")
        fw.write("company_id\ttitle\tperson_id\ttype\tcreate_time\tupdate_time\t\n")
        for line in fr:
            parts = line.strip().split('\t')
            subj = parts[0]
            obj = parts[1]
            for i,p in enumerate(parts[5:]):
                fw.write("%s\t%s\t%s\trelation\t%s\t%s\n"%(subj, p, obj, dt, dt))
            # treate all management relation as "高管"
            spo.write("%s\t高管\t%s\trelation\t%s\t%s\n"%(subj, obj, dt, dt))


read_nodes('data/company_node.txt', 'data/spo.txt', company_attr)
read_nodes('data/person_node.txt', 'data/spo.txt', person_attr, 'a')
read_edges('data/management_edge.txt', 'data/management.txt', 'data/spo.txt', edge_attr)
