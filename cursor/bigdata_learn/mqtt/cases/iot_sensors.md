# 案例2：传感器数据上报与订阅（MQTT）

## 一、案例目标

- 设计 IoT 设备上传感器数据的 Topic 结构。
- 使用 JSON payload 上报温度/湿度等数据并进行订阅查看。

---

## 二、Topic 设计

- 设备上报传感器数据：
  - `devices/<deviceId>/sensors/<sensorType>`
  - 示例：`devices/device1/sensors/temperature`

---

## 三、示例 payload（见 `data/sensor_payloads.json`）

```json
{
  "value": 23.5,
  "unit": "C",
  "ts": "2024-03-14T10:00:01Z"
}
```

---

## 四、订阅与发布示例

订阅所有设备的温度上报：

```bash
mosquitto_sub -h localhost -p 1883 -t "devices/+/sensors/temperature" -q 1
```

模拟 device1 上报温度：

```bash
mosquitto_pub -h localhost -p 1883 \
  -t "devices/device1/sensors/temperature" \
  -m '{"value": 23.5, "unit": "C", "ts": "2024-03-14T10:00:01Z"}' \
  -q 1
```

---

## 五、练习建议

1. 为湿度、压力等不同传感器类型设计相应 Topic，并用 `+` 通配符一次性订阅。  
2. 结合 InfluxDB/Elasticsearch，将订阅到的传感器数据写入时序/搜索系统以便后续分析。  

