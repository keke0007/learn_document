# 案例1：基础发布/订阅与 QoS（MQTT）

## 一、案例目标

- 搭建最简单的 MQTT 发布/订阅链路。
- 体验 QoS 0/1/2 的基本差异。

---

## 二、准备工作

- 启动本地 MQTT Broker（如 Mosquitto）：

```bash
mosquitto -p 1883
```

---

## 三、订阅与发布示例

### 1. QoS 0：最多一次

订阅：

```bash
mosquitto_sub -h localhost -p 1883 -t "test/qos0" -q 0
```

发布：

```bash
mosquitto_pub -h localhost -p 1883 -t "test/qos0" -m "hello qos0" -q 0
```

### 2. QoS 1：至少一次

订阅：

```bash
mosquitto_sub -h localhost -p 1883 -t "test/qos1" -q 1
```

发布：

```bash
mosquitto_pub -h localhost -p 1883 -t "test/qos1" -m "hello qos1" -q 1
```

### 3. QoS 2：仅一次（如 Broker 支持）

订阅：

```bash
mosquitto_sub -h localhost -p 1883 -t "test/qos2" -q 2
```

发布：

```bash
mosquitto_pub -h localhost -p 1883 -t "test/qos2" -m "hello qos2" -q 2
```

---

## 四、练习建议

1. 使用 `-r` 选项发布保留消息，观察新订阅客户端的行为。  
2. 使用通配符主题（如 `test/#`）订阅多个 Topic。  

