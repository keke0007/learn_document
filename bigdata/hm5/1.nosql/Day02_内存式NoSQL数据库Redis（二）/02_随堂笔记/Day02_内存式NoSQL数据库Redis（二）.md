# 内存式NoSQL数据库Redis（二）

## 知识点01：课程回顾

1. Redis功能和应用场景
   - 功能：基于内存实现KV数据存储【读写】
   - 本质：基于内存的KV类型的NoSQL数据库
   - 场景：1-缓存【Java Web架构】：高并发、**==2-数据库【大数据实时：存储实时统计的结果】：高性能==**、3-消息队列
     - 我们工作中怎么用Redis：实时架构中
     - 数据同步：Flume、Canal、OGG
     - 数据存储：Kafka
     - 数据计算：Flink
     - 数据应用：Redis【实时推荐、实时风控、实时报表】
   - 特点：高并发和高性能，读写只基于内存
   - 区分
     - MySQL：RDBMS，侧重于稳定性和安全性【1-存储离线工具元数据。2-存储离线统计分析的结果】
     - HDFS：分布式文件系统，用于离线架构中
     - Hive：离线数据仓库工具，底层还是HDFS
     - Zookeeper：实时存储系统，用于解决分布式架构中共享问题，小数据存储
2. Redis搭建
   - 启动服务端：redis-server redis.conf
   - 启动客户端：redis-cli -h node1 -p 6379 
   - 关闭服务端：shutdown、kill
   - 关闭客户端：exit
3. Redis数据结构和类型
   - 数据结构：KV结构
     - 数据库、Key【表】、Value【数据】
   - 数据类型
     - K：String
     - V：String、Hash、List、Set、Zset



## 知识点02：课程目标

1. 常用命令
   - 目标：**掌握每种类型的常用命令：Redis通过命令来区分KV类型**
   - String：读写命令
   - Hash：读写命令
   - List：顺序读写命令
   - Set：读写，长度
   - Zset：顺序读写，长度
2. Jedis的使用
   - 目标：**掌握如何通过Java代码读写Redis**



## 知识点03：【掌握】Redis的通用命令

- **目标**：**掌握Redis常用的通用命令**

- **实施**

  - **keys**：列举当前数据库中所有Key
    - 语法：keys 通配符
    - 举例：keys *
    - 类似：show tables
  - **del key**：删除某个KV
    - 语法：del key
  - **exists key** ：判断某个Key是否存在
    - 语法：exists key
  - **type key**：判断这个K对应的V的类型的
    - 语法：type key
  - **expire K** 过期时间：设置某个K的过期时间，一旦到达过期时间，这个K会被自动删除
    - 语法：expire key 时间
  - **ttl K**：查看某个K剩余的存活时间
    - 语法：ttl key
  - select N：切换数据库的
    - Redis中有数据库的概念，默认自带16个数据库：db0 - db15
    - 默认都是操作0数据库，用select后面加上数据库的编号可以实现切换
  - move key N：将某个Key移动到某个数据库中
  - flushdb：清空当前数据库的所有Key
  - flushall：清空所有数据库的所有Key

  ```
  node1:6379> keys *
  1) "h1"
  2) "s1"
  node1:6379> keys s*
  1) "s1"
  node1:6379> keys *
  1) "h1"
  2) "s1"
  node1:6379> del h1
  (integer) 1
  node1:6379> keys *
  1) "s1"
  node1:6379> exists s1
  (integer) 1
  node1:6379> exists h1
  (integer) 0
  node1:6379> type s1
  string
  node1:6379> hset h1 name zhangsan
  (integer) 1
  node1:6379> type h1
  hash
  node1:6379> 
  node1:6379> expire h1 20
  (integer) 1
  node1:6379> keys *
  1) "h1"
  2) "s1"
  node1:6379> ttl h1
  (integer) 5
  node1:6379> ttl h1
  (integer) 3
  node1:6379> ttl h1
  (integer) 2
  node1:6379> 
  node1:6379> ttl h1
  (integer) -2
  node1:6379> keys *
  1) "s1"
  node1:6379> 
  node1:6379> select 1
  OK
  node1:6379[1]> select 2
  OK
  node1:6379[2]> select 0
  OK
  node1:6379> select 1
  OK
  node1:6379[1]> set s1 spark
  OK
  node1:6379[1]> keys *
  1) "s1"
  node1:6379[1]> get s1
  "spark"
  node1:6379[1]> select 0
  OK
  node1:6379> keys *
  1) "s1"
  node1:6379> get s1
  "hadoop"
  node1:6379> select 1
  OK
  node1:6379[1]> del s1
  (integer) 1
  node1:6379[1]> keys *
  (empty list or set)
  node1:6379[1]> 
  node1:6379[1]> keys *
  (empty list or set)
  node1:6379[1]> select 0
  OK
  node1:6379> set s2 spark
  OK
  node1:6379> keys *
  1) "s1"
  2) "s2"
  node1:6379> move s2 1
  (integer) 1
  node1:6379> select 1
  OK
  node1:6379[1]> keys *
  1) "s2"
  node1:6379[1]> select 0
  OK
  node1:6379> keys *
  1) "s1"
  node1:6379> flushdb
  OK
  node1:6379> keys *
  (empty list or set)
  node1:6379> flushall
  OK
  node1:6379> select 1
  OK
  node1:6379[1]> keys *
  (empty list or set)
  ```

  

