CREATE DATABASE IF NOT EXISTS `knowledge_graph` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE knowledge_graph;
CREATE TABLE IF NOT EXISTS company (
                      id varchar(20) PRIMARY KEY,
                      label varchar(20),
                      create_time datetime,
                      update_time datetime,
                      industry varchar(20),
                      first_register_addr varchar(100),
                      security_short_name varchar(20),
                      legal_entity varchar(20),
                      manager varchar(20),
                      code int NOT NULL UNIQUE KEY,
                      company_address varchar(100),
                      register_number varchar(50),
                      zipcode varchar(20),
                      company_name varchar(100))
                      DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS management (
                      company_id varchar(20) NOT NULL,
                      title varchar(50), 
                      person_id varchar(20) NOT NULL,
                      type varchar(20) NOT NULL,
                      create_time datetime,
                      update_time datetime,
                      UNIQUE KEY (person_id, company_id))
                      DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS spo (
                      subj varchar(100),
                      pred varchar(100),
                      obj varchar(500),
                      type varchar(20),
                      create_time datetime,
		              update_time datetime,
                      UNIQUE KEY (subj, pred, obj))
                      DEFAULT CHARSET=utf8;
 CREATE TABLE IF NOT EXISTS person (
                      id varchar(20) PRIMARY KEY,
                      label varchar(20),
                      create_time datetime,
                      update_time datetime,
                      education varchar(50),
                      birth varchar(20),
                      name varchar(20),
                      sex varchar(20),
                      UNIQUE KEY (birth, sex, name))
                      DEFAULT CHARSET=utf8;


LOAD DATA LOCAL INFILE 'company_node.txt' INTO TABLE company CHARACTER SET utf8 FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'person_node.txt' INTO TABLE person CHARACTER SET utf8 FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'management_edge.txt' INTO TABLE management CHARACTER SET utf8 FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'spo.txt' INTO TABLE spo CHARACTER SET utf8 FIELDS TERMINATED BY '\t' IGNORE 1 LINES;