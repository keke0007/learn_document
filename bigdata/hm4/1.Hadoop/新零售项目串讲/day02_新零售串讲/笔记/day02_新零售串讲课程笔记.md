# day02_新零售串讲课程笔记

今日目标:  选择其中三个表, 带着从ODS层 到DWD层 整个实施操作(全量操作 以及 增量操作)



## 1- ods层:

ODS层作用:

```properties
	对接数据源, 一般和数据源保持相同粒度, 简单来说, 数据源中有那些表, 那么在ODS层就需要构建那些表, 表中字段与数据源的字段保持一致
	在ODS层建表的时候, 我们会习惯性加上一个日期分区字段, 用于标记在何时将数据导入到ODS层

数据源: Mysql
ODS层: 位于HIVE中

思考: 如何将Mysql中数据导入到HIVE中呢?  Sqoop
```

从数据源将数据同步到ODS层的时候, 一般有四种同步方式:

* 1- 全量覆盖同步方式

```properties
适用于: 
	表数据变更的频次不多, 不需要记录其历史变化, 而且整个表数据量相对来说较少, 可以采用全量覆盖同步

操作方式:
	每次同步的时候, 都需要将原有的数仓中数据全部删除 然后重新导入业务库的数据即可
	建表的时候, 不需要构建分区表

比如说:  地区表,  时间表
```

* 2- 仅新增同步方式

```properties
适用于: 
	业务数据只会有新增的操作, 不会有变更的操作, 数据量比较多

操作方式:
	在数仓建表的时候, 需要构建分区表, 分区字段和同步数据的周期是一致的, 比如说: 每天都需要同步新增的数据, 就以天作为分区字段即可, 如果月新增, 就以月作为分区
	每次进行同步数据的时候, 将对应周期下的新增数据放置到对应分区日期目录下
```

* 3- 新增及更新同步方式

```properties
适用于:
	业务端数据既有更新的操作, 又有新增的操作, 而且数据量比较大

操作方式: 
	在数仓建表的时候, 需要构建分区表, 分区字段和同步数据的周期是一致的, 比如说: 每天都需要同步新增和更新的数据, 就以天作为分区字段即可, 如果月新增, 就以月作为分区
	每次进行同步的时候, 将对应周期下的新增和更新的数据放置到对应日期分区下即可
```

* 4- 全量同步方式(了解)

```properties
适用于: 
	业务库的数据量不是很大, 但是也存在更新和新增. 而且不需要保留太多的历史版本

操作方式:
	在数仓中建表的时候, 需要构建分区表, 分区字段和同步数据的周期是一致的
	每次导入都是导入截止当前时间的全量数据, 定期将历史数据删除即可
```



----

### 1.1 构建ODS层表

* 全量覆盖表:  日期表

```properties
-- 日期表:   t_date
drop table yp_ods.t_date; 
CREATE TABLE yp_ods.t_date ( 
    dim_date_id string COMMENT '日期', 
    date_code string COMMENT '日期编码', 
    lunar_calendar string COMMENT '农历', 
    year_code string COMMENT '年code', 
    year_name string COMMENT '年名称', 
    month_code string COMMENT '月份编码', 
    month_name string COMMENT '月份名称', 
    quanter_code string COMMENT '季度编码', 
    quanter_name string COMMENT '季度名称', 
    year_month string COMMENT '年月', 
    year_week_code string COMMENT '一年中第几周', 
    year_week_name string COMMENT '一年中第几周名称', 
    year_week_code_cn string COMMENT '一年中第几周（中国）', 
    year_week_name_cn string COMMENT '一年中第几周名称（中国',
    week_day_code string COMMENT '周几code', 
    week_day_name string COMMENT '周几名称', 
    day_week string COMMENT '周', 
    day_week_cn string COMMENT '周(中国)',
    day_week_num string COMMENT '一周第几天', 
    day_week_num_cn string COMMENT '一周第几天（中国）', 
    day_month_num string COMMENT '一月第几天', 
    day_year_num string COMMENT '一年第几天', 
    date_id_wow string COMMENT '与本周环比的上周日期', 
    date_id_mom string COMMENT '与本月环比的上月日期', 
    date_id_wyw string COMMENT '与本周同比的上年日期', 
    date_id_mym string COMMENT '与本月同比的上年日期', 
    first_date_id_month string COMMENT '本月第一天日期', 
    last_date_id_month string COMMENT '本月最后一天日期',
    half_year_code string COMMENT '半年code', 
    half_year_name string COMMENT '半年名称', 
    season_code string COMMENT '季节编码', 
    season_name string COMMENT '季节名称', 
    is_weekend string COMMENT '是否周末（周六和周日）', 
    official_holiday_code string COMMENT '法定节假日编码', 
    official_holiday_name string COMMENT '法定节假日', 
    festival_code string COMMENT '节日编码', 
    festival_name string COMMENT '节日', 
    custom_festival_code string COMMENT '自定义节日编码', 
    custom_festival_name string COMMENT '自定义节日', 
    update_time string COMMENT '更新时间' 
)
COMMENT '时间维度表' 
row format delimited fields terminated by '\t' 
stored as orc tblproperties ('orc.compress' = 'ZLIB');
```

