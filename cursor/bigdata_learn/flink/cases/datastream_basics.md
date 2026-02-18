# 案例1：DataStream 基础操作

## 案例描述
学习 Flink DataStream API 的基本操作，包括数据源、转换和输出。

## 数据准备

### 数据文件 (words.txt)
```
hello world
hello flink
flink is great
stream processing
flink streaming
hello stream processing
```

### 数据文件 (numbers.txt)
```
1,2,3,4,5
6,7,8,9,10
11,12,13,14,15
```

## Java 实现

### 完整代码 (DataStreamBasics.java)
```java
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.ReduceFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.util.Collector;

import java.util.Arrays;

public class DataStreamBasics {
    public static void main(String[] args) throws Exception {
        // 创建执行环境
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // ============================================
        // 1. 从集合创建数据流
        // ============================================
        
        DataStream<Integer> numbers = env.fromCollection(
            Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        );
        
        System.out.println("从集合创建的数据流:");
        numbers.print();
        
        // ============================================
        // 2. 从文件创建数据流
        // ============================================
        
        DataStream<String> lines = env.readTextFile("data/words.txt");
        
        System.out.println("\n从文件读取的数据:");
        lines.print();
        
        // ============================================
        // 3. Transformation 操作
        // ============================================
        
        // map: 一对一转换
        DataStream<Integer> doubled = numbers.map(new MapFunction<Integer, Integer>() {
            @Override
            public Integer map(Integer value) throws Exception {
                return value * 2;
            }
        });
        System.out.println("\n每个数字乘以2:");
        doubled.print();
        
        // 使用 Lambda 表达式
        DataStream<Integer> tripled = numbers.map(x -> x * 3);
        System.out.println("\n每个数字乘以3:");
        tripled.print();
        
        // filter: 过滤
        DataStream<Integer> evens = numbers.filter(x -> x % 2 == 0);
        System.out.println("\n偶数:");
        evens.print();
        
        // flatMap: 一对多转换
        DataStream<String> words = lines.flatMap(new FlatMapFunction<String, String>() {
            @Override
            public void flatMap(String value, Collector<String> out) throws Exception {
                String[] words = value.split(" ");
                for (String word : words) {
                    out.collect(word);
                }
            }
        });
        
        // 使用 Lambda 表达式
        DataStream<String> wordsLambda = lines.flatMap(
            (String line, Collector<String> out) -> {
                Arrays.stream(line.split(" ")).forEach(out::collect);
            }
        );
        
        System.out.println("\n所有单词:");
        wordsLambda.print();
        
        // ============================================
        // 4. 键值对操作
        // ============================================
        
        // 转换为键值对
        DataStream<Tuple2<String, Integer>> wordPairs = wordsLambda
            .map(word -> new Tuple2<>(word, 1));
        
        // keyBy 和 reduce
        DataStream<Tuple2<String, Integer>> wordCounts = wordPairs
            .keyBy(0)
            .reduce(new ReduceFunction<Tuple2<String, Integer>>() {
                @Override
                public Tuple2<String, Integer> reduce(
                    Tuple2<String, Integer> value1,
                    Tuple2<String, Integer> value2
                ) throws Exception {
                    return new Tuple2<>(value1.f0, value1.f1 + value2.f1);
                }
            });
        
        System.out.println("\n单词计数:");
        wordCounts.print();
        
        // 使用 Lambda 表达式
        DataStream<Tuple2<String, Integer>> wordCountsLambda = wordPairs
            .keyBy(0)
            .reduce((a, b) -> new Tuple2<>(a.f0, a.f1 + b.f1));
        
        // ============================================
        // 5. 数据输出
        // ============================================
        
        // 打印输出
        wordCountsLambda.print("WordCount");
        
        // 保存到文件
        wordCountsLambda.writeAsText("output/word_counts");
        
        // ============================================
        // 6. 执行作业
        // ============================================
        
        env.execute("DataStream Basics");
    }
}
```

### 运行方式
```bash
# 编译
mvn clean package

# 运行
flink run target/flink-basics-1.0.jar
```

## Scala 实现

### 完整代码 (DataStreamBasics.scala)
```scala
import org.apache.flink.api.scala._
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment

object DataStreamBasics {
  def main(args: Array[String]): Unit = {
    // 创建执行环境
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    
    // ============================================
    // 1. 从集合创建数据流
    // ============================================
    
    val numbers = env.fromCollection(Seq(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    
    println("从集合创建的数据流:")
    numbers.print()
    
    // ============================================
    // 2. 从文件创建数据流
    // ============================================
    
    val lines = env.readTextFile("data/words.txt")
    
    println("\n从文件读取的数据:")
    lines.print()
    
    // ============================================
    // 3. Transformation 操作
    // ============================================
    
    // map: 一对一转换
    val doubled = numbers.map(_ * 2)
    println("\n每个数字乘以2:")
    doubled.print()
    
    // filter: 过滤
    val evens = numbers.filter(_ % 2 == 0)
    println("\n偶数:")
    evens.print()
    
    // flatMap: 一对多转换
    val words = lines.flatMap(_.split(" "))
    
    println("\n所有单词:")
    words.print()
    
    // ============================================
    // 4. 键值对操作
    // ============================================
    
    // 转换为键值对并计数
    val wordCounts = words
      .map((_, 1))
      .keyBy(0)
      .sum(1)
    
    println("\n单词计数:")
    wordCounts.print()
    
    // ============================================
    // 5. 数据输出
    // ============================================
    
    // 打印输出
    wordCounts.print("WordCount")
    
    // 保存到文件
    wordCounts.writeAsText("output/word_counts")
    
    // ============================================
    // 6. 执行作业
    // ============================================
    
    env.execute("DataStream Basics")
  }
}
```

### 运行方式
```bash
# 编译
sbt clean package

# 运行
flink run target/scala-2.12/flink-basics_2.12-1.0.jar
```

## 预期结果

### 单词计数结果
```
(hello, 3)
(flink, 3)
(world, 1)
(is, 1)
(great, 1)
(stream, 2)
(processing, 2)
(streaming, 1)
```

## 学习要点

1. **执行环境**：StreamExecutionEnvironment
2. **数据源**：fromCollection、readTextFile
3. **转换操作**：map、filter、flatMap
4. **键值对操作**：keyBy、reduce
5. **数据输出**：print、writeAsText
6. **作业执行**：execute() 触发执行
