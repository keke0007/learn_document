# 案例3：设备控制指令下发（MQTT）

## 一、案例目标

- 设计服务端向设备下发控制指令的 Topic。
- 使用 JSON payload 表达开关/配置更新等操作。

---

## 二、Topic 设计

- 设备控制指令：
  - `devices/<deviceId>/control`
  - 示例：`devices/device1/control`

---

## 三、示例 payload（见 `data/control_payloads.json`）

```json
{
  "cmd": "set_threshold",
  "sensor": "temperature",
  "value": 30,
  "ts": "2024-03-14T10:05:00Z"
}
```

或简单开关控制：

```json
{
  "cmd": "switch",
  "target": "relay1",
  "state": "ON"
}
```

---

## 四、订阅与发布示例

设备侧订阅控制指令：

```bash
mosquitto_sub -h localhost -p 1883 -t "devices/device1/control" -q 1
``>

服务端发布控制指令：

```bash
mosquitto_pub -h localhost -p 1883 \
  -t "devices/device1/control" \
  -m '{"cmd":"switch","target":"relay1","state":"ON","ts":"2024-03-14T10:05:00Z"}' \
  -q 1
```

---

## 五、练习建议

1. 思考控制指令的可靠性要求，并尝试用不同 QoS 等级实验消息交付行为。  
2. 结合日志/时序系统记录设备执行控制指令的结果，形成“命令-执行-反馈”闭环。  

