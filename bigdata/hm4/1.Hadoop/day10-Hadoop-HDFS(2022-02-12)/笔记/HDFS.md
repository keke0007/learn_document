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

#将小文件和并上传到HDFS
 hadoop fs -appendToFile day01.txt day02.txt  day03.txt  /big.txt   
 hadoop fs -appendToFile *.txt  /big.txt   
 
 hdfs dfs -appendToFile day01.txt day02.txt  day03.txt  /big.txt   
 hdfs dfs -appendToFile *.txt  /big.txt   
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



### HDFS的远程拷贝命令

#### 集群内主机之间拷贝

```shell
#格式
scp -r local_folder remote_username@remote_ip:remote_folder 
  -r表示拷贝是的目录
  
#演示
#推送
scp -r /root/dir  root@node2:/root  #指定远程访问的用户身份
scp -r /root/dir   node2:/root      #简化写法：默认以root用户身份访问

#拉取
scp -r root@node1:/root/dir /root  #把远端的文件拉取到本地
```



#### 跨集群的数据拷贝

```shell
hadoop distcp hdfs://node1:8020/jdk-8u241-linux-x64.tar.gz  hdfs://node10:8020/
```



### HDFS小文件解决方案

```shell
#---------在上传到HDFS之前，将小文件合并---------------------
#方式1
hadoop fs -appendToFile  *.txt  /big.txt

#方式2
    FileInputStream inputStream = new FileInputStream(file1); //根据File对象获取输入流
    IOUtils.copy(inputStream,outputStream);
    
#---------在上传到HDFS之后，将小文件合并---------------------
#方式3
 Archive档案,将小文件打包形成一个归档文件
```



### HDFS的Archive

#### 概念

+ Archive可以理解为将HDFS上已经存在的小文件进行"打包"，打包成一个文件，只占一条元数据，后缀是*.har

+ Archive在打包之后可以透明的访问其中的每一个小文件

+ Archive归档之后，原来的小文件不会被删除

+ Archive归档之后，会生成一个文件夹（test.har）,该文件夹下有四个文件

  ![image-20220212161358640](image\image-20220212161358640.png)

+ 将归档文件之后，原来的归档文件不会自动删除，需要手动删除

+ 归档文件只是打包，并没有压缩，不会减少空间的占用

+ 当原来的小文件内容发生改变，则归档文件不会跟着改变，除非创建新的归档文件

+ 归档的过程实际上是执行MapReduce任务

#### 操作

```shell
#1、创建Archive文件
#将/config目录下的所有文件进行打包归档，归档之后的包命名为test.har，将打包后的归档文件放在/outputdir
hadoop fs -mkdir /config
cd /export/server/hadoop-3.1.4/etc/hadoop/
hadoop fs -put  ./* /config   

hadoop archive -archiveName test.har -p /config  /outputdir

#2、查看归档后的part-0文件
#将所有小文件的内容都显示到终端上（没有意义）
hadoop fs -cat /outputdir/test.har/part-0

#3、查看归档包中有哪些小文件（显示小文件名）
hadoop fs -ls har://hdfs-node1:8020/outputdir/test.har

#4、单独显示或者操作其中的某个小文件
hadoop fs -cat  har://hdfs-node1:8020/outputdir/test.har/capacity-scheduler.xml
hadoop fs -cat  har:///outputdir/test.har/capacity-scheduler.xml

#5、将归档包中的小文件还原,
 mkdir /config2
 hadoop fs -cp har:///outputdir/test.har/* /config2
 
```



#### HDFS的SnapShot快照

#### 概念

+ HDFS的快照就是将HDFS系统的某一个目录或者某一个文件一个时间点的状态和内容保存下来
+ 如果以后源数据发生了误删除或者丢失、错乱，则可以使用快照来恢复原来的数据

#### 操作

```shell
#1、开启指定目录的快照功能
hdfs dfsadmin -allowSnapshot /config

#2、关闭指定目录的快照功能
hdfs dfsadmin  -disallowSnapshot  /config

#3、创建快照,使用默认的名字，快照在/config/.snapshot/s20220212-164145.611目录
hdfs dfs -createSnapshot /config

#4、创建快照，自己来指定名字
hdfs dfs -createSnapshot /config mysnap1

#5、给快照重命名
hdfs dfs -renameSnapshot /config  mysnap1 mysnap2

#6、比较两个快照的差异
#  + 表示增加文件    - 减少文件  M 修改文件
 hdfs snapshotDiff  /config  s20220212-164145.611 mysnap2 
 
#7、恢复快照
hdfs dfs -cp -ptopax /config/.snapshot/mysnap1  /config3

#、删除快照
#如果一个目录有快照，则该目录不能直接被删除，必须把所有快照都删除了，才能删除该目录
hdfs dfs -deleteSnapshot /config  mysnap2
```

