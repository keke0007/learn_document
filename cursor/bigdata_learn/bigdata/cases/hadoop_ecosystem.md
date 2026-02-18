# Hadoop 生态系统案例

## 案例概述

本案例通过实际命令和代码演示 Hadoop 生态系统的使用，包括 HDFS、MapReduce、YARN 等。

## 知识点

1. **HDFS**
   - 文件系统操作
   - 副本机制
   - 数据存储

2. **MapReduce**
   - 编程模型
   - 作业提交
   - 性能优化

3. **YARN**
   - 资源管理
   - 应用提交
   - 监控管理

## 案例代码

### 案例1：HDFS 操作

```bash
#!/bin/bash
# hdfs_operations.sh

# 创建目录
hdfs dfs -mkdir -p /data/input
hdfs dfs -mkdir -p /data/output

# 上传文件
hdfs dfs -put local_file.txt /data/input/
hdfs dfs -put -f local_file.txt /data/input/  # 强制覆盖

# 查看文件
hdfs dfs -ls /data/input
hdfs dfs -ls -R /data  # 递归查看
hdfs dfs -cat /data/input/file.txt

# 下载文件
hdfs dfs -get /data/output/result.txt ./local_result.txt

# 删除文件
hdfs dfs -rm /data/old_file.txt
hdfs dfs -rm -r /data/old_directory  # 递归删除

# 查看文件系统使用情况
hdfs dfs -df -h
hdfs dfsadmin -report

# 设置副本数
hdfs dfs -setrep -w 3 /data/important_file.txt

# 查看文件块信息
hdfs fsck /data/input/file.txt -files -blocks -locations
```

### 案例2：MapReduce WordCount

```java
// WordCount.java
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {
    public static class TokenizerMapper 
        extends Mapper<Object, Text, Text, IntWritable> {
        
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        
        @Override
        public void map(Object key, Text value, Context context) 
            throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }
    
    public static class IntSumReducer 
        extends Reducer<Text, IntWritable, Text, IntWritable> {
        
        private IntWritable result = new IntWritable();
        
        @Override
        public void reduce(Text key, Iterable<IntWritable> values, 
                          Context context) 
            throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
    
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

### 案例3：YARN 应用提交

```bash
#!/bin/bash
# yarn_submit.sh

# 提交 MapReduce 作业
yarn jar hadoop-examples.jar wordcount \
    /data/input \
    /data/output

# 查看运行中的应用
yarn application -list

# 查看应用详情
yarn application -status application_1234567890_0001

# 查看应用日志
yarn logs -applicationId application_1234567890_0001

# 杀死应用
yarn application -kill application_1234567890_0001

# 查看节点状态
yarn node -list -all
```

## 验证数据

### HDFS 性能测试

| 操作 | 数据量 | 耗时 | 说明 |
|-----|--------|------|------|
| 写入 | 1GB | 30s | 3副本 |
| 读取 | 1GB | 15s | 本地读取 |
| 复制 | 1GB | 45s | 跨节点 |

### MapReduce 性能

| 数据量 | Map 任务数 | Reduce 任务数 | 执行时间 |
|--------|-----------|--------------|---------|
| 10GB | 80 | 10 | 5min |
| 100GB | 800 | 20 | 45min |
| 1TB | 8000 | 50 | 6h |

## 总结

1. **HDFS**
   - 适合大文件存储
   - 副本保证可靠性
   - 流式访问模式

2. **MapReduce**
   - 适合批处理
   - 自动容错
   - 数据本地性优化

3. **YARN**
   - 统一资源管理
   - 多应用支持
   - 动态资源分配
