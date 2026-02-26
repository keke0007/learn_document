# HDFS

## 今日重点

+ 理解HDFS的原理
+ 理解分布式存储思想
+ 掌握HDFS的shell操作命令

  

## Hadoop

### Hadoop概念

+ Hadoop是一个软件，这个软件包含三个模块
  + **HDFS: Hadoop分布式文件系统**
  + MapReduce:分布式计算系统
  + Yarn:分布式资源调度系统

  ![image-20220122222108151](image\image-20220122222108151.png)
  



## 资源网址

+ apache的资源包下载

  ```shell
  https://archive.apache.org/dist/
  ```

+ Hadoop-3.1.4官网

  ```shell
  https://hadoop.apache.org/docs/r3.1.4/
  ```

  

## HDFS文件系统

### 概述

+ HDFS的全称：Hadoop分布式文件系统
+ HDFS合适存储大容量数据，合适存储大文件
+ HDFS可以将一些廉价的计算机进行整合，形成一个完整的存储系统，并且对外提供统一的访问路径

### 特性

+ HDFS在存储数据时将文件进行切分，切分成多个block（128=134217728字节），每一个block会有多个副本（默认3个副本）

  ![image-20220127203207871](image\image-20220127203207871.png)

  ![image-20220127204234380](image\image-20220127204234380.png)

+ HDFS在读取文件的时候，不能保证实时性，HDFS在存储大体量数据时，速度慢，时间长，一般适合一次写入多次读取,所以不适合做网盘
+ HDFS只适合存大文件，不适合存小文件，因为每在HDFS上存储一个文件，namenode的内存就会记录一条元数据，每条元数据大概150字节，小文件过多，元数据过多，则会大量占用namenode内存
+ HDFS不支持文件的随机修改，只支持文件的追加写入
+ HDFS的存储可以近乎无限扩展

### HDFS的架构

+ HDFS是主从架构，主节点是namenode，从节点是datanode

  ![image-20220127211952710](image\image-20220127211952710.png)

+ HDFS角色的功能

  + NameNode

    + 保存整个HDFS集群的元数据

      ![image-20220127211018639](image\image-20220127211018639.png)

      + NameNode需要知道每一个DataNode上block的信息
      + 客户端在上传或者下载文件时，需要从NameNode设置或者获取元数据信息
      + NameNode的元数据信息是保存在内存中，但是会定时保存到硬盘（Secondary NameNode）

  + DataNode
    + 保存具体文件数据
    + 要定时与NameNode之间发送心跳包
    + 要定时向NameNode汇报Block信息
    + 客户端要下载或者上传文件时，具体的文件操作是和DataNode进行交互

  + Seconday NameNode
    + 辅助NameNode进行元数据管理(元数据持久化存储，保存到硬盘)
  + Client
    + Client负责上传文件和下载文件的发起工作
    + Client在上传文件时会对文件进行切片

### HDFS的切片机制

+ HDFS的BLOCK只是一个逻辑单位
+ 假如BLOCK的大小设置为128M，意思是这个BLOCK最大是128M
+ BLOCK的大小可以通过：hdfs-site.xml中的dfs.blocksize参数来进行设置



### HDFS的副本机制

+ HDFS的每个BLOCK都会有多个副本，默认是3个
+ HDFS的副本数可以通过hdfs-site.xml中的dfs.replication参数来进行设置

### HDFS的NameSpace

+ HDFS会给每一个存储的文件提供一个统一的访问路径

  ```shell
  #格式
  hdfs://namenode:port/dir-a/dir-b/dir-c/file.data。
  #使用1-使用绝对前缀方式
  hdfs://node1:8020/dir/a.txt
  hadoop  fs -put a.txt hdfs://node1:8020/dir
  #使用1-使用相对前缀方式
  /dir/a.txt
  hadoop  fs -put a.txt /dir
  ```

### HDFS的元数据

```shell
在HDFS中，Namenode管理的元数据具有两种类型：
	文件自身属性信息
文件名称、权限，修改时间，文件大小，副本数，数据块大小。
	文件块位置映射信息
记录文件块和DataNode之间的映射信息，即哪个块位于哪个节点上。
```

### HDFS的机架感知

