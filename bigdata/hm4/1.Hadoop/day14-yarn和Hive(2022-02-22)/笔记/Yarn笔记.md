## Yarn

### 概述

+ Yarn是分布式的资源协调服务框架

+ Yarn是Hadoop的一个组件

+ Yarn之上可以运行各种分布式计算（MapReduce、Spark）

+ 官网地址

  ```shell
  https://hadoop.apache.org/docs/r2.6.5/hadoop-yarn/hadoop-yarn-site/YARN.html
  ```

  

### 组件

+ ResourceManager:ResourceManager负责所有资源的监控、分配和管理；
  + Applications Manager
  + Resoure Scheduler
+ NodeManager:完成具体资源的分配，完成具体的任务执行
  + 定时向ResourceManager汇报本节点资源（CPU、内存）的使用情况
  + 

+ ApplicationMaster
  + 每启动一个执行任务，都会有一个AppMaster
  + 监控所有任务运行状态，并在任务运行失败时重新为任务申请资源以重启任务。

![image-20220222220937626](image\image-20220222220937626.png)

### Yarn任务的执行过程

![image-20220222220901054](image\image-20220222220901054.png)

![image-20220222202450663](image\image-20220222202450663.png)

### Yarn的调度器

当多个客户端同时向Yarn提交资源时，Yarn如何来管理集群中的资源，如果调度这些任务，这个由Yarn的调度器来完成。

#### 队列调度器(**FIFO Scheduler**)        -------不用

#### 容量调度器(Capacity Scheduler)  ----- Apache Hadoop默认使用

+ 1：备份三台主机原来的容量调度器默认配置文件

  ```shell
  cd /export/server/hadoop-3.1.4/etc/hadoop
  cp capacity-scheduler.xml capacity-scheduler.xml_bak
  ```

+ 2：修改node1上的capacity-scheduler.xml文件， 内容如下

```xml
<configuration>
	<!-- 分为两个队列，分别为prod和dev -->  
	<property>
		<name>yarn.scheduler.capacity.root.queues</name>
		<value>prod,dev</value> 
	</property>
	<!-- dev继续分为两个队列，分别为eng和science -->      
	<property>
		<name>yarn.scheduler.capacity.root.dev.queues</name>
		<value>eng,science</value> 
	</property>
	<!-- 设置prod队列40% -->      
	<property>
		<name>yarn.scheduler.capacity.root.prod.capacity</name>
		<value>40</value>
	</property> 
	<!-- 设置dev队列60% -->  
	<property>
		<name>yarn.scheduler.capacity.root.dev.capacity</name>
		<value>60</value> 
	</property>
	<!-- 设置dev队列可使用的资源上限为75% -->  
	<property>
		<name>yarn.scheduler.capacity.root.dev.maximum-capacity</name>
		<value>75</value> 
	</property>
	<!-- 设置eng队列50% -->    
	<property>
		<name>yarn.scheduler.capacity.root.dev.eng.capacity</name>
		<value>50</value> 
	</property>
	<!-- 设置science队列50% -->   
	<property>
		<name>yarn.scheduler.capacity.root.dev.science.capacity</name>
		<value>50</value>
	</property>
</configuration>
```

+ 3. 将修改后的文件分发给node2和node3

  ```shell
  scp capacity-scheduler.xml node2:$PWD
  scp capacity-scheduler.xml node3:$PWD
  ```

+ 4. 重启Yarn集群

  ```shell
  stop-yarn.sh
  start-yarn.sh
  ```

+ 5. 通过8088页面查看是否生效

     ![image-20220222212715825](image\image-20220222212715825.png)

+ 6.使用指定队列来求PI值

  ```shell
   hadoop jar hadoop-mapreduce-examples-3.1.4.jar   pi  -Dmapreduce.job.queuename=prod 2 100000
  ```

  

#### 公平调度器（Fair Scheduler）     ------Cloudera Hadoop默认使用





