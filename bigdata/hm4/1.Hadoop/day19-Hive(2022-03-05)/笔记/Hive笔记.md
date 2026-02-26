## Hive框架

### 数据仓库

+ 数据仓库的数据是由各种各样的数据集合而成

+ 数据仓库的数据存在HDFS上

+ 数据仓库中的数据就是用于分析，通过分析得出有价值个东西，给领导层或者组织机构提供决策支持

  ![image-20220224193821843](image\image-20220224193821843.png)

### 数据仓库的主要特点

+ 主题性：数仓中的数据不是泛泛而存，而是面向某一个方向，某一个主题

+ 集成性：数据仓库中存储的数据是来源于多个数据源的集成，集成之后可能由于这种格式问题不统一，需要ETL处理

+ 稳定性：在下一个数据采集周期未到来时，数仓中的数据一般很少发生变化，没有增删改，只有查询操作

+ 时变性：在下一个采集周期到来时，数据中的数据会发生变化

  

### 数据仓库和数据库的区别

+ 数据库中的数据为为了业务的正常开展而存在的（生存问题）
+ 数据仓库中的数据是为了进一步分析而存在        （优化问题）
+ 数据仓库的数据可以来自数据库

### 数据仓库的分层

  数仓的分层其实就是将不同阶段的数据存放在不同的数据库中

+ 数据应用层(app层)---》数据库(didi_app)   ---》表
+ 数据仓库层(dw层) ---》数据库 (didi_dw)     ---》表
+ 源数据层(odfs层)  ---》数据库（didi_ods） ---》表



### ETL

ETL，是英文Extract-Transform-Load的缩写，用来描述将数据从来源端经过抽取（extract）、转换（transform）、加载（load）至目的端的过程。

![image-20220224200123840](image\image-20220224200123840.png)

### Hive的概述

+ Hive是一个数仓管理工具，Hive是管理数仓，Hive可以将数仓中的文件活起来
+ Hive可以将数仓HDFS上的格式化文件映射成一张张的表（数据库table）
+ Hive还可以提供类SQL语言（Hsql）来操作映射的表,Hsql的语法和标准SQL类似
+ Hive提供的SQL在底层会自动转成MapReduce任务去读取数仓中的数据进行处理
+ Hive的底层封装了很多MapRedue的模板，当你写了Hive之后，Hive的执行器会自动拆解你的SQL，根据你写SQL来匹配这些模板。
+ Hive存在的意义就是避免我们去写MapReduce来实现数据分析
+ Hive底层默认是MapReduce计算引擎，我们可以换成其他计算引擎：Spark，Tez
+ 如果Hive的引擎是MapRedue，则Hive只能用于离线分析（分析历史数据）
+ Hive本身不存任何数据，因为真实的数据存在HDFS上，表的元数据存在第三方的数据库（MySQL）

![image-20220224201410020](image\image-20220224201410020.png)



### Hive的架构

![image-20220224203348652](image\image-20220224203348652.png)



设置本地模式

```shell
set hive.exec.mode.local.auto=true; #
```



### Hive的操作