- **小结**：掌握Redis常用的通用命令



## 知识点04：【掌握】String类型的常用命令

- **目标**：掌握String类型的常用命令

- **实施**
  
  - 应用：类似于Java中String，存储单个值
  - **set**：给String类型的Value的进行赋值或者更新【不存在就插入，存在就更新】
    - 语法：set  K  V
  - **get**：读取String类型的Value的值
    - 语法：get  K
  - **mset**：用于批量写多个String类型的KV
    - 语法：mset  K1 V1 K2 V2 ……
  - **mget**：用于批量读取String类型的Value
    - 语法：mget K1 K2 K3……
  - setnx：只能用于新增数据，当K不存在时可以进行新增
  - 语法：setnx K V
  - **incr**：用于对数值类型的字符串进行递增，递增1,一般用于做计数器
    - 语法：incr K
  - **incrby**：指定对数值类型的字符串增长固定的步长
    - 语法：incr K  step
  - decr：对数值类型的数据进行递减，递减1
    - 语法：decr K
  - decrby：按照指定步长进行递减
    - 语法：decrby  K step
  - strlen：统计字符串的长度
    - 语法：strlen K
  - getrange：用于截取字符串
    - 语法：getrange  K   start[开始位置]  end[结束位置]
  
  ```
  node1:6379> keys *
  (empty list or set)
  node1:6379> set s1 zookeeper
  OK
  node1:6379> keys *
  1) "s1"
  node1:6379> get s1
  "zookeeper"
  node1:6379> set s1 "this is zookeeper"
  OK
  node1:6379> get s1
  "this is zookeeper"
  node1:6379> mset s2 hadoop s3 hive s4 hue
  OK
  node1:6379> keys *
  1) "s4"
  2) "s3"
  3) "s1"
  4) "s2"
  node1:6379> mget s1 s3 s4
  1) "this is zookeeper"
  2) "hive"
  3) "hue"
  node1:6379> setnx s5 spark
  (integer) 1
  node1:6379> keys *
  1) "s5"
  2) "s1"
  3) "s4"
  4) "s3"
  5) "s2"
  node1:6379> get s5
  "spark"
  node1:6379> setnx s5 flink
  (integer) 0
  node1:6379> get s5
  "spark"
  node1:6379> 
  node1:6379> set s6 2
  OK
  node1:6379> get s6
  "2"
  node1:6379> incr s6
  (integer) 3
  node1:6379> get s6
  "3"
  node1:6379> incr s6
  (integer) 4
  node1:6379> get s6
  "4"
  node1:6379> incrby s6 6
  (integer) 10
  node1:6379> get s6
  "10"
  node1:6379> decr s6
  (integer) 9
  node1:6379> decrby s6 3
  (integer) 6
  node1:6379> get s5
  "spark"
  node1:6379> strlen s5
  (integer) 5
  node1:6379> getrange s5 0 2
  "spa"
  node1:6379> 
  ```
  