### HDFS的权限

```shell

hadoop fs -chmod 777 /config       #变更目录或文件的权限位
hadoop fs -chmod -R 777 /config     #变更目录及子目录的权限位

hadoop fs -chown lft: /config #变更目录或文件的所属用户
hadoop fs -chown  :lft /config  #变更目录或文件的所属用户组


hadoop fs -chown  lft:lft /config  #变更目录或文件的所属用户和用户组
```



### HDFS的动态扩容和缩容

#### 扩容

1. 关闭原来Hadoop集群，添加在hdfs-site.xml添加以下内容,然后讲hdfs-site.xml分发到node2，node3

   ```xml
   <property>
           <name>dfs.hosts.exclude</name>
           <value>/export/server/hadoop-3.1.4/etc/hadoop/excludes</value>
   </property>
   ```

2. 关闭node3

3. 根据node3克隆node4

4. 修改node4的Mac地址

5. 修改node4的ip地址：192.168.88.164

6. 修改node4的主机名：node4

   -------------------------------------------

7. 启动node1,node2,node3主机，并打开hadoop集群

8. 配置主机名和ip地址的映射，在node1，node2，node3，node4的/etc/hosts文件修改内容如下:

   ```shell
   192.168.88.161 node1 node1.itcast.cn
   192.168.88.162 node2 node2.itcast.cn
   192.168.88.163 node3 node3.itcast.cn
   192.168.88.164 node4 node4.itcast.cn
   ```

9. 配置免密登录

   + 删除从node3克隆的秘钥信息：rm /root/.ssh/  -fr

   + 在node4上生成公钥和私钥:ssh-keygen -t rsa

   + 将node4的公钥发送给node1:ssh-copy-id node1

   + 将node1的所有主机公钥分发给其他主机

     ```shell
     scp /root/.ssh/authorized_keys node2:/root/.ssh
     scp /root/.ssh/authorized_keys node3:/root/.ssh
     scp /root/.ssh/authorized_keys node4:/root/.ssh
     ```

10.在node1的/export/server/hadoop-3.1.4/etc/hadoop/workers修改以下内容：

```shell
node1
node2
node3
node4
```

11.在node4上重新配置hadoop

