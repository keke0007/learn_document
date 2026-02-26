# Zookeeper框架

## 大数据生态圈

![img](image\1)

## Zookeeper的概述

+ ZK是一个分布式协调服务框架
  + 分布式：ZK的安装是横跨多台主机,有自己的集群
  + 协调服务：ZK单独存在没有意义，ZK主要为其他集群提供服务的，让其它集群能够顺序完成一些任务和工作（**动物管理员**）

+ 后期的很多大数据框架都需要依赖Zookeeper，比如：Hadoop，HBase、Kafka
+ ZK有可以理解成一个数据库系统，它本身可以存数据

## Zookeeper的特性

+ 全局数据一致:客户端在ZK集群上每存一份数据，则这份数据在所有主机上都有备份数据，以后其他客户端不管访问哪一台主机，则看到的数据都是一样的
+ 可靠性：在ZK集群中，只要有一份数据发生改变，则其他主机也会跟着改变
+ 顺序性：在ZK集群中，在一台主机上进行数据操作的顺序比如是A，B，则其他主机上操作的顺序也是A,B,不会发生错乱
+ 数据更新原子性：Client在ZK集群上的任何一个操作，都是事务操作，不可再分，这个操作过程要么全部成功才算成功，只要有一个环节失败，则整体失败，则数据退回到操作之前的状态
+ 实时性: Client在ZK集群上进行操作时间不会太长（ms级），会在有限时间之内完成操作，其他的客户端可以近乎实时的获取到操作之后的数据

## Zookeeper的角色

### 概述

ZK是主从架构的集群，主节点是Leader，从节点是Follower和Observer

![image-20220120201536095](image\image-20220120201536095.png)

### 角色的功能

+ **Leader**
  + Leader是整个集群的管理者
  + Leader来完成整个集群所有的**事务操作**即写操作（增删改）
  + Leader也可以完成读请求操作
  + 一个ZK集群只能有一个Leader，如果当前Leader的所在主机宕机，则由其他的Follower重新选举新的Leader

+ **Follower**
  + 只能完成客户端发过来的读请求
  + 如果Client发过来写请求，则需要转发给Leader去处理
  + 如果Leader挂掉，Follower会参与Leader选举（政治权利）

+ **Observer**
  + Observer除了不能选举Leader之外，其他的功能和Follower一样（被剥夺的政治权利）
  + 一个ZK集群，Observer存在的唯一的意义就是增加集群对外的读取能力

## Zookeeper的安装

+ Zookeeper集群一般是奇数台（建议）

+ Zookeeper是基于Java语言研发的，所以在安装ZK之前，必须先安装JDK

+ 我们在这里搭建的集群模式：Leader + Follower，其实还有（Leader + Follower + Observer）模式

+ Zookeeper如果启动失败唯一的排查错误方式就是查看日志，ZK会在你执行启动命令的所在目录生成zookeeper.out，这个文件就是日志文件

+ 使用jps（java相关进程）命令可以查看Zookeeper进程

   ```shel
   QuorumPeerMain
   ```

+ 如果要设置开机启动项，则可以在/etc/rc.d/rc.local文件中添加命令

+ 一键启动脚本

  ```shell
  #!/bin/bash
  for num in 1 2 3
  do
          ssh root@node${num} "source /etc/profile;zkServer.sh $1"
          echo "正在操作第${num}主机"
  done
  ```

  



## Zookeeper的数据模型

+ ZK是一个树形结构的系统,类似Linux的文件系统,就靠这个系统来存储数据

  ![image-20220120213305062](image\image-20220120213305062.png)

+ ZK中的每一个节点叫znode

+ ZK中的Znode即具有文件的特性，又具有文件夹（目录）的特性
  + 文件特性：每一个Znode节点可以存储数据
  + 文件夹特性：每一个Znode节点可以有子节点

+ Znode具有原子性操作，当你在某一台主机上创建了一个Znode节点，则其他的主机也会创建该节点，这个过程是原子不可再分的

![image-20220120213832267](image\image-20220120213832267.png)

+ Znode存储数据大小有限制，由于Zookeeper是来管理其他集群，每一个节点存储都是配置信息，所以数据量一般不会太大都是以K为单位，最多不超过1M

+ 在Znode的树形结构中，必须使用绝对路径来访问节点

  ```shell
  正确方式：/app1/p_3
  错误方式：p_3
  ```

## ZK的节点类型

```shell
PERSISTENT：永久节点
EPHEMERAL： 临时节点
PERSISTENT_SEQUENTIAL：永久节点、序列化（顺序）
EPHEMERAL_SEQUENTIAL：临时节点、序列化（顺序）
```

## ZK的shell操作

+ 使用客户端连接服务器

  + 方式1

    ```shell
    zkCli.sh -server node1:2181  #连接指定主机服务器
    ```

  + 方式2

    ```shell
    zkCli.sh  #默认连接本机的Zookeeper
    ```