- **小结**：掌握String类型的常用命令



## 知识点05：【掌握】Hash类型的常用命令

- **目标**：掌握Hash类型的常用命令

- **实施**

  - 应用：类似于一个Map集合，一般用于存储整体对象
  - **hset**：用于为某个K添加一个属性
    - 语法：hset   K   k   v
  - **hget**：用于获取某个K的某个属性的值
    - 语法：hget  K  k
  - **hmset**：批量的为某个K赋予新的属性
    - 语法：hmset  K   k1  v1 k2  v2……
  - **hmget**：批量的获取某个K的多个属性的值
    - 语法：hmget   K  k1  k2 k3……
  - **hgetall**：获取所有属性的值
    - 语法：hgetall  K
  - hdel：删除某个属性
    - 语法：hdel  K  k1
  - hlen：统计K对应的Value总的属性的个数
    - 语法：hlen K
  - hexists：判断这个K的V中是否包含这个属性
    - 语法：hexists K  k1
  - hvals：获取所有属性的value的
    - 语法：hvals K
  - hkeys：后去所有属性
    - 语法：hkeys K

  ```
  node1:6379> hset p1 name laoda
  (integer) 1
  node1:6379> keys *
  1) "p1"
  2) "s5"
  3) "s1"
  4) "s4"
  5) "s3"
  6) "s6"
  7) "s2"
  node1:6379> hset p1 age 18
  (integer) 1
  node1:6379> hset p2 name laoer
  (integer) 1
  node1:6379> hset p2 age 20
  (integer) 1
  node1:6379> keys *
  1) "p1"
  2) "s5"
  3) "s1"
  4) "s4"
  5) "p2"
  6) "s3"
  7) "s6"
  8) "s2"
  node1:6379> hget p1 name
  "laoda"
  node1:6379> hget p2 name
  "laoer"
  node1:6379> hget p2 age
  "20"
  node1:6379> hget p1 age
  "18"
  node1:6379> hmset p1 gender male addr shanghai
  OK
  node1:6379> hmget p1 name gender addr
  1) "laoda"
  2) "male"
  3) "shanghai"
  node1:6379> hgetall p1
  1) "name"
  2) "laoda"
  3) "age"
  4) "18"
  5) "gender"
  6) "male"
  7) "addr"
  8) "shanghai"
  node1:6379> hdel p1 gender
  (integer) 1
  node1:6379> hgetall p1
  1) "name"
  2) "laoda"
  3) "age"
  4) "18"
  5) "addr"
  6) "shanghai"
  node1:6379> hlen p1
  (integer) 3
  node1:6379> hexists p1 name
  (integer) 1
  node1:6379> hexists p1 gender
  (integer) 0
  node1:6379> hvals p1
  1) "laoda"
  2) "18"
  3) "shanghai"
  node1:6379> hkeys p1
  1) "name"
  2) "age"
  3) "addr"
  node1:6379> 
  ```

- **小结**：掌握Hash类型的常用命令



## 知识点06：【掌握】List类型的常用命令

- **目标**：掌握List类型的常用命令

