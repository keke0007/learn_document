# day01_SparkBase

* 1- Spark的基本介绍 (了解)
* 2- Spark环境的安装 (参考安装文档, 将其搭建成功)
* 3- 基于Pycharm完成pyspark的入门案例 (掌握)
* 4- Spark on Yarn环境搭建 (参考安装文档, 将其搭建成功,并理解当中两种部署方式)



## 1. Spark的基本介绍

### 1.1 Spark的基本介绍

* MapReduce: 分布式计算分析引擎

```properties
	MR: 分布式计算操作 可以用于处理大规模的数据, 主要是用于批处理, 用于离线处理操作
	
	MR存在弊端是什么? 
		1- 执行效率比较低
		2- API相对比较底层, 开发效率比较慢
		3- 执行迭代计算不方便
	
	什么是迭代计算? 
		简单来说, 在执行过程中, 整个任务需要划分为好几个步骤, 每一个步骤需要依赖上一个执行结果, 一级一级进行计算操作, 这个过程称为迭代计算
```

​		也正因为MR存在这样的一些弊端, 在一些场景中, 希望能够有一款执行效率比较高效, 能够更好的支持迭代计算, 同时还能处理大规模的数据的软件, 而Spark就是在这样的背景下产生了



Apache Spark 是一款用于处理大规模数据的分布式计算分析引擎, 基于内存计算, 整个Spark的核心数据结构为 RDD



RDD: 弹性的分布式数据集



Apache Spark 最早期是来源于加州大学伯克莱分校一帮博士发布的论文, 而产生的, 后期贡献给了Apache 成为Apache旗下顶级开源项目, 官网地址:  http://spark.apache.org

![image-20220521135303701](day01_pyspark课程笔记.assets/image-20220521135303701.png)

Spark 采用 Scala 语言编写的



为什么说Spark的执行速度快呢?

```properties
原因一: Spark提供了一个全新的数据结构  RDD  (理解为一个庞大的容器, 可以在这个容器中进行不断的计算操作)
	通过这个数据结构, 让分布式执行引擎能够在内存中进行计算, 同时能够更好的进行迭代计算
	对于MR来说, 主要是基于磁盘来计算, 而且迭代计算的时候, 需要将多个MR进行串联 执行效率比较低

原因二: Spark基于线程来运行的, MR是基于进程运行的
	线程的启动和销毁的速度, 要高于进程的启动和销毁的
```



基于线程和进程各自有那些优缺点呢?

![image-20220521140059198](day01_pyspark课程笔记.assets/image-20220521140059198.png)



### 1.2 Spark的发展史

![image-20220521140517342](day01_pyspark课程笔记.assets/image-20220521140517342.png)

![image-20220521140853895](day01_pyspark课程笔记.assets/image-20220521140853895.png)

关注:

```properties
	Spark是一个分布式计算引擎, PySpark是一个python的库, 专门用于操作Spark的python库
```



### 1.3 Spark的特点

* 1- 运行速度快

```properties
原因一: 基于内存计算的 采用DAG(有向无环图) 进行计算操作, 中间的结果优先保存到内存中, 如果内存不足也可以保存到磁盘

原因二:  Spark是基于线程来运行的, 线程的启动和销毁效率高于进程
```

* 2- 易用性

```properties
原因一:  Spark提供多种语言的客户端, 可以基于多种语言来运行Spark: 比如说 python  SQL  scala  Java  R ...

原因二:  Spark提供了更加高阶的API, 而且这些API在不同的语言上, 基本上都是一样的, 大大的降低了程序员的学习成本
```

* 3- 通用型

```properties
Spark提供了多种工具库, 用于满足各种计算的场景

Spark Core: Spark 核心库,  次重点, 它是学习的基础
	主要是用于放置Spark的核心API, 内存管理API, 包括维护RDD的数据结构

Spark SQL:  通过Sql操作Spark计算框架   最为重要的

Spark Streaming: Spark的流式计算框架, 主要用于支持流式计算(实时计算)(目前不使用, 整个实时主要基于Flink来完成)

Spark MLlib:  Spark的机器学习库, 主要包括一些相关机器学习的算法: 回归 聚类,,,,,  (针对特定人群)
Spark  graphX: Spark的图计算库,  比如说: 地图行程规划 (针对特定人群)

structured Streaming:  结构化流
```

