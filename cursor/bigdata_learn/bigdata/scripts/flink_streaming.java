/**
 * Flink 实时流处理示例
 * 演示 Flink DataStream API 的使用
 */

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.ReduceFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;

import java.util.Properties;

public class FlinkStreaming {
    public static void main(String[] args) throws Exception {
        // 创建流执行环境
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 设置事件时间
        env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        
        // Kafka 配置
        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("bootstrap.servers", "localhost:9092");
        kafkaProps.setProperty("group.id", "flink-consumer-group");
        
        // 从 Kafka 读取数据
        DataStream<String> stream = env
            .addSource(new FlinkKafkaConsumer<>(
                "input-topic",
                new SimpleStringSchema(),
                kafkaProps
            ));
        
        // 数据转换
        DataStream<Tuple2<String, Integer>> parsed = stream
            .map(new MapFunction<String, Tuple2<String, Integer>>() {
                @Override
                public Tuple2<String, Integer> map(String value) {
                    String[] parts = value.split(",");
                    return new Tuple2<>(parts[0], Integer.parseInt(parts[1]));
                }
            });
        
        // 窗口聚合
        DataStream<Tuple2<String, Integer>> result = parsed
            .keyBy(0)
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .reduce(new ReduceFunction<Tuple2<String, Integer>>() {
                @Override
                public Tuple2<String, Integer> reduce(
                    Tuple2<String, Integer> value1,
                    Tuple2<String, Integer> value2) {
                    return new Tuple2<>(value1.f0, value1.f1 + value2.f1);
                }
            });
        
        // 输出结果
        result.print();
        
        // 执行作业
        env.execute("Flink Streaming Job");
    }
}
