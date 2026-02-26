## MapReduce的概述

### 分布式计算引擎的发展

+ 第一代分布式计算疫情:  MapReduce （Storm）
+ 第二代分布式计算引擎：Tez
+ 第三代分布式计算引擎：Spark
+ 第四代分布式计算引擎：Flink



### 什么是分布式计算

将一个大的计算任务进行拆分，分别去计算，最后再将这些小任务的结果进行合并

### MapReduce的思想

+ MapReduce分成两个大阶段,分别是Map阶段（分）和Reduce阶段（合）
+ MapReduce划分的小任务之间不能有依赖关系
+ MapReduce整个的处理过程采用的键值对模型：(K1,V1),(K2,V2),(K2,[V2]),(K3,V3)
+ MapRduce框架大部分大代码都开发完了，我们只需要填充一些指定的代码即可
+ MapReduce只是一段API代码，它的运行所需要的内存、cpu都是由Yarn来分配
+ MapReduce的API并没有使用Java的类型，而是自己封装了一套数据类型
