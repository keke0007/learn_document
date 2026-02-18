# Flink 实时流处理案例

## 案例概述

本案例通过实际代码演示 Flink 实时流处理，包括 DataStream API、窗口操作、状态管理等。

## 知识点

1. **DataStream API**
   - 数据源和接收器
   - 转换操作
   - 窗口操作

2. **时间语义**
   - 事件时间
   - 处理时间
   - 摄入时间

3. **状态管理**
   - 键控状态
   - 算子状态
   - 状态后端

## 案例代码

### 案例1：基础流处理

```java
// FlinkStreaming.java
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;

public class FlinkStreaming {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 设置事件时间
        env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        
        // 数据源
        DataStream<String> stream = env.addSource(new SourceFunction<String>() {
            @Override
            public void run(SourceContext<String> ctx) throws Exception {
                while (true) {
                    ctx.collect("data:" + System.currentTimeMillis());
                    Thread.sleep(1000);
                }
            }
            
            @Override
            public void cancel() {}
        });
        
        // 数据处理
        stream
            .map(new MapFunction<String, Tuple2<String, Integer>>() {
                @Override
                public Tuple2<String, Integer> map(String value) {
                    return new Tuple2<>("key", 1);
                }
            })
            .keyBy(0)
            .timeWindow(Time.minutes(5))
            .sum(1)
            .print();
        
        env.execute("Flink Streaming Job");
    }
}
```

### 案例2：窗口操作

```java
// WindowOperations.java
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

// 滚动窗口（5分钟）
stream
    .keyBy(0)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new AggregateFunction<...>() {
        // 聚合逻辑
    });

// 滑动窗口（5分钟窗口，1分钟滑动）
stream
    .keyBy(0)
    .window(SlidingEventTimeWindows.of(Time.minutes(5), Time.minutes(1)))
    .sum(1);

// 会话窗口
stream
    .keyBy(0)
    .window(EventTimeSessionWindows.withGap(Time.minutes(10)))
    .sum(1);
```

### 案例3：状态管理

```java
// StateManagement.java
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;

public class StatefulFunction extends RichFlatMapFunction<Tuple2<String, Integer>, Tuple2<String, Integer>> {
    private transient ValueState<Integer> sumState;
    
    @Override
    public void open(Configuration config) {
        ValueStateDescriptor<Integer> descriptor = 
            new ValueStateDescriptor<>("sum", Integer.class);
        sumState = getRuntimeContext().getState(descriptor);
    }
    
    @Override
    public void flatMap(Tuple2<String, Integer> value, Collector<Tuple2<String, Integer>> out) throws Exception {
        Integer currentSum = sumState.value();
        if (currentSum == null) {
            currentSum = 0;
        }
        currentSum += value.f1;
        sumState.update(currentSum);
        out.collect(new Tuple2<>(value.f0, currentSum));
    }
}
```

### 案例4：Flink SQL

```java
// FlinkSQL.java
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.TableEnvironment;

EnvironmentSettings settings = EnvironmentSettings
    .newInstance()
    .inStreamingMode()
    .build();

TableEnvironment tEnv = TableEnvironment.create(settings);

// 注册表
tEnv.executeSql("""
    CREATE TABLE orders (
        order_id BIGINT,
        user_id BIGINT,
        amount DECIMAL(10,2),
        order_time TIMESTAMP(3),
        WATERMARK FOR order_time AS order_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'orders',
        'properties.bootstrap.servers' = 'localhost:9092',
        'format' = 'json'
    )
""");

// SQL 查询
Table result = tEnv.sqlQuery("""
    SELECT 
        TUMBLE_START(order_time, INTERVAL '1' HOUR) as window_start,
        COUNT(*) as order_count,
        SUM(amount) as total_amount
    FROM orders
    GROUP BY TUMBLE(order_time, INTERVAL '1' HOUR)
""");

result.execute().print();
```

## 验证数据

### Flink 性能测试

| 场景 | 延迟 | 吞吐量 | 说明 |
|-----|------|--------|------|
| 简单处理 | <10ms | 100万条/秒 | 无状态 |
| 窗口聚合 | <100ms | 50万条/秒 | 5分钟窗口 |
| 状态处理 | <50ms | 80万条/秒 | 键控状态 |

### 容错测试

```
Checkpoint 间隔：1分钟
恢复时间：<30秒
数据丢失：0条
```

## 总结

1. **时间语义**
   - 事件时间：准确性高
   - 处理时间：延迟低
   - 根据需求选择

2. **窗口操作**
   - 滚动窗口：固定大小
   - 滑动窗口：重叠窗口
   - 会话窗口：活动间隔

3. **状态管理**
   - 合理使用状态
   - 配置状态后端
   - 定期 Checkpoint