* 仅新增同步表: 订单评价表

```properties
-- 订单评价表 : t_goods_evaluation
DROP TABLE if exists yp_ods.t_goods_evaluation;
CREATE TABLE yp_ods.t_goods_evaluation ( 
	`id` string, 
	`user_id` string COMMENT '评论人id', 
	`store_id` string COMMENT '店铺id', 
	`order_id` string COMMENT '订单id', 
	`geval_scores` INT COMMENT '综合评分', 
	`geval_scores_speed` INT COMMENT '送货速度评分0-5分(配送评分)', 
	`geval_scores_service` INT COMMENT '服务评分0-5分', 
	`geval_isanony` TINYINT COMMENT '0-匿名评价，1-非匿名', 
	`create_user` string, 
	`create_time` string, 
	`update_user` string, 
	`update_time` string, 
	`is_valid` TINYINT COMMENT '0 ：失效，1 ：开启'
)
comment '商品评价表' 
partitioned by (dt string) 
row format delimited fields terminated by '\t' stored as orc tblproperties ('orc.compress'='ZLIB');
```

* 新增及更新同步表: 店铺表

```properties
DROP TABLE if exists yp_ods.t_store; 
CREATE TABLE yp_ods.t_store ( 
	`id` string COMMENT '主键', 
	`user_id` string, 
	`store_avatar` string COMMENT '店铺头像', 
	`address_info` string COMMENT '店铺详细地址', 
	`name` string COMMENT '店铺名称', 
	`store_phone` string COMMENT '联系电话', 
	`province_id` INT COMMENT '店铺所在省份ID', 
	`city_id` INT COMMENT '店铺所在城市ID', 
	`area_id` INT COMMENT '店铺所在县ID', 
	`mb_title_img` string COMMENT '手机店铺 页头背景图',
	`store_description` string COMMENT '店铺描述', 
	`notice` string COMMENT '店铺公告', 
	`is_pay_bond` TINYINT COMMENT '是否有交过保证金 1：是0：否', 
	`trade_area_id` string COMMENT '归属商圈ID', 
	`delivery_method` TINYINT COMMENT '配送方式 1 ：自提 ；3 ：自提加配送均可; 2 : 商家配送', 
	`origin_price` DECIMAL, 
	`free_price` DECIMAL, 
	`store_type` INT COMMENT '店铺类型 22天街网店 23实体店 24直营店铺 33会员专区店', 
	`store_label` string COMMENT '店铺logo', 
	`search_key` string COMMENT '店铺搜索关键字', 
	`end_time` string COMMENT '营业结束时间', 
	`start_time` string COMMENT '营业开始时间', 
	`operating_status` TINYINT COMMENT '营业状态 0 ：未营业 ；1 ：正在营业', 
	`create_user` string, 
	`create_time` string, 
	`update_user` string, 
	`update_time` string, 
	`is_valid` TINYINT COMMENT '0关闭，1开启，3店铺申请中', 
	`state` string COMMENT '可使用的支付类型:MONEY金钱支付;CASHCOUPON现金券支付', 
	`idCard` string COMMENT '身份证', 
	`deposit_amount` DECIMAL(11,2) COMMENT '商圈认购费用总额', 
	`delivery_config_id` string COMMENT '配送配置表关联ID', 
	`aip_user_id` string COMMENT '通联支付标识ID', 
	`search_name` string COMMENT '模糊搜索名称字段:名称_+真实名称', 
	`automatic_order` TINYINT COMMENT '是否开启自动接单功能 1：是 0 ：否', 
	`is_primary` TINYINT COMMENT '是否是总店 1: 是 2: 不是',
	`parent_store_id` string COMMENT '父级店铺的id，只有当is_primary类型为2时有效'
)
comment '店铺表' 
partitioned by (dt string) 
row format delimited fields terminated by '\t' 
stored as orc tblproperties ('orc.compress'='ZLIB');
```



### 1.2 全量导入数据到ODS层

