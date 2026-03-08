# nacos源码分析

### 授课思路

- 目标人群

  主要定位还是有工作经验和对底层感兴趣的小伙伴

- 授课方式

  笔记+processon画图+源码

- 源码环境搭建

  搭建3台机器的nacos集群，nacos版本：2.2.0，JDK版本：1.8+，maven版本：3.2+

  参考官方文档：https://nacos.io/zh-cn/docs/cluster-mode-quick-start.html

  - 下载nacos源码

    ![image-20230524205926132](nacos笔记.assets/image-20230524205926132.png)  

  - 导入IDEA

    ```shell
    //以tag2.2.0创建分支  分支名称2.2.0
    git branch 2.2.0 2.2.0
    //切换到分支2.2.0
    git checkout 2.2.0
    ```
  
  - 执行命令：mvn clean install -DskipTests，遇到如下问题
  
    ![image-20230524211007303](nacos笔记.assets/image-20230524211007303.png)
  
    使用如下命令：mvn clean install -DskipTests -Drat.skip=true
  
    ![image-20230524211154563](nacos笔记.assets/image-20230524211154563.png)
  
      注释插件
  
    ![image-20230524211505104](nacos笔记.assets/image-20230524211505104.png)
  
    
  
    代码检查问题，注视掉maven-checkstyle-plugin
  
    ![image-20230903114820961](nacos笔记.assets/image-20230903114820961.png)
  
    
  
      成功构建
  
    ![image-20230524102429570](nacos笔记.assets/image-20230524102429570.png) 
  
  - 本地启动3台nacos服务，端口8848,8850,8852，配置如下
  
    ![image-20230524114822361](nacos笔记.assets/image-20230524114822361.png)  
  
    ![image-20230524114926387](nacos笔记.assets/image-20230524114926387.png) 
  
    修改配置文件
  
    ![image-20230524214405581](nacos笔记.assets/image-20230524214405581.png)
  
     
    
    启动成功后访问任意一台nacos机器：http://192.168.30.38:8848/nacos/index.html,用户名:nacos，密码：nacos
    
    ![image-20230524104435197](nacos笔记.assets/image-20230524104435197.png)
    
    ![image-20230524110439327](nacos笔记.assets/image-20230524110439327.png) 



- 服务注册流程
- 配置发布流程
- 插件机制

### 架构图

nacos的核心架构图，也是我们整个课程体系的核心，我们将围绕这个架构图来分析各个功能，比如回调机制，寻址机制

![image-20230524142721392](nacos笔记.assets/image-20230524142721392.png)



### 1.启动流程

| 9848 | 1000  | 客户端gRPC请求服务端端口，用于客户端向服务端发起连接和请求 |
| ---- | ----- | ---------------------------------------------------------- |
| 9849 | 1001  | 服务端gRPC请求服务端端口，用于服务间同步等                 |
| 7848 | -1000 | Jraft请求服务端端口，用于处理服务端间的Raft相关请求        |

- jraft协议初始化 

  端口号: server.port - 1000，raft协议使用的服务器，包括选举，心跳等

  processon流程图: client -> server网络通信

  

- GrpcSdkServer

  注册俩个请求接收器，

  一个是普通请求：grpcCommonRequestAcceptor.request

  一个是双向流PRC：grpcBiStreamRequestAcceptor.requestBiStream

  端口号: server.port + 1000, client->server端使用的服务器 

  processon流程图: client-> server网络通信

  

- GrpcClusterServer

  一个是普通请求：grpcCommonRequestAcceptor.request

  一个是双向流PRC：grpcBiStreamRequestAcceptor.requestBiStream
  
  端口号: server.port + 1001 server->server端使用的服务器 
  
  processon流程图: server-> server网络通信
  
  

### 2.服务发现模块

#### 2.0 领域模型

- 数据模型

  <img src="nacos笔记.assets/image-20230602100421394.png" alt="image-20230602100421394" style="zoom:50%;" /> 

- 服务领域模型

  <img src="nacos笔记.assets/image-20230602100451831.png" alt="image-20230602100451831" style="zoom:50%;" /> 

#### 2.1 服务注册

- Grpc 服务注册流程

  ![image-20230602104522876](nacos笔记.assets/image-20230602104522876.png) 

- Http服务注册流程

  ![image-20230602105657524](nacos笔记.assets/image-20230602105657524.png) 



#### 2.2 心跳检测

- 客户端定时心跳

  - HTTP方式

    定时发送http请求：/nacos/v1/ns/instance/beat 

    ![image-20230602145746981](nacos笔记.assets/image-20230602145746981.png)

  - GRPC方式

    构造HealthCheckRequest请求

    ![image-20230602150114259](nacos笔记.assets/image-20230602150114259.png)

- 服务端接收心跳

  - HTTP方式

    更新最后一次心跳时间

    ![image-20230602151114972](nacos笔记.assets/image-20230602151114972.png)

    

  - GRPC方式

    直接返回，这里不需要更新client的最后一次更新时间，因为是长链接，可以在链接断开的时候动态感知到

    ![image-20230602151250753](nacos笔记.assets/image-20230602151250753.png) 

- 服务端心跳检测

  - 代码入口

    <img src="nacos笔记.assets/image-20230602110111225.png" alt="image-20230602110111225" style="zoom:50%;" /> 

   

  - 临时实例

    ![image-20230602113716558](nacos笔记.assets/image-20230602113716558.png) 

  - 持久化实例

    <img src="nacos笔记.assets/image-20230602143923380.png" alt="image-20230602143923380" style="zoom:50%;" /> 