![image-20220521142802817](day01_pyspark课程笔记.assets/image-20220521142802817.png)

* 4- 随处运行

```properties
原因一: 编写的Spark程序可以运行在不同的资源调度平台上: local模式 Yarn平台 Spark集群 云上的调度平台(mesos....)

原因二: Spark程序可以和大数据生态圈中各种软件进行集成, 让我们更加的方便使用Spark对接各个软件
```





## 2. Spark环境安装

### 2.1 Local模式安装

Local模式主要是用于本地代码测试操作

本质上就是一个单进程的程序, 在一个进程中运行多个线程

类似于pandas, 都是一个单进程程序 无法处理大规模的数据, 只处理小规模

![image-20220521145505765](day01_pyspark课程笔记.assets/image-20220521145505765.png)

安装操作, 可以直接参考课件中<<spark的部署文档>>

* 上传安装包:

```properties
	要求:  将安装包上传到 某一台linux节点的 /export/software 下

如果想使用rz上传: 
	请先安装: 
		yum -y install lrzsz
```

* 注意:  如果使用 浏览器访问 node1:4040 无法访问的时候 尝试去看一下, 在windows本地hosts文件中是否有以下配置
  * hosts文件地址:  C:\Windows\System32\drivers\etc

```properties
192.168.88.161 node1 node1.itcast.cn
192.168.88.162 node2 node2.itcast.cn
192.168.88.163 node3 node3.itcast.cn
```

或者 也有可能没有启动spark的客户端



如何退出客户端:  (禁止使用 ctrl + z ,此种操作本质是挂载在后台)

```properties
尝试使用以下方式: 
	ctrl + c
	ctrl + d
	:quit
	quit
	!quit
	:exit
	exit
	!exit
```



### 2.2 PySpark库安装

安装pyspark. 其实就是在python上安装一个pyspark的库, 要求首先必须先有python环境, 而spark要求python环境必须为 3以上版本

![image-20220521152139602](day01_pyspark课程笔记.assets/image-20220521152139602.png)

```properties
目前虚拟机上安装的python版本为 2.7.5 . 但是实际spark要求版本必须为 3以上的版本,而且在本地windwos上安装python环境也是为3.8.8版本, 需要在虚拟机中也需要安装这个python版本
```



安装 python环境和 pyspark的环境, 可以直接参考部署文档即可



扩展: anaconda的常用命令

```properties
安装库: 
	conda install  包名
	pip install -i 镜像地址 包名

卸载库: 
	conda uninstall 包名
	pip uninstall 包名

设置 anaconda下载的库的镜像地址:  
	conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
	conda config --set show_channel_urls yes

如何使用anaconda构建虚拟(沙箱)环境:

1- 查看当前有那些虚拟环境: 
conda env list

2- 如何创建一个新的虚拟环境
conda create 虚拟环境名称  python=版本号

例如: 创建一个pyspark_env 虚拟环境
conda create -n pyspark_env  python=3.8

3- 如何进入虚拟环境(激活)
source activate pyspark_env 
或者
conda activate pyspark_env

4- 如何退出虚拟环境:
deactivate pyspark_env 
或者
conda deactivate
```



注意: 如果大家使用的提供统一虚拟环境, 在后续的快照中, 其实将所有的环境都安装完成了, 但是在安装过程中, 出现了一个小失误, 将pyspark库安装为3.2.0版本了, 而不是3.1.2的版本, 所以需要大家卸载3.2.0版本, 安装3.1.2版本 否则后续会存在兼容问题



而且三个节点都安装了3.2.0的版本, 建议大家可以将三个节点都替换为3.1.2,以免引起兼容问题

```properties
卸载方式: 
	pip uninstall pyspark
	
安装: 
	pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyspark==3.1.2
```



