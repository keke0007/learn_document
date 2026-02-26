
  
-- 创建数据库
CREATE DATABASE IF NOT EXISTS db_hive ;
USE db_hive;


-- 创建表：emp
CREATE TABLE `emp`(
  `empno` int, 
  `ename` string, 
  `job` string, 
  `mgr` int, 
  `hiredate` string, 
  `sal` double, 
  `comm` double, 
  `deptno` int)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'field.delim'='\t', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  'hdfs://node1.itcast.cn:8020/user/hive/warehouse/db_hive.db/emp'
TBLPROPERTIES (
  'bucketing_version'='2', 
  'transient_lastDdlTime'='1631525001') ;
  
  
-- 创建表：dept
CREATE TABLE `dept`(
  `deptno` int, 
  `dname` string, 
  `loc` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'field.delim'='\t', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  'hdfs://node1.itcast.cn:8020/user/hive/warehouse/db_hive.db/dept'
TBLPROPERTIES (
  'bucketing_version'='2', 
  'transient_lastDdlTime'='1631525006') ;