​	

#### 2.3 服务下线

- 页面操作 服务的上下线

  ![image-20230602153020077](nacos笔记.assets/image-20230602153020077.png) 

  InstanceController->update

  ![image-20230602153118742](nacos笔记.assets/image-20230602153118742.png) 

​		通过CP协议更新元数据信息<img src="nacos笔记.assets/image-20230602153151071.png" alt="image-20230602153151071" style="zoom:50%;" />

#### 2.4 服务订阅

- GRPC服务订阅

  推送的方式

  ![image-20231112165539007](nacos笔记.assets/image-20231112165539007.png)  

- HTTP服务拉取

  总体就是 刚启动立即拉取+10S后定时拉取 + 订阅推送 推拉结合 服务实例的更新

  ![image-20230602174229930](nacos笔记.assets/image-20230602174229930.png) 

​		



#### 2.5 服务查询

- http方式

  CatalogController.instances() ->  serviceStorage.getData(service)

  

- GRPC方式

  ServiceQueryRequestHandler.handle() -> serviceStorage.getData(service)

  

### 3.配置模块

#### 3.0 领域模型

<img src="nacos笔记.assets/image-20230602100607260.png" alt="image-20230602100607260" style="zoom:50%;" /> 

#### 3.1 配置流程

![image-20230524145225819](nacos笔记.assets/image-20230524145225819.png)

<img src="nacos笔记.assets/image-20230524145120289.png" alt="image-20230524145120289" style="zoom:50%;" /> 

#### 3.2 配置发布

无论哪种方式，最后调用的都是同一个接口的方法，同一份配置数据会写 DB+缓存+文件

- HTTP接口方式

  请求地址：http://192.168.30.38:8848/nacos/v1/cs/configs

  请求参数：

  ![image-20230606110857412](nacos笔记.assets/image-20230606110857412.png)

  完整的发布时序图参考processon:   配置发布流程

- SDK方式

  ![image-20230606151047407](nacos笔记.assets/image-20230606151047407.png) 

#### 3.3 配置订阅

- http方式

  - 注册监听器

    ```
    NacosContextRefresher.onApplicationEvent -> configService.addListener(dataId, group, listener);
    ```

  - 完整时序图

    ![image-20230607145144948](nacos笔记.assets/image-20230607145144948.png)  最后一步刷新spring属性的原理图可以参考博客：https://blog.csdn.net/Apandam/article/details/130781918

- GRPC方式

  - 时序图

    ![image-20230607173326449](nacos笔记.assets/image-20230607173326449.png) 

    

#### 3.4 配置查询

- http

  入口：ConfigController.getConfig 查询文件数据然后返回

  ```。
  file = DiskUtil.targetFile(dataId, group, tenant);
  ```

- GRPC

  入口：ConfigQueryRequestHandler.handler 查询文件数据然后返回

  ```
  file = DiskUtil.targetFile(dataId, group, tenant);
  ```

  

#### 3.5 灰度发布

- 新增灰度配置

  灰度配置新增完成之后，会根据灰度的IP地址过滤掉不属于灰度的IP，来推送配置信息

  ![image-20230608142805955](nacos笔记.assets/image-20230608142805955.png) 

  

  查询的时候返回灰度的配置，俩种类型的代码逻辑是类似的

  GRPC：ConfigQueryResponse

  ![image-20230608151314004](nacos笔记.assets/image-20230608151314004.png) 

  HTTP方式

  ![image-20230608151443789](nacos笔记.assets/image-20230608151443789.png) 

- 停止灰度

  ![image-20230608151632954](nacos笔记.assets/image-20230608151632954.png) 

  一旦停止灰度，则对应的缓存没有响应的灰度的标记位，此时灰度IP的客户单来拉取的时候就是最新的配置了

  

- 灰度发布

  俩个流程的结合：

  首先发送：配置修改请求，使用灰度的配置来修改当前的配置

  其次发送：灰度删除请求

#### 3.6 多版本管理&配置回滚

<img src="nacos笔记.assets/image-20230608104841570.png" alt="image-20230608104841570" style="zoom:50%;" /> 

#### 3.7 其他概念的一些解释

参考文章：https://zhuanlan.zhihu.com/p/557028685?utm_id=0

### 4.核心机制

#### 4.1 一致性协议

##### 4.1.1 协议抽象

![image-20230524152918779](nacos笔记.assets/image-20230524152918779.png) 

##### 4.1.2 AP协议

自研的distro协议，主要算法过程如下

- 启动阶段

  ![image-20230524153518190](nacos笔记.assets/image-20230524153518190.png) 

  

- 数据校验

  ![image-20230524153540475](nacos笔记.assets/image-20230524153540475.png)

- 写数据

  ![image-20230524153732149](nacos笔记.assets/image-20230524153732149.png)

  ![image-20230524153702273](nacos笔记.assets/image-20230524153702273.png) 

- 读数据

  ![image-20230524153831243](nacos笔记.assets/image-20230524153831243.png) 

- 源码分析 

  processon流程图：AP协议，详细分析上面的4个流程，写请求, 数据校验， 全量拉取，读请求

  ![image-20230530173918347](nacos笔记.assets/image-20230530173918347.png)