如何将spark程序, 提交到spark local模式进行执行运行呢? 

```properties
使用命令:  
	Spark-submit 

如何使用(简单使用): 
	cd /export/server/spark/bin
	./spark-submit --master
	
案例使用:
	./spark-submit --master local[2] /export/server/spark/examples/src/main/python/pi.py 10
	
整个spark程序大致分为两部分: 
	一部分是 Driver程序 : 类似于 MR中 appMaster角色
	一部分为 executor程序 : 类似于 MR中 mapTask和reduceTask
```



### 2.3 Spark集群模式架构

![image-20220521164506199](day01_pyspark课程笔记.assets/image-20220521164506199.png)



## 3. 基于pycharm完成PySpark入门案例

### 3.0 如何清理远端环境

![image-20220521171136368](day01_pyspark课程笔记.assets/image-20220521171136368.png)

![image-20220521171205801](day01_pyspark课程笔记.assets/image-20220521171205801.png)

![image-20220521171350725](day01_pyspark课程笔记.assets/image-20220521171350725.png)

接下来, 还需要清理远端地址:

![image-20220521171430061](day01_pyspark课程笔记.assets/image-20220521171430061.png)

![image-20220521171536439](day01_pyspark课程笔记.assets/image-20220521171536439.png)



清理后, 重新配置当前项目使用远端环境: 

![image-20220521171631634](day01_pyspark课程笔记.assets/image-20220521171631634.png)

![image-20220521171841645](day01_pyspark课程笔记.assets/image-20220521171841645.png)

![image-20220521171907691](day01_pyspark课程笔记.assets/image-20220521171907691.png)

![image-20220521171931529](day01_pyspark课程笔记.assets/image-20220521171931529.png)

![image-20220521171950403](day01_pyspark课程笔记.assets/image-20220521171950403.png)

![image-20220521172113437](day01_pyspark课程笔记.assets/image-20220521172113437.png)

全部点击ok关闭即可

![image-20220521172201933](day01_pyspark课程笔记.assets/image-20220521172201933.png)

![image-20220521172238415](day01_pyspark课程笔记.assets/image-20220521172238415.png)

设置自动上传

![image-20220521172259590](day01_pyspark课程笔记.assets/image-20220521172259590.png)



### 3.1 pycharm连接远程环境

背景说明:

```properties
	一般在企业中, 会存在两套线上环境, 一套环境是用于开发(测试)环境, 一套环境是用于生产环境, 首先一般都是先在开发测试环境上进行编写代码, 并且在此环境上进行测试, 当整个项目全部开发完成后, 需要将其上传到生产环境, 面向用于使用
	
	如果说还是按照之前的本地模式开发方案, 每个人的环境有可能都不一致, 导致整个团队无法统一一套开发环境进行使用, 从而导致后续在进行测试 上线的时候, 出现各种各样环境问题
	
	pycharm提供了一些解决方案: 远程连接方案, 允许所有的程序员都去连接远端的测试环境的, 确保大家的环境都是统一, 避免各种环境问题发生, 而且由于连接的远程环境, 所有在pycharm编写代码, 会自动上传到远端环境中, 在执行代码的时候, 相当于是直接在远端环境上进行执行操作
```

操作实现: 本次这里配置远端环境, 指的连接虚拟机中虚拟环境, 可以配置为 base环境, 也可以配置为 pyspark_env虚拟环境, 但是建议配置为 base环境, 因为base环境自带python包更全面一些

![image-20211106161942329](day01_pyspark课程笔记.assets/image-20211106161942329.png)

![image-20211106162224194](day01_pyspark课程笔记.assets/image-20211106162224194.png)

![image-20211106155834393](day01_pyspark课程笔记.assets/image-20211106155834393.png)

![image-20211106155927905](day01_pyspark课程笔记.assets/image-20211106155927905.png)

![image-20211106162610727](day01_pyspark课程笔记.assets/image-20211106162610727.png)

![image-20211203165949987](day01_pyspark课程笔记.assets/image-20211203165949987.png)

