# day05_保险项目课程笔记

今日内容:

* 1- 扩展知识点: 
* 2- 计算保费参数因子





## 1- 扩展知识点

### 1.1 如何进行横向迭代计算

需求: 已知 c1列数据, 计算出 c2 和 c3列数据

| c1   | c2 = c1+2 | c3=c1*(c2+3) |
| ---- | :-------: | ------------ |
| 1    |           |              |
| 2    |           |              |
| 3    |           |              |

```properties
-- 需求: 已知 c1列数据, 计算出 c2 和 c3列数据
-- 规则:  c1列为 1,2,3  c2=c1+2  c3=c1*(c2+3)
-- 初始化数据:
create or replace  temporary  view t1 (c1) as
select stack(3,1,2,3);
-- 计算 c2
select
    c1,
    c1 + 2 as c2
from t1;

-- 计算 c3:  c1*(c2+3) 需要基于上一个结果来计算下一个结果
-- 子查询:
select
    c1,
    c2,
    c1 * (c2 + 3) as c3
from (select
    c1,
    c1 + 2 as c2
from t1) t2;

-- with as
with t2 as (
    select
        c1,
        c1 + 2 as c2
    from t1
)
select
    c1,
    c2,
    c1 * (c2 + 3) as c3
from t2;

-- 视图(临时视图 和 永久视图) 
-- 表


推荐使用: with as  和 视图的方式
```



### 1.2 如何进行纵向迭代计算

需求:  计算 c4:

​		计算逻辑:  当c2=1 , 则 c4=1 ; 否则 c4 = (上一个c4 +  当前的c3)/2

| c1   | c2   | c3   | c4   |
| ---- | ---- | ---- | ---- |
| 1    | 1    | 6    | 1    |
| 1    | 2    | 23   |      |
| 1    | 3    | 8    |      |
| 1    | 4    | 4    |      |
| 1    | 5    | 10   |      |
| 2    | 1    | 23   | 1    |
| 2    | 2    | 14   |      |
| 2    | 3    | 17   |      |
| 2    | 4    | 20   |      |

代码实现:

```properties
-- 如何进行纵向迭代计算操作
-- 需求:  计算 c4:
--    计算逻辑:  当c2=1 , 则 c4=1 ; 否则 c4 = (上一个c4 +  当前的c3) / 2

-- 初始化数据集:
create or replace  temporary view t1 (c1,c2,c3,c4) as
    values (1,1,6,1),
           (1,2,23,NULL),
           (1,3,8,NULL),
           (1,4,4,NULL),
           (1,5,10,NULL),
           (2,1,23,1),
           (2,2,14,NULL),
           (2,3,17,NULL),
           (2,4,20,NULL);

select * from t1;

-- 计算下一行:
select
    c1,
    c2,
    c3,
    if(
        c2 = 1,
        1,
        (lag(c4,1) over(partition by c1 order by c2) + c3) / 2
    ) as  c4
from t1;

-- 基于上一个结果, 计算下一行
with t2 as (
    select
        c1,
        c2,
        c3,
        if(
            c2 = 1,
            1,
            (lag(c4,1) over(partition by c1 order by c2) + c3) / 2
        ) as  c4
    from t1
)
select
    c1,
    c2,
    c3,
    if(
        c2 = 1,
        1,
        (lag(c4,1) over(partition by c1 order by c2) + c3) / 2
    ) as  c4
from  t2;

-- 基于上一个结果, 计算下一行
with t2 as (
    select
        c1,
        c2,
        c3,
        if(
            c2 = 1,
            1,
            (lag(c4,1) over(partition by c1 order by c2) + c3) / 2
        ) as  c4
    from t1
),
t3 as (
    select c1,
           c2,
           c3,
           if(
               c2 = 1,
               1,
               (lag(c4, 1) over (partition by c1 order by c2) + c3) / 2
           ) as c4
    from t2
)
select c1,
       c2,
       c3,
       if(
           c2 = 1,
           1,
           (lag(c4, 1) over (partition by c1 order by c2) + c3) / 2
       ) as c4
from t3;

-- 基于上一个结果, 计算下一行
with t2 as (
    select
        c1,
        c2,
        c3,
        if(
            c2 = 1,
            1,
            (lag(c4,1) over(partition by c1 order by c2) + c3) / 2
        ) as  c4
    from t1
),
t3 as (
    select c1,
           c2,
           c3,
           if(
               c2 = 1,
               1,
               (lag(c4, 1) over (partition by c1 order by c2) + c3) / 2
           ) as c4
    from t2
),
t4 as (
    select
       c1,
       c2,
       c3,
       if(
           c2 = 1,
           1,
           (lag(c4, 1) over (partition by c1 order by c2) + c3) / 2
       ) as c4
from t3
)
select
   c1,
   c2,
   c3,
   if(
       c2 = 1,
       1,
       (lag(c4, 1) over (partition by c1 order by c2) + c3) / 2
   ) as c4
from t4;

```