##### 4.1.3 CP协议

- 介绍

  ![image-20230525170349395](nacos笔记.assets/image-20230525170349395.png)

  

- 先看下CP协议的动画版，理解下什么是raft协议

  http://thesecretlivesofdata.com/raft/

  - leader选举的过程

    - 心跳

  - 写日志的过程

    - 日志复制 过半节点写入成功才算成功

    - 日志提交 

      

  - leader宕机或网络分区

    

    

- raft算法的实现

  raft官网地址：https://raft.github.io/

  Jraft实现：https://github.com/sofastack/sofa-jraft。我们查看1.3.12版本的源码，因为nacos中也是使用的这个版本的源码

  ![image-20230525180117781](nacos笔记.assets/image-20230525180117781.png) 

  

- jraft在nacos中的应用

  Jraft在nacos的CP一致性协议是如何实现的

- 1.4.1版本raft协议的实现

  为什么看这个版本呢，主要是这个版本是自己实现的raft协议，而且相比较于2.0版本的代码也简单点，所以我们可以从中借鉴一部分实现思路



#### 4.2 寻址机制

##### 4.2.1 文件寻址方式

JDK的WatchService+监听器模式应用, 监听目标目录是否有变化，如果有变化，则回调对应的监听器即可

缺点：工作量较大，如果集群动态扩容缩容，需要更改每个nacos节点的cluster.conf配置文件，如果更新失败，还有可能导致集群的状态的不一致性

![image-20230525105904014](nacos笔记.assets/image-20230525105904014.png)



##### 4.2.2 地址服务器的方式

- 请求流程图

  <img src="nacos笔记.assets/image-20230525110504485.png" alt="image-20230525110504485" style="zoom:40%;" /> 

  

  

- 相关实现类

  ![image-20230525111835322](nacos笔记.assets/image-20230525111835322.png)



#### 4.3 事件机制

典型的发布订阅(观察者)模式的应用，nacos高性能体现的一个重要方面

![image-20230525145024754](nacos笔记.assets/image-20230525145024754.png) 





#### 4.4 网络连接

##### 4.4.0 现状分析

​	一下这俩种推送方式我们会在介绍具体的源码分析过程中，具体的进行分析，目前你大概知道有这么回事就行了

![image-20230602092314309](nacos笔记.assets/image-20230602092314309.png)



##### 4.4.1 配置模块

![image-20230524154818316](nacos笔记.assets/image-20230524154818316.png) 

![image-20230524154911249](nacos笔记.assets/image-20230524154911249.png)

##### 4.4.2 服务注册

![image-20230524155104137](nacos笔记.assets/image-20230524155104137.png) 

##### 4.4.3 核心功能

![image-20230524160412209](nacos笔记.assets/image-20230524160412209.png) 

<img src="nacos笔记.assets/image-20230529105525626.png" alt="image-20230529105525626" style="zoom: 80%;" /> 

##### 4.4.4 源码分析

- client->server 

  - 通道建立过程

    ![image-20230529145834310](nacos笔记.assets/image-20230529145834310.png)

  - 断线重连过程 

    客户端断链检测

    ![image-20230529153500637](nacos笔记.assets/image-20230529153500637.png)

    服务端断链检测：清空内存数据，同时关闭close原先的连接

    ![image-20230529153825186](nacos笔记.assets/image-20230529153825186.png) 




#### 4.5 高可用机制

- 同城容灾

  ![image-20230608162155411](nacos笔记.assets/image-20230608162155411.png) 

  

- 数据多级容灾

  Nacos 持久化存储做了主备容灾，而且底层存储数据多副本高可用保障。

  Nacos Server 有全量缓存数据，即使存储挂或者不可用，只影响写，核心的读服务不受影响。

  Nacos SDK 有所需服务和配置缓存，Server 即使全挂，走本地缓存+文件，保证核心业务调用不受影响。

  

#### 4.6 插件机制

插件仓库地址：https://github.com/nacos-group/nacos-plugin

以授权插件为例

- client

  根据java的SPI机制加载默认的实现

  ![image-20230609142935146](nacos笔记.assets/image-20230609142935146.png) 

- server

  ![image-20230609143013186](nacos笔记.assets/image-20230609143013186.png) 

#### 4.7 回调机制

统一使用监听器模式来回调用户处理

- 服务模块

  ![image-20230608165507352](nacos笔记.assets/image-20230608165507352.png)

- 配置模块

  ![image-20230608165633141](nacos笔记.assets/image-20230608165633141.png)

   

  

#### 4.8 数据存储