​		通过 sqoop完成数据导入到HIVE中

````
sqoop导入HIVE的时候, 有二种导入方式:  
方式一: sqoop原生方案 : 仅支持textFile存储格式
方式二: sqoop hcatalog方式 : 支持多种存储格式
````

执行导入操作:

* 1- 全量覆盖方式导入:  日期表

```shell
sqoop import \
--connect jdbc:mysql://192.168.88.80:3306/yipin \
--username root \
--password 123456 \
--query "SELECT  * FROM t_date where 1=1 and \$CONDITIONS" \
--hcatalog-database yp_ods \
--hcatalog-table t_date \
-m 1
```

* 2-仅新增同步导入:  订单评价表

```sql
sqoop import \
--connect jdbc:mysql://192.168.88.80:3306/yipin \
--username root \
--password 123456 \
--query "SELECT  *,'2022-05-03' as dt FROM t_goods_evaluation where create_time <='2022-05-03 23:59:59'  and \$CONDITIONS" \
--hcatalog-database yp_ods \
--hcatalog-table t_goods_evaluation \
-m 1


注意: 这里写 1 =1 相当于将当天的数据全部导入了, 实际上仅需要导入截止今天以前的所有数据
	今天的数据, 是在第二天导入的
	
说明: 当前执行日期为 2022-05-05 , 实际导入 2022-05-04以前的数据, 目前为了后续演示增量过程,假设今天为2022-05-04, 导入2022-05-03以前的所有的数据即可
```

* 3- 新增及更新同步导入:  店铺表

```shell
sqoop import \
--connect jdbc:mysql://192.168.88.80:3306/yipin \
--username root \
--password 123456 \
--query "SELECT  *,'2022-05-03' as dt FROM t_store where create_time <='2022-05-03 23:59:59' OR update_time <='2022-05-03 23:59:59' and \$CONDITIONS" \
--hcatalog-database yp_ods \
--hcatalog-table t_store \
-m 1

说明: 当前执行日期为 2022-05-05 , 实际导入 2022-05-04以前的数据, 目前为了后续演示增量过程,假设今天为2022-05-04, 导入2022-05-03以前的所有的数据即可
```

### 1.3 在mysql端模拟一份增量数据

```sql
-- 日期表(全量覆盖的方式):
--    新增一条数据
INSERT INTO yipin.`t_date` VALUES ('20320101','2032-01-01','20311201','2031','2031年','01','01月','1','Q1','203201','52','203152','01','203201','3','星期三','01','01','4','3','01','001','20311225','20311201','10000000','20310101','20320101','20320131','1','上半年','S04','冬季','否','H01','元旦','F01','元旦','','','2021-12-20 14:20:57.401');
   
-- 订单评价表(仅新增同步):
INSERT INTO yipin.`t_goods_evaluation` VALUES ('22222222','430eff5a55d911e998ec7cd30ad32e2e','7b09b44e5b6d11e998ec7cd30ad32e2e','dd190411306814f41f',10,10,10,1,'430eff5a55d911e998ec7cd30ad32e2e','2022-05-04 09:42:02',NULL,NULL,1);
	
-- 店铺表(新增及更新同步):
UPDATE  yipin.`t_store` SET NAME='博学谷教育平台' , update_time = '2022-05-04 05:50:55' WHERE id = '0afb5daf777d11e998ec7cd30ad32e2e';
	
INSERT INTO yipin.`t_store` VALUES ('11020','02554155777c11e998ec7cd30ad32e2e',NULL,NULL,'酷丁鱼幼儿教育',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0af148be777d11e998ec7cd30ad32e2e',NULL,NULL,NULL,24,NULL,NULL,'22:00','08:00',0,'02554155777c11e998ec7cd30ad32e2e','2022-05-04 05:50:55',NULL,NULL,3,'MONEY',NULL,NULL,'0afaf8ad777d11e998ec7cd30ad32e2e',NULL,'名称_**亿隆电子科技开发有限公司',0,1,NULL);

```



### 1.4 完成增量数据同步操作