- **实施**

  - 应用：类似于Java中List集合，利用有序特性来实现顺序读写
  - **lpush**：将每个元素放到集合的左边，左序放入
    - 语法：lpush K  e1 e2 e3 ……
  - **rpush**：将每个元素放到集合的右边，右序放入
    - 语法：rpush K e1 e2 e3……
  - **lrange**：通过下标的范围来获取元素的数据
    - 语法：lrange  K  start  end
    - 从左往右：下标从0开始
    - 从右往左：下标从-1开始
    - 特殊：查询所有元素：lrange  K  0  -1
  - llen：统计集合的长度
    - 语法：llen  K
  - lpop：删除左边的一个元素
    - 语法：lpop K
  - rpop：删除右边的一个元素
    - 语法：rpop K

  ```
  node1:6379> lpush list1 1 2 3 3
  (integer) 4
  node1:6379> rpush list1 4 4 5 6 7
  (integer) 9
  node1:6379> lrange list1 0 -1
  1) "3"
  2) "3"
  3) "2"
  4) "1"
  5) "4"
  6) "4"
  7) "5"
  8) "6"
  9) "7"
  node1:6379> lrange list1 0 3
  1) "3"
  2) "3"
  3) "2"
  4) "1"
  node1:6379> lrange list1 5 8
  1) "4"
  2) "5"
  3) "6"
  4) "7"
  node1:6379> lrange list1 -4 -1
  1) "4"
  2) "5"
  3) "6"
  4) "7"
  node1:6379> llen list1
  (integer) 9
  node1:6379> lpop list1
  "3"
  node1:6379> lrange list1 0 -1
  1) "3"
  2) "2"
  3) "1"
  4) "4"
  5) "4"
  6) "5"
  7) "6"
  8) "7"
  node1:6379> rpop list1
  "7"
  node1:6379> lrange list1 0 -1
  1) "3"
  2) "2"
  3) "1"
  4) "4"
  5) "4"
  6) "5"
  7) "6"
  node1:6379> 
  ```

- **小结**：掌握List类型的常用命令



## 知识点07：【掌握】Set类型的常用命令

- **目标**：掌握Set类型的常用命令

- **实施**

  - 应用：类似于Java中Set集合，去重
  - **sadd**：用于添加元素到Set集合中
    - 语法：sadd  K  e1 e2 e3……
  - **smembers**：用于查看Set集合的所有成员
    - 语法：smembers K
  - sismember：判断是否包含这个成员
    - 语法：sismember K  k
  - srem：删除其中某个元素
    - 语法：srem  K  k
  - **scard**：统计集合长度
    - 语法：scard K
  - sunion：取两个集合的并集
    - 语法：sunion K1 K2……
  - **sinter**：取两个集合的交集
    - 语法：sinter K1 K2

  ```
  node1:6379> sadd set1 5 2 1 1 3 1
  (integer) 4
  node1:6379> smembers set1
  1) "1"
  2) "2"
  3) "3"
  4) "5"
  node1:6379> srem set1 3
  (integer) 1
  node1:6379> smembers set1
  1) "1"
  2) "2"
  3) "5"
  node1:6379> sismember set1 5
  (integer) 1
  node1:6379> sismember set1 3
  (integer) 0
  node1:6379> scard set1
  (integer) 3
  node1:6379> sadd set2 1 3 4 4 5 7
  (integer) 5
  node1:6379> smembers set2
  1) "1"
  2) "3"
  3) "4"
  4) "5"
  5) "7"
  node1:6379> sunion set1 set2
  1) "1"
  2) "2"
  3) "3"
  4) "4"
  5) "5"
  6) "7"
  node1:6379> sinter set1 set2
  1) "1"
  2) "5"
  node1:6379> 
  ```

- **小结**：掌握Set类型的常用命令



## 知识点08：【掌握】Zset类型的常用命令

- **目标**：掌握Zset类型的常用命令

