# 案例1：RDD 基础操作

## 案例描述
学习 Spark RDD 的基本操作，包括创建、转换和行动操作。

## 数据准备

### 数据文件 (words.txt)
```
hello world
hello spark
spark is great
big data
spark streaming
hello big data
```

### 数据文件 (numbers.txt)
```
1,2,3,4,5
6,7,8,9,10
11,12,13,14,15
```

## Scala 实现

### 完整代码 (RDDBasics.scala)
```scala
import org.apache.spark.{SparkConf, SparkContext}

object RDDBasics {
  def main(args: Array[String]): Unit = {
    // 创建 SparkConf
    val conf = new SparkConf()
      .setAppName("RDD Basics")
      .setMaster("local[*]")
    
    // 创建 SparkContext
    val sc = new SparkContext(conf)
    
    try {
      // ============================================
      // 1. 创建 RDD
      // ============================================
      
      // 从集合创建
      val numbers = sc.parallelize(Seq(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
      println("从集合创建的 RDD:")
      numbers.collect().foreach(println)
      
      // 从文件创建
      val lines = sc.textFile("data/words.txt")
      println("\n从文件读取的行数: " + lines.count())
      
      // ============================================
      // 2. Transformation 操作
      // ============================================
      
      // map: 转换每个元素
      val doubled = numbers.map(x => x * 2)
      println("\n每个数字乘以2:")
      doubled.collect().foreach(println)
      
      // filter: 过滤
      val evens = numbers.filter(x => x % 2 == 0)
      println("\n偶数:")
      evens.collect().foreach(println)
      
      // flatMap: 一对多转换
      val words = lines.flatMap(line => line.split(" "))
      println("\n所有单词:")
      words.collect().foreach(println)
      
      // distinct: 去重
      val uniqueWords = words.distinct()
      println("\n去重后的单词:")
      uniqueWords.collect().foreach(println)
      
      // ============================================
      // 3. Action 操作
      // ============================================
      
      // count: 计数
      println("\n单词总数: " + words.count())
      println("唯一单词数: " + uniqueWords.count())
      
      // first: 第一个元素
      println("\n第一个单词: " + words.first())
      
      // take: 取前 n 个
      println("\n前5个单词:")
      words.take(5).foreach(println)
      
      // reduce: 归约
      val sum = numbers.reduce((a, b) => a + b)
      println("\n数字总和: " + sum)
      
      // ============================================
      // 4. 键值对操作
      // ============================================
      
      // map: 转换为键值对
      val wordPairs = words.map(word => (word, 1))
      println("\n单词键值对:")
      wordPairs.take(10).foreach(println)
      
      // reduceByKey: 按键聚合
      val wordCounts = wordPairs.reduceByKey(_ + _)
      println("\n单词计数:")
      wordCounts.collect().foreach(println)
      
      // sortBy: 排序
      val sortedCounts = wordCounts.sortBy(_._2, ascending = false)
      println("\n按计数排序:")
      sortedCounts.collect().foreach(println)
      
      // ============================================
      // 5. 分区操作
      // ============================================
      
      println("\nRDD 分区数: " + numbers.partitions.length)
      
      // mapPartitions: 按分区处理
      val partitionedSum = numbers.mapPartitions(iter => {
        Iterator(iter.sum)
      })
      println("\n每个分区的和:")
      partitionedSum.collect().foreach(println)
      
      // ============================================
      // 6. 保存结果
      // ============================================
      
      // 保存为文本文件
      wordCounts.saveAsTextFile("output/word_counts")
      
      println("\n结果已保存到 output/word_counts")
      
    } finally {
      // 关闭 SparkContext
      sc.stop()
    }
  }
}
```

### 运行方式
```bash
spark-submit --class RDDBasics \
  --master local[*] \
  target/scala-2.12/spark-basics_2.12-1.0.jar
```

## PySpark 实现