创建项目后, 设置自动上传操作

![image-20211106163027500](day01_pyspark课程笔记.assets/image-20211106163027500.png)

校验是否有pyspark



![image-20211106163226670](day01_pyspark课程笔记.assets/image-20211106163226670.png)



ok 后, 就可以在项目上创建子项目进行干活了: 最终项目效果图

![image-20211106163432558](day01_pyspark课程笔记.assets/image-20211106163432558.png)

最后, 就可以在 main中编写今日代码了, 比如WordCount代码即可



-----

扩展: 关于pycharm 专业版 高级功能

* 1- 直接连接远端虚拟机, 进行文件上传, 下载 查看等等操作

![image-20211203170639696](day01_pyspark课程笔记.assets/image-20211203170639696.png)

![image-20211203171031827](day01_pyspark课程笔记.assets/image-20211203171031827.png)

* 2- 可以模拟shell控制台:

![image-20211203171106626](day01_pyspark课程笔记.assets/image-20211203171106626.png)

![image-20211203171158038](day01_pyspark课程笔记.assets/image-20211203171158038.png)

![image-20211203171222021](day01_pyspark课程笔记.assets/image-20211203171222021.png)



* 3- 模拟datagrip操作:

![image-20211203171303185](day01_pyspark课程笔记.assets/image-20211203171303185.png)

### 3.2 WordCount代码实现_Local



#### 3.2.1 WordCount案例流程实现

![image-20220521192646832](day01_pyspark课程笔记.assets/image-20220521192646832.png)

#### 3.2.2 编写代码实现

```properties
# 演示 WordCount案例实现
from pyspark import SparkContext, SparkConf
import os

# 锁定远程的环境版本(固定内容, 用于锁定python及spark环境版本)
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

# 在spark中, 如果基于python来编写spark程序, 要求python程序必须得有主入口类
# main函数快捷键:  main + 回车
if __name__ == '__main__':
    # 1) 创建SparkContext对象:
    conf = SparkConf().setMaster('local[*]').setAppName("WordCount")
    sc = SparkContext(conf=conf)

    # 2) 读取数据:
    # 参数1: 表示文件的路径(支持HDFS 本地, )
    # 如果是本地文件:  file:///路径
    # 如果是hdfs文件: hdfs://node1:8020/
    # 注意: 由于使用远端环境的操作, 此处所说的本地指的远端环境的本地路径(linux目录)
    # 读取方式: 一行一行的进行读取
    # 读取到数据: ['hello world hello hadoop','hadoop hello world hive','hive hive hadoop']
    rdd_init = sc.textFile('file:///export/data/workspace/ky04_pyspark_parent/_01_pyspark_base/data/words.txt')

    # print(rdd_init.collect())
    # 3) 对数据进行切割操作:
    # 希望得到的结果:
    """
        [
            [hello, world, hello ,hadoop],
            [hadoop,hello,world,hive],
            [hive, hive, hadoop]
        ]
    """
    # 对于map理解: 对RDD容器中数据进行一对一的转换操作, 转换的逻辑是什么取决于我们传递的函数
    # rdd_map = rdd_init.map(lambda line: line.split(' '))
    # 希望得到的结果:
    """
            [
                hello, world, hello ,hadoop,hadoop,hello,world,hive,hive, hive, hadoop
            ]
    """
    # 对于flatMap理解: 对RDD容器中数据进行一对多的转换操作, 核心思想是: 先按照map来进行转换, 转换后进行扁平化(压扁)处理
    rdd_flatMap = rdd_init.flatMap(lambda line: line.split(' '))

    # 4) 将每一个单词转换为 (单词,1): 一对一转换使用 Map   一对多转换使用 flatMap
    # 得到结果:
    """
        [
            ('hello', 1), 
            ('world', 1), 
            ('hello', 1), 
            ('hadoop', 1), 
            ('hadoop', 1), 
            ('hello', 1), 
            ('world', 1), 
            ('hive', 1), 
            ('hive', 1), 
            ('hive', 1), 
            ('hadoop', 1)
        ]
    
    """
    rdd_tupleMap = rdd_flatMap.map(lambda word: (word, 1))

    # 5) 根据单词进行分组, 将相同单词放置在一起, 对value进行求和计算
    rdd_res = rdd_tupleMap.reduceByKey(lambda agg,curr: agg + curr)
    # [('world', 2), ('hadoop', 3), ('hive', 3), ('hello', 3)]
    # 6) 输出结果对象
    print(rdd_res.collect())

    # 7) 关闭sc对象
    sc.stop()
```