- 统一数据存储模型

  ```java
  package com.alibaba.nacos.core.storage.kv;
  
  import com.alibaba.nacos.core.exception.KvStorageException;
  
  import java.util.List;
  import java.util.Map;
  
  /**
   * Universal KV storage interface.
   */
  public interface KvStorage {
      
      enum KvType {
          /**
           * Local file storage.
           */
          File,
      
          /**
           * Local memory storage.
           */
          Memory,
      
          /**
           * RocksDB storage.
           */
          RocksDB,
      }
      
      
      /**
       * get data by key.
       *
       * @param key byte[]
       * @return byte[]
       * @throws KvStorageException KVStorageException
       */
      byte[] get(byte[] key) throws KvStorageException;
      
      /**
       * batch get by List byte[].
       *
       * @param keys List byte[]
       * @return Map byte[], byte[]
       * @throws KvStorageException KvStorageException
       */
      Map<byte[], byte[]> batchGet(List<byte[]> keys) throws KvStorageException;
      
      /**
       * write data.
       *
       * @param key   byte[]
       * @param value byte[]
       * @throws KvStorageException KvStorageException
       */
      void put(byte[] key, byte[] value) throws KvStorageException;
      
      /**
       * batch write.
       *
       * @param keys    List byte[]
       * @param values List byte[]
       * @throws KvStorageException KvStorageException
       */
      void batchPut(List<byte[]> keys, List<byte[]> values) throws KvStorageException;
      
      /**
       * delete with key.
       *
       * @param key byte[]
       * @throws KvStorageException KvStorageException
       */
      void delete(byte[] key) throws KvStorageException;
      
      /**
       * batch delete with keys.
       *
       * @param keys List byte[]
       * @throws KvStorageException KvStorageException
       */
      void batchDelete(List<byte[]> keys) throws KvStorageException;
      
      /**
       * do snapshot.
       *
       * @param backupPath snapshot file save path
       * @throws KvStorageException KVStorageException
       */
      void doSnapshot(final String backupPath) throws KvStorageException;
      
      /**
       * load snapshot.
       *
       * @param path The path to the snapshot file
       * @throws KvStorageException KVStorageException
       */
      void snapshotLoad(String path) throws KvStorageException;
      
      /**
       * Get all keys.
       *
       * @return all keys
       * @throws KvStorageException KVStorageException
       */
      List<byte[]> allKeys() throws KvStorageException;
      
      /**
       * shutdown.
       */
      void shutdown();
      
  }
  ```

- 实现类型

  - 文件
  - 内存
  - RocksDb

  

### 5.亮点分析

##### 1.跳跃表

ConcurrentSkipListMap

参考文章：https://blog.csdn.net/Zong_0915/article/details/126139005

##### 2.nacos的SPI加载器

NacosServiceLoader其实本质就是使用的JDK的SPI机制，默认加载 /META-INF/services目录下的文件

<img src="nacos笔记.assets/image-20230524180251424.png" alt="image-20230524180251424" style="zoom: 70%;" /> 

##### 3.心跳检查的拦截器链条的使用

```java
package com.alibaba.nacos.naming.interceptor;

import com.alibaba.nacos.common.spi.NacosServiceLoader;

import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

public abstract class AbstractNamingInterceptorChain<T extends Interceptable>
        implements NacosNamingInterceptorChain<T> {
    
    private final List<NacosNamingInterceptor<T>> interceptors;
    
    protected AbstractNamingInterceptorChain(Class<? extends NacosNamingInterceptor<T>> clazz) {
        this.interceptors = new LinkedList<>();
        interceptors.addAll(NacosServiceLoader.load(clazz));
        interceptors.sort(Comparator.comparingInt(NacosNamingInterceptor::order));
    }
    
    /**
     * Get all interceptors.
     *
     * @return interceptors list
     */
    protected List<NacosNamingInterceptor<T>> getInterceptors() {
        return interceptors;
    }
    
    @Override
    public void addInterceptor(NacosNamingInterceptor<T> interceptor) {
        interceptors.add(interceptor);
        interceptors.sort(Comparator.comparingInt(NacosNamingInterceptor::order));
    }
    
    @Override
    public void doInterceptor(T object) {
        for (NacosNamingInterceptor<T> each : interceptors) {
            if (!each.isInterceptType(object.getClass())) {
                continue;
            }
            if (each.intercept(object)) {
                object.afterIntercept();
                return;
            }
        }
        object.passIntercept();
    }
}
```

##### 4.UDP可靠消息推送的设计机制

```
UdpConnector
```

##### 5. 简单读写锁的使用

```java
package com.alibaba.nacos.config.server.utils;

/**
 * Simplest read-write lock implementation. Requires locking and unlocking must be called in pairs.
 *
 * @author Nacos
 */
public class SimpleReadWriteLock {
    
    /**
     * Zero means no lock; Negative Numbers mean write locks; Positive Numbers mean read locks, and the numeric value
     * represents the number of read locks.
     */
    private int status = 0;
    
    /**
     * Try read lock.
     */
    public synchronized boolean tryReadLock() {
        if (isWriteLocked()) {
            return false;
        } else {
            status++;
            return true;
        }
    }
    
    /**
     * Release the read lock.
     */
    public synchronized void releaseReadLock() {
        // when status equals 0, it should not decrement to negative numbers
        if (status == 0) {
            return;
        }
        status--;
    }
    
    /**
     * Try write lock.
     */
    public synchronized boolean tryWriteLock() {
        if (!isFree()) {
            return false;
        } else {
            status = -1;
            return true;
        }
    }
    
    public synchronized void releaseWriteLock() {
        status = 0;
    }
    
    private boolean isWriteLocked() {
        return status < 0;
    }
    
    private boolean isFree() {
        return status == 0;
    }
}
```

##### 6.配置加载顺序

```java
properties search order:PROPERTIES->JVM->ENV->DEFAULT_SETTING
```

##### 7.过滤器链条