- **实施**

  - 应用：类似于Java中TreeMap概念，有序且元素不重复
  - **zadd**：用于添加元素到Zset集合中
    - 语法：zadd  K   score1 e1   score2 e2……
    - score：评分，用于实现对元素排序
    - e：元素
  - **zrange**：范围查询
    - 语法：zrange K  start end 【WITHSCORES】
    - 用法：与lrange基本一致
    - WITHSCORES：是否在结果中添加评分
    - 注意：数值会存在精度不准确的问题，从开发层面建议转换成整数再写入
  - **zrevrange**：倒序查询
    - 语法：zrevrange K start end [withscores]
  - zrem：移除一个元素
    - 语法：zrem K  e……
  - **zcard**：统计集合长度
    - 语法：zcard  K
  - zscore：获取评分
    - 语法：zscore  K  e

  ```
  node1:6379> zadd zset1 20.5 yinyu 99 shengwu 100 yuwen 35.7 shuxue
  (integer) 4
  node1:6379> zrange zset1 0 -1
  1) "yinyu"
  2) "shuxue"
  3) "shengwu"
  4) "yuwen"
  node1:6379> zrange zset1 0 -1 withscores
  1) "yinyu"
  2) "20.5"
  3) "shuxue"
  4) "35.700000000000003"
  5) "shengwu"
  6) "99"
  7) "yuwen"
  8) "100"
  node1:6379> zrevrange zset1 0 -1 
  1) "yuwen"
  2) "shengwu"
  3) "shuxue"
  4) "yinyu"
  node1:6379> zrevrange zset1 0 -1 withscores
  1) "yuwen"
  2) "100"
  3) "shengwu"
  4) "99"
  5) "shuxue"
  6) "35.700000000000003"
  7) "yinyu"
  8) "20.5"
  node1:6379> zrem zset1 shuxue
  (integer) 1
  node1:6379> zrange zset1 0 -1
  1) "yinyu"
  2) "shengwu"
  3) "yuwen"
  node1:6379> zcard zset1
  (integer) 3
  node1:6379> zscore zset1 yinyu
  "20.5"
  node1:6379> zscore zset1 yuwen
  "100"
  node1:6379> 
  ```

- **小结**

  - 掌握Zset类型的常用命令



## 知识点09：【了解】BitMap类型的常用命令

- **目标**：了解BitMap类型的常用命令

- **实施**

  - 功能：通过一个String对象的存储空间，来构建位图，用每一位0和1来表示状态

    ![image-20210520075811401](Day02_内存式NoSQL数据库Redis（二）.assets/image-20210520075811401.png)

    

    - Redis中一个String最大支持512M =  2^32次方，1字节 = 8位
    - 使用时，可以指定每一位对应的值，要么为0，要么为1，默认全部为0

    - 用下标来标记每一位，第一个位的下标为0

    ![image-20210520075824978](Day02_内存式NoSQL数据库Redis（二）.assets/image-20210520075824978.png)

  - 举例：统计UV

    - 一个位图中包含很多位，可以用每一个位表示一个用户id

    - 读取数据，发现一个用户id，就将这个用户id对应的那一位改为1

    - 统计整个位图中所有1的个数，就得到了UV

  - setbit：修改某一位的值

    - 语法：setbit  bit1  位置   0/1

      ```
      setbit bit1 0 1
      ```

  - getbit：查看某一位的值

    - 语法：getbit  K  位置

      ```
      getbit bit1 9
      ```

  - bitcount：用于统计位图中所有1的个数

    - 语法：bitcount  K [start   end]

      ```
      bitcount bit1
      #start和end表示的是字节:1 字节 = 8 位
      bitcount bit1 0 10
      ```

  - bitop：用于位图的运算：and/or/not/xor

    - 语法：bitop  and/or/xor/not  bitrs   bit1 bit2

      ```
      bitop and bit3 bit1 bit2
      bitop or bit4 bit1 bit2
      ```

    ![image-20210520080018074](Day02_内存式NoSQL数据库Redis（二）.assets/image-20210520080018074.png)

  ```
  node1:6379> setbit bit1 0 1
  (integer) 0
  node1:6379> getbit bit1 0
  (integer) 1
  node1:6379> getbit bit1 1
  (integer) 0
  node1:6379> getbit bit1 2
  (integer) 0
  node1:6379> getbit bit1 3
  (integer) 0
  node1:6379> setbit bit1 9 1
  (integer) 0
  node1:6379> setbit bit1 17 1
  (integer) 0
  node1:6379> bitcount bit1 
  (integer) 3
  node1:6379> bitcount bit1 0 7
  (integer) 3
  node1:6379> bitcount bit1 0 0
  (integer) 1
  node1:6379> bitcount bit1 0 1
  (integer) 2
  node1:6379> bitcount bit1 0 2
  (integer) 3
  node1:6379> setbit bit2 0 1
  (integer) 0
  node1:6379> setbit bit2 10 1
  (integer) 0
  node1:6379> bitop and bit3 bit1 bit2
  (integer) 3
  node1:6379> bitcount bit3
  (integer) 1
  node1:6379> 
  ```