简单写法(合并写法):

```python
# 演示 WordCount案例实现, 进阶版
from pyspark import SparkContext, SparkConf
import os

# 锁定远程的环境版本(固定内容, 用于锁定python及spark环境版本)
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    # 1) 创建SparkContext对象:
    conf = SparkConf().setMaster('local[*]').setAppName("WordCount")
    sc = SparkContext(conf=conf)

    # 2) 完成WordCount案例 (链式编程法)
    result = sc\
        .textFile('file:///export/data/workspace/ky04_pyspark_parent/_01_pyspark_base/data/words.txt')\
        .flatMap(lambda line: line.split(' '))\
        .map(lambda word:(word,1))\
        .reduceByKey(lambda agg,curr:agg+curr).collect()

    # 3) 输出打印
    print(result)

    #4) 关闭资源
    sc.stop()
```





可能遇到的错误:

![image-20220521194846835](day01_pyspark课程笔记.assets/image-20220521194846835.png)

```properties
异常:   JAVA_HOME is not set

出现位置: 当pycharm采用SSH连接远程python环境的时候, 启动执行Spark程序可能会报出

原因:  当前python无法加载到JDK位置

解决方案: 
	第一步: 需要在linux的 /root/.bashrc 文件中 添加以下内容: 
		export JAVA_HOME=/export/server/jdk1.8.0_241/
		export PYSPARK_PYTHON=/root/anaconda3/bin/python3
		配置后, 重新加载一个bashrc文件: source /root/.bashrc 
	第二步: 在代码中, 指定linux中Spark的所在目录: 以下代码放置在main函数上面即可, 用于锁定环境版本
		# 锁定远程的环境版本(固定内容, 用于锁定python及spark环境版本)
		os.environ['SPARK_HOME'] = '/export/server/spark'
		os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
		os.environ['PYSPARK_DRIVER_PYTHON']='/root/anaconda3/bin/python3'
```

### 3.3 [扩展]部署windows开发环境(不需要做)

* 1- 第一步: 需要安装Python 环境 , 建议使用anaconda 来安装即可 

* 2- 第二步: 在Python安装pySpark

```properties
执行:
	pip install pyspark==3.1.2
```

![image-20211011092950093](day01_pyspark课程笔记.assets/image-20211011092950093.png)

* 3- 第三步: 配置 hadoop的环境

![image-20211011093110189](day01_pyspark课程笔记.assets/image-20211011093110189.png)

```properties
首先, 需要将 hadoop-3.3.0 放置到一个没有中文, 没有空格的目录下

接着将目录中bin目录下有一个 hadoop.dll文件, 放置在c:/windows/system32 目录下  (配置后, 需要重启电脑)

最后, 将这个hadoop3.3.0 配置到环境变量中: 
```

![image-20211011093357951](day01_pyspark课程笔记.assets/image-20211011093357951.png)

![image-20211011093606044](day01_pyspark课程笔记.assets/image-20211011093606044.png)

配置后, 一定一直点确定退出, 否则就白配置了....

* 4-第四步: 配置spark本地环境

![image-20211011093739472](day01_pyspark课程笔记.assets/image-20211011093739472.png)

```properties
首先, 需要将 spark-3.1.2... 放置到一个没有中文, 没有空格的目录下

最后, 将这个 spark-3.1.2... 配置到环境变量中:
```

![image-20211011093930392](day01_pyspark课程笔记.assets/image-20211011093930392.png)

![image-20211011094107829](day01_pyspark课程笔记.assets/image-20211011094107829.png)