+ ZK的shell操作

  ```shell
  #1：创建普通永久节点
    #永久节点：不管终端有没有关闭，这个节点永久存在
   create /app1 hello
  #2: 创建永久顺序节（ 序列化）点
    #永久顺序节点:和永久节点一样，只是在节点名字的后边加上一串数字，数字越大表示节点创建的时间越晚
  create -s /app2 world
  
  #3:创建临时节点
   #临时节点：创建的节点随着客户端和服务器之间的会话存在而存在
  create -e /tempnode world
  
  #4:创建顺序的临时节点
  create -s -e /tempnode2 aaa
  
  #5：创建子节点
   #临时节点不能有字节点
  create /app1/app11 hello11
  
  #5:获取节点数据
  
     get  /app1
     get  /app1/app11
  
  #6:修改节点数据
     set /app1  hadoop
  
  #7:删除节点
    delete  /app1  #删除的节点不能有子节点
    rmr    /app1 #递归删除
  ```
  


## ZK的作用

![image-20220120221422458](image\image-20220120221422458.png)

## ZK的Watch机制

#### 概念

+ watch机制就是ZK对Znode节点进行监控，监控Znode节点的一举一动，如果Znode节点发生了变动，则立刻会触发通知机制，采取相应的处理方案
  + 节点的新增
  + 节点的删除
  + 节点的数据变化

+ 默认情况下，在终端中的演示的watch机制只能被触发一次，如果想要在此被触发，则需要重新设置，但是通过JavaAPI去实现watch机制可以重复触发。

+ watch机制涉及的参数

  ```shell
  通知状态（keeperState），             事件类型（EventType）       节点路径（path）
  WatchedEvent state:SyncConnected    type:NodeDeleted          path:/app1
  ```

## Znode的属性

```shell
[zk: localhost:2181(CONNECTED) 0] get /app1
hello3
cZxid = 0x60000000b                     # Znode创建的事务id，该值一般不变
ctime = Sat Jan 22 14:09:31 CST 2022    # 创建时间  
mZxid = 0x600000013                     #修改的事务id，即每次对znode的修改都会更新mZxid。
mtime = Sat Jan 22 14:14:08 CST 2022    #修改时间
pZxid = 0x60000000b                     #和cZxid相同
cversion = 0                            #子节点的版本号。当znode的子节点有变化时，cversion 的值就会增加1。
dataVersion = 6                         #数据版本，每次对数据进行修改，则该值会加1
aclVersion = 0
ephemeralOwner = 0x0                   #永久节点：该值为0x0，临时节点：当前的会话id
dataLength = 6                         #数据长度
numChildren = 0                        #子节点数量
```

## ZK的JavaAPI操作

### 意义

+ ZK在管理其他集群时，其他集群就是ZK的一个客户端，这些集群需要主动的通过JavaAPI对Zookeeper的znode进行操作
+ 以后如果有新的研发框架需要使用Zookeeper来进行协调管理，则就需要编写本框架和Zookeeper之间结合的操作代码

### 相关的类

+ 操作Zookeeper有两套JavaAPI
  + ZK提供的原生API（JDBC）
  + 第三方封装的工具类API（DBUtils，JDBCTemplate，MyBatis）
    + **curator-framework**：对zookeeper的底层api的一些封装
    + **curator-recipes**：封装了一些高级特性，如：Cache事件监听、选举、分布式锁、分布式计数器等

### 依赖引入

```xml
<dependencies>
        <dependency>
            <groupId>org.apache.curator</groupId>
            <artifactId>curator-framework</artifactId>
            <version>2.12.0</version>
        </dependency>

        <dependency>
            <groupId>org.apache.curator</groupId>
            <artifactId>curator-recipes</artifactId>
            <version>2.12.0</version>
        </dependency>

        <dependency>
            <groupId>com.google.collections</groupId>
            <artifactId>google-collections</artifactId>
            <version>1.0</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>1.7.25</version>
        </dependency>
    </dependencies>
```







## ZK的选举机制

在ZK集群的Leader宕机之后，剩余的Follower会选举出新的Leader,Leader选举有两个时机。

+ 时机1-第一次启动集群的Leader选举 

  + 当票数过半时，谁的myid最大，谁就是Leader

  ![image-20220122192348706](E:\lesson\狂野大数据\day06-Zookeeper和Hadoop(2022-01-22)\笔记\image\image-20220122192348706.png)

  

+ 时机2-在集群工作的中Leader选举（Leader挂掉了）

  + 所有主机都给自己投票，当票数过半时，开始选举Leader，如果票数不过半，则放弃Leader选举
  +  当所有主机都投完票之后，看哪台主机的数据version最新，最新的直接当Leader
  + 当PK的主机数据Version相同时，则比较myid，myid最大则优先当Leader

  ![image-20220122193815898](E:\lesson\狂野大数据\day06-Zookeeper和Hadoop(2022-01-22)\笔记\image\image-20220122193815898.png)