* 思考:  如果从业务库中获取到需要增量的数据呢? 

  * 全量覆盖的表操作: 日期表

  ```sql
  -- 日期表(全量覆盖): 如果更新的频次以天基准, 对于全量覆盖的表来说, 每天都是将之前的所有的数据全部都删除, 然后重新将全量的数据导入到目标表即可
  
  -- 思考: 是否可以使用sqoop直接进行全量的覆盖呢? 表存储格式为ORC  , 导入数据需要使用hcatalog方式, 而这种方式仅支持追加, 不支持覆盖写入
  
  -- 如何解决呢? 先将表清空了, 然后执行导入操作
  -- 对于HIVE的表, 默认是无法直接对数据进行处理, 也就是无法修改数据,或者删除数据, 所以想 delete  update 都是无法执行的, 一般建议将表先删除, 然后重新建表即可(不建议使用truncate)
  
  -- 第一步: 先将表删除, 然后重新建表
  drop table if exists yp_ods.t_date; 
  CREATE TABLE if not exists yp_ods.t_date ( 
      dim_date_id string COMMENT '日期', 
      date_code string COMMENT '日期编码', 
      lunar_calendar string COMMENT '农历', 
      year_code string COMMENT '年code', 
      year_name string COMMENT '年名称', 
      month_code string COMMENT '月份编码', 
      month_name string COMMENT '月份名称', 
      quanter_code string COMMENT '季度编码', 
      quanter_name string COMMENT '季度名称', 
      year_month string COMMENT '年月', 
      year_week_code string COMMENT '一年中第几周', 
      year_week_name string COMMENT '一年中第几周名称', 
      year_week_code_cn string COMMENT '一年中第几周（中国）', 
      year_week_name_cn string COMMENT '一年中第几周名称（中国',
      week_day_code string COMMENT '周几code', 
      week_day_name string COMMENT '周几名称', 
      day_week string COMMENT '周', 
      day_week_cn string COMMENT '周(中国)',
      day_week_num string COMMENT '一周第几天', 
      day_week_num_cn string COMMENT '一周第几天（中国）', 
      day_month_num string COMMENT '一月第几天', 
      day_year_num string COMMENT '一年第几天', 
      date_id_wow string COMMENT '与本周环比的上周日期', 
      date_id_mom string COMMENT '与本月环比的上月日期', 
      date_id_wyw string COMMENT '与本周同比的上年日期', 
      date_id_mym string COMMENT '与本月同比的上年日期', 
      first_date_id_month string COMMENT '本月第一天日期', 
      last_date_id_month string COMMENT '本月最后一天日期',
      half_year_code string COMMENT '半年code', 
      half_year_name string COMMENT '半年名称', 
      season_code string COMMENT '季节编码', 
      season_name string COMMENT '季节名称', 
      is_weekend string COMMENT '是否周末（周六和周日）', 
      official_holiday_code string COMMENT '法定节假日编码', 
      official_holiday_name string COMMENT '法定节假日', 
      festival_code string COMMENT '节日编码', 
      festival_name string COMMENT '节日', 
      custom_festival_code string COMMENT '自定义节日编码', 
      custom_festival_name string COMMENT '自定义节日', 
      update_time string COMMENT '更新时间' 
  )
  COMMENT '时间维度表' 
  row format delimited fields terminated by '\t' 
  stored as orc tblproperties ('orc.compress' = 'ZLIB');
  
  -- 第二步: 执行 sqoop命令 进行全量数据导入操作:
  sqoop import \
  --connect jdbc:mysql://192.168.88.80:3306/yipin \
  --username root \
  --password 123456 \
  --query "SELECT  * FROM t_date where 1=1 and \$CONDITIONS" \
  --hcatalog-database yp_ods \
  --hcatalog-table t_date \
  -m 1
  ```

  * 仅新增同步方式:

  ```sql
  -- 订单评价表(仅新增同步): 表只有新增的操作, 没有更新的操作. 对于这种同步方式的表, 我们只需要每天将其新增的数据导入到对应日期分区下即可
  
  -- 思考: 如何获取到上一天的新增数据呢?
  SELECT *, '2022-05-04' as dt  FROM  t_goods_evaluation WHERE create_time BETWEEN '2022-05-04 00:00:00' AND '2022-05-04 23:59:59';
  
  -- 基于 sqoop完成导入:
  sqoop import \
  --connect jdbc:mysql://192.168.88.80:3306/yipin \
  --username root \
  --password 123456 \
  --query "SELECT *, '2022-05-04' as dt  FROM  t_goods_evaluation WHERE create_time BETWEEN '2022-05-04 00:00:00' AND '2022-05-04 23:59:59'  and \$CONDITIONS" \
  --hcatalog-database yp_ods \
  --hcatalog-table t_goods_evaluation \
  -m 1
  ```

  * 新增及更新同步方式:

  ```sql
  -- 店铺表(新增及更新同步):  表既有更新又有新增 对于这种同步方式表, 我们需要将其上一天的新增和更新的数据放置到对应分区下即可
  
  SELECT  *,'2022-05-03' as dt FROM t_store where create_time BETWEEN '2022-05-04 00:00:00' AND '2022-05-04 23:59:59' OR update_time BETWEEN '2022-05-04 00:00:00' and '2022-05-04 23:59:59'
  
  -- sqoop导入操作
  sqoop import \
  --connect jdbc:mysql://192.168.88.80:3306/yipin \
  --username root \
  --password 123456 \
  --query "SELECT  *,'2022-05-04' as dt FROM t_store where create_time BETWEEN '2022-05-04 00:00:00' AND '2022-05-04 23:59:59' OR update_time BETWEEN '2022-05-04 00:00:00' and '2022-05-04 23:59:59' and \$CONDITIONS" \
  --hcatalog-database yp_ods \
  --hcatalog-table t_store \
  -m 1
  ```

  > 目前, 书写的这些sqoop的脚本, 是比较死板的, 希望能够自动获取上一天的日期, 进行导入处理
  >
  > 如何解决呢?  希望能够自动获取上一天的日期, 而且希望支持根据指定的日期导入相关的数据
  >
  > ​        此时需要编写 SHELL脚本, 通过shell脚本来实现这个逻辑

  ```shell
  #!/bin/bash
  
  # 1- ENV PATH
  HIVE_HOME=/usr/bin/hive
  
  # 2- Tran
  if [ $# == 1 ]
  then
     dateStr=$1
  else
     dateStr=`date -d '-1 day' +'%Y-%m-%d'`
  fi
  
  echo ${dateStr}
  
  # 3- HIVE DELETE TABLE AND  CREATE
  echo '----------HIVE EXE START-----------------'
  
  ${HIVE_HOME} -S -e "
  
  drop table if exists yp_ods.t_date; 
  CREATE TABLE if not exists yp_ods.t_date ( 
      dim_date_id string COMMENT '日期', 
      date_code string COMMENT '日期编码', 
      lunar_calendar string COMMENT '农历', 
      year_code string COMMENT '年code', 
      year_name string COMMENT '年名称', 
      month_code string COMMENT '月份编码', 
      month_name string COMMENT '月份名称', 
      quanter_code string COMMENT '季度编码', 
      quanter_name string COMMENT '季度名称', 
      year_month string COMMENT '年月', 
      year_week_code string COMMENT '一年中第几周', 
      year_week_name string COMMENT '一年中第几周名称', 
      year_week_code_cn string COMMENT '一年中第几周（中国）', 
      year_week_name_cn string COMMENT '一年中第几周名称（中国',
      week_day_code string COMMENT '周几code', 
      week_day_name string COMMENT '周几名称', 
      day_week string COMMENT '周', 
      day_week_cn string COMMENT '周(中国)',
      day_week_num string COMMENT '一周第几天', 
      day_week_num_cn string COMMENT '一周第几天（中国）', 
      day_month_num string COMMENT '一月第几天', 
      day_year_num string COMMENT '一年第几天', 
      date_id_wow string COMMENT '与本周环比的上周日期', 
      date_id_mom string COMMENT '与本月环比的上月日期', 
      date_id_wyw string COMMENT '与本周同比的上年日期', 
      date_id_mym string COMMENT '与本月同比的上年日期', 
      first_date_id_month string COMMENT '本月第一天日期', 
      last_date_id_month string COMMENT '本月最后一天日期',
      half_year_code string COMMENT '半年code', 
      half_year_name string COMMENT '半年名称', 
      season_code string COMMENT '季节编码', 
      season_name string COMMENT '季节名称', 
      is_weekend string COMMENT '是否周末（周六和周日）', 
      official_holiday_code string COMMENT '法定节假日编码', 
      official_holiday_name string COMMENT '法定节假日', 
      festival_code string COMMENT '节日编码', 
      festival_name string COMMENT '节日', 
      custom_festival_code string COMMENT '自定义节日编码', 
      custom_festival_name string COMMENT '自定义节日', 
      update_time string COMMENT '更新时间' 
  )
  COMMENT '时间维度表' 
  row format delimited fields terminated by '\t' 
  stored as orc tblproperties ('orc.compress' = 'ZLIB');
  "
  
  echo '----------HIVE EXE END  SUCCESS-----------------'
  
  
  # 4- SQOOP IMPORT
  
  SQOOP_HOME=/usr/bin/sqoop
  
  
  echo '----------SQOOP IMPORT START-----------------'
  
  # PUBLIC PATH
  URL='jdbc:mysql://192.168.88.80:3306/yipin'
  USERNAME='root'
  PASSWORD='123456'
  
  
  ${SQOOP_HOME} import \
  --connect ${URL} \
  --username ${USERNAME} \
  --password ${PASSWORD} \
  --query "SELECT  * FROM t_date where 1=1 and \$CONDITIONS" \
  --hcatalog-database yp_ods \
  --hcatalog-table t_date \
  -m 1
  
  wait
  
  ${SQOOP_HOME} import \
  --connect ${URL} \
  --username ${USERNAME} \
  --password ${PASSWORD} \
  --query "SELECT *, '${dateStr}' as dt  FROM  t_goods_evaluation WHERE create_time BETWEEN '${dateStr} 00:00:00' AND '${dateStr} 23:59:59'  and \$CONDITIONS" \
  --hcatalog-database yp_ods \
  --hcatalog-table t_goods_evaluation \
  -m 1
  
  
  wait
  
  ${SQOOP_HOME} import \
  --connect ${URL} \
  --username ${USERNAME} \
  --password ${PASSWORD} \
  --query "SELECT  *,'${dateStr}' as dt FROM t_store where create_time BETWEEN '${dateStr} 00:00:00' AND '${dateStr} 23:59:59' OR update_time BETWEEN '${dateStr} 00:00:00' and '${dateStr} 23:59:59' and \$CONDITIONS" \
  --hcatalog-database yp_ods \
  --hcatalog-table t_store \
  -m 1
  
  
  
  echo '----------SQOOP IMPORT END SUCCESS----------------'
  ```