```sql
-- 一、##################数据库操作##################
-- 1、创建数据库
/*
   1)在hive中每创建一个数据库，则会自动在HDFS的/user/hive/warehouse/下创建对应的文件夹
     但是这个目录存放位置可以在core-site.xml中通过以下标签设置,设置完之后需要重写hive的所有服务
    <property>
        <name>hive.metastore.warehouse.dir</name>
        <value>/user/hive/warehouse</value>
    </property>
   2)在hive中每创建一个数据库, 则会在MySQL中的hive数据库更新元数据
 */
create database myhive;
create database if not exists myhive; //如果不存在，则创建,如果存在，则不报错，什么都不做
-- 2、选择数据库
use  myhive;

-- 3、创建数据库时，手动指定你数据库存储目录的位置
create database myhive2 location '/myhive2';

-- 4、 查看数据库详细信息
  -- 查看数据库的元数据目录和用户信息-简单信息
  desc database myhive;
-- 5、删除数据库
 /*
    1）会将HDFS上对应的数据库文件夹删除
    2）会将MySQL上的所有数据库和表的元数据删除
  */
 -- 操作1：数据库中如果没有表，则删除
  drop database myhive;

 -- 操作2：数据库中如果有表，则删除
  drop database mytest3 cascade;



-- 二、##################数据库表操作##################

-- 1、MySQL的数据类型
/*
   int      整形
   double   浮点型
   decimal	任意精度的带符号小数
   string   字符串 (MySQL是varchar)
   date     年月日（2022-01-26）
   time     时分秒 (12:34:56)
   datetime 年月日  时分秒  2022-01-26 12:34:56）

   复杂类型：
     Array   数组
     Map     集合
     Struct  对象
 */

-- 2、创建表
 /*
     1:在hive中创建表，会在使用的数据库hdfs目录下创建表目录
     2:在Hive中，表可以分为两大类
       内部表(管理表):
         1)创建表时不添加 external关键字
         2)是私有表，删除表时，HDFS上的表数据和MySQL元数据全部删除

       外部表：
         1)创建表时添加 external关键字
         2)是公有表，删除表时，只会删除MySQL元数据，而HDFS上的表数据不会删除

  */

----------------------------内部表操作----------------------------
-- 2.1 创建内部表
    set hive.stats.column.autogather=false;
    set hive.exec.mode.local.auto=true; -- 开启本地模式

    create database if not exists myhive;
    use myhive;

    create table stu(id int,name string);
    insert into stu values (1,"zhangsan");  //实际开发中不存在，只是用于测试，每执行一次就会调用MR，并在HDFS上生成小文件
    insert into stu values (2,"lisi");  //实际开发中不存在，只是用于测试，每执行一次就会调用MR，并在HDFS上生成小文件
    select * from stu;

-- 2.2 验证内部表的特性
   drop table stu;  -- 删除内部表，其实本质是是将HDFS上的文件和元数据删除，HDFS上的文件暂时被存放到垃圾桶中

-- 2.3 创建表并指定分隔符
/*
   1:Hive默认识别的分隔符是 '\001' ,这个分隔符是不可显示的，但是Hive可以识别
 */
use myhive;
create table stu2(id int,name string) row format delimited fields terminated by ',';
insert into stu2 values (1,"zhangsan");

select * from stu2;

-- 2.4  根据另外一张表来创建新表
create  table  stu3 as select * from stu2; //1：stu3复制了stu2的表结构 2：将stu2的数据插入到stu3

select * from stu3;

-- 2.5 复制另外一张表的表结构
create  table  stu4 like stu2;


-- 2.6 查看一张表结构
  -- 操作1：查看基本字段
desc stu2;
  -- 操作2：查看详细信息
    /*
       Table Type:   MANAGED_TABLE   表示该表是管理表，也就是内部表
     */
desc formatted stu2;

-- 2.7 给内部表添加数据
 -- 方式1：使用hadoop fs -put 将数据文件上传到表目录文件夹
create table stu5(id int,name string) row format delimited fields terminated by ',';
select * from stu5;

 -- 方式2：Load命令来加载
/*
   load data [local] inpath '/export/data/datas/student.txt'
   [overwrite] | into table student [partition (partcol1=val1,…)];
 */

-- 操作1-本地加载
 -- 本地加载本质上是将本地的文件上传到hdfs对应的表目录，做的是复制
create table stu6(id int,name string) row format delimited fields terminated by ',';
load data local inpath '/export/data/a.txt' into table stu6;
select * from stu6;

-- 操作2-hdfs加载
 -- hdfs加载本质是将hdfs的文件从源目录剪切到表目录
load data  inpath '/hive/data/b.txt' into table stu6;
select * from stu6;



----------------------------外部表操作----------------------------
-- 2.1 创建外部表
-- 1）创建教师表
create external table teacher (tid string,tname string) row format delimited fields terminated by '\t';

-- 2)创建学生表
create external table student (sid string,sname string,sbirth string , ssex string ) row format delimited fields terminated by '\t';

-- 2.2 给student表添加数据-本地加载

load data  local inpath '/export/data/student.txt' into table  student;         -- 追加添加
select * from student;


load data  local inpath '/export/data/student.txt' overwrite into table  student; -- 覆盖添加
select * from student;

-- 2.3 给teacher表添加数据-hdfs加载
/*
    准备工作:
     hadoop fs -put teacher.txt /hive/data/
        将teacher.txt 上传到 /hive/data/目录
*/
load data   inpath '/hive/data/teacher.txt'  into table  teacher;
select * from teacher;

load data   inpath '/hive/data/teacher.txt' overwrite into table  teacher;
select * from teacher;

-- 2.4 删除外部表
drop  table teacher;  //只删除元数据，不会删除表数据
select *from teacher; //表已经不存在了

//重新创建表（修改映射关系）
create external table teacher (tid string,tname string) row format delimited fields terminated by '\t';
//重新查询到数据
select *from teacher;


-- 2.5 多张外部表共享一份表数据
/*
   1:现有一份数据已经存储在hdfs上，而且不想移动位置
   2:创建表和hdfs上的数据之间产生映射关系
 */
//创建covid1表
create external table covid1
(
    date_value date,
    county     string,
    state      string,
    fips       string,
    cases      int,
    deaths     int
)
    row format delimited fields terminated by ','
    location '/hive/data/covid';

select  * from covid1 limit 10;

select count(*) from covid1;


//创建covid2表 和covid共享同一份文件
create external table covid2
(
    date_value date,
    county     string,
    state      string,
    fips       string,
    cases      int,
    deaths     int
)
    row format delimited fields terminated by ','
    location '/hive/data/covid';
select  * from covid2 limit 20;

-- 删除表

drop table covid1;
select * from covid2; //不会影响covid2的查询




----------------------------复杂数据类型----------------------------
-- 1、Array类型
/*
 zhangsan	beijing,shanghai,tianjin,hangzhou
wangwu	changchun,chengdu,wuhan,beijing
 */
//创建表
create external table hive_array
(
    name           string,
    work_locations array<string>
)
row format delimited fields terminated by '\t'
collection items terminated by ',';

//给表加载数据
load data local inpath '/export/data/array.txt' into table hive_array;

-- 查询数据
select * from hive_array;

-- 查询work_locations数组中第一个元素
select name, work_locations[0] location from hive_array;

-- 查询location数组中元素的个数
select name, size(work_locations) location_size from hive_array;

-- 查询location数组中包含tianjin的信息
select * from hive_array where array_contains(work_locations,'tianjin');

-- 2、Map类型
/*
    1,zhangsan,father:xiaoming#mother:xiaohuang#brother:xiaoxu,28
    2,lisi,father:mayun#mother:huangyi#brother:guanyu,22
    3,wangwu,father:wangjianlin#mother:ruhua#sister:jingtian,29
    4,mayun,father:mayongzhen#mother:angelababy,26
 */
create table hive_map
(
    id      int,
    name    string,
    members map<string,string>,
    age     int
)
row format delimited fields terminated by ','
collection items terminated by '#'
map keys terminated by ':';

load data  local inpath '/export/data/map.txt' into table  hive_map;

select * from hive_map;

-- 根据键找对应的值
select id, name, members['father'] father, members['mother'] mother, age from hive_map;

-- 获取所有的键
select id, name, map_keys(members) as relation from hive_map;

-- 获取所有的值
select id, name, map_values(members) as relation from hive_map;
-- 获取键值对个数
select id,name,size(members) num from hive_map;

-- 获取有指定key的数据
select * from hive_map where array_contains(map_keys(members), 'brother');

-- 查找包含brother这个键的数据，并获取brother键对应的值
select id,name, members['brother'] brother from hive_map where array_contains(map_keys(members), 'brother');


-- struct架构
/*
192.168.1.1#zhangsan:40:male
192.168.1.2#lisi:50:female
192.168.1.3#wangwu:60:male
192.168.1.4#zhaoliu:70:female
 */
create table hive_struct
(
    ip   string,
    person struct<name:string, age:int,gender:string>
)
row format delimited fields terminated by '#'
collection items terminated by ':';

load data  local inpath '/export/data/struct.txt' into table  hive_struct;

select * from hive_struct;

select * from hive_struct;
--根据struct来获取指定的成员的值
select ip, person.name from hive_struct;
select ip, person.age from hive_struct;
select ip, person.gender from hive_struct;
select ip,person.name,person.age,person.gender from hive_struct;
select ip,person.name,person.age,person.gender from hive_struct where person.name = 'wangwu' ;


----------------------分区表操作----------------------------
/*
    采集数据:
      采集周期: 1天
      存放目录: /logs
           2022_01_01.dat
           2022_01_02.dat
           2022_01_03.dat
           ...
           2022_02_01.dat
           2022_02_02.dat
           2022_02_03.dat
           ...

           2023_01_01.dat
           2023_01_02.dat
           2023_01_03.dat
           ...
           2023_02_01.dat
           2023_02_02.dat
           2023_02_03.dat
           ...

     存放目录:/logs
      year=2022
         month=01
           2022_01_01.dat
           2022_01_02.dat
           2022_01_03.dat
         month=02
           2022_02_01.dat
           2022_02_02.dat
           2022_02_03.dat
           ...
      year=2023
         month=01
           2023_01_01.dat
           2023_01_02.dat
           2023_01_03.dat
         month=02
           2023_02_01.dat
           2023_02_02.dat
           2023_02_03.dat

    1)分区表就是将表数据文件进行分类管理
    2)分区表表现形式就是分文件夹
    3)这里的分区和MapReduce没有关系
    4)分区表可以极大的调高数据查询效率（分区字段可以加在where条件中）
 */

-- 1、创建分区表

/*
    静态分区：
       所有的分区的值需要手动指定
    动态分区：
      所有的分区的值自动生成
 */


use myhive;
----------------单级分区表(一级文件夹)---------------
create table score
(
    sid    string, -- 学号
    cid    string, -- 学科id
    sscore int     -- 成绩
)
partitioned by (month string)     -- 指定一个分区字段，理论上这个分区子字段可以随便写，分区字段和表字段没有关系
row format delimited fields terminated by '\t';

/*
    month=01
      score.txt
    month=02
      score.txt
 */

 -- 2、给分区表添加数据
-- /user/hive/warehouse/myhive.db/score/month=202006
load data local inpath '/export/data/score.txt' into table score partition (month='202006');

-- /user/hive/warehouse/myhive.db/score/month=202007
load data local inpath '/export/data/score.txt' into table score partition (month='202007');

-- /user/hive/warehouse/myhive.db/score/month=202008
load data local inpath '/export/data/score.txt' into table score partition (month='202008');

-- 3.查询数据
select * from score;

-- 3.1 条件查询 - 只查询6月份的月考成绩
select * from score where  month='202006';

-- 3.1 条件查询 - 只查询6月份或7月份成绩
select * from score where  month='202007';


----------------多级分区表(多级文件夹)---------------
create table score2
(
    sid    string,
    cid    string,
    sscore int
)
partitioned by (year string,month string,day string)
row format delimited fields terminated by '\t';


load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2022',month='01',day='01');


load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2022',month='01',day='02');

load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2022',month='02',day='01');

load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2022',month='02',day='02');


load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2023',month='01',day='01');


load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2023',month='01',day='02');

load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2023',month='02',day='01');

load data local inpath '/export/data/score.txt'
    into table score2 partition (year='2023',month='02',day='02');


-- 查询
-- 查询所有数据
select * from score2 ;

-- 查询指定时间的成绩(2022年成绩)
select * from score2 where year='2022';

-- 查询指定时间的成绩(2023年2月成绩)
select * from score2 where year='2023' and month='02';

-- 查询指定时间的成绩(2023年2月2日成绩)

select * from score2 where year='2023' and month='02' and day = '02';


--- union all,将两个表的结果上下拼接在一起（和join不同，join是左右拼接）
explain select * from score where month = '202006' union all select * from score where month = '202007';
select * from score where month = '202006' or month = '202007';

-- 查看分区信息
show  partitions score;
show  partitions score2;

-- 查看表结构,包含分区信息
desc score;
desc formatted  covid2;  //Table Type: EXTERNAL_TABLE


-- 添加分区
alter table score add partition(month='202009');

alter table score add partition(month='202010') partition(month='202011');

--删除分区
alter table score drop partition(month = '202010');


--- ------------------动态分区----------------------------
-- 1、开启动态分区
set hive.exec.dynamic.partition=true; //hive3.x不支持该参数，2.x支持
set hive.exec.dynamic.partition.mode=nonstrict;


-------------------一级动态分区------------------------
-- 2、创建一个中间表，并加载数据
create table test1(
                      id int,
                      date_val string,
                      name string,
                      score int
)
row format delimited fields terminated by ',';
;
load data local inpath '/export/data/partiton_test1.txt' into table test1;

select * from test1;


-- 3、创建最终分区表
drop table test2;
create table test2(
          id int,
          name string,
          score int
)
partitioned by (xxx string)
row format delimited fields terminated by ',';

-- 4、查询普通表数据查询并插入分区表，在插入的过程中运行MapReduce，进行动态分区
insert overwrite table test2 partition (xxx)
select id, name, score, date_val     -- 动态分区就是根据select的最后一个字段来进行分区的
from test1;  -- 中间普通表



-------------------二级动态分区------------------------
-- 1、创建普通表
create table test3(
          id int,
          date_val string,
          name string,
          sex string,
          score int
)
row format delimited fields terminated by ',';
;

load data local inpath '/export/data/partiton_test3.txt' into table test3;

-- 2、创建分区表
drop table if exists test4;
create table test4(
      id int,
      name string,
      score int
)
partitioned by (xxx string, yyy string)
row format delimited fields terminated by ',';

-- 3、将普通的表数据进行查询，插入到目标分区表，插入时会自动执行MapReduce，完成动态分区
insert overwrite table test4 partition (xxx,yyy)
select id,name,score,date_val ,sex from test3; -- 这里的分区本质是看select的最后两个字段

select * from test4 where xxx='202106' and yyy='man';


-------------------分桶表(了解)--------------------------
/*
   1:Hive中的分桶就是MapReduce中的分区，将数据在同一个文件夹下进行分文件存储

   2:Hive中的分区和MapReduce中分区没什么系，将数据进行分到不同的文件夹存储
 */

//1：设置参数
set hive.enforce.bucketing=true; -- 开启分桶功能,从hive2.x开始，Hive默认已经开启了分桶功能，该参数不再支持
//2:设置reduce的个数(因为MapReduce的分区需要设置Reduce个数)
set mapreduce.job.reduces=3;   --该参数在Hive2.x版本之后不起作用, 不用设置Reduce个数，Hive会自动设置


//3:创建普通表
create table course_common
(
    cid    string,
    c_name string,
    tid    string
) row format delimited fields terminated by '\t';

//4:给普通表添加数据
load data local inpath '/export/data/course.txt' into table course_common;

select * from course_common;

//5:创建分桶表
drop table course;
create table course
(
    cid    string,
    c_name string,
    tid    string
)
clustered by (cid) into 3 buckets  ---  对cid求hash值，对3取模，如果取模的值相同，则数据存入同一个地方
row format delimited fields terminated by '\t';



//6:将普通表的数据进行查询，并将结果插入到分桶表
insert overwrite table course select * from course_common cluster by(cid);

//7:分桶的作用
/*
    1： 提高表与表join的效率
        1）:分桶字段必须一致，分桶字段其实就是join的字段
        2）：分桶数量必须相同
    2: 数据抽样
 */


id
1123e4567-e89b-12d3-a456-426655440000
2123e4567-e89b-12d3-a456-42665544s1100
3123e4567-e89b-111-a456-426655440111


use zzz;

set hive.stats.column.autogather=false;
set hive.exec.mode.local.auto=true;

insert into zzz values(2,'lisi');
select count(*) from zzz;



//#################表结构修改###########################
--1、清空表数据
-- 1.1 查看表类型(通过Table Type参数查看)
desc formatted stu3;
desc formatted covid2;

truncate table stu3;  //truncate只能清空内部表（可以理解为将hdfs上表数据目录下的文件删除，表结构和元数据都在）
select * from stu3;

truncate table covid2;//truncate不能能清空外部表
select * from covid2;


//#################表数据加载总结 ###########################
-- 1、insert into 添加分区表数据（不用）
create table score3 like score;
show tables;
insert into table score3 partition(month ='202007') values ('001','002',100);

-- 2、通过查询方式添加（常用）！！！！！！！！！！！！！！
create table score4 like score;
insert overwrite table score4 partition(month = '202006') select sid,cid,sscore from score ;

-- 3、通过load方式加载（常用）！！！！！！！！！！！！！
create table score5 like score;
load data local inpath '/export/data/score.txt' overwrite into table score5 partition(month='202006');

-- 4、如果现有数据后创建表，则可以通过location方法加载数据\
create external table covid2
(
    date_value date,
    county     string,
    state      string,
    fips       string,
    cases      int,
    deaths     int
)
row format delimited fields terminated by ','
location '/hive/data/covid';

-- 5、通过hadoop fs -mv/put 加载


-- 6、多插入模式加载（熟悉）!!!!!!!!!!!!!!

load data local inpath '/export/data/score.txt' overwrite into table score partition(month='202006');
select * from score;

create table score_first( sid string,cid  string) partitioned by (month string) row format delimited fields terminated by '\t' ;
create table score_second(cid string,sscore int) partitioned by (month string) row format delimited fields terminated by '\t';

-- 将score表的前两个字段查询出来插入到score_first
-- 将score表的后两个字段查询出来插入到score_second
from score
insert overwrite table score_first partition(month='202006') select sid,cid
insert overwrite table score_second partition(month = '202006')  select cid,sscore;

select * from score_first;
select * from score_second;



//#################表数据导出###########################
-- 1、将select查询的结果导出到Linux本地（导出的默认分隔符是:'\001')
insert  overwrite local directory '/export/data/exporthive' select * from score where sscore > 80;
-- 2、将select查询的结果导出到Linux本地,并指定分隔符（目标目录自动创建）
insert overwrite local directory '/export/data/exporthive' row format delimited fields terminated by '\t' select * from student;

-- 3、将select查询结果导出到hdfs上，,并指定分隔符（目标目录自动创建）

insert overwrite  directory '/export/data/exporthive' row format delimited fields terminated by '\t' select * from student;

-- 4、将select查询结果在Linux命令行终端进行导出：
 -- 切记：这条命令是在Linux上执行，不是在hive中执行
hive -e "select * from myhive.score;" > /export/data/exporthive/score.txt


//#################SQL的查询 ###########################
set hive.stats.column.autogather=false;
set hive.exec.mode.local.auto=true;
-- 1、基本查询
select sid as myid ,sscore from score;

--2、聚合函数
/*
   如果在本地模式下不能执行mr，则需要做以下配置:
    vim /export/server/hive/conf/hive-env.sh    添加以下内容
    1: 将 exprot HADOOP_HEAPSIZE=1024  注释打开
    2：将RunJar服务关闭，并且重启
 */
use myhive;
select count(sid) from score;

select max(sscore) from score;

-- 3、limit查询

select * from student limit 3;

select * from student limit 3,5; //从索引为3的行（第4行）开始查询



-- 4、条件查询
select * from score where sscore is null;
select * from score where sscore in(80,90,99);

select * from covid2;

--  查询以 'c'字母开头的县
select * from covid2 where county like 'C%';

--  查询以 第二个字符是'c'字母的县

select * from covid2 where county like '_c%';

--  查询名字是四个字母的县
select * from covid2 where county like '____';

-- 查询包含 'chi' 名字的州
select  * from covid2 where state like '%chi%';

-- 查询包含 'c' 名字的县
select * from covid2 where county rlike '[c]';

-- 查询学号不是 1 3 5 的学生
select * from student where sid not in('01','03','05');

-- 查询每一个学生的平均分数
select  * from score;

-- 5、分组查询
//分组之后，不管每一组有多少条数据，每一组最后只剩下一条数据
select sid , avg(sscore) from score group by  sid;
//如果有分组，则select的后边只能跟分组字段和聚合函数
select sid ,cid, avg(sscore) from score group by  sid; //不能执行

--  统计每一个州的确诊病例总人数
select state, sum(cases) from covid2 group by state;
select state, sum(cases) total_cases from covid2 group by state order by  total_cases desc ;

--  统计每一个州,每一个县的确诊病例总人数
select state ,county,sum(cases)  total_cases from covid2 group by state ,county order by total_cases desc;
select state ,county,sum(cases)  total_cases from covid2 group by county,state;

--  统计每一个州的总确诊人数，并筛选出总确诊人数大于100万的州
-- 对分组后的结果再进行筛选，就必须使用havinig

select state, sum(cases) total_cases
from covid2
group by state
having total_cases > 1000000
order by  total_cases desc;





//###################join操作###########################
-- 1、内连接
/*
    1)内连接求的是多张表的交集
    2)内连接又分为两种
        隐式内连接
       显式内连接
 */
use myhive;
-- 1.1 查询每一个老师所教授的课程

select * from teacher;
select * from course;

-- 隐式内连接
set hive.stats.column.autogather=false;
set hive.exec.mode.local.auto=true;
select * from  teacher, course  where teacher.tid = course.tid ;

--如果有三张表，该怎么写
select * from A a, B a ,C c where a.id = b.id and b.id = c.id;

-- 显式内连接
select * from  teacher inner join course  on teacher.tid = course.tid ;
select * from  teacher  join course  on teacher.tid = course.tid ;

select *
from A a
     join B b on a.id = b.id
     join C c on b.id = c.id;

-- 2、外连接
/*
   1) 外连接是以某一张表为主，不是求交集
   2) 外连接分为三种
      左外连接:以左表为主，会把左表的数据全部输出，右表有交集的数据输出，没有交集的数据则输出NULL
      右外连接:以右表为主，会把右表的数据全部输出，左表有交集的数据输出，没有交集的数据则输出NULL
      满外连接
 */

-- 2.1 左外连接
select * from  teacher left join course  on teacher.tid = course.tid ;

-- 给左表添加一行右表没有的数据
insert into teacher values ('06','周七');

select * from  teacher left join course  on teacher.tid = course.tid ;



select *
from A a
         left join B b on a.id = b.id
         left join C c on b.id = c.id;


-- 2.2 右外连接

-- 给右表添加一行左表没有的数据
insert into course values('04','地理','05');
select * from  teacher right join course  on teacher.tid = course.tid ;

-- 2.3 满外连接(左外和右外的并集)
select * from  teacher full join course  on teacher.tid = course.tid ;




//###################排序操作###########################

-- 1、Order by ！！！！！！！！！！！！！！1
/*
   1:用于对最终的结果进行全局排序，要求只能有一个Reduce
 */
SELECT * FROM student s LEFT JOIN score sco ON s.sid = sco.sid ORDER BY sco.sscore ASC;
SELECT * FROM student s LEFT JOIN score sco ON s.sid = sco.sid ORDER BY sco.sscore DESC;

-- 如果order by后边跟多个字段，则最前边的字段时排序的主要条件，如果主要相同，则按照次要条件排序
-- order by后边的排序字段不能随便调换位置
select sid ,avg(sscore) avg from score group by sid order by sid,avg;

select sid ,avg(sscore) avg from score group by sid order by '颜值' desc ,'能力' desc;

-- 2、Sort By是将每一个Reduce的输出结果进行排序
--1)设置reduce个数
set mapreduce.job.reduces=3;
--2)查看设置reduce个数
set mapreduce.job.reduces;
--3）查询成绩按照成绩降序排列
-- sort by会自动的将每一个Reduce输出的内容进行排序
select * from score sort by sscore desc;

--4)将查询结果导入到文件中（按照成绩降序排列  ）
insert overwrite local directory '/export/data/sort'
select * from score sort by sscore;


-- 3. Distribute By +  sort by 分区排序 ！！！！！！！！！！
-- 1)设置reduce的个数，将我们对应的sid划分到对应的reduce当中去
set mapreduce.job.reduces=7;

-- 2)通过distribute by进行数据的分区
-- 使用distribute来设置MR的K2，然后使用K2的hash值对reduce个数取模进行分区
-- sort by 会对每一个分区后的数据再进行排序
explain  select * from score distribute by sid sort by sscore;

--
insert overwrite local directory '/export/data/distribute'
select * from score distribute by sid sort by sscore desc;


-- 4、Cluster by
--    distribute by sid  sort by sid  等价于 ---->cluster by  sid
      ---》100个不同sid  ---》  reduce格式 设置为3个
--   当distribute by 和 sort by的字段相同时，则可以使用过cluster by简化书写
--  Cluster by默认只能是升序排序，不能指定其他排序方式

set mapreduce.job.reduces=2;

insert overwrite local directory '/export/data/cluster'
select * from score cluster by sid ;





//#################Hive的函数########################

set hive.stats.column.autogather=false;
set hive.exec.mode.local.auto=true;
-- 1、内置函数
select round(3.466); //四舍五入保留整数
select sid ,round(avg(sscore)) as avg_score from score group by sid;
select sid ,round(avg(sscore),2) as avg_score from score group by sid;


-- 2、逻辑控制语句

--- if语句
select sid,sscore , if(sscore >= 60,'及格', '不及格') as flag from score;

-- case语句 -用法1
select
       sid,
       sscore,
       case sscore
           when 0 then '零分'
           when 100 then '满分'
           else '有分'
      end  as flag
from score;

-- case语句 -用法2 ！！！！！！！！！！！！！！！

select
   sid,
   sscore,
   case
       when  sscore >= 85 and sscore <= 100 then '优秀'
       when  sscore >= 70 then '良好'
       when  sscore >= 60 then '及格'
       else '不及格'
   end as flag
from score;

//------------转换函数----------------
select cast(12.34 as int);
select cast('1234' as int) + 10;
select cast('2020-12-23' as date);



//---------行转列-------------
-- 1、准备emp.txt数据
20      SMITH
30      ALLEN
30      WARD
20      JOINS
30      MARTIN
10      CLARK
20      SCOTT
10      KING
30      TURNER
20      ADAMS
30      JAMES
20      FORD
10      MILLER
-- 2、创建表
use myhive;
create table emp(
                    deptno int,
                    ename string
) row format delimited fields terminated by '\t';

-- 3、加载数据
load data local inpath '/export/data/emp.txt' into table  emp;
select * from emp;

-- 4、行转列操作
-- collect_list(不去重)/collect_set(去重)  ： 该函数也是一个聚合函数，将同一组的中字段值存放到一个数组中
select deptno, collect_list(ename) as ems
from emp
group by deptno;

-- concat_ws的作用
select concat_ws("|",'hello1','hello2','hello3');
select concat_ws("|",数组);

-- concat_ws遍历数组，每遍历一个元素就进行字符串拼接，分隔符是 |
select deptno, concat_ws('|',collect_list(ename))   as ems
from emp
group by deptno;

-- 向原表中添加10号部门重复的员工名
insert into emp values (10,'KING');

-- collect_set会去重，
select deptno, concat_ws('|',collect_set(ename))   as ems
from emp
group by deptno;


//---------列转行------------------------------
--1、准备数据emp2.txt
10      CLARK|KING|MILLER
20      SMITH|JONES|SCOTT|ADAMS|FORD
30      ALLEN|WARD|MARTIN|BLAKE|TURNER|JAMES

--2、创建表
create table emp2(
 deptno int,
 names array<string>
)
row format delimited fields terminated by '\t'
collection items terminated by '|';

--3、加载数据
load data local inpath '/export/data/emp2.txt' into table  emp2;
select * from emp2;


--4、使用explode函数进行炸裂操作
select  explode(names) from emp2;

-- 5、需要使用LATERAL VIEW侧视图和explode配合进行分析
/*
    emp2表和 explode生成的表进行join，判断explode的每一行是否包含在emp2表的数组中
    如果在数组中，则join成功，否则失败
    tmp_tb：是explode生成的中间临时表的别名
    as name :输出列的名字
 */
select deptno, name
from emp2 lateral view  explode(names) tmp_tb as name;

//---------reflect函数------------------------------
/*
   1）在hive中调用java的静态方法
 */
-- 1、创建表并加载数据
create table test_reflect(col1 int,col2 int) row format delimited fields terminated by ',';
load data local inpath '/export/data/test_reflect.txt' into table  test_reflect;
select * from test_reflect;

-- 2、使用java中的静态函数Max
select col1,col2,reflect('java.lang.Math','max',col1,col2) from test_reflect; //Math.max(10,20);
select col1,col2,reflect('java.lang.Math','max',col1,col2) from test_reflect; //Math.max(10,20);

-- 3、使用java中的静态函数UUID

select reflect('java.util.UUID','randomUUID'); //UUID.randomUUID();
select concat(col1,"---",reflect('java.util.UUID','randomUUID')) from test_reflect; //Math.max(10,20);


//---------开窗函数（窗口函数）-分组排序开窗函数------------------------------
-- ROW_NUMBER,RANK,DENSE_RANK

--1.1准备数据test1.txt
cookie1,2018-04-10,1
cookie1,2018-04-11,5
cookie1,2018-04-12,7
cookie1,2018-04-13,3
cookie1,2018-04-14,2
cookie1,2018-04-15,4
cookie1,2018-04-16,4
cookie2,2018-04-10,2
cookie2,2018-04-11,3
cookie2,2018-04-12,5
cookie2,2018-04-13,6
cookie2,2018-04-14,3
cookie2,2018-04-15,9
cookie2,2018-04-16,7

-- 1.2创建表
CREATE TABLE test_window_func1(
  cookieid string,
  createtime string,   --day
  pv INT
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

-- 1.3 给表加载数据
load data local inpath '/export/data/test1.txt' into table  test_window_func1;
select * from test_window_func1;

-- 1.4 使用开窗函数来实现分组并组内排序
 -- 需求1：按照cookieid进行分组，并且在每一组中按照pv进行降序排序
select
   *,
   row_number() over (partition by cookieid  order by pv desc )  as rk1, // 1 2 3 4 5
   rank() over (partition by cookieid  order by pv desc )  as rk2,       // 1 2 3 3 5
   dense_rank()  over (partition by cookieid  order by pv desc )  as rk3 // 1 2 3 3 4
from
     test_window_func1;

-- 需求2：按照cookieid进行分组，并且在每一组中按照pv进行降序排序,选出每一组排名前三的信息（TopN问题）

-- 以下写法报错，因为SQL的执行顺序：from  where select ，where的时候，别名还没有出现
select
    *,
    dense_rank()  over (partition by cookieid  order by pv desc )  as rk3 -- 1 2 3 3 4
from
    test_window_func1
;

-- -------以下代码通过子查询可以执行
select
       *
from (
     select *,
            dense_rank() over (partition by cookieid order by pv desc ) as rk3 -- 1 2 3 3 4
     from test_window_func1
 )t
where rk3 <=3;


-- 需求3：查询新冠疫情数据表中每一个州确诊人数最多的县TopN

select
    *
from (
         select *,
                dense_rank() over (partition by state order by cases desc ) as rk3 -- 1 2 3 3 4
         from covid2
     )t
where t.rk3 <=1;


-- 需求4：特殊用法
-- 4.1 如果去掉partition by,则会把一张表所有的数据当成一组进行排序
-- 类似：select  * from test_window_func1 order by pv;
select
    *,
    dense_rank()  over ( order by pv desc )  as rk3 -- 1 2 3 3 4
from
    test_window_func1
;

-- 4.2 分组和排序的后边都可以指定多个字段
select
    *,
    dense_rank()  over (partition by cookieid,pv  order by cookieid,createtime desc )  as rk3 -- 1 2 3 3 4
from
    test_window_func1
;

//---------开窗函数（窗口函数）-指定区间进行统计开窗函数------------------------------
-- 1、创建表
create table test_window_func2(
  cookieid string,
  createtime string,   --day
  pv int
)
row format delimited fields terminated by ',';

-- 2、加载数据

load data local inpath '/export/data/test1.txt' into table  test_window_func2;

-- 3、使用聚合开窗函数进行统计
-- select sum(sscore) from score;
-- 累加区间：从开头到当前行（默认）
select cookieid,createtime,pv,
       sum(pv) over(partition by cookieid order by createtime) as pv1
from test_window_func2;


-- 等价与上边的写法
select cookieid,createtime,pv,
       sum(pv) over(partition by cookieid order by createtime rows between unbounded preceding and current row) as pv2
from test_window_func2;

-- 累加区间：从前三行累加到当前行
select cookieid,createtime,pv,
       sum(pv) over(partition by cookieid order by createtime rows between 3 preceding and current row)
from test_window_func2;

-- 累加区间：从前三行累加到下1行
select cookieid,createtime,pv,
       sum(pv) over(partition by cookieid order by createtime rows between 3 preceding and 1 following) as pv5
from test_window_func2;

-- 累加区间：从当前行加到组的最后
select cookieid,createtime,pv,
       sum(pv) over(partition by cookieid order by createtime rows between current row and unbounded following) as pv6
from test_window_func2;



-- 注意以上的sum可以替换为avg,max,min

select cookieid,createtime,pv,
       max(pv) over(partition by cookieid order by createtime) as pv1
from test_window_func2;


select cookieid,createtime,pv,
       min(pv) over(partition by cookieid order by createtime) as pv1
from test_window_func2;

select cookieid,createtime,pv,
       avg(pv) over(partition by cookieid order by createtime) as pv1
from test_window_func2;


--- lag lead

-- ------------------lag演示-------------------------------
-- 将上1行数据放在当前行
select  cookieid,createtime,pv,
    lag(createtime,1) over (partition by cookieid order by createtime)
from test_window_func2;

-- 将上2行数据放在当前行
select  cookieid,createtime,pv,
        lag(createtime,2) over (partition by cookieid order by createtime)
from test_window_func2;

-- ------------------lead演示-------------------------------
-- 将下1行数据放在当前行
select  cookieid,createtime,pv,
        lead(createtime,1) over (partition by cookieid order by createtime)
from test_window_func2;

-- 将下2数据放在当前行
select  cookieid,createtime,pv,
        lead(createtime,2) over (partition by cookieid order by createtime)
from test_window_func2;




----------------自定义函数-UDF-------------
-- UDF 一进一出函数

-- 1:准备数据user.txt
1001,17801112345,张三
1002,13901618845,李四
1003,13609975312,王五

-- 2、创建表
create  table test_user(
    uid string,
    phone_num string,
    uname  string
)row format delimited fields terminated by ',';

-- 3、给表加载数据
load data local inpath '/export/data/user.txt'  overwrite  into table  test_user;

select * from test_user;

-- 4、编写java程序
 -- 4.1 导入maven依赖
<dependencies>
    <dependency>
        <groupId>org.apache.hive</groupId>
        <artifactId>hive-exec</artifactId>
        <version>3.1.2</version>
    </dependency>
    <dependency>
        <groupId>org.apache.hadoop</groupId>
        <artifactId>hadoop-common</artifactId>
        <version>3.1.4</version>
    </dependency>
</dependencies>

-- 4.2 编写java代码
    public class MyUDF  extends UDF {
        //17801112345 ---> 178****2345
        public String  evaluate(String phoneNumStr){
            //匹配手机号是否合法
        String regex = "1[35789][0-9]{9}";
        boolean flag = phoneNumStr.matches(regex);
        if (!flag){
            return null;
        }else{
                String str1 = phoneNumStr.substring(0,3);
                String str2 = phoneNumStr.substring(7);

                return str1 + "****"+str2;
    }
}

-- 5、 将代码打成jar包
-- 6、 将jar包上传到hive的lib目录
-- 7、 将jar包进行重命名
mv day19_udf-1.0-SNAPSHOT.jar my_udf.jar
-- 8、在hive的客户端添加我们的jar包
  hive> add jar /export/server/hive/lib/my_udf.jar

-- 9、设置函数与我们的自定义函数关联-临时函数
 hive> create temporary function my_jiami as 'cn.itcast.udf.MyUDF';

-- 10、使用函数
hive>select my_jiami(phone_num) from test_user;

-- 11、设置函数与我们的自定义函数关联-永久函数
-- 11.1 把自定义函数的jar上传到hdfs中.
    hadoop fs -mkdir /hive_func
    hadoop fs -put my_udf.jar /hive_func
-- 11.2. 创建永久函数
  hive> create function my_jiami2 as 'cn.itcast.udf.MyUDF'
    using jar 'hdfs://node1:8020/hive_func/my_udf.jar';
--11.3 验证(关闭hive终端，重新进入验证)
 hive>select my_jiami2(phone_num) from test_user;


----------------Hive压缩方式---------------
 Hive推荐使用Snappy压缩（谷歌推荐）

----------------Hive数据的存储格式---------------
-- 行存储(TextFile默认， SEQUENCEFILE)
  select * from A ; -- 效率高
  select id from A ; -- 效率低
-- 列存储（ORC,PARQUET）
  select * from A ; --  效率低
  select id from A ; -- 效率高

-- 总结，在应用中一般都是查询指定的列，所以后期所有的Hive数据存储基本都使用列式存储（ORC）



----------------Hive压缩方式+存储方式-操作1---------------

-- 1、文本存储格式 - 18.13M
---文本存储，源文件多大，加载之后还是多大，并没有节省磁盘空间
create table log_text (
  track_time string,
  url string,
  session_id string,
  referer string,
  ip string,
  end_user_id string,
  city_id string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE ;  -- 表数据文件的存储格式

load data local inpath '/export/data/log.data' into table log_text ;

select * from log_text;


-- 2、orc存储格式(列式存储) -- 2.87M
create table log_orc(
    track_time string,
    url string,
    session_id string,
    referer string,
    ip string,
    end_user_id string,
    city_id string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS orc ;

-- 给orc存储格式表加载数据不能使用load，因为要走MR，所以必须使用 insert into ... select
insert into table log_orc select * from log_text ;

select * from log_orc limit 10;

-- 2、parquet存储格式（列式存储） -- 13M
create table log_parquet(
                        track_time string,
                        url string,
                        session_id string,
                        referer string,
                        ip string,
                        end_user_id string,
                        city_id string
)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    STORED AS parquet ;

-- 给orc存储格式表加载数据不能使用load，因为要走MR，所以必须使用 insert into ... select
insert into table log_parquet select * from log_text ;

select * from log_parquet limit 10;


-- 存储文件的压缩比总结：
  ORC >  Parquet >  textFile
-- 存储文件的查询速度总结：
  ORC > TextFile > Parquet


----------------Hive压缩方式+存储方式-操作2---------------
/*
  1: ORC存储 + ORC默认的压缩                  -- 2.78M
  2: ORC存储 + 不压缩 （去掉ORC默认的压缩）     -- 7.69 MB
  3：ORC存储 + Snappy压缩                    -- 3.75 MB
 */

-- 1、ORC存储 + ORC默认的压缩
create table log_orc(
    track_time string,
    url string,
    session_id string,
    referer string,
    ip string,
    end_user_id string,
    city_id string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS orc
tblproperties ("orc.compress"="ZLIB");


-- 2、  ORC存储 + 不压缩 （去掉ORC默认的压缩）
create table log_orc_none( -- 7.69 MB
     track_time string,
     url string,
     session_id string,
     referer string,
     ip string,
     end_user_id string,
     city_id string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS orc
tblproperties ("orc.compress"="NONE");

insert into table log_orc_none select * from log_text ;

-- 2、 ORC存储 + Snappy压缩

create table log_orc_snappy( -- 3.75 MB
       track_time string,
       url string,
       session_id string,
       referer string,
       ip string,
       end_user_id string,
       city_id string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS orc tblproperties ("orc.compress"="SNAPPY");

insert into table log_orc_snappy select * from log_text ;


create table ori
(id bigint,
 time_val bigint,
 uid string,
 keyword string,
 url_rank  int,
 click_num int,
 click_url string
) row format delimited fields terminated by '\t';


load data local inpath '/export/data/big_file/*' into table ori;

select * from ori limit 10;

```


