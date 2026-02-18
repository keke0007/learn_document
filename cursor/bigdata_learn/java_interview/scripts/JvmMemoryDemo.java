/**
 * JVM 内存管理演示
 * 
 * 运行参数示例：
 * -Xms20m -Xmx20m -Xmn10m -XX:+PrintGCDetails
 */
public class JvmMemoryDemo {
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
    
    /**
     * 演示大对象直接进入老年代
     * VM参数：-Xms20m -Xmx20m -Xmn10m -XX:+PrintGCDetails
     *         -XX:PretenureSizeThreshold=3145728
     */
    public static void testPretenureSizeThreshold() {
        byte[] allocation = new byte[4 * _1MB]; // 直接分配在老年代
    }
    
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
    
    /**
     * 演示堆内存溢出
     * VM参数：-Xms20m -Xmx20m -XX:+HeapDumpOnOutOfMemoryError
     */
    public static void testHeapOOM() {
        java.util.List<byte[]> list = new java.util.ArrayList<>();
        while (true) {
            list.add(new byte[_1MB]);
        }
    }
    
    public static void main(String[] args) {
        System.out.println("JVM Memory Demo");
        System.out.println("================");
        
        // 取消注释以运行不同的测试
        // testAllocation();
        // testPretenureSizeThreshold();
        // testTenuringThreshold();
        // testHeapOOM();
    }
}