执行脚本, 观察是否可以执行成功呢? 

```properties
select  * from yp_ods.t_date where dim_date_id = '20320101';
select  * from yp_ods.t_store where  dt = '2022-05-04';

可以查看对应分区下, 相关的数据是否有没有生成
```

后续可以将这个脚本配置在oozie中, 进行定时运行即可





说明:

```properties
删除分区的命令: 
	alter table 表名 drop partition(分区字段=值);
```



## 2- DWD层

DWD层作用: 

```
	DWD层 和 ODS层 保持相同粒度, 从ODS层将数据抽取出来,  对数据进行清洗 转换 以及拉链等相关工作
```



### 2.1 构建DWD层表

* 1- 构建全量覆盖表: 日期表

```properties
-- 日期表:   t_date
drop table yp_dwd.dim_date; 
CREATE TABLE yp_dwd.dim_date ( 
    dim_date_id string COMMENT '日期', 
    date_code string COMMENT '日期编码', 
    lunar_calendar string COMMENT '农历', 
    year_code string COMMENT '年code', 
    year_name string COMMENT '年名称', 
    month_code string COMMENT '月份编码', 
    month_name string COMMENT '月份名称', 
    quanter_code string COMMENT '季度编码', 
    quanter_name string COMMENT '季度名称', 
    year_month string COMMENT '年月', 
    year_week_code string COMMENT '一年中第几周', 
    year_week_name string COMMENT '一年中第几周名称', 
    year_week_code_cn string COMMENT '一年中第几周（中国）', 
    year_week_name_cn string COMMENT '一年中第几周名称（中国',
    week_day_code string COMMENT '周几code', 
    week_day_name string COMMENT '周几名称', 
    day_week string COMMENT '周', 
    day_week_cn string COMMENT '周(中国)',
    day_week_num string COMMENT '一周第几天', 
    day_week_num_cn string COMMENT '一周第几天（中国）', 
    day_month_num string COMMENT '一月第几天', 
    day_year_num string COMMENT '一年第几天', 
    date_id_wow string COMMENT '与本周环比的上周日期', 
    date_id_mom string COMMENT '与本月环比的上月日期', 
    date_id_wyw string COMMENT '与本周同比的上年日期', 
    date_id_mym string COMMENT '与本月同比的上年日期', 
    first_date_id_month string COMMENT '本月第一天日期', 
    last_date_id_month string COMMENT '本月最后一天日期',
    half_year_code string COMMENT '半年code', 
    half_year_name string COMMENT '半年名称', 
    season_code string COMMENT '季节编码', 
    season_name string COMMENT '季节名称', 
    is_weekend string COMMENT '是否周末（周六和周日）', 
    official_holiday_code string COMMENT '法定节假日编码', 
    official_holiday_name string COMMENT '法定节假日', 
    festival_code string COMMENT '节日编码', 
    festival_name string COMMENT '节日', 
    custom_festival_code string COMMENT '自定义节日编码', 
    custom_festival_name string COMMENT '自定义节日', 
    update_time string COMMENT '更新时间' 
)
COMMENT '时间维度表' 
row format delimited fields terminated by '\t' 
stored as orc tblproperties ('orc.compress' = 'SNAPPY');
```