配置后, 一定一直点确定退出, 否则就白配置了....

* 5-配置pySpark环境

```properties
需要修改环境变量
```

![image-20211011094309104](day01_pyspark课程笔记.assets/image-20211011094309104.png)

![image-20211011094415551](day01_pyspark课程笔记.assets/image-20211011094415551.png)

配置后, 一定一直点确定退出, 否则就白配置了....



* 6- 配置 jdk的环境:

![image-20211106093351456](day01_pyspark课程笔记.assets/image-20211106093351456.png)

```
首先: 需要将 jdk1.8 放置在一个没有中文, 没有空格的目录下

接着:要在环境变量中配置 JAVA_HOME, 并在path设置
```

![image-20211106093508597](day01_pyspark课程笔记.assets/image-20211106093508597.png)

![image-20211106093623797](day01_pyspark课程笔记.assets/image-20211106093623797.png)

### 3.4 从HDFS上读取文件并实现排序

```python
# 演示: 从HDFS上读取文件, 并对结果的value值进行排序操作
from pyspark import SparkContext, SparkConf
import os

# 锁定远程的环境版本(固定内容, 用于锁定python及spark环境版本)
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    # 1- 创建sparkContext对象:
    conf = SparkConf().setMaster("local[*]").setAppName("WordCount")
    sc = SparkContext(conf=conf)

    # 2- 读取数据
    rdd_init = sc.textFile("hdfs://node1:8020/pyspark_data/words.txt")

    # 2- 对每一行执行切割转换, 将其转换为 一个个单词:
    rdd_flatMap = rdd_init.flatMap(lambda line: line.split())

    # 3- 对数据进行转换为 单词,1 模式
    rdd_map = rdd_flatMap.map(lambda word: (word, 1))

    # 4) 根据key分组聚合统计操作
    rdd_res = rdd_map.reduceByKey(lambda agg, curr: agg + curr)

    # 5) 对结果排序:
    # 参数指定按照那一列进行排序:
    # rdd_sort = rdd_res.sortBy(lambda wd_tup: wd_tup[1] , ascending=False)
    # 以下处理 纯属娱乐, 没有实际价值
    # rdd_res = rdd_res.map(lambda wd_tup:(wd_tup[1],wd_tup[0]))
    # rdd_sort = rdd_res.sortByKey(ascending=False)
    # rdd_sort = rdd_sort.map(lambda wd_tup: (wd_tup[1], wd_tup[0]))

    print(rdd_res.top(10, lambda wd_tup: wd_tup[1] ))
    
    
    # 6) 关闭SC
    sc.stop()
```



### 3.5 基于Spark-Submit进行任务提交

```properties
cd /export/server/spark/bin

./spark-submit --master local[*] python脚本文件


示例:
	./spark-submit --master local[*] /export/data/workspace/ky04_pyspark_parent/_01_pyspark_base/src/_03_pyspark_wd.py
	

说明: 
	spark-submit脚本: 主要用于将spark程序提交到指定的资源平台上, 例如: local  spark集群, yarn集群 ....
	在提交spark任务过程中, 可以设置任务的资源的参数配置 如果不设置, 都是采用默认值
```



## 4. Spark On Yarn环境搭建

### 4.1 Spark On Yarn的本质

​		本质:  将Spark程序运行在yarn集群中, 由yarn完成任务调度工作

### 4.2 配置Spark On Yarn

​		关于整个配置, 大家直接参考<<spark环境部署文档>>  一定要参考今天的最新的安装部署文档

### 4.3 提交应用测试

* 将编写的WordCount的代码提交到yarn平台运行
  * 注意: 需要将代码中 --master参数删除 或者 修改为 yarn

```properties
cd /export/server/spark/bin
./spark-submit \
--master yarn \
--conf "spark.pyspark.driver.python=/root/anaconda3/bin/python3" \
--conf "spark.pyspark.python=/root/anaconda3/bin/python3" \
/export/data/workspace/ky04_pyspark_parent/_01_pyspark_base/src/_03_pyspark_wd.py
```



