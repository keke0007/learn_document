# Sentinel


## 1.授课思路

- 源码环境搭建
- dashboard
- 客户端client

## 2.源码环境搭建

- 架构图

  ![image-20240502130359307](sentinel.assets/image-20240502130359307.png) 

- 环境搭建

  官网地址：https://sentinelguard.io/zh-cn/index.html

  代码仓库：https://github.com/alibaba/Sentinel

  maven: 3.x，jdk: 1.8，github地址：https://github.com/alibaba/Sentinel

  ```shell
  git clone https://github.com/alibaba/Sentinel.git
  git branch 1.8.7 1.8.7
  git checkout 1.8.7
  mvn clean install -DskipTests
  ```

  构建过程中遇到问题：

  - 注释掉maven-pmd-plugin插件

  ![image-20240509102945804](sentinel.assets/image-20240509102945804.png) 

  - 注释掉sentinel-quarkus-adapter

  ![image-20240509103406312](sentinel.assets/image-20240509103406312.png)

  构建成功如下（第一次构建时间稍微长点）：

  <img src="sentinel.assets/image-20240509102140085.png" alt="image-20240509102140085" style="zoom: 80%;" /> 

## 3.sentinel核心

### 3.1 dashboard

#### 1.菜单

##### 1.首页

请求URL：http://localhost:8080/app/briefinfos.json

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "success",
    "data": [
        {
            "app": "com.alibaba.csp.sentinel.demo.annotation.aop.DemoApplication",
            "appType": 0,
            "machines": [
                {
                    "app": "com.alibaba.csp.sentinel.demo.annotation.aop.DemoApplication",
                    "appType": 0,
                    "hostname": "LAPTOP-L47MR6AE",
                    "ip": "192.168.3.38",
                    "port": 8720,
                    "lastHeartbeat": 1714661381078,
                    "heartbeatVersion": 1714661381068,
                    "version": "1.8.7",
                    "dead": false,
                    "healthy": true
                }
            ],
            "dead": false,
            "shown": true
        }
    ]
}
```



##### 2.实时监控

- 图形

  ![image-20240509105127233](sentinel.assets/image-20240509105127233.png) 

- 请求URL

  每10秒发送一次请求：

  http://localhost:8080//metric/queryTopResourceMetric.json?app=com.alibaba.csp.sentinel.demo.annotation.aop.DemoApplication&desc=true&pageIndex=1&pageSize=6

##### 3.簇点链路

流控规则+熔断规则+热点规则+授权规则 这几个菜单的综合

##### 4.流控规则  

###### 4.1 demo案例

- 首先使用 jmeter模拟请求接口 QPS是4

  ![image-20240509150628882](sentinel.assets/image-20240509150628882.png)  

  ![image-20240509151453571](sentinel.assets/image-20240509151453571.png) 

- 创建限流规则

   <img src="sentinel.assets/image-20240509151648095.png" alt="image-20240509151648095" style="zoom:80%;" />  

- 限流结果

  ![image-20240509151808610](sentinel.assets/image-20240509151808610.png) 

###### 4.2 限流效果

- 快速失败

  ```java
  package com.alibaba.csp.sentinel.slots.block.flow.controller;
  
  import com.alibaba.csp.sentinel.node.Node;
  import com.alibaba.csp.sentinel.node.OccupyTimeoutProperty;
  import com.alibaba.csp.sentinel.slots.block.RuleConstant;
  import com.alibaba.csp.sentinel.slots.block.flow.PriorityWaitException;
  import com.alibaba.csp.sentinel.slots.block.flow.TrafficShapingController;
  import com.alibaba.csp.sentinel.util.TimeUtil;
  
  /**
   * Default throttling controller (immediately reject strategy).
   *
   * @author jialiang.linjl
   * @author Eric Zhao
   */
  public class DefaultController implements TrafficShapingController {
  
      private static final int DEFAULT_AVG_USED_TOKENS = 0;
  
      private double count;
      private int grade;
  
      public DefaultController(double count, int grade) {
          this.count = count;
          this.grade = grade;
      }
  
      @Override
      public boolean canPass(Node node, int acquireCount) {
          return canPass(node, acquireCount, false);
      }
  
      @Override
      public boolean canPass(Node node, int acquireCount, boolean prioritized) {
          int curCount = avgUsedTokens(node);
          if (curCount + acquireCount > count) {
              if (prioritized && grade == RuleConstant.FLOW_GRADE_QPS) {
                  long currentTime;
                  long waitInMs;
                  currentTime = TimeUtil.currentTimeMillis();
                  waitInMs = node.tryOccupyNext(currentTime, acquireCount, count);
                  if (waitInMs < OccupyTimeoutProperty.getOccupyTimeout()) {
                      node.addWaitingRequest(currentTime + waitInMs, acquireCount);
                      node.addOccupiedPass(acquireCount);
                      sleep(waitInMs);
  
                      // PriorityWaitException indicates that the request will pass after waiting for {@link @waitInMs}.
                      throw new PriorityWaitException(waitInMs);
                  }
              }
              return false;
          }
          return true;
      }
  
      private int avgUsedTokens(Node node) {
          if (node == null) {
              return DEFAULT_AVG_USED_TOKENS;
          }
          return grade == RuleConstant.FLOW_GRADE_THREAD ? node.curThreadNum() : (int)(node.passQps());
      }
  
      private void sleep(long timeMillis) {
          try {
              Thread.sleep(timeMillis);
          } catch (InterruptedException e) {
              // Ignore.
          }
      }
  }
  
  ```

  

- warm up

  预热算法参考文章：https://blog.csdn.net/weixin_43063328/article/details/121569083

  所谓冷启动，或预热是指，系统长时间处理低水平请求状态，当大量请求突然到来时，并非所有请求都放行，而是慢慢的增加请求，目的时防止大量请求冲垮应用，达到保护应用的目的。

  ![image-20240520124336954](sentinel.assets/image-20240520124336954.png) 

  ![image-20240525224631616](sentinel.assets/image-20240525224631616.png)

  

- 排队等待

  这种方式严格控制了请求通过的间隔时间，也即是让请求以均匀的速度通过，对应的是漏桶算法

  ![image-20240520135020003](sentinel.assets/image-20240520135020003.png) 

  ![image-20240509182920148](sentinel.assets/image-20240509182920148.png) 

  发现QPS始终稳定在2,而且没有拒绝的QPS

  ![image-20240509154334668](sentinel.assets/image-20240509154334668.png)

  实现原理: 实现类ThrottlingController
  
  ![image-20240520151327536](sentinel.assets/image-20240520151327536.png) 

###### 4.3 流控模式

- 关联

  <img src="sentinel.assets/image-20240512130858195.png" alt="image-20240512130858195" style="zoom:80%;" /> 

  使用jmeter模拟请求/write,QPS=4，此时会发现read请求被限流了

  <img src="sentinel.assets/image-20240512131058351.png" alt="image-20240512131058351" style="zoom:80%;" /> 

  read请求被限流了

  <img src="sentinel.assets/image-20240512205758943.png" alt="image-20240512205758943" style="zoom:50%;" /> 

- 链路

  新增流控规则

  ![image-20240513125958233](sentinel.assets/image-20240513125958233.png) 

  使用jmeter压测端口：/test1,发现被流控

  ![image-20240513143954993](sentinel.assets/image-20240513143954993.png)

  ![image-20240513143913176](sentinel.assets/image-20240513143913176.png)

  压测路径/test2,则正常

  ![image-20240513144101113](sentinel.assets/image-20240513144101113.png)

  

  

##### 5.熔断规则  

- 慢调用比例

  <img src="sentinel.assets/image-20240522194244584.png" alt="image-20240522194244584" style="zoom:50%;" /> 

  使用jmeter压测，QPS设置5,

  ![image-20240522194651723](sentinel.assets/image-20240522194651723.png) 

  我们可以发现，每隔2秒会发送一次探测请求，发现请求失败，又被流控了

  ![image-20240522194638311](sentinel.assets/image-20240522194638311.png) 

-  异常数/异常比例

  短路器的三种状态的转换

<img src="sentinel.assets/image-20240523195207832.png" alt="image-20240523195207832" style="zoom:67%;" /> 

##### 6.热点规则  

文档：https://sentinelguard.io/zh-cn/docs/parameter-flow-control.html

- 添加依赖

  ```
  <dependency>
              <groupId>com.alibaba.csp</groupId>
              <artifactId>sentinel-parameter-flow-control</artifactId>
          </dependency>
  ```

- 新增热点参数规则

  <img src="sentinel.assets/image-20240513184806610.png" alt="image-20240513184806610" style="zoom:50%;" /> 

- 使用jmeter测试

  非热点参数，QPS=2

  <img src="sentinel.assets/image-20240513184257850.png" alt="image-20240513184257850" style="zoom:50%;" /> 

​		热点参数，WPS=6，QPS全部通过

 		![image-20240513184859240](sentinel.assets/image-20240513184859240.png) 

 

##### 7.系统规则  

https://sentinelguard.io/zh-cn/docs/system-adaptive-protection.html

![image-20240528132712421](sentinel.assets/image-20240528132712421.png) 

##### 8.授权规则  

主要是对黑白名单（调用来源）的控制

##### 9.集群流控  

官方文档：https://sentinelguard.io/zh-cn/docs/cluster-flow-control.html

整体的架构图

![image-20240518123608425](sentinel.assets/image-20240518123608425.png) 

- tokenserver的初始化流程

  ![image-20240518172623003](sentinel.assets/image-20240518172623003.png) 

- tokenclient的初始化过程

  ![image-20240518182808785](sentinel.assets/image-20240518182808785.png) 

##### 10.机器列表

机器正常：

![image-20240502224636429](sentinel.assets/image-20240502224636429.png)

机器下线：

![image-20240502224752272](sentinel.assets/image-20240502224752272.png) 



实现原理：

- 客户端发送心跳

  ![image-20240502204452661](sentinel.assets/image-20240502204452661.png) 

  

- dashboard接收心跳

  ![image-20240502220658811](sentinel.assets/image-20240502220658811.png) 

##### 11.规则持久化

文档：https://github.com/alibaba/Sentinel/wiki/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%99%E6%89%A9%E5%B1%95

- dashborad改造

  - 复制nacos目录，copy到rule规则下

    <img src="sentinel.assets/image-20240513165154161.png" alt="image-20240513165154161" style="zoom:50%;" /> 

    注意以下问题，注释掉scope

    <img src="sentinel.assets/image-20240513165353317.png" alt="image-20240513165353317" style="zoom:50%;" /> 

    

  - 修改代码改造我们nacos注册地址

    <img src="sentinel.assets/image-20240513165321705.png" alt="image-20240513165321705" style="zoom:50%;" /> 

  - 更改注入的类

    ![image-20240513170116927](sentinel.assets/image-20240513170116927.png) 

  - 改造页面取消注释

    ![image-20240513170140594](sentinel.assets/image-20240513170140594.png) 

  - 添加流控规则

    ![image-20240513170207156](sentinel.assets/image-20240513170207156.png) 

    然后在nacos中发现新增的配置

    ![image-20240513170315069](sentinel.assets/image-20240513170315069.png) 

- client改造

  - 添加pom依赖

    ```properties
