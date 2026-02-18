# 案例4：排序算法对比（冒泡 / 插入 / 选择 / 快排）

## 案例目标
用同一组无序数组，对比几种常见排序算法的：
- 思路差异（交换谁、移动谁）
- 时间复杂度（最好 / 最坏 / 平均）
- 是否稳定、是否原地排序

## 验证数据

- 文件：`data_structure/data/numbers_unsorted.txt`
  ```text
  7 2 9 4 1 5 3 8 6
  ```
- 排序后结果应该是：`1 2 3 4 5 6 7 8 9`

## Java 代码示例：多种排序实现骨架

```java
package dsalgo;

import java.util.Arrays;

public class SortAlgorithmsDemo {

    // 冒泡排序（Bubble Sort）
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                    swapped = true;
                }
            }
            if (!swapped) break; // 提前结束
        }
    }

    // 插入排序（Insertion Sort）
    public static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    // 选择排序（Selection Sort）
    public static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }
            int tmp = arr[i];
            arr[i] = arr[minIdx];
            arr[minIdx] = tmp;
        }
    }

    // 快速排序（Quick Sort）—— 简单实现
    public static void quickSort(int[] arr, int left, int right) {
        if (left >= right) return;
        int pivot = arr[left];
        int i = left, j = right;
        while (i < j) {
            while (i < j && arr[j] >= pivot) j--;
            while (i < j && arr[i] <= pivot) i++;
            if (i < j) {
                int tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
            }
        }
        arr[left] = arr[i];
        arr[i] = pivot;

        quickSort(arr, left, i - 1);
        quickSort(arr, i + 1, right);
    }

    public static void main(String[] args) {
        int[] original = {7, 2, 9, 4, 1, 5, 3, 8, 6};

        int[] a1 = Arrays.copyOf(original, original.length);
        bubbleSort(a1);
        System.out.println("Bubble:     " + Arrays.toString(a1));

        int[] a2 = Arrays.copyOf(original, original.length);
        insertionSort(a2);
        System.out.println("Insertion:  " + Arrays.toString(a2));

        int[] a3 = Arrays.copyOf(original, original.length);
        selectionSort(a3);
        System.out.println("Selection:  " + Arrays.toString(a3));

        int[] a4 = Arrays.copyOf(original, original.length);
        quickSort(a4, 0, a4.length - 1);
        System.out.println("Quick:      " + Arrays.toString(a4));
    }
}
```

### 期望输出（形如）

```text
Bubble:     [1, 2, 3, 4, 5, 6, 7, 8, 9]
Insertion:  [1, 2, 3, 4, 5, 6, 7, 8, 9]
Selection:  [1, 2, 3, 4, 5, 6, 7, 8, 9]
Quick:      [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 费曼式讲解：4 种排序的“人格特质”

### 1. 冒泡排序：相邻交换，慢悠悠的“冒泡”
- **过程**：不断比较相邻元素，大的往后“冒”
- **时间复杂度**：最好 O(n)（已排好 + 提前结束），最坏/平均 O(n²)
- **空间复杂度**：O(1)，原地排序
- **稳定性**：稳定（相等元素相对位置不变）

### 2. 插入排序：像打扑克整理手牌
- **过程**：认为前 i-1 个元素已经有序，把第 i 个插到合适位置
- **时间复杂度**：最好 O(n)，最坏/平均 O(n²)
- **空间复杂度**：O(1)，原地排序
- **稳定性**：稳定

### 3. 选择排序：每次选择一个最小的放到前面
- **过程**：每一轮从未排序部分选最小的，放到当前起始位置
- **时间复杂度**：无论好坏都是 O(n²)
- **空间复杂度**：O(1)，原地排序
- **稳定性**：不稳定（最小元素可能与前面相同值元素交换）

### 4. 快速排序：分而治之的“快”，但怕极端情况
- **过程**：选一个基准 pivot，把小的放左边，大的放右边，然后递归
- **时间复杂度**：平均 O(n log n)，最坏 O(n²)（数组近乎有序 & pivot 选得差）
- **空间复杂度**：递归栈 O(log n)（平均）
- **稳定性**：通常实现是不稳定的

---

## 你应该能回答的几个问题

1. 为什么冒泡/插入在“几百个元素的小数组”上并不一定慢到不能接受？
2. 为什么选择排序几乎只在讲解教材里出现，实际项目中很少用？
3. 快排为什么要特别注意“近乎有序”的输入？（可以用随机 pivot 或三数取中优化）

