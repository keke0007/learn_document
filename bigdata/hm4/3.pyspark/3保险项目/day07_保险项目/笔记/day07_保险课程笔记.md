# day07_保险项目课程笔记

今日内容:

* 现金价值需求分析和流程计算



## 1. 保险现金价值和准备金

### 1.1 什么是现金价值

* 1- 保单是一种带有储蓄性质的
* 2- 保险人为履行合同责任通常提存责任准备金，当被保险人中途退保或者解约的时候, 保险公司需要退还用户一部分保费(这部分保费其实就是现金价值)
* 3- 可以根据保单现金价值, 进行保单贷款, 一般是可以贷到保单现金价值的70%

### 1.2 什么是准备金

​		保险准备金(reserve)是指保险人为保证其如约履行保险**赔偿**或**给付**义务，根据政府有关法律规定或业务特定需要，从保费收入或盈余中提取的与其所承担的保险责任相对应的一定数量的基金

​		准备金用来作为未来赔付的保证。准备金是衡量保险公司偿付能力的重要指标，偿付能力越强，保险公司信用评级越高。



​		从保险公司角度来说, 不管是现金价值, 还是保险准备金, 都是准备金, 都是不能动的钱,都可以认为是保险公司负债



## 2. 现金价值相关计算

需求三:  根据投保年龄, 性别, 缴费期 以及保单年度来计算现金价值(共计: 19338),涉及的指标共计有37个指标

```properties
需求分析: 
	1- 通过测试模板. 可以看到, 整个现金价值结果表共计有47个字段(10个维度字段 + 37个指标字段)
	2- 其中10个维度字段, 除了利率维度以外, 其他的维度与保费参数因子表维度信息完全一致, 后期可以直接从保费参数因子表中提取即可
	3- 在现金价值表中, 当保单年度为0的时候, 是有意义, 所以需要在现金价值结果表, 将保单年度为0的数据也要生成, 此数据共计274条, 所以最终结果表数据量: 19338 + 274 = 19612条
	4- 剩余的37个指标字段中, 有一部分字段是可以直接从保费参数因子表中直接读取: 15个字段  
			qx,qx,qx_d,qx_ci,dx_d,dx_ci,lx,lx_d
			ppp_,bpp_, expense, db1,db2_factor
			db3,db4
		
	   需要我们手动计算的:  22个字段
	   		cx ,cx_,ci_cx,ci_cx_,dx,dx_d_
	   		db2,db5
	   		np_,pvnp,pvdb1,pvdb3,pvdb3,pvdb4,pcdb5
	   		pvr,rt,np,sur_ben,cv_1a,cv_1b,cv_2
	   

操作步骤:  
	1- 首先在DW层构建现金价值结果表
	2- 读取保费参数因子表 从当中将不需要生成的维度数据以及不需要在重新计算的指标字段数据全部都提取出来
	3- 基于提取后的结果信息基础上, 在此基础上进行横向迭代计算, 计算出剩余的相关的指标
	4- 将整个计算结果保存到现金价值结果表
```



### 2.1 构建现金价值结果表

