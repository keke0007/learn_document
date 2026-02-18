-- PostgreSQL 学习示例：创建数据库与 Schema（示意）

-- 在 postgres 或有权限的用户下：
-- CREATE DATABASE bigdata_learn;

-- 使用 psql 连接到 bigdata_learn 后：
CREATE SCHEMA IF NOT EXISTS bigdata_demo;
SET search_path TO bigdata_demo;

