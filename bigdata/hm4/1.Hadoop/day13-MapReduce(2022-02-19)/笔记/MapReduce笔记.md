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



## JavaBean参与MapReduce

+ 1:在MR中，如果有自定义类，则该类必须要能够被序列化,实现Writable接口

  ```java
  public class CovidCountBean implements Writable {
      private int  cases;//累计确诊病例数
      private int  deaths;//累计死亡病例数
      
  }
  ```

  

+ 2:重写接口中的方法

  ```java
      //序列化方法:反序列化的顺序一定要和序列化顺序一致
      @Override
      public void write(DataOutput dataOutput) throws IOException {
          dataOutput.writeInt(cases);
          dataOutput.writeInt(deaths);
      }
  
      //反序列化方法:反序列化的顺序一定要和序列化顺序一致
      @Override
      public void readFields(DataInput dataInput) throws IOException {
          this.cases = dataInput.readInt();
          this.deaths = dataInput.readInt();
      }
  ```

   

## MapReduce中的分区

### 概述

+ 分区的关键字：partition

+ 分区的意义实际上就是对K2和V2进行标记，相同标记的数据以后会被分到同一个reduce

+ 分区的标记编号必须从0开始（可以这样理解，0表示这个键值对以后会被第一个Reduce拉取）

+ 如果设置了分区，则一般Reduce的个数要大于等于分区的个数

+ 当没有设置分区时，MapReduce有自己默认的分区，用的机制是Hash

  ![image-20220219141009341](image\image-20220219141009341.png)

### 意义

+ 在实际应用中分区的意义是将数据分散到不同的reduce去处理，避免大量数据都集中到一个reduce，造成数据倾斜

### 操作

1. 正常编写Map代码
2. 写分区代码
   + 自定义类继承Partitioner类
   + 重写getPartition方法，在该方法中对每一个K2和V2打标记

3. 正常编写Reduce代码
4. 编写主类代码，在主类中要指定两个内容
   + 指定自定义分区类的名字： job.setPartitionerClass(StatePartitioner.class);
   + 指定Reduce的个数：         job.setNumReduceTasks(6);



## MapReduce的排序

### 概述

+ MapReduce的Shuffle有默认的排序，是按照K2进行排序，排序的规则是字典顺序
+ 如果默认的排序规则不满足我们的需求，则我们需要自定义排序规则
+ MapReduce的排序不需要我们自己来完成，你只需要制定排序的规则即可（即按照哪个字段排）
+ MapReduce只能按照K2排序，所以你要将哪个字段作为排序的依据，则需要将字段包含在K2中

### 操作

+ 1：JavaBean类实现一个接口：WritableComparable
+ 2：重写compareTo方法，在该方法中制定排序规则

```java
//第一种方式
public class CovidBean implements Writable,Comparable<CovidBean> {
    //制定比较规则
    @Override
    public int compareTo(CovidBean o) {
        return 0;
    }

    //实现序列化
    @Override
    public void write(DataOutput dataOutput) throws IOException {

    }

    //实现反序列化
    @Override
    public void readFields(DataInput dataInput) throws IOException {

    }
    
}
//源码
public interface WritableComparable<T> extends Writable, Comparable<T> {
}

//第二种方式

public class CovidBean implements WritableComparable<CovidBean> {
        //制定比较规则
    @Override
    public int compareTo(CovidBean o) {
        return 0;
    }

    //实现序列化
    @Override
    public void write(DataOutput dataOutput) throws IOException {

    }

    //实现反序列化
    @Override
    public void readFields(DataInput dataInput) throws IOException {

}
```



## MapReduce的Combiner(规约)

### 概念

+ Combiner是MR的一种优化手段，可有可无
+ Combiner是MR在Map阶段对数据做提前的合并，减少Map和Reduce之间数据传输的数据量
+ Combiner其实就是（分组+Reduce），只是它是在每一个Map阶段后进行，而普通的Reduce是对所有Map的结果进行整体汇总
+ Combiner虽好，但是不是所有的情况都能使用，有些时候如果使用了Combiner，会影响最终的结果，这样得不偿失

### 操作

```java
//1:定义类继承Reduce类，重写reduce方法 ,如果Combiner代码和Reducer代码一样，则可以不用写，直接在主类中指定Combiner类为Reducer即可。

//2:在主类中指定Combiner类名
job.setCombinerClass(WordCountReducer.class);
```



## MapReduce的分组



### 操作

1. 自定义类继承**WritableComparator**类
2. 在自定义类中定义无参构造，在无参构造中调用父类的构造方法
3. 重写compare方法，在该方法中指定分组规则
4. 在主类中指定自定义分组类名