```sql
-- 保费现金价值结果表:
drop table if exists insurance_dw.cv_src ;
create table if not exists insurance_dw.cv_src(
    age_buy       smallint comment '投保年龄',
    nursing_age   smallint comment '长期护理保险金给付期满年龄',
    sex           string comment '性别',
    t_age         smallint comment '满期年龄(Terminate Age)',
    ppp           smallint comment '交费期间(Premuim Payment Period PPP)',
    bpp           smallint comment '保险期间(BPP)',
    interest_rate_cv decimal(6, 4) comment '现金价值预定利息率（Interest Rate CV）',
    sa            decimal(12, 2) comment '基本保险金额(Baisc Sum Assured)',
    policy_year   smallint comment '保单年度',
    age           smallint comment '保单年度对应的年龄',
    qx            decimal(8, 7) comment '死亡率',
    kx            decimal(8, 7) comment '残疾死亡占死亡的比例',
    qx_d          decimal(8, 7) comment '扣除残疾的死亡率',
    qx_ci         decimal(8, 7) comment '残疾率',
    dx_d          decimal(8, 7) comment '',
    dx_ci         decimal(8, 7) comment '',
    lx            decimal(8, 7) comment '有效保单数',
    lx_d          decimal(8, 7) comment '健康人数',
    cx            decimal(8, 7) comment '当期发生该事件的概率，如下指的是死亡发生概率',
    cx_           decimal(8, 7) comment '对Cx做调整，不精确的话，可以不做',
    ci_cx         decimal(8, 7) comment '当期发生重疾的概率',
    ci_cx_        decimal(8, 7) comment '当期发生重疾的概率，调整',
    dx            decimal(8, 7) comment '有效保单生存因子',
    dx_d_         decimal(8, 7) comment '健康人数生存因子',
    ppp_          smallint comment '是否在缴费期间，1-是，0-否',
    bpp_          smallint comment '是否在保险期间，1-是，0-否',
    expense       decimal(8, 7) comment '附加费用率',
    db1           decimal(12, 2) comment '残疾给付',
    db2_factor    decimal(8, 7) comment '长期护理保险金给付因子',
    db2           decimal(12, 2) comment '长期护理保险金',
    db3           decimal(12, 2) comment '养老关爱金',
    db4           decimal(12, 2) comment '身故给付保险金',
    db5           decimal(12, 2) comment '豁免保费因子',
    np_         DECIMAL(12, 2) comment '净保费',
    pvnp        DECIMAL(17, 7) comment '净保费现值',
    pvdb1       DECIMAL(17, 7) comment '',
    pvdb2       DECIMAL(17, 7) comment '',
    pvdb3       DECIMAL(17, 7) comment '',
    pvdb4       DECIMAL(17, 7) comment '',
    pvdb5       DECIMAL(17, 7) comment '',
    pvr         DECIMAL(17, 7) comment '保单价值准备金',
    rt          DECIMAL(6, 3) comment '',
    np          DECIMAL(17, 7) comment '修匀净保费',
    sur_ben     DECIMAL(17, 7) comment '生存金',
    cv_1a       DECIMAL(17, 7) comment '现金价值年末（生存给付前）',
    cv_1b       DECIMAL(17, 7) comment '现金价值年末（生存给付后）',
    cv_2        DECIMAL(17, 7) comment '现金价值年中'
)comment '现金价值表（到每个保单年度）'
row format delimited fields terminated by ',';
```

注意: 建表操作, 需要放置在 _02_insurance_create_dw.sql 脚本文件中

### 2.2 步骤13~16

完整的SQL语句:

```sql
-- 此脚本用于计算保单的现金价值
-- 开启禁止精度丢失(精度保护)
set spark.sql.decimalOperations.allowPrecisionLoss=false;
-- 开启 shuffle分区数量为 4个 (默认为: 200)
set spark.sql.shuffle.partitions=4;

-- 步骤13: 首先从保费参数因子表将不需要生成维度和不需要计算的指标字段提取出来 并计算 cx
create or replace  view  insurance_dw.cv_src16 as
with cv_src13  as(
    select
        t1.sa,
        t1.bpp,
        t1.sex,
        input.interest_rate_cv,
        t1.age_buy,
        t1.nursing_age,
        t1.t_age,
        t1.ppp,
        t1.policy_year,
        t1.age,
        t1.qx,
        t1.kx,
        t1.qx_d,
        t1.qx_ci,
        t1.dx_d,
        t1.dx_ci,
        t1.lx,
        t1.lx_d,
        t1.ppp_,
        t1.bpp_,
        t1.expense,
        t1.db1,
        t1.db2_factor,
        t1.db3,
        t1.db4,
        cast(
            t1.dx_d / pow((1+input.interest_rate_cv),(t1.age +1))
        as decimal(17,12))  as cx
    from insurance_dw.prem_src10 t1
        join insurance_dw.input
    union all
    select distinct
        t1.sa,
        t1.bpp,
        t1.sex,
        input.interest_rate_cv,
        t1.age_buy,
        t1.nursing_age,
        t1.t_age,
        t1.ppp,
        0 as policy_year,
        null as age,
        null as qx,
        null as kx,
        null as qx_d,
        null as qx_ci,
        null as dx_d,
        null as dx_ci,
        null as lx,
        null as lx_d,
        null as ppp_,
        null as bpp_,
        null as expense,
        null as db1,
        null as db2_factor,
        null as db3,
        null as db4,
        null as cx
    from insurance_dw.prem_src10 t1
        join insurance_dw.input
),
cv_src14 as (
    select
        *,
        cast(cx * pow((1 + interest_rate_cv),0.5) as decimal(17,12)) as cx_,
        cast(
            dx_ci / pow((1 + interest_rate_cv),(age + 1))
        as decimal(17,12)) as  ci_cx
    from cv_src13
),
cv_src15 as (
    select
        *,
        cast(
            ci_cx * pow((1+interest_rate_cv),0.5)
        as decimal(17,12)) as  ci_cx_,

        cast(
            lx / pow((1+interest_rate_cv),age)
        as decimal(17,12)) as  dx,

        cast(
            lx_d / pow((1+interest_rate_cv),age)
        as decimal(17,12)) as  dx_d_
    from cv_src14
)
select
    *,
    cast(
        sum(dx * db2_factor) over (partition by sex,ppp,age_buy order by policy_year rows between current row  and unbounded following)
            /
        dx
    as decimal(17,12)) as  db2,

    cast(
        (
            ifnull(sum(dx * ppp_) over (partition by sex,ppp,age_buy order by policy_year rows between 1 following  and unbounded following),0)
                /
            dx
        ) * pow((1+interest_rate_cv),0.5)
    as decimal(17,12)) as  db5
from  cv_src15;

-- 校验:步骤 13 ~ 16
select
    *
from insurance_dw.cv_src16 where sex = 'F' and age_buy=20 and ppp=20 order by policy_year;



```