```java
private static class VirtualFilterChain implements IConfigFilterChain {
        
        private final List<? extends IConfigFilter> additionalFilters;
        
        private int currentPosition = 0;
        
        public VirtualFilterChain(List<? extends IConfigFilter> additionalFilters) {
            this.additionalFilters = additionalFilters;
        }
        
        @Override
        public void doFilter(final IConfigRequest request, final IConfigResponse response) throws NacosException {
            if (this.currentPosition != this.additionalFilters.size()) {
                this.currentPosition++;
                IConfigFilter nextFilter = this.additionalFilters.get(this.currentPosition - 1);
                nextFilter.doFilter(request, response, this);
            }
        }
    }
```



##### 8.客户端限流

```java
private Response requestProxy(RpcClient rpcClientInner, Request request, long timeoutMills)
                throws NacosException {
            try {
                request.putAllHeader(super.getSecurityHeaders(resourceBuild(request)));
                request.putAllHeader(super.getCommonHeader());
            } catch (Exception e) {
                throw new NacosException(NacosException.CLIENT_INVALID_PARAM, e);
            }
            JsonObject asJsonObjectTemp = new Gson().toJsonTree(request).getAsJsonObject();
            asJsonObjectTemp.remove("headers");
            asJsonObjectTemp.remove("requestId");
            boolean limit = Limiter.isLimit(request.getClass() + asJsonObjectTemp.toString());
            if (limit) {
                throw new NacosException(NacosException.CLIENT_OVER_THRESHOLD,
                        "More than client-side current limit threshold");
            }
            return rpcClientInner.request(request, timeoutMills);
        }
```

![image-20231209145950892](nacos笔记.assets/image-20231209145950892.png) 

##### 9.失败重试间隔的方式

```java
private void push(RpcPushTask retryTask) {
        ConfigChangeNotifyRequest notifyRequest = retryTask.notifyRequest;
        if (retryTask.isOverTimes()) {
            Loggers.REMOTE_PUSH
                    .warn("push callback retry fail over times .dataId={},group={},tenant={},clientId={},will unregister client.",
                            notifyRequest.getDataId(), notifyRequest.getGroup(), notifyRequest.getTenant(),
                            retryTask.connectionId);
            connectionManager.unregister(retryTask.connectionId);
        } else if (connectionManager.getConnection(retryTask.connectionId) != null) {
            // first time:delay 0s; second time:delay 2s; third time:delay 4s
            ConfigExecutor.getClientConfigNotifierServiceExecutor()
                    .schedule(retryTask, retryTask.tryTimes * 2, TimeUnit.SECONDS);
        } else {
            // client is already offline, ignore task.
        }
        
    }
```

##### 10.CountDownLatch使用

```java
final CountDownLatch latch = new CountDownLatch(peers.majorityCount());
            for (final String server : peers.allServersIncludeMyself()) {
                if (isLeader(server)) {
                    latch.countDown();
                    continue;
                }
                final String url = buildUrl(server, API_ON_PUB);
                HttpClient.asyncHttpPostLarge(url, Arrays.asList("key", key), content, new Callback<String>() {
                    @Override
                    public void onReceive(RestResult<String> result) {
                        if (!result.ok()) {
                            Loggers.RAFT
                                    .warn("[RAFT] failed to publish data to peer, datumId={}, peer={}, http code={}",
                                            datum.key, server, result.getCode());
                            return;
                        }
                        latch.countDown();
                    }
                    
                    @Override
                    public void onError(Throwable throwable) {
                        Loggers.RAFT.error("[RAFT] failed to publish data to peer", throwable);
                    }
                    
                    @Override
                    public void onCancel() {
                    
                    }
                });
                
            }
```

##### 11.生命周期的钩子函数

监听+策略模式的使用，这个好处

![image-20230903150320211](nacos笔记.assets/image-20230903150320211.png)

##### 12.nacos spi机制

```
NacosServiceLoader.load(NacosApplicationListener.class)
```

很简单，使用的就是JDK的SPI的机制，默认加载/META-INF/services/包名+类名

![image-20230903151334633](nacos笔记.assets/image-20230903151334633.png) 

##### 13.内存缓存的思想

![image-20230903151732799](nacos笔记.assets/image-20230903151732799.png)

##### 14.文件监听

```java
WatchFileCenter.registerWatcher(EnvUtil.getConfPath(), new FileWatcher() {
            @Override
            public void onChange(FileChangeEvent event) {
                try {
                    Map<String, ?> tmp = EnvUtil.loadProperties(EnvUtil.getApplicationConfFileResource());
                    SOURCES.putAll(tmp);
                    NotifyCenter.publishEvent(ServerConfigChangeEvent.newEvent());
                } catch (IOException ignore) {
                    LOGGER.warn("Failed to monitor file ", ignore);
                }
            }
            
            @Override
            public boolean interest(String context) {
                return StringUtils.contains(context, "application.properties");
            }
        });
```

##### 15.builder设计模式

