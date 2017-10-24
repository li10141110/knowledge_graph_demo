# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-29 17:08:03 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-29 18:58:13 


import json
from pymongo import *
import json
import pymysql
import sys
from server.logger import *
from server.config import *
import os
from config import MYSQL_USER, MYSQL_PWD



logger = config_logger("SERVER.MODELS", "INFO")


def init():
	conn = pymysql.connect(
			host = 'localhost',
			port = 3306,
			user = MYSQL_USER,
			password = MYSQL_PWD,
			charset ='utf8',
			db = 'knowledge_graph')
	cursor = conn.cursor()
	return conn, cursor


fname = os.getcwd() + "/templates/data.json"


edge_sql_comp = """SELECT subj, obj, pred, company.company_name, company.code, person.name, type FROM spo JOIN company JOIN person WHERE spo.subj=company.id AND spo.obj=person.id AND company.code=%s;""" 
edge_sql_pers = """SELECT subj, obj, pred, company.company_name, company.code, person.name, type FROM spo JOIN company JOIN person WHERE spo.subj=company.id AND spo.obj=person.id AND person.name="%s";"""
secondary_edge_sql = 'SELECT * FROM spo WHERE subj="%s"'

def execute(conn, cursor, attr):
    js = {}
    edges, secondary_nodes, secondary_edges = [], [], []
    try:
        sql = edge_sql_comp%(attr[1]) if attr[0]=='company' else edge_sql_pers%(attr[1])
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[-1]=="relation":
                secondary_nodes.append((row[1],row[5]))
                edges.append({"source": row[3], "target": row[5], "relation": u"高管", "label": row[-1]})
            # else: 
                # secondary_edges.append({"source": row[3], "target": row[1], "relation": row[2], "label": row[-1]})
        for node in secondary_nodes:
            sql = secondary_edge_sql % node[0]
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                if row[1]==u'姓名': continue
                secondary_edges.append({"source": node[1], "target": row[2], "relation": row[1], "label": row[3]})
    except:
        logger.error("ERROR: " + sql)
        conn.rollback()
    # js["nodes"] = nodes
    js["edges"] = edges
    js["secondary_edges"] = secondary_edges
    mydata = json.dumps(js, ensure_ascii=False).encode("utf8")
    with open(fname, 'w') as f:
        f.write(mydata)
        f.close()
	return mydata
