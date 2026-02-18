-- Oracle 学习示例：用户与表空间创建（示意）
-- 实际执行需 DBA 根据环境调整路径和权限。

CREATE TABLESPACE bigdata_ts
  DATAFILE 'bigdata_ts01.dbf'
  SIZE 200M
  AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED;

CREATE USER bigdata_user
  IDENTIFIED BY bigdata_pass
  DEFAULT TABLESPACE bigdata_ts
  TEMPORARY TABLESPACE temp;

GRANT CONNECT, RESOURCE TO bigdata_user;

