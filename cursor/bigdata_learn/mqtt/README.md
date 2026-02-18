# MQTT 学习总览

`mqtt/` 模块整理了 MQTT 在物联网与消息传输中的主要知识点，并将它们与 `cases/` + `data/` + `scripts/` 中的案例和验证数据对应起来。

---

## 一、核心知识点概览

- 发布/订阅模型（Pub/Sub）。
- Topic 与通配符（`+`、`#`）。
- QoS 等级（0/1/2）。
- 保留消息、遗嘱消息、会话保持（clean session）。

---

## 二、知识点与案例/数据对照表

| 模块                 | 关键知识点                          | 案例文档                  | 数据文件                 | 脚本文件                    |
|----------------------|-------------------------------------|---------------------------|--------------------------|-----------------------------|
| 基础发布/订阅        | Topic、QoS 0/1/2、基础 pub/sub       | `basic_pub_sub.md`        | `sensor_payloads.json`   | `basic_pub_sub.sh`         |
| 传感器上报           | Topic 设计、JSON payload 结构       | `iot_sensors.md`          | `sensor_payloads.json`   | `iot_sensors.sh`           |
| 设备控制             | 控制指令主题、可靠性与 QoS 选择     | `device_control.md`       | `control_payloads.json`  | `device_control.sh`        |

---

## 三、如何使用本模块学习

1. 阅读 `GUIDE.md`，了解 MQTT 核心概念与学习路径。
2. 启动本地或测试 MQTT Broker（如 Mosquitto），使用 `mosquitto_sub` / `mosquitto_pub` 或其它客户端。
3. 根据 `cases/` 文档，使用 `scripts/` 中的脚本发布/订阅 `data/` 中示例 payload，对照输出结果理解 Topic 与 QoS 行为。

当你能够：

- 熟练编写与订阅不同 Topic；  
- 正确选择 QoS 等级与 Topic 命名；  
- 使用 JSON payload 表达 IoT 业务数据；

就基本具备了在项目中使用 MQTT 的核心能力。