* 2- 仅新增同步的表:  订单评价表

```sql
-- 订单评价表 : t_goods_evaluation
DROP TABLE if exists yp_dwd.fact_goods_evaluation;
CREATE TABLE yp_dwd.fact_goods_evaluation ( 
	`id` string, 
	`user_id` string COMMENT '评论人id', 
	`store_id` string COMMENT '店铺id', 
	`order_id` string COMMENT '订单id', 
	`geval_scores` INT COMMENT '综合评分', 
	`geval_scores_speed` INT COMMENT '送货速度评分0-5分(配送评分)', 
	`geval_scores_service` INT COMMENT '服务评分0-5分', 
	`geval_isanony` TINYINT COMMENT '0-匿名评价，1-非匿名', 
	`create_user` string, 
	`create_time` string, 
	`update_user` string, 
	`update_time` string, 
	`is_valid` TINYINT COMMENT '0 ：失效，1 ：开启'
)
comment '商品评价表' 
partitioned by (dt string) 
row format delimited fields terminated by '\t' stored as orc tblproperties ('orc.compress'='SNAPPY');
```

* 3- 新增及更新的表: 需要构建为拉链表(用于后续维护历史变化)

```sql
DROP TABLE if exists yp_dwd.dim_store; 
CREATE TABLE yp_dwd.dim_store ( 
	`id` string COMMENT '主键', 
	`user_id` string, 
	`store_avatar` string COMMENT '店铺头像', 
	`address_info` string COMMENT '店铺详细地址', 
	`name` string COMMENT '店铺名称', 
	`store_phone` string COMMENT '联系电话', 
	`province_id` INT COMMENT '店铺所在省份ID', 
	`city_id` INT COMMENT '店铺所在城市ID', 
	`area_id` INT COMMENT '店铺所在县ID', 
	`mb_title_img` string COMMENT '手机店铺 页头背景图',
	`store_description` string COMMENT '店铺描述', 
	`notice` string COMMENT '店铺公告', 
	`is_pay_bond` TINYINT COMMENT '是否有交过保证金 1：是0：否', 
	`trade_area_id` string COMMENT '归属商圈ID', 
	`delivery_method` TINYINT COMMENT '配送方式 1 ：自提 ；3 ：自提加配送均可; 2 : 商家配送', 
	`origin_price` DECIMAL, 
	`free_price` DECIMAL, 
	`store_type` INT COMMENT '店铺类型 22天街网店 23实体店 24直营店铺 33会员专区店', 
	`store_label` string COMMENT '店铺logo', 
	`search_key` string COMMENT '店铺搜索关键字', 
	`end_time` string COMMENT '营业结束时间', 
	`start_time` string COMMENT '营业开始时间', 
	`operating_status` TINYINT COMMENT '营业状态 0 ：未营业 ；1 ：正在营业', 
	`create_user` string, 
	`create_time` string, 
	`update_user` string, 
	`update_time` string, 
	`is_valid` TINYINT COMMENT '0关闭，1开启，3店铺申请中', 
	`state` string COMMENT '可使用的支付类型:MONEY金钱支付;CASHCOUPON现金券支付', 
	`idCard` string COMMENT '身份证', 
	`deposit_amount` DECIMAL(11,2) COMMENT '商圈认购费用总额', 
	`delivery_config_id` string COMMENT '配送配置表关联ID', 
	`aip_user_id` string COMMENT '通联支付标识ID', 
	`search_name` string COMMENT '模糊搜索名称字段:名称_+真实名称', 
	`automatic_order` TINYINT COMMENT '是否开启自动接单功能 1：是 0 ：否', 
	`is_primary` TINYINT COMMENT '是否是总店 1: 是 2: 不是',
	`parent_store_id` string COMMENT '父级店铺的id，只有当is_primary类型为2时有效',
    `end_date` string COMMENT '结束日期'
)
comment '店铺表' 
partitioned by (start_date string) 
row format delimited fields terminated by '\t' 
stored as orc tblproperties ('orc.compress'='SNAPPY');
```