```java
/*
 * Copyright 1999-2018 Alibaba Group Holding Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.alibaba.nacos.core.cluster;

import com.alibaba.nacos.api.ability.ServerAbilities;
import com.alibaba.nacos.core.utils.Loggers;
import com.alibaba.nacos.sys.env.EnvUtil;
import com.alibaba.nacos.common.utils.StringUtils;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Collections;
import java.util.Map;
import java.util.Objects;
import java.util.TreeMap;

/**
 * Cluster member node.
 *
 * @author <a href="mailto:liaochuntao@live.com">liaochuntao</a>
 */
public class Member implements Comparable<Member>, Cloneable, Serializable {
    
    private static final long serialVersionUID = -6061130045021268736L;
    
    private String ip;
    
    private int port = -1;
    
    private volatile NodeState state = NodeState.UP;
    
    private Map<String, Object> extendInfo = Collections.synchronizedMap(new TreeMap<>());
    
    private String address = "";
    
    private transient int failAccessCnt = 0;
    
    private ServerAbilities abilities = new ServerAbilities();
    
    public Member() {
        String prefix = "nacos.core.member.meta.";
        extendInfo.put(MemberMetaDataConstants.SITE_KEY,
                EnvUtil.getProperty(prefix + MemberMetaDataConstants.SITE_KEY, "unknow"));
        extendInfo.put(MemberMetaDataConstants.AD_WEIGHT,
                EnvUtil.getProperty(prefix + MemberMetaDataConstants.AD_WEIGHT, "0"));
        extendInfo
                .put(MemberMetaDataConstants.WEIGHT, EnvUtil.getProperty(prefix + MemberMetaDataConstants.WEIGHT, "1"));
    }
    
    public ServerAbilities getAbilities() {
        return abilities;
    }
    
    public void setAbilities(ServerAbilities abilities) {
        this.abilities = abilities;
    }
    
    public static MemberBuilder builder() {
        return new MemberBuilder();
    }
    
    public int getPort() {
        return port;
    }
    
    public void setPort(int port) {
        this.port = port;
    }
    
    public NodeState getState() {
        return state;
    }
    
    public void setState(NodeState state) {
        this.state = state;
    }
    
    public Map<String, Object> getExtendInfo() {
        return extendInfo;
    }
    
    public void setExtendInfo(Map<String, Object> extendInfo) {
        Map<String, Object> newExtendInfo = Collections.synchronizedMap(new TreeMap<>());
        newExtendInfo.putAll(extendInfo);
        this.extendInfo = newExtendInfo;
    }
    
    public String getIp() {
        return ip;
    }
    
    public void setIp(String ip) {
        this.ip = ip;
    }
    
    public String getAddress() {
        if (StringUtils.isBlank(address)) {
            address = ip + ":" + port;
        }
        return address;
    }
    
    public void setAddress(String address) {
        this.address = address;
    }
    
    public Object getExtendVal(String key) {
        return extendInfo.get(key);
    }
    
    public void setExtendVal(String key, Object value) {
        extendInfo.put(key, value);
    }
    
    public void delExtendVal(String key) {
        extendInfo.remove(key);
    }
    
    public boolean check() {
        return StringUtils.isNoneBlank(ip, address) && port != -1;
    }
    
    public int getFailAccessCnt() {
        return failAccessCnt;
    }
    
    public void setFailAccessCnt(int failAccessCnt) {
        this.failAccessCnt = failAccessCnt;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Member that = (Member) o;
        if (StringUtils.isAnyBlank(address, that.address)) {
            return port == that.port && StringUtils.equals(ip, that.ip);
        }
        return StringUtils.equals(address, that.address);
    }
    
    @Override
    public String toString() {
        return "Member{" + "ip='" + ip + '\'' + ", port=" + port + ", state=" + state + ", extendInfo=" + extendInfo
                + '}';
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(ip, port);
    }
    
    @Override
    public int compareTo(Member o) {
        return getAddress().compareTo(o.getAddress());
    }
    
    /**
     * get a copy.
     *
     * @return member.
     */
    public Member copy() {
        Member copy = null;
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(this);
            // convert the input stream to member object
            ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
            ObjectInputStream ois = new ObjectInputStream(bais);
            copy = (Member) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            Loggers.CORE.warn("[Member copy] copy failed", e);
        }
        return copy;
    }
    
    public static final class MemberBuilder {
        
        private String ip;
        
        private int port;
        
        private NodeState state;
        
        private Map<String, String> extendInfo = Collections.synchronizedMap(new TreeMap<>());
        
        private MemberBuilder() {
        }
        
        public MemberBuilder ip(String ip) {
            this.ip = ip;
            return this;
        }
        
        public MemberBuilder port(int port) {
            this.port = port;
            return this;
        }
        
        public MemberBuilder state(NodeState state) {
            this.state = state;
            return this;
        }
        
        public MemberBuilder extendInfo(Map<String, String> extendInfo) {
            this.extendInfo.putAll(extendInfo);
            return this;
        }
        
        /**
         * build Member.
         *
         * @return {@link Member}
         */
        public Member build() {
            Member serverNode = new Member();
            if (Objects.nonNull(this.extendInfo)) {
                serverNode.extendInfo.putAll(this.extendInfo);
            }
            serverNode.state = this.state;
            serverNode.ip = this.ip;
            serverNode.port = this.port;
            serverNode.address = this.ip + ":" + this.port;
            return serverNode;
        }
    }
    
}

```

##### 16.工厂设计模式的使用

