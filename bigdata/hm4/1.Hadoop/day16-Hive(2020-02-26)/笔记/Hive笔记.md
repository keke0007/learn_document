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
```