<dependency>
          <groupId>com.alibaba.csp</groupId>
      <artifactId>sentinel-datasource-nacos</artifactId>
    </dependency>
  ```
    
    
    
  - 添加初始化扩展点
  
    ![image-20240513170408065](sentinel.assets/image-20240513170408065.png)
  
  - 新增初始化类
  
    ```java
    package com.alibaba.csp.sentinel.demo.annotation.aop.init;
    
    import com.alibaba.csp.sentinel.datasource.ReadableDataSource;
    import com.alibaba.csp.sentinel.datasource.nacos.NacosDataSource;
    import com.alibaba.csp.sentinel.init.InitFunc;
    import com.alibaba.csp.sentinel.slots.block.flow.FlowRule;
    import com.alibaba.csp.sentinel.slots.block.flow.FlowRuleManager;
    import com.alibaba.fastjson.JSON;
    import com.alibaba.fastjson.TypeReference;
    
    import java.util.List;
    
    public class DataSourceInitFunc implements InitFunc {
    
        @Override
      public void init() throws Exception {
            final String remoteAddress = "localhost:8848";
            final String groupId = "SENTINEL_GROUP";
            final String dataId = "com.alibaba.csp.sentinel.demo.annotation.aop.DemoApplication-flow-rules";
    
            ReadableDataSource<String, List<FlowRule>> flowRuleDataSource = new NacosDataSource<>(remoteAddress, groupId, dataId,
                source -> JSON.parseObject(source, new TypeReference<List<FlowRule>>() {}));
            FlowRuleManager.register2Property(flowRuleDataSource.getProperty());
        }
    }
    ```
  
    

#### 2.sentinel SPI机制

springboot自动装配，扫描第三方包里面的/META_INF/Service/

```
加载/META_INF/Service/文件 缓存到对应的SpiLoader这个类中
```



#### 3.配置加载

官方文档地址：https://sentinelguard.io/zh-cn/docs/general-configuration.html

```java
private static void load() {
        // 从高到低加载配置
        // Order: system property -> system env -> default file (classpath:sentinel.properties) -> legacy path
        String fileName = System.getProperty(SENTINEL_CONFIG_PROPERTY_KEY);
        if (StringUtil.isBlank(fileName)) {
            fileName = System.getenv(SENTINEL_CONFIG_ENV_KEY);
            if (StringUtil.isBlank(fileName)) {
                fileName = DEFAULT_SENTINEL_CONFIG_FILE;
            }
        }

        Properties p = ConfigUtil.loadProperties(fileName);
        if (p != null && !p.isEmpty()) {
            RecordLog.info("[SentinelConfigLoader] Loading Sentinel config from {}", fileName);
            properties.putAll(p);
        }

        for (Map.Entry<Object, Object> entry : new CopyOnWriteArraySet<>(System.getProperties().entrySet())) {
            String configKey = entry.getKey().toString();
            String newConfigValue = entry.getValue().toString();
            String oldConfigValue = properties.getProperty(configKey);
            //保证后面加载文件的优先级别计较高
            properties.put(configKey, newConfigValue);
            if (oldConfigValue != null) {
                RecordLog.info("[SentinelConfigLoader] JVM parameter overrides {}: {} -> {}",
                        configKey, oldConfigValue, newConfigValue);
            }
        }
    }
```



#### 4.命令处理器注册以及端口号监听

<img src="sentinel.assets/image-20240518125155779.png" alt="image-20240518125155779" style="zoom: 80%;" />  

| 命令名称 | 处理器                    | 作用     |
| -------- | ------------------------- | -------- |
| setRules | ModifyRulesCommandHandler | 修改规则 |
| metric   |                           |          |



#### 5.处理器链条的构建

![image-20240506214334599](sentinel.assets/image-20240506214334599.png) 

#### 6.滑动时间窗口统计QPS

![image-20240516121134227](sentinel.assets/image-20240516121134227.png)



#### 

 