### 2.2 全量导入数据到DWD层

* 1- 全量覆盖同步方式的表: 日期表

```sql
-- HIVE压缩配置
set hive.exec.compress.intermediate=true; 
set hive.exec.compress.output=true;
--写入时压缩生效 
set hive.exec.orc.compression.strategy=COMPRESSION;

insert overwrite table yp_dwd.dim_date
select * from yp_ods.t_date;
```

* 2- 仅新增同步表: 订单评价表

```sql
-- 动态分区的设置
SET hive.exec.dynamic.partition=true; 
SET hive.exec.dynamic.partition.mode=nonstrict; 
set hive.exec.max.dynamic.partitions.pernode=10000; 
set hive.exec.max.dynamic.partitions=100000; 
set hive.exec.max.created.files=150000;
-- HIVE压缩配置
set hive.exec.compress.intermediate=true; 
set hive.exec.compress.output=true;
--写入时压缩生效 
set hive.exec.orc.compression.strategy=COMPRESSION;


insert overwrite table yp_dwd.fact_goods_evaluation partition(dt)
select   *  from yp_ods.t_goods_evaluation; 
```

* 3- 新增及更新同步表: 店铺表

```sql
-- 动态分区的设置
SET hive.exec.dynamic.partition=true; 
SET hive.exec.dynamic.partition.mode=nonstrict; 
set hive.exec.max.dynamic.partitions.pernode=10000; 
set hive.exec.max.dynamic.partitions=100000; 
set hive.exec.max.created.files=150000;
-- HIVE压缩配置
set hive.exec.compress.intermediate=true; 
set hive.exec.compress.output=true;
-- 写入时压缩生效 
set hive.exec.orc.compression.strategy=COMPRESSION;


insert overwrite table yp_dwd.dim_store partition(start_date)
select     
id,
user_id,
store_avatar,
address_info,
name,
store_phone,
province_id,
city_id,
area_id ,
mb_title_img,
store_description,
notice,
is_pay_bond,
trade_area_id,
delivery_method,
origin_price,
free_price ,
store_type,
store_label,
search_key,
end_time,
start_time,
operating_status ,
create_user,
create_time,
update_user,
update_time,
is_valid,
state,
idcard ,
deposit_amount,
delivery_config_id,
aip_user_id,
search_name,
automatic_order ,
is_primary,
parent_store_id ,
'9999-99-99' as  end_date,
dt  as start_date

from yp_ods.t_store; 
```