- **小结**：了解BitMap类型的常用命令



## 知识点10：【了解】HyperLogLog类型的常用命令

- **目标**：了解HyperLogLog类型的常用命令

- **实施**

  - 功能：**类似于Set集合**，用于实现数据的去重，底层实现原理不一样

  - 应用：适合于**数据量比较庞大**的情况下的使用，**存在一定的误差率**

  - pfadd：用于添加元素

    - 语法：pfadd  K   e1 e2 e3……

      ```
      pfadd pf1 userid1 userid1 userid2 userid3 userid4 userid3 userid4
      pfadd pf2 userid1 userid2 userid2 userid5 userid6
      ```

  - pfcount：用于统计个数

    - 语法：pfcount K

      ```
      pfcount pf1
      ```

  - pfmerge：用于实现集合合并

    - 语法：pfmerge  pfrs  pf1 pf2……

      ```
      pfmerge pf3 pf1 pf2
      ```

- **小结**：了解HyperLogLog类型的常用命令



## 知识点11：【掌握】Jedis：使用方式与Jedis依赖

- **目标**：**掌握Redis的使用方式及构建Jedis工程依赖**

- **实施**

  - **Redis的使用方式**

    - 命令操作Redis，一般用于测试开发阶段

    - 分布式计算或者Java程序读写Redis，一般用于实际生产开发

      - Spark/Flink读写Redis

      - 所有数据库使用Java操作方式整体是类似的

        ```java
        //todo:1-构建客户端连接对象
        Connection conn = DriverManager.getConnect(url,username,password)
        //todo:2-执行操作：所有操作都在客户端连接对象中：方法
        prep.execute(SQL)
        //todo:3-释放连接
        conn.close
        ```

  - **Jedis依赖**

    - 参考附录一添加依赖

- **小结**

  - 掌握Redis的使用方式及构建Jedis工程依赖



## 知识点12：【掌握】Jedis：构建连接

- **目标**：实现Jedis的客户端连接

- **实施**

  ```java
  package bigdata.itcast.cn.jedis;
  
  import org.junit.After;
  import org.junit.Before;
  import org.junit.Test;
  import redis.clients.jedis.Jedis;
  import redis.clients.jedis.JedisPool;
  import redis.clients.jedis.JedisPoolConfig;
  
  /**
   * @ClassName JedisClientTest
   * @Description TODO 测试Jedis客户端的开发，实现Redis数据库的操作
   * @Create By     Frank
   */
  public class JedisClientTest {
  
      // todo:1-构建一个连接对象
      Jedis jedis = null;
  
      @Before
      public void getConnection(){
          //方式一：直接构建一个Jedis连接实例
  //        jedis = new Jedis("node1",6379);
          //方式二：使用连接池构建
          //构建连接池配置
          JedisPoolConfig config = new JedisPoolConfig();
          config.setMaxTotal(10); //设置最大连接数
          //构建连接池
          JedisPool jedisPool = new JedisPool(config,"node1",6379);
          //获取连接
          jedis = jedisPool.getResource();
      }
      // todo:2-实现具体的操作
  
      // todo:3-释放连接
      @After
      public void closeConnection(){
          jedis.close();
      }
  }
  
  ```

- **小结**：实现Jedis的客户端连接



## 知识点13：【掌握】Jedis：String操作

- **目标**：Jedis中实现String的操作

- **实施**

  ```
  set/get/incr/exists/expire/setexp/ttl
  ```

  ```java
      @Test
      public void testString(){
          //set/get/incr/exists/expire/setex/ttl
  //        jedis.set("s1","hadoop");
  //        System.out.println(jedis.get("s1"));
  //        jedis.set("s2","1");
  //        jedis.incr("s2");
  //        System.out.println(jedis.get("s2"));
  //        System.out.println(jedis.exists("s1"));
  //        System.out.println(jedis.exists("s3"));
  //        jedis.expire("s1",20);
  //        while(true){
  //            System.out.println(jedis.ttl("s1"));
  //        }
          jedis.setex("s3",10,"hive");
      }
  ```