​		发现, 通过不断的一条SQL 一条SQL的进行迭代计算, 每一次只能算出来一个值. 但是如何说我们一个组内有几万行数据, 那么这种操作, 是不非常的不合适.... 甚至我们有时候根本就不知道一个组内有多少行数据



​		思考: 如何解决呢?  目前并没有一个函数能够解决这个问题的, 需要自定义UDAF函数, 后续我们可以使用 UDAF函数 和 窗口函数结合, 一次性完成整个计算操作

```properties
import pandas as pd
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os

# 锁定远端操作环境, 避免存在多个版本环境的问题
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ["PYSPARK_PYTHON"] = "/root/anaconda3/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/root/anaconda3/bin/python"

# 快捷键:  main 回车
if __name__ == '__main__':
    print("纵向迭代计算操作演示")

    # 1- 创建SparkSession核心对象
    spark = SparkSession.builder.appName('demo01').master('local[*]').getOrCreate()

    # 2- 初始化数据
    spark.sql("""
        create or replace  temporary view t1 (c1,c2,c3,c4) as
            values (1,1,6,1),
                   (1,2,23,NULL),
                   (1,3,8,NULL),
                   (1,4,4,NULL),
                   (1,5,10,NULL),
                   (2,1,23,1),
                   (2,2,14,NULL),
                   (2,3,17,NULL),
                   (2,4,20,NULL);
    """)
    @F.pandas_udf(returnType='float')
    def udaf_fun(c3:pd.Series,c4:pd.Series) -> float:
        tmp = 0  # 1 -> 12 --> 10  --> 7
        for i in range(0,len(c3)):
            if i == 0:
                tmp = c4[i]
            else:
                tmp = (tmp + c3[i]) / 2
        return tmp


    spark.udf.register('udaf_fun',udaf_fun) # 支持在SQL中使用

    spark.sql("""
        select  
            c1,
            c2,
            c3,
            udaf_fun(c3,c4) over(partition by c1 order by c2) as c4
        from t1
    """).show()
```





## 2- 计算保费参数因子

### 2.1 需求说明

* 需求一:  根据性别, 投保年龄, 缴费期以及保单年度来统计其中23个保费参数因子指标
  * 此需求最终结果, 共计有19338条数据

![image-20220623213601387](day05_保险项目课程笔记.assets/image-20220623213601387.png)

计算逻辑: 

* 1- 形成维度表(10个维度字段)的数据: 19338条

```properties
	除了性别, 投保年龄, 缴费期 以及保单年度需要生成后, 可以认为 通过这四个, 就可以确定唯一的一条数据
	
	其他的维度字段, 要不就是固定的值, 要不就可以使用其他的字段计算而出的
	
	后期关注点:  性别  投保年龄  缴费期  保单年度
		性别: 男 女
		缴费期: 10 15 20 30
		投保年龄:   18~60岁
		保单年度: 投保第一年, 就是第一个保单年度, 第二年就是第二个保单年度, 依次类推, 直到计算到106岁截止
			比如: 
				以 18岁投保, 保证终身(106岁), 意味着共计会有 106-18 = 88 个保单年度
```

* 2- 统计23个指标, 基于横向迭代计算操作

```properties
	对于指标计算来说, 需要解析每个指标字段的计算规则
	
	以其中一个指标为例,, 讲解其整个解析过程: 死亡率
		计算规则:  =IF(J13<=105,VLOOKUP(J13,MORT_10_13,IF(Sex="M",2,3)),0)*MortRatio_Prem_0*(I13<=BPP)
		
		说明: 
			A * MortRatio_Prem_0 * C
			
			MortRatio_Prem_0 :IF(Sex="M",1,1)  = 1
			       |
			       |
			A *  1 * C
			
			解析C: (I13<=BPP) 保单年度 <= 保障期间
				发现保单年度 一定是小于等于 保障期间, 也就说这个条件一定也是成立的,  True --> 1
				   |
				   |
			A * 1 * 1
			
			解析 A: IF(J13<=105,VLOOKUP(J13,MORT_10_13,IF(Sex="M",2,3)),0)
				当用户年龄小于等于105岁的时候: 
					执行: VLOOKUP(J13,MORT_10_13,IF(Sex="M",2,3))
						根据用户年龄 与 生命表进行匹配, 匹配后, 如果是男性返回生命表第二列数据, 否则返回生命表第三列数据
				否则: 0
				
	
	当前我们是带着大家分析了其中一个指标的计算流程方案, 实际生产中, 剩下的22个指标, 我们都需要大家一个个进行分析, 找到那些指标需要先计算, 那些指标需要后计算, 那些指标可以一起计算, 最终形成一份计算流程图表
	
	对于当前学习环境, 不需要大家直接对接Excel进行分析了, 因为这个工作实在有点太费时间了, 本次直接将所有的指标计算流程, 全部提供给大家,  我们可以直接根据计算流程图完成统计计算操作即可, 但是建议大家在计算的过程中, 可以根据计算流程图, 和Excel对应计算规则, 来理解Excel相关规则信息(反推)
```