+ 第一个BLOCK副本会存储在离客户端最近的一台主机上，如果客户端就是集群中的主机，则直接存在客户端所在主机，如果Client不在集群范围内或者不在同一个子网，则会在集群中随机选一个机架，在该机架中随机选一个健康（心跳正常，硬盘容量正常）的主机，将这个BLOCK存入
+ 第二个BLOCK副本会存入另外一个机架（随机选择），会在该机架上随机选一台健康的主机，将数据存入
+ 第三个BLOCK副本会在第二个BLOCK副本的机架上随机选择另外一台健康主机，将BLOCK数据存入

![image-20220127215209884](image\image-20220127215209884.png)

### HDFS的shell命令

```shell
#格式
hadoop fs -命令  参数    #该命令可以操作任何文件系统
hdfs dfs  -命令         #该命令只能操作HDFS文件系统

#文件的上传
hadoop fs -put a.txt /dir
hdfs  dfs -put  a.txt /dir

#文件的下载
hadoop fs -get /dir/a.txt /root
hdfs dfs  -get /dir/a.txt /root

#创建文件夹 -单级
hadoop fs -mkdir /dir2
hdfs dfs  -mkdir /dir2

#创建文件夹-多级
hadoop fs -mkdir -p   /aaa/bbb/ccc
hdfs dfs -mkdir -p /aaa/bbb/ccc

#删除文件
hadoop fs -rm /a.txt
hdfs dfs -rm /a.txt

#删除文件夹
hadoop fs -rm -r /a.txt
hdfs dfs  -rm -r /a.txt


#在HDFS上进行文件的复制
hadoop fs -cp /dir/1.txt /  #这里的两个路径都是HDFS路径
hdfs dfs -cp /dir/1.txt /  #这里的两个路径都是HDFS路径

#在HDFS上进行文件的移动（剪切）
hadoop fs -mv /dir/1.txt /    #这里的两个路径都是HDFS路径
hadoop fs -mv /dir/1.txt /    #这里的两个路径都是HDFS路径

#调整HDFS文件副本的数量
hdfs dfs -setrep -w 2 /1.txt
```

### HDFS的安全模式

##### 概述

 安全模式是hadoop的一种**保护机制**，用于保证集群中的数据块的安全性。当集群启动的时候，会首先进入安全模式。当系统处于安全模式时会检查数据块的完整性。

在安全模式下，HDFS主要做两件事情

+ DataNode会将自己的Block信息汇报给NameNode
+ NameNode会检查副本率（实际的副本数/理论的副本数）是否达到 0.9990 ,如果没有达到，则会进行副本的动态调整，如果副本率满足了需求之后，则默认在20多秒之后自动关闭安全模式

##### 特点

在安全模式状态下，文件系统只接受读数据请求，而不接受删除、修改等变更请求。在当整个系统达到安全标准时，HDFS自动离开安全模式。

##### 操作命令

```shell
hdfs  dfsadmin -safemode  get #查看安全模式状态
hdfs  dfsadmin -safemode  enter #进入安全模式
hdfs  dfsadmin -safemode  leave #离开安全模式
```

### HDFS的读写流程

#### 写流程

![](image\1-HDFS的写数据流程.jpg)



#### 读流程

![](image\2-HDFS的读文件流程.bmp)

### HDFS元数据的辅助管理

#### 概述

+ NameNode在工作的时候元数据在存放在内存中，保证访问速度最优
+ NamNode内存中的元数据容易发生掉电丢失，所以必须持久化存储到硬盘上
+ 由于NameNode要接收客户端的各种请求，所以为了减轻NameNode压力，持久化元数据的任务就交给了SecondaryNameNode

#### 持久化文件

+ fsimage镜像文件
  + 镜像文件，保存了所有过去NameNode的元数据

+ edits日志文件
  + 保存了最近一段时间的元数据操作日志

   NameNode完整的元数据 = fsimage文件 + edits日志文件



#### SecondaryNameNode作用

![image-20220210213201629](image\image-20220210213201629.png)

+ snn会在满足条件的时候将nn的fsimage和edits文件拷贝到所在主机

  ```shell
  dfs.namenode.checkpoint.period=3600  //两次连续的checkpoint之间的时间间隔。默认1小时
  dfs.namenode.checkpoint.txns=1000000 //最大没有执行checkpoint事务的数量，满足将强制执行紧急checkpoint，即使尚未达到检查点周期。默认100万事务数量。
  ```

+ snn会将拷贝过来的fsimage和edit进行合并（合并之后并不会删除镜像文件和日志文件）

+ snn将fsimage和edit进行合并之后会生成新的fsimage，并替换原来的fsimage

+ 原来的edits会重新生成