```java
package com.alibaba.nacos.core.cluster.lookup;

import com.alibaba.nacos.api.exception.NacosException;
import com.alibaba.nacos.common.utils.StringUtils;
import com.alibaba.nacos.core.cluster.MemberLookup;
import com.alibaba.nacos.core.cluster.ServerMemberManager;
import com.alibaba.nacos.sys.env.EnvUtil;
import com.alibaba.nacos.core.utils.Loggers;

import java.io.File;
import java.util.Arrays;
import java.util.Objects;

/**
 * An addressing pattern factory, responsible for the creation of all addressing patterns.
 *
 * @author <a href="mailto:liaochuntao@live.com">liaochuntao</a>
 */
public final class LookupFactory {
    
    private static final String LOOKUP_MODE_TYPE = "nacos.core.member.lookup.type";
    
    @SuppressWarnings("checkstyle:StaticVariableName")
    private static MemberLookup LOOK_UP = null;
    
    private static LookupType currentLookupType = null;
    
    /**
     * Create the target addressing pattern.
     *
     * @param memberManager {@link ServerMemberManager}
     * @return {@link MemberLookup}
     * @throws NacosException NacosException
     */
    public static MemberLookup createLookUp(ServerMemberManager memberManager) throws NacosException {
        if (!EnvUtil.getStandaloneMode()) {
            String lookupType = EnvUtil.getProperty(LOOKUP_MODE_TYPE);
            LookupType type = chooseLookup(lookupType);
            LOOK_UP = find(type);
            currentLookupType = type;
        } else {
            LOOK_UP = new StandaloneMemberLookup();
        }
        LOOK_UP.injectMemberManager(memberManager);
        Loggers.CLUSTER.info("Current addressing mode selection : {}", LOOK_UP.getClass().getSimpleName());
        return LOOK_UP;
    }
    
    /**
     * Switch to target addressing mode.
     *
     * @param name          target member-lookup name
     * @param memberManager {@link ServerMemberManager}
     * @return {@link MemberLookup}
     * @throws NacosException {@link NacosException}
     */
    public static MemberLookup switchLookup(String name, ServerMemberManager memberManager) throws NacosException {
        LookupType lookupType = LookupType.sourceOf(name);
        
        if (Objects.isNull(lookupType)) {
            throw new IllegalArgumentException(
                    "The addressing mode exists : " + name + ", just support : [" + Arrays.toString(LookupType.values())
                            + "]");
        }
        
        if (Objects.equals(currentLookupType, lookupType)) {
            return LOOK_UP;
        }
        MemberLookup newLookup = find(lookupType);
        currentLookupType = lookupType;
        if (Objects.nonNull(LOOK_UP)) {
            LOOK_UP.destroy();
        }
        LOOK_UP = newLookup;
        LOOK_UP.injectMemberManager(memberManager);
        Loggers.CLUSTER.info("Current addressing mode selection : {}", LOOK_UP.getClass().getSimpleName());
        return LOOK_UP;
    }
    
    private static MemberLookup find(LookupType type) {
        if (LookupType.FILE_CONFIG.equals(type)) {
            LOOK_UP = new FileConfigMemberLookup();
            return LOOK_UP;
        }
        if (LookupType.ADDRESS_SERVER.equals(type)) {
            LOOK_UP = new AddressServerMemberLookup();
            return LOOK_UP;
        }
        // unpossible to run here
        throw new IllegalArgumentException();
    }
    
    private static LookupType chooseLookup(String lookupType) {
        if (StringUtils.isNotBlank(lookupType)) {
            LookupType type = LookupType.sourceOf(lookupType);
            if (Objects.nonNull(type)) {
                return type;
            }
        }
        File file = new File(EnvUtil.getClusterConfFilePath());
        if (file.exists() || StringUtils.isNotBlank(EnvUtil.getMemberList())) {
            return LookupType.FILE_CONFIG;
        }
        return LookupType.ADDRESS_SERVER;
    }
    
    public static MemberLookup getLookUp() {
        return LOOK_UP;
    }
    
    public static void destroy() throws NacosException {
        Objects.requireNonNull(LOOK_UP).destroy();
    }
    
    public enum LookupType {
        
        /**
         * File addressing mode.
         */
        FILE_CONFIG(1, "file"),
        
        /**
         * Address server addressing mode.
         */
        ADDRESS_SERVER(2, "address-server");
        
        private final int code;
        
        private final String name;
        
        LookupType(int code, String name) {
            this.code = code;
            this.name = name;
        }
        
        /**
         * find one {@link LookupType} by name, if not found, return null.
         *
         * @param name name
         * @return {@link LookupType}
         */
        public static LookupType sourceOf(String name) {
            for (LookupType type : values()) {
                if (Objects.equals(type.name, name)) {
                    return type;
                }
            }
            return null;
        }
        
        public int getCode() {
            return code;
        }
        
        public String getName() {
            return name;
        }
        
        @Override
        public String toString() {
            return name;
        }
    }
    
}

```

##### 17.模板方法+策略模式的使用

```java
package com.alibaba.nacos.core.cluster;

import com.alibaba.nacos.api.exception.NacosException;

import java.util.Collection;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Addressable pattern base class.
 *
 * @author <a href="mailto:liaochuntao@live.com">liaochuntao</a>
 */
public abstract class AbstractMemberLookup implements MemberLookup {
    
    protected ServerMemberManager memberManager;
    
    protected AtomicBoolean start = new AtomicBoolean(false);
    
    @Override
    public void injectMemberManager(ServerMemberManager memberManager) {
        this.memberManager = memberManager;
    }
    
    @Override
    public void afterLookup(Collection<Member> members) {
        this.memberManager.memberChange(members);
    }
    
    @Override
    public void destroy() throws NacosException {
        if (start.compareAndSet(true, false)) {
            doDestroy();
        }
    }
    
    @Override
    public void start() throws NacosException {
        if (start.compareAndSet(false, true)) {
            doStart();
        }
    }
    
    /**
     * subclass can override this method if need.
     * @throws NacosException NacosException
     */
    protected abstract void doStart() throws NacosException;
    
    /**
     * subclass can override this method if need.
     * @throws NacosException nacosException
     */
    protected abstract void doDestroy() throws NacosException;
}

```