- **小结**：Jedis中实现String的操作

  

## 知识点14：【掌握】Jedis：其他类型操作

- **目标**：Jedis中实现其他类型操作

- **实施**

  - **Hash类型**

    ```
    hset/hmset/hget/hgetall/hdel/hlen/hexists
    ```

    ```java
        public void testHash(){
            //hset/hmset/hget/hgetall/hdel/hlen/hexists
            jedis.hset("m1","name","zhangsan");
            System.out.println(jedis.hget("m1","name"));
            Map<String,String> maps = new HashMap<>();
            maps.put("age","18");
            maps.put("phone","110");
            jedis.hmset("m1",maps);
            List<String> hmget = jedis.hmget("m1", "name", "age");
            System.out.println(hmget);
            System.out.println("=");
            Map<String, String> m1 = jedis.hgetAll("m1");
            for(Map.Entry map : m1.entrySet()){
                System.out.println(map.getKey()+"\t"+map.getValue());
            }
            System.out.println("=");
            System.out.println(jedis.hlen("m1"));
            jedis.hdel("m1","name");
            System.out.println(jedis.hlen("m1"));
            System.out.println(jedis.hexists("m1","name"));
            System.out.println(jedis.hexists("m1","age"));
        }
    ```

  - **List类型**

    ```
    lpush/rpush/lrange/llen/lpop/rpop
    ```

    ```java
      @Test
        public void testList(){
            //lpush/rpush/lrange/llen/lpop/rpop
            jedis.lpush("list1","1","2","3");
            System.out.println(jedis.lrange("list1",0,-1));
            jedis.rpush("list1","4","5","6");
            System.out.println(jedis.lrange("list1",0,-1));
            System.out.println(jedis.llen("list1"));
            jedis.lpop("list1");
            jedis.rpop("list1");
            System.out.println(jedis.lrange("list1",0,-1));
        }
    ```

  - **Set类型**

    ```
    sadd/smembers/sismember/scard/srem
    ```

    ```java
      @Test
        public void testSet(){
            //sadd/smembers/sismember/scard/srem
            jedis.sadd("set1","1","2","3","1","2","3","4","5","6");
            System.out.println("长度："+jedis.scard("set1"));
            System.out.println("内容："+jedis.smembers("set1"));
            System.out.println(jedis.sismember("set1","1"));
            System.out.println(jedis.sismember("set1","7"));
            jedis.srem("set1","2");
            System.out.println("内容："+jedis.smembers("set1"));
    
        }
    ```

  - **Zset类型**

    ```
    zadd/zrange/zrevrange/zcard/zrem
    ```

    ```java
        @Test
        public void testZset(){
          //zadd/zrange/zrevrange/zcard/zrem
            jedis.zadd("zset1",20.9,"yuwen");
            jedis.zadd("zset1",10.5,"yinyu");
            jedis.zadd("zset1",70.9,"shuxue");
            jedis.zadd("zset1",99.9,"shengwu");
            Set<String> zset1 = jedis.zrange("zset1", 0, -1);
            System.out.println(zset1);
            System.out.println(jedis.zrevrange("zset1",0,-1));
            System.out.println(jedis.zcard("zset1"));
            jedis.zrem("zset1","yuwen");
            System.out.println(jedis.zrangeWithScores("zset1",0,-1));
        }
    ```

- **小结**：Jedis中实现其他类型操作



## 附录一：Jedis Maven依赖

```xml
   <dependencies>
        <!-- Jedis 依赖 -->
        <dependency>
            <groupId>redis.clients</groupId>
            <artifactId>jedis</artifactId>
            <version>4.2.3</version>
        </dependency>
        <!-- JUnit 4 依赖 -->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.0</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
        </plugins>
    </build>
```
