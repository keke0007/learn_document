# JVM 内存管理案例

## 案例概述

本案例通过实际代码演示 JVM 内存管理的各个方面，包括堆内存分配、垃圾回收、内存溢出等问题。

## 知识点

1. **堆内存结构**
   - 新生代（Eden、Survivor）
   - 老年代
   - 内存分配策略

2. **垃圾回收**
   - Minor GC（新生代 GC）
   - Major GC（老年代 GC）
   - Full GC（整堆 GC）

3. **内存溢出**
   - OutOfMemoryError 类型
   - 内存溢出排查方法

## 案例代码

### 案例1：新生代内存分配

```java
public class YoungGenAllocation {
    private static final int _1MB = 1024 * 1024;
    
    /**
     * 演示新生代内存分配
     * VM参数：-Xms20m -Xmx20m -Xmn10m -XX:+PrintGCDetails
     */
    public static void testAllocation() {
        byte[] allocation1, allocation2, allocation3, allocation4;
        allocation1 = new byte[2 * _1MB];
        allocation2 = new byte[2 * _1MB];
        allocation3 = new byte[2 * _1MB];
        allocation4 = new byte[4 * _1MB]; // 出现一次 Minor GC
    }
}
```

**预期结果：**
- 前三个对象分配在 Eden 区
- 第四个对象分配时，Eden 区空间不足，触发 Minor GC
- GC 后，前三个对象可能进入 Survivor 区或老年代

### 案例2：大对象直接进入老年代

```java
public class BigObjectAllocation {
    private static final int _1MB = 1024 * 1024;
    
    /**
     * 演示大对象直接进入老年代
     * VM参数：-Xms20m -Xmx20m -Xmn10m -XX:+PrintGCDetails
     *         -XX:PretenureSizeThreshold=3145728
     */
    public static void testPretenureSizeThreshold() {
        byte[] allocation = new byte[4 * _1MB]; // 直接分配在老年代
    }
}
```

**预期结果：**
- 4MB 对象直接分配在老年代
- 不会触发 Minor GC

### 案例3：长期存活对象进入老年代

```java
public class TenuringThreshold {
    private static final int _1MB = 1024 * 1024;
    
    /**
     * 演示长期存活对象进入老年代
     * VM参数：-Xms20m -Xmx20m -Xmn10m -XX:+PrintGCDetails
     *         -XX:MaxTenuringThreshold=1
     */
    public static void testTenuringThreshold() {
        byte[] allocation1, allocation2, allocation3;
        allocation1 = new byte[_1MB / 4];
        allocation2 = new byte[4 * _1MB];
        allocation3 = new byte[4 * _1MB];
        allocation3 = null;
        allocation3 = new byte[4 * _1MB];
    }
}
```

**预期结果：**
- allocation1 经过一次 GC 后进入老年代
- MaxTenuringThreshold=1 表示对象在 Survivor 区存活一次后进入老年代

### 案例4：堆内存溢出

```java
import java.util.ArrayList;
import java.util.List;

public class HeapOOM {
    static class OOMObject {
    }
    
    /**
     * 演示堆内存溢出
     * VM参数：-Xms20m -Xmx20m -XX:+HeapDumpOnOutOfMemoryError
     */
    public static void main(String[] args) {
        List<OOMObject> list = new ArrayList<>();
        while (true) {
            list.add(new OOMObject());
        }
    }
}
```

**预期结果：**
- 抛出 java.lang.OutOfMemoryError: Java heap space
- 生成堆转储文件（heap dump）

### 案例5：方法区（元空间）溢出

```java
import java.lang.reflect.Method;
import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

public class MethodAreaOOM {
    static class OOMObject {
    }
    
    /**
     * 演示方法区溢出（通过 CGLIB 动态生成类）
     * VM参数：-XX:MetaspaceSize=10m -XX:MaxMetaspaceSize=10m
     */
    public static void main(String[] args) {
        while (true) {
            Enhancer enhancer = new Enhancer();
            enhancer.setSuperclass(OOMObject.class);
            enhancer.setUseCache(false);
            enhancer.setCallback(new MethodInterceptor() {
                @Override
                public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy) throws Throwable {
                    return proxy.invokeSuper(obj, args);
                }
            });
            enhancer.create();
        }
    }
}
```

**预期结果：**
- 抛出 java.lang.OutOfMemoryError: Metaspace

## 验证数据

### GC 日志示例

```
[GC (Allocation Failure) [PSYoungGen: 6144K->640K(9216K)] 6144K->4736K(19456K), 0.0031234 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]
```

**日志解析：**
- `PSYoungGen`: 使用 Parallel Scavenge 收集器的新生代
- `6144K->640K(9216K)`: GC 前 6144K，GC 后 640K，总容量 9216K
- `6144K->4736K(19456K)`: 整个堆 GC 前 6144K，GC 后 4736K，总容量 19456K
- `0.0031234 secs`: GC 耗时

### 内存监控命令

```bash
# 查看堆内存使用情况
jmap -heap <pid>

# 生成堆转储文件
jmap -dump:format=b,file=heap.hprof <pid>

# 查看 GC 情况（每 1 秒输出一次）
jstat -gcutil <pid> 1000

# 查看类加载情况
jstat -class <pid>

# 查看 JIT 编译情况
jstat -compiler <pid>
```

### 性能测试数据

| 测试场景 | 堆大小 | 新生代大小 | GC 次数 | GC 耗时 | 总耗时 |
|---------|--------|-----------|---------|---------|--------|
| 正常分配 | 20m | 10m | 1 | 3ms | 50ms |
| 大对象 | 20m | 10m | 0 | 0ms | 5ms |
| 长期存活 | 20m | 10m | 2 | 6ms | 60ms |

## 总结

1. **内存分配策略**
   - 对象优先在 Eden 区分配
   - 大对象直接进入老年代
   - 长期存活对象进入老年代

2. **GC 触发条件**
   - Eden 区空间不足时触发 Minor GC
   - 老年代空间不足时触发 Major GC
   - 方法区空间不足时触发 Full GC

3. **调优建议**
   - 合理设置堆大小和新生代比例
   - 选择合适的 GC 收集器
   - 监控 GC 日志，及时发现问题