### 2.3 增量导入数据到DWD层

* 1- 全量覆盖的同步表: 日期表

```sql
-- HIVE压缩配置
set hive.exec.compress.intermediate=true; 
set hive.exec.compress.output=true;
--写入时压缩生效 
set hive.exec.orc.compression.strategy=COMPRESSION;

insert overwrite table yp_dwd.dim_date
select * from yp_ods.t_date;
```

* 2-  仅新增同步的表: 订单评价表

```sql
-- 动态分区的设置
SET hive.exec.dynamic.partition=true; 
SET hive.exec.dynamic.partition.mode=nonstrict; 
set hive.exec.max.dynamic.partitions.pernode=10000; 
set hive.exec.max.dynamic.partitions=100000; 
set hive.exec.max.created.files=150000;
-- HIVE压缩配置
set hive.exec.compress.intermediate=true; 
set hive.exec.compress.output=true;
--写入时压缩生效 
set hive.exec.orc.compression.strategy=COMPRESSION;


insert overwrite table yp_dwd.fact_goods_evaluation partition(dt)
select   *  from yp_ods.t_goods_evaluation where dt = '2022-05-04';


注意: 当覆盖写入到一个分区表的时候, 只会覆盖掉对应分区的数据, 其他分区是不受影响的
```



变更为脚本: 

```shell
#!/bin/bash

# 1- HIVE ENV PATH
HIVE_HOME=/usr/bin/hive

# 2- TRAN
if [ $# == 1 ]
then
   dateStr=$1
else
   dateStr=`date -d '-1 day' +'%Y-%m-%d'`
fi

echo ${dateStr}
# 3- EXE HIVE SQL

echo '----------EXE HIVE SQL START----------------'

${HIVE_HOME} -S -e "

SET hive.exec.dynamic.partition=true; 
SET hive.exec.dynamic.partition.mode=nonstrict; 
set hive.exec.max.dynamic.partitions.pernode=10000; 
set hive.exec.max.dynamic.partitions=100000; 
set hive.exec.max.created.files=150000;
set hive.exec.compress.intermediate=true; 
set hive.exec.compress.output=true;
set hive.exec.orc.compression.strategy=COMPRESSION;

insert overwrite table yp_dwd.dim_date
select * from yp_ods.t_date;

insert overwrite table yp_dwd.fact_goods_evaluation partition(dt)
select  * from yp_ods.t_goods_evaluation where dt = '${dateStr}';

"
echo '----------EXE HIVE SQL END  SUCCESS----------------'

```



后续将脚本配置在OOZIE中, 进行定时调度即可