##### 18.线程池集中化的定义

```java

package com.alibaba.nacos.core.utils;

import com.alibaba.nacos.common.executor.ExecutorFactory;
import com.alibaba.nacos.common.executor.NameThreadFactory;
import com.alibaba.nacos.common.utils.ThreadFactoryBuilder;
import com.alibaba.nacos.sys.env.EnvUtil;

import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * core module global executor.
 *
 * @author <a href="mailto:liaochuntao@live.com">liaochuntao</a>
 */
@SuppressWarnings("all")
public class GlobalExecutor {
    
    private static final ScheduledExecutorService COMMON_EXECUTOR = ExecutorFactory.Managed
            .newScheduledExecutorService(ClassUtils.getCanonicalName(GlobalExecutor.class), 4,
                    new NameThreadFactory("com.alibaba.nacos.core.common"));
    
    private static final ScheduledExecutorService DISTRO_EXECUTOR = ExecutorFactory.Managed
            .newScheduledExecutorService(ClassUtils.getCanonicalName(GlobalExecutor.class),
                    EnvUtil.getAvailableProcessors(2), new NameThreadFactory("com.alibaba.nacos.core.protocal.distro"));
    
    public static final ThreadPoolExecutor sdkRpcExecutor = new ThreadPoolExecutor(
            EnvUtil.getAvailableProcessors(RemoteUtils.getRemoteExecutorTimesOfProcessors()),
            EnvUtil.getAvailableProcessors(RemoteUtils.getRemoteExecutorTimesOfProcessors()), 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(RemoteUtils.getRemoteExecutorQueueSize()),
            new ThreadFactoryBuilder().daemon(true).nameFormat("nacos-grpc-executor-%d").build());
    
    public static final ThreadPoolExecutor clusterRpcExecutor = new ThreadPoolExecutor(
            EnvUtil.getAvailableProcessors(RemoteUtils.getRemoteExecutorTimesOfProcessors()),
            EnvUtil.getAvailableProcessors(RemoteUtils.getRemoteExecutorTimesOfProcessors()), 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(RemoteUtils.getRemoteExecutorQueueSize()),
            new ThreadFactoryBuilder().daemon(true).nameFormat("nacos-cluster-grpc-executor-%d").build());
    
    public static void runWithoutThread(Runnable runnable) {
        runnable.run();
    }
    
    public static void executeByCommon(Runnable runnable) {
        if (COMMON_EXECUTOR.isShutdown()) {
            return;
        }
        COMMON_EXECUTOR.execute(runnable);
    }
    
    public static void scheduleByCommon(Runnable runnable, long delayMs) {
        if (COMMON_EXECUTOR.isShutdown()) {
            return;
        }
        COMMON_EXECUTOR.schedule(runnable, delayMs, TimeUnit.MILLISECONDS);
    }
    
    public static void submitLoadDataTask(Runnable runnable) {
        DISTRO_EXECUTOR.submit(runnable);
    }
    
    public static void submitLoadDataTask(Runnable runnable, long delay) {
        DISTRO_EXECUTOR.schedule(runnable, delay, TimeUnit.MILLISECONDS);
    }
    
    public static void schedulePartitionDataTimedSync(Runnable runnable, long interval) {
        DISTRO_EXECUTOR.scheduleWithFixedDelay(runnable, interval, interval, TimeUnit.MILLISECONDS);
    }
    
}

```

##### 19. 注册JVM的钩子函数

```java
Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            Loggers.REMOTE.info("Nacos {} Rpc server stopping", serverName);
            try {
                BaseRpcServer.this.stopServer();
                Loggers.REMOTE.info("Nacos {} Rpc server stopped successfully...", serverName);
            } catch (Exception e) {
                Loggers.REMOTE.error("Nacos {} Rpc server stopped fail...", serverName, e);
            }
        }));
```

##### 20. 配置的优先级别加载

![image-20230919230834460](nacos笔记.assets/image-20230919230834460.png) 

##### 21.延时sleep

```java
 // sleep x milliseconds to switch next server.
                    if (!isRunning()) {
                        // first round, try servers at a delay 100ms;second round, 200ms; max delays 5s. to be reconsidered.
                        Thread.sleep(Math.min(retryTurns + 1, 50) * 100L);
                    }
```

##### 22.策略模式->请求处理器

![image-20230924161316236](nacos笔记.assets/image-20230924161316236.png)

##### 23.模板方法加过滤器的思想

```java
public Response handleRequest(T request, RequestMeta meta) throws NacosException {
        for (AbstractRequestFilter filter : requestFilters.filters) {
            try {
                Response filterResult = filter.filter(request, meta, this.getClass());
                if (filterResult != null && !filterResult.isSuccess()) {
                    return filterResult;
                }
            } catch (Throwable throwable) {
                Loggers.REMOTE.error("filter error", throwable);
            }
            
        }
        return handle(request, meta);
    }
```

##### 24 延时任务执行的缓冲

![image-20230924205107736](nacos笔记.assets/image-20230924205107736.png)