+ 这里node4上已经有了从node3上克隆过来的hadoop，必须将/export/server/hadoop-3.1.4/data目录下的内容全部清空,这样node4的hadoop就配置完了

  ~~~shell
  rm -fr /export/server/hadoop-3.1.4/data/*
  ~~~

  

12.在node4上启动hdfs

```shell
hdfs --daemon start datanode
```

13.设置负载均衡

```shell
hdfs dfsadmin -setBalancerBandwidth 104857600  #设置贷款
hdfs balancer -threshold 5  #设置block数量
```

14、观察webUI页面是否添加成功

![image-20220212195607067](image\image-20220212195607067.png)

#### 缩容

1. 在node1编辑：vim /export/server/hadoop-3.1.4/etc/hadoop/excludes，在该文件中添加要退役的主机名
2. 在node1上刷新namenode：hdfs dfsadmin -refreshNodes
3. 在node4上手动关闭datanode
4. 在node1上执行负载均衡命令：hdfs balancer -threshold 5



### HDFS的ID

+ namespaceID：namenode名称空间id

  在单节点或者高可用情况下，整个集群只有一个namespaceID

  在联邦机制下，当横向扩展namenode时，扩展几个namenode，就会有几个namespaceID

+ clusterID：集群id，不管是单节点，高可用，联邦都属于同一个集群，所有clusterID都相同

+ blockpoolID:数据池ID

   在单节点或者高可用情况下，整个id都相同

​        在联邦机制下，当有多个namenode同时工作，每一个namenode都有自己的数据池，都有自己的blockpoolID



### HDFS的高可用搭建

```shell

集群部署节点角色的规划（3节点）
------------------
	node1   namenode    resourcemanager  zkfc   nodemanager  datanode   zookeeper   journal node
	node2   namenode    resourcemanager  zkfc   nodemanager  datanode   zookeeper   journal node
	node3                                       nodemanager  datanode   zookeeper    journal node
------------------

安装步骤：
1.安装配置zooekeeper集群(可选)
	1.1解压
		mkdir -p /opt/export/server
		tar -zxvf zookeeper-3.4.5.tar.gz -C /opt/export/server
	1.2修改配置
		cd /opt/export/server/zookeeper-3.4.5/conf/
		cp zoo_sample.cfg zoo.cfg
		vim zoo.cfg
		修改：dataDir=/opt/export/data/zkdata
		在最后添加：
		server.1=node1:2888:3888
		server.2=node2:2888:3888
		server.3=node3:2888:3888
		保存退出
		然后创建一个tmp文件夹
		mkdir /opt/export/data/zkdata
		echo 1 > /opt/export/data/zkdata/myid
		
	1.3将配置好的zookeeper拷贝到其他节点
		scp -r /opt/export/server/zookeeper-3.4.5 node2:/opt/export/server
		scp -r /opt/export/server/zookeeper-3.4.5 node3:/opt/export/server
		
		编辑node2、node3对应/opt/export/data/zkdata/myid内容
		node2：
			mkdir /opt/export/data/zkdata
			echo 2 > /opt/export/data/zkdata/myid
		node3：
			mkdir /opt/export/data/zkdata
			echo 3 > /opt/export/data/zkdata/myid

2.安装配置hadoop集群
    2.0 node1和node2安装以下软件
	  yum install psmisc -y
	  
	 
	2.1解压
	    在三台主机创建以下目录：
		mkdir -p /opt/export/server
		mkdir -p /opt/export/software
		mkdir -p /opt/export/opt/export/data/zkdata
		
		在node1上将hadoop安装包上传到/opt/export/software目录,并解压
		
		tar zxvf hadoop-3.1.4-bin-snappy-CentOS7.tar.gz  -C /opt/export/server
		
		在node1上创建以下目录
		mkdir -p /opt/export/server/hadoop-3.1.4/data
		mkdir -p /opt/export/server/hadoop-3.1.4/journaldata
		
	2.2配置3台主机的修改hadoop环境变量
		vim /etc/profile

		export HADOOP_HOME=/opt/export/server/hadoop-3.1.4
		export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

		source /etc/profile
3.在node1上修改配置文件
##############################################################################
3.1 修改hadoop-env.sh

cd /opt/export/server/hadoop-3.1.4/etc/hadoop
vim hadoop-env.sh

export JAVA_HOME=/export/server/jdk1.8.0_241
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_JOURNALNODE_USER=root
export HDFS_ZKFC_USER=root


###############################################################################
				
3.2 修改core-site.xml
<configuration>
	<!-- HA集群名称，该值要和hdfs-site.xml中的配置保持一致 -->
	<property>
		<name>fs.defaultFS</name>
		<value>hdfs://mycluster</value>
	</property>

	<!-- hadoop本地磁盘存放数据的公共目录 -->
	<property>
		<name>hadoop.tmp.dir</name>
		<value>/opt/export/server/hadoop-3.1.4/data</value>
	</property>

	<!-- ZooKeeper集群的地址和端口-->
	<property>
		<name>ha.zookeeper.quorum</name>
		<value>node1:2181,node2:2181,node3:2181</value>
	</property>
</configuration>

###############################################################################
				
3.3 修改hdfs-site.xml
<configuration>
	<!--指定hdfs的nameservice为mycluster，需要和core-site.xml中的保持一致 -->
	<property>
		<name>dfs.nameservices</name>
		<value>mycluster</value>
	</property>
	
	<!-- mycluster下面有两个NameNode，分别是nn1，nn2 -->
	<property>
		<name>dfs.ha.namenodes.mycluster</name>
		<value>nn1,nn2</value>
	</property>

	<!-- nn1的RPC通信地址 -->
	<property>
		<name>dfs.namenode.rpc-address.mycluster.nn1</name>
		<value>node1:8020</value>
	</property>

	<!-- nn1的http通信地址 -->
	<property>
		<name>dfs.namenode.http-address.mycluster.nn1</name>
		<value>node1:9870</value>
	</property>

	<!-- nn2的RPC通信地址 -->
	<property>
		<name>dfs.namenode.rpc-address.mycluster.nn2</name>
		<value>node2:8020</value>
	</property>
	
	<!-- nn2的http通信地址 -->
	<property>
		<name>dfs.namenode.http-address.mycluster.nn2</name>
		<value>node2:9870</value>
	</property>

	<!-- 指定NameNode的edits元数据在JournalNode上的存放位置 -->
	<property>
		<name>dfs.namenode.shared.edits.dir</name>
		<value>qjournal://node1:8485;node2:8485;node3:8485/mycluster</value>
	</property>
	
	<!-- 指定JournalNode在本地磁盘存放数据的位置 -->
	<property>
		<name>dfs.journalnode.edits.dir</name>
		<value>/opt/export/server/hadoop-3.1.4/journaldata</value>
	</property>

	<!-- 开启NameNode失败自动切换 -->
	<property>
		<name>dfs.ha.automatic-failover.enabled</name>
		<value>true</value>
	</property>

	<!-- 指定该集群出故障时，哪个实现类负责执行故障切换 -->
	<property>
		<name>dfs.client.failover.proxy.provider.mycluster</name>
		<value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
	</property>

	<!-- 配置隔离机制方法-->
	<property>
		<name>dfs.ha.fencing.methods</name>
		<value>sshfence</value>
	</property>
	
	<!-- 使用sshfence隔离机制时需要ssh免登陆 -->
	<property>
		<name>dfs.ha.fencing.ssh.private-key-files</name>
		<value>/root/.ssh/id_rsa</value>
	</property>
	
	<!-- 配置sshfence隔离机制超时时间 -->
	<property>
		<name>dfs.ha.fencing.ssh.connect-timeout</name>
		<value>30000</value>
	</property>
</configuration>

###############################################################################
			
3.4 修改mapred-site.xml
<configuration>
	<!-- 指定mr框架为yarn方式 -->
	<property>
	<name>mapreduce.framework.name</name>
	<value>yarn</value>
	</property>
</configuration>	

###############################################################################
			
3.5 修改yarn-site.xml
<configuration>
	<!-- 开启RM高可用 -->
	<property>
		<name>yarn.resourcemanager.ha.enabled</name>
		<value>true</value>
	</property>
	<!-- 指定RM的cluster id -->
	<property>
		<name>yarn.resourcemanager.cluster-id</name>
		<value>yrc</value>
	</property>
	<!-- 指定RM的名字 -->
	<property>
		<name>yarn.resourcemanager.ha.rm-ids</name>
		<value>rm1,rm2</value>
	</property>
	<!-- 分别指定RM的地址 -->
	<property>
		<name>yarn.resourcemanager.hostname.rm1</name>
		<value>node1</value>
	</property>
	<property>
		<name>yarn.resourcemanager.hostname.rm2</name>
		<value>node2</value>
	</property>
	<!-- 指定zk集群地址 -->
	<property>
		<name>yarn.resourcemanager.zk-address</name>
		<value>node1:2181,node2:2181,node3:2181</value>
	</property>
	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
</configuration>
			
				
3.6 修改workers
	node1
	node2
	node3
	
	
3.7 修改start-yarn.sh和stop-yarn.sh,在第二行添加以下内容

vim  /opt/export/server/hadoop-3.1.4/sbin/start-yarn.sh 

YARN_RESOURCEMANAGER_USER=root
HADOOP_SECURE_DN_USER=yarn
YARN_NODEMANAGER_USER=root

vim  /opt/export/server/hadoop-3.1.4/sbin/stop-yarn.sh 

YARN_RESOURCEMANAGER_USER=root
HADOOP_SECURE_DN_USER=yarn
YARN_NODEMANAGER_USER=root



3.8 分发hadoop包
cd /opt/export/server/
scp -r hadoop-3.1.4 root@node2:$PWD
scp -r hadoop-3.1.4 root@node3:$PWD


			
			
4.启动集群			
###注意：严格按照下面的步骤!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
4.1启动zookeeper集群（分别在node1、node2、node3上启动zk）
	
	zkServer.sh start
	#查看状态：一个leader，两个follower
	zkServer.sh status
	
4.2手动启动journalnode（分别在在node1、node2、node3上执行）
	/opt/export/server/hadoop-3.1.4/sbin/hadoop-daemon.sh start journalnode
	#运行jps命令检验,多了JournalNode进程

4.3格式化namenode
	#在node1上执行命令:
	/opt/export/server/hadoop-3.1.4/bin/hdfs namenode -format
	
	#格式化后会在根据core-site.xml中的hadoop.tmp.dir配置的目录下生成个hdfs初始化文件，
	
	#在node1启动namenode进程
	/opt/export/server/hadoop-3.1.4/bin/hdfs --daemon start namenode

	
	##在node2上启动备用namenode并进行元数据同步
	/opt/export/server/hadoop-3.1.4/bin/hdfs namenode -bootstrapStandby

4.4格式化ZKFC(在active(node1)上执行即可)
	/opt/export/server/hadoop-3.1.4/bin/hdfs zkfc -formatZK

4.5启动HDFS(在node1上执行)
	/opt/export/server/hadoop-3.1.4/sbin/start-dfs.sh

4.6启动YARN（在node1上执行）   
	/opt/export/server/hadoop-3.1.4/sbin/start-yarn.sh
	如果node2上没有启动ResourceManage，则还需要手动在standby上手动启动备份的  resourcemanager
	/opt/export/server/hadoop-3.1.4/sbin/yarn-daemon.sh start resourcemanager

			
			
测试集群工作状态的一些指令 ：
       hdfs dfsadmin -report	 查看hdfs的各节点状态信息

			
		
```

