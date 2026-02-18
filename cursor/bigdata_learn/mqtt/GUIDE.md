## MQTT 学习指南（物联网 & 消息传输）

## 📚 项目概述

本指南在 `mqtt/` 目录下，参考其他模块（如 `redis/`、`influxDB/`、`mongoDB/` 等）的组织方式，提供一套系统的 **MQTT 学习路径**，重点覆盖：

- **核心知识点**：发布/订阅模型、主题与通配符、QoS 等级、保留消息、遗嘱消息、会话与持久订阅。
- **案例场景**：设备上报传感器数据、服务端下发控制指令、简单 IoT 仪表盘。
- **验证数据**：小规模示例 payload（JSON），方便在本地或测试 MQTT Broker 中动手练习。

---

## 📁 项目结构

```
mqtt/
├── README.md                        # MQTT 知识点总览（详细文档）
├── GUIDE.md                         # 本指南文档（学习路径 + 快速上手）
├── cases/                           # 实战案例目录
│   ├── basic_pub_sub.md             # 案例1：基础发布/订阅与 QoS
│   ├── iot_sensors.md               # 案例2：传感器数据上报与订阅
│   └── device_control.md            # 案例3：设备控制指令下发
├── data/                            # 验证数据（JSON payload 示例）
│   ├── sensor_payloads.json         # 传感器上报示例
│   └── control_payloads.json        # 控制指令示例
└── scripts/                         # mosquitto_pub/sub 或其它 CLI 示例
    ├── basic_pub_sub.sh             # 基础发布/订阅命令
    ├── iot_sensors.sh               # 传感器主题发布示例
    └── device_control.sh            # 控制主题发布示例
```

---

## 🎯 学习路径（建议 1~2 天）

### 阶段一：基础概念（0.5 天）

- MQTT 协议特点：轻量、基于 TCP、发布/订阅模型。
- Broker / Client / Topic 概念。

### 阶段二：核心特性（0.5~1 天）

- QoS 等级：0（最多一次）、1（至少一次）、2（仅一次）。
- 主题与通配符：`/` 层级、`+` 单层、`#` 多层。
- 保留消息（Retained Message）、遗嘱消息（Last Will）。

### 阶段三：实战场景（0.5~1 天）

- 设备上报传感器数据（案例2）。
- 服务端下发控制指令（案例3）。
- 匹配订阅主题设计与 QoS 选择。

---

## 🚀 快速开始

> 以下示例假设你已安装 Mosquitto 或其他 MQTT Broker，并能通过 `localhost:1883` 访问。

### 步骤1：订阅主题

```bash
# 订阅所有设备的温度上报
mosquitto_sub -h localhost -p 1883 -t "devices/+/sensors/temperature" -q 1
```

### 步骤2：发布测试消息

```bash
mosquitto_pub -h localhost -p 1883 -t "devices/device1/sensors/temperature" -m '{"value": 23.5, "unit": "C"}' -q 1
```

更多命令可参考 `scripts/` 下的脚本。

---

## 📖 核心知识点速查

- **Topic 设计**：`devices/<deviceId>/sensors/<sensorType>`、`devices/<deviceId>/control` 等。
- **QoS 选择**：日志型数据用 QoS 0/1，关键控制指令可考虑 QoS 1 或 QoS 2。
- **会话与持久订阅**：`clean session` / `session expiry`。

---

## 📊 验证数据说明

- `data/sensor_payloads.json`：包含温度/湿度等 JSON payload 示例。
- `data/control_payloads.json`：包含开关设备、更新配置等控制指令示例。

---

## 🔧 实战案例概览

- `basic_pub_sub.md`：从最简单的发布/订阅与 QoS 实验开始。
- `iot_sensors.md`：模拟多个设备定期上报传感器数据，订阅端聚合展示。
- `device_control.md`：模拟服务端向设备主题发送控制指令，客户端响应。

---

## ✅ 学习检查清单

- [ ] 能使用命令行客户端订阅和发布 MQTT 消息。
- [ ] 理解并合理选择不同 QoS 等级。
- [ ] 能设计清晰且可扩展的 Topic 命名。

---

## 🎓 学习成果

完成本指南后，你将能够：

- 在本地或测试环境中搭建简易 MQTT 消息通道。
- 为 IoT 场景设计合适的主题结构与 QoS 策略。
- 将 MQTT 与其他大数据/时序组件（如 InfluxDB、Elasticsearch）组合，构建采集 + 存储 + 分析的完整链路。

