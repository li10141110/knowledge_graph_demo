This is a demo for a simple knowledge graph. See blog [项目实战--知识图谱初探](http://www.shuang0420.com/2017/09/05/%E9%A1%B9%E7%9B%AE%E5%AE%9E%E6%88%98-%E7%9F%A5%E8%AF%86%E5%9B%BE%E8%B0%B1%E5%88%9D%E6%8E%A2/) for detail.

# Repository contents

- **distributed_crawler/:** 

  contain files about distributed crawler with scrapy-redis

  run from docker: run ``./build.sh`` to build image and ``./run.sh`` to run crawler; results will be stored in your localhost redis server

- **data/:**

  run ``python nodes_edges.py`` to generate node and edge file for Neo4j;

  run ``python spo.py`` to generate basic file for MySQL/Postgres;

  run ``./dump.sh`` to dump files into database

- **visualization/:**

  flask server with d3 for visualization;

  only designed for MySQL visualization 

  run ``python run_server.py`` to start server

  check results at ``http://localhost:8080/api/v1?``

  ​

# Distributed_crawler

Data is stored in local redis server. Samples are as follow.

**Company basic info**

```
{"basic_info": {"首次注册登记地点": "上海市武川路111号", "企业法人营业执照注册号": "企股沪总字第019024号", "公司注册地址邮箱": "201506", "公司名称": "上海凤凰企业(集团)股份有限公司", "法人代表": "周卫中", "证券简称": "凤凰Ｂ股", "代码": "900916", "总经理": "--", "公司注册地址": "上海市金山工业区开乐大街158号6号楼"}}
```

**Management basic info**

```
{"basic_info": {"出生年份": "1961", "性别": "男", "职务": "董事,常务副总经理", "代码": "SZ000661", "学历": " ", "姓名": "安吉祥"}}
{"basic_info": {"出生年份": "1965", "性别": "男", "职务": "董事", "代码": "SZ000661", "学历": "博士研究生", "姓名": "金磊"}}
```

**Notice info**

```
{"basic_info": {"code": "SZ000661", "title": "长春高新：董事会关于2017年半年度募集资金存放与使用情况的专项报告", "url": "http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?CompanyCode=10000983&gather=1&id=3646359", "text": "长春高新技术产业（集团）股份有限公司\r\n                                               董事会\r\n         关于 2017 年半年度募集资金存放与使用情况的专项报告\r\n               本公司及董事会全体成员保证信息披露的内容真实、准确、完整，没有虚假\r\n       记载、误导性陈述或重大遗漏。\r\n                根据中国证监会发布的《上市公司监管指引第 2 号——上市公司募集资金\r\n       管理和使用的监管要求》和深圳证券交易所颁布的《深圳证券交易所主板上市公\r\n       司规范运作指引》等有关规定，长春高新技术产业（集团）股份有限公司（以下\r\n       简称“公司”或“本公司”）董事会编制了截至 2017 年 6 月 30 日募集资金存放\r\n       与实际使用情况的专项报告。\r\n              ……………… 2017 年 8 月 18 日", "notice_type": "临时公告", "date": "2017-08-18"}}
```




# Data

Data is extracted from Redis, handled and stored in /data, finally dumped into database using ``dump.sh``

## Required file for Neo4j

**company_node.txt**

```
:ID	:LABEL	create_time	update_time	industry	first_register_addr	security_short_name	legal_entity	manager	code	company_address	register_number	zipcode	company_name
comp0	Company	2017-10-23 19:47:36	2017-10-23 19:47:36	医药	南京市工商行政管理局经济技术开发区分局	龙蟠科技	石俊峰	石俊峰	603906	江苏省南京经济技术开发区恒通大道6号320192000004815	210038	江苏龙蟠科技股份有限公司
comp1	Company	2017-10-23 19:47:36	2017-10-23 19:47:36	医药	--	中持股份	许国栋	邵凯	603903	北京市海淀区西小口路66号D区2号楼四层402室	110108012528207	100192	中持水务股份有限公司
comp2	Company	2017-10-23 19:47:36	2017-10-23 19:47:36	医药	衢州市工商行政管理局	牧 高 笛	陆暾华	陆暾华	603908	浙江省衢州市世纪大道895号1幢	3308002003757	324000	牧高笛户外用品股份有限公司
comp3	Company	2017-10-23 19:47:36	2017-10-23 19:47:36	医药	厦门市工商行政管理局	合诚股份	黄和宾	刘德全	603909	福建省厦门市湖里区枋钟路2368号1101-1104单元	350200100007638	361009	合诚工程咨询集团股份有限公司
```

**person_node.txt**

```
:ID	:LABEL	create_time	update_time	education	birth	name	sex
pers0	Person	2017-10-23 19:47:36	2017-10-23 19:47:36	 	1954	杨占民	男
pers1	Person	2017-10-23 19:47:36	2017-10-23 19:47:36	 	1961	安吉祥	男
pers2	Person	2017-10-23 19:47:36	2017-10-23 19:47:36	博士研究生	1965	金磊	男
pers3	Person	2017-10-23 19:47:36	2017-10-23 19:47:36	硕士及研究生	1965	张辉	女
```

**management_edge.txt**

```
:START_ID	:END_ID	:TYPE	create_time	update_time	title
comp2397	pers281	isManagedBy	2017-10-23 19:47:36	2017-10-23 19:47:36	董事
comp3260	pers66	isManagedBy	2017-10-23 19:47:36	2017-10-23 19:47:36	职工监事
comp3260	pers64	isManagedBy	2017-10-23 19:47:36	2017-10-23 19:47:36	独立董事
comp2879	pers206	isManagedBy	2017-10-23 19:47:36	2017-10-23 19:47:36	董事
```

## Required file for MySQL/PostgresSQL

**management.txt**

```
company_id	title	person_id	type	create_time	update_time
comp2397	董事	pers281	relation	2017-10-23 19:48:19	2017-10-23 19:48:19
comp3260	职工监事	pers66	relation	2017-10-23 19:48:19	2017-10-23 19:48:19
comp3260	独立董事	pers64	relation	2017-10-23 19:48:19	2017-10-23 19:48:19
comp2879	董事	pers206	relation	2017-10-23 19:48:19	2017-10-23 19:48:19
```

**spo.txt**

```
subj	pred	obj	type	create_time	update_time
comp0	行业	医药	property	2017-10-23 19:48:19	2017-10-23 19:48:19
comp0	首次注册登记地点	南京市工商行政管理局经济技术开发区分局	property	2017-10-23 19:48:19	2017-10-23 19:48:19
comp0	证券简称	龙蟠科技	property	2017-10-23 19:48:19	2017-10-23 19:48:19
comp0	法人代表	石俊峰	property	2017-10-23 19:48:19	2017-10-23 19:48:19
```



# Visualization

**Example:**

```
http://localhost:8080/api/v1?company=600129
```

![](http://ox5l2b8f4.bkt.clouddn.com/demo2.png)

```
http://localhost:8080/api/v1?person=周万森
```

![](http://ox5l2b8f4.bkt.clouddn.com/demo1.png)