### 完整代码 (rdd_basics.py)
```python
from pyspark import SparkConf, SparkContext

def main():
    # 创建 SparkConf
    conf = SparkConf().setAppName("RDD Basics").setMaster("local[*]")
    
    # 创建 SparkContext
    sc = SparkContext(conf=conf)
    
    try:
        # ============================================
        # 1. 创建 RDD
        # ============================================
        
        # 从集合创建
        numbers = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        print("从集合创建的 RDD:")
        print(numbers.collect())
        
        # 从文件创建
        lines = sc.textFile("data/words.txt")
        print(f"\n从文件读取的行数: {lines.count()}")
        
        # ============================================
        # 2. Transformation 操作
        # ============================================
        
        # map: 转换每个元素
        doubled = numbers.map(lambda x: x * 2)
        print("\n每个数字乘以2:")
        print(doubled.collect())
        
        # filter: 过滤
        evens = numbers.filter(lambda x: x % 2 == 0)
        print("\n偶数:")
        print(evens.collect())
        
        # flatMap: 一对多转换
        words = lines.flatMap(lambda line: line.split(" "))
        print("\n所有单词:")
        print(words.collect())
        
        # distinct: 去重
        unique_words = words.distinct()
        print("\n去重后的单词:")
        print(unique_words.collect())
        
        # ============================================
        # 3. Action 操作
        # ============================================
        
        # count: 计数
        print(f"\n单词总数: {words.count()}")
        print(f"唯一单词数: {unique_words.count()}")
        
        # first: 第一个元素
        print(f"\n第一个单词: {words.first()}")
        
        # take: 取前 n 个
        print("\n前5个单词:")
        print(words.take(5))
        
        # reduce: 归约
        sum_result = numbers.reduce(lambda a, b: a + b)
        print(f"\n数字总和: {sum_result}")
        
        # ============================================
        # 4. 键值对操作
        # ============================================
        
        # map: 转换为键值对
        word_pairs = words.map(lambda word: (word, 1))
        print("\n单词键值对:")
        print(word_pairs.take(10))
        
        # reduceByKey: 按键聚合
        word_counts = word_pairs.reduceByKey(lambda a, b: a + b)
        print("\n单词计数:")
        print(word_counts.collect())
        
        # sortBy: 排序
        sorted_counts = word_counts.sortBy(lambda x: x[1], ascending=False)
        print("\n按计数排序:")
        print(sorted_counts.collect())
        
        # ============================================
        # 5. 分区操作
        # ============================================
        
        print(f"\nRDD 分区数: {numbers.getNumPartitions()}")
        
        # mapPartitions: 按分区处理
        def partition_sum(iterator):
            yield sum(iterator)
        
        partitioned_sum = numbers.mapPartitions(partition_sum)
        print("\n每个分区的和:")
        print(partitioned_sum.collect())
        
        # ============================================
        # 6. 保存结果
        # ============================================
        
        # 保存为文本文件
        word_counts.saveAsTextFile("output/word_counts")
        
        print("\n结果已保存到 output/word_counts")
        
    finally:
        # 关闭 SparkContext
        sc.stop()

if __name__ == "__main__":
    main()
```

### 运行方式
```bash
spark-submit rdd_basics.py
```

## 预期结果

### 单词计数结果
```
(hello, 3)
(spark, 3)
(world, 1)
(is, 1)
(great, 1)
(big, 2)
(data, 2)
(streaming, 1)
```

### 按计数排序
```
(hello, 3)
(spark, 3)
(big, 2)
(data, 2)
(world, 1)
(is, 1)
(great, 1)
(streaming, 1)
```

## 学习要点

1. **RDD 创建**：从集合、文件创建 RDD
2. **Transformation**：惰性操作，不立即执行
3. **Action**：触发计算，返回结果
4. **键值对操作**：reduceByKey、groupByKey 等
5. **分区操作**：mapPartitions 提高效率
6. **持久化**：对重复使用的 RDD 进行缓存