### 2.6 步骤 17~18

```properties
-- 步骤 17
create or replace  view insurance_dw.cv_src18 as
with cv_src17  as (
    select
        age_buy,
        sex,
        ppp,
        cast (
            sum(
                if(
                    policy_year = 1,
                    0.5 * ci_cx_ * db1 * pow((1+interest_rate_cv),-0.25),
                    ci_cx_ * db1
                )
            )
        as decimal(17,12)) as  t11,

        cast(
            sum(
                if(
                    policy_year = 1,
                    0.5 * ci_cx_ * db2 * pow((1+interest_rate_cv),-0.25),
                    ci_cx_ * db2
                )
            )
        as decimal(17,12)) AS  v11,

        cast(sum(dx * db3) as decimal(17,12)) as  w11,
        cast(sum(dx * ppp_) as decimal(17,12)) as q11,

        cast(
            sum(
                if(
                    policy_year = 1,
                    0.5 * ci_cx_ * pow((1+interest_rate_cv),0.25),
                    0
                )
            )
        as decimal(17,12)) as t9,

        cast(
            sum(
                if(
                    policy_year = 1,
                    0.5 * ci_cx_ * pow((1+interest_rate_cv),0.25),
                    0
                )
            )
        as decimal(17,12))  as v9,

        cast(sum(dx * expense) as decimal(17,12)) as s11,
        cast(sum(cx_ * db4) as decimal(17,12)) as x11,
        cast(sum(ci_cx_ * db5) as decimal(17,12)) as y11

    from insurance_dw.cv_src16
    group by  ppp,sex,age_buy
)
select
    t1.age_buy,
    t1.sex,
    t1.ppp,
    (input.sa * (t1.t11 + t1.v11 + t1.w11) + t2.prem * (t1.t9 + t1.v9 +t1.x11 + t1.y11))
            /
    (t1.q11 - t1.s11)  as prem_cv
from cv_src17 t1
    join insurance_dw.input  on 1 =1
    join insurance_dw.prem_std12 t2 on t1.age_buy =  t2.age_buy and t1.sex = t2.sex and t1.ppp = t2.ppp



-- 校验: 步骤 17~18
select
    *
from insurance_dw.cv_src18 where sex = 'M' and age_buy=24 and ppp=20 ;
```



总结:

```properties
1- 当我们在计算的过程中, 发现计算后结果与实际结果偏差比较大,  一般不是由于精度偏差导致的
	解决方案: 
		1.1 判断当前这个对应指标计算的逻辑是否正常(不要过于相信自己, 仔细检查小的点, 比如字段问题, 括号这些问题
		1.2 如果当前步骤可以确定是正确的, 判断当前这个逻辑中是否用到了其他的指标字段, 判断是否是其他指标出现计算错误而导致的
				这个错误, 需要不断的往深处去找 直到找到计算错误的初始点, 然后解决掉

2- 当发现精度偏差不是特别大的时候, 此时可以优先尝试重新开启一下精度保护, 重新全部执行测算一次

3- 如果发现依然无法解决问题, 此时尝试将所有的保留小数位扩大, 以保证更好的精度

4- 如果精度是符合范围内, 可以暂时不关心, 继续往下核算即可, 除非偏差越来越大
```



### 2.7 构建准备金毛保费结果表

* 1- 建表操作:  _02_insurance_create_dw.sql

```sql
-- 保单价值准备金毛保险费表
drop table if exists insurance_dw.prem_cv;
create table if not exists insurance_dw.prem_cv (
    age_buy smallint comment '年投保龄',
    sex     string comment '性别',
    ppp     smallint comment '缴费期间',
    prem_cv      decimal(15, 7) comment '保单价值准备金毛保险费(Preuim)'
)comment '保单价值准备金毛保险费表'
row format delimited fields terminated by '\t';
```

* 2- 将结果数据灌入到目标表

```sql
-- 将 保费价值准备金毛保费数据导入到结果表中
insert overwrite  table insurance_dw.prem_cv
select
    age_buy,
    sex,
    ppp,
    prem_cv
from insurance_dw.cv_src18;

-- 校验毛保费结果表:
select
    *
from insurance_dw.prem_cv where sex = 'M' and age_buy=24 and ppp=20 ;
```

