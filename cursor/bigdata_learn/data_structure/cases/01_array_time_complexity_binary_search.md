# 案例1：数组与时间复杂度 + 二分查找（Binary Search）

## 案例目标
用一组有序数组的小例子，理解三件事：
- 数组的**连续内存**特性 → 随机访问 O(1)
- 顺序查找 vs 二分查找的时间复杂度差异
- 二分查找的边界与返回值处理

## 验证数据

- 文件：`data_structure/data/numbers_small.txt`
  ```text
  1 3 5 7 9 11 13 15
  ```
- 要求：在该有序数组中查找若干目标值（例如 7、1、15、100）

## Java 代码示例（可直接复制）

```java
package dsalgo;

public class ArrayBinarySearchDemo {

    // 经典二分查找：返回目标值索引，未找到返回 -1
    public static int binarySearch(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1; // 右边界是“闭区间”的右端

        while (left <= right) { // 区间 [left, right] 仍然有效
            int mid = left + (right - left) / 2; // 防止溢出
            int midVal = nums[mid];

            if (midVal == target) {
                return mid;
            } else if (midVal < target) {
                left = mid + 1;  // 目标在右半部分
            } else {
                right = mid - 1; // 目标在左半部分
            }
        }
        return -1; // 找不到
    }

    public static void main(String[] args) {
        int[] nums = {1, 3, 5, 7, 9, 11, 13, 15};

        int[] targets = {7, 1, 15, 100};
        for (int target : targets) {
            int idx = binarySearch(nums, target);
            System.out.printf("target=%d, index=%d%n", target, idx);
        }
    }
}
```

### 期望输出（可对照验证）

```text
target=7, index=3
target=1, index=0
target=15, index=7
target=100, index=-1
```

---

## 费曼式讲解（你应该能讲给非程序员听）

### 1. 数组是什么？
- **通俗说法**：一排连在一起的格子，每个格子可以放一个数，你可以通过“下标”直接跳到第几个格子。
- **关键特性**：
  - 连续内存：所以 `nums[7]` 可以 O(1) 取到（根据起始地址直接偏移）
  - 长度固定：创建后长度不变，插入/删除中间元素代价高

### 2. 顺序查找 vs 二分查找
- 顺序查找：一个个看过去，最坏要看 n 次，时间复杂度 O(n)
- 二分查找：每次把搜索区间砍一半，最坏看 log₂n 次，时间复杂度 O(log n)

**类比**：
- 顺序查找：翻电话簿从头往后翻
- 二分查找：先翻中间一页，看姓氏在前半本还是后半本，再继续对半翻

### 3. 二分查找的关键边界
- 区间定义：这里用的是 **闭区间** [left, right]
  - 进入循环条件是 `left <= right`
  - `mid = left + (right - left) / 2` 避免溢出
  - `mid` 比目标小 → `left = mid + 1`
  - `mid` 比目标大 → `right = mid - 1`

**你必须能回答的问题**：
- 为什么循环条件是 `left <= right` 而不是 `<`？
- 为什么返回 -1 表示没找到，而不是抛异常？

---

## 时间复杂度与空间复杂度（顺便一起记牢）

- **访问元素 `nums[i]`**：O(1) 时间，O(1) 额外空间
- **顺序查找**：O(n) 时间，O(1) 额外空间
- **二分查找**：O(log n) 时间，O(1) 额外空间

> 直觉：数组越大，二分查找比顺序查找的优势越明显。

