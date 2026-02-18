# 案例3：二叉树遍历与二叉搜索树（BST）

## 案例目标
通过一个小二叉搜索树（BST），理解：
- 前序 / 中序 / 后序遍历的顺序差异
- BST 的性质：左 < 根 < 右
- 为什么对 BST 做中序遍历会得到有序序列

## 验证数据

- 文件：`data_structure/data/tree_nodes.txt`
  ```text
  5 3 7 2 4 6 8
  ```
- 插入顺序：5, 3, 7, 2, 4, 6, 8
- 对应 BST 结构：

```
      5
    /   \
   3     7
  / \   / \
 2   4 6   8
```

## Java 代码示例：构建 BST + 遍历

```java
package dsalgo;

public class BinarySearchTreeDemo {

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    // 向 BST 插入一个值
    public static TreeNode insert(TreeNode root, int val) {
        if (root == null) return new TreeNode(val);
        if (val < root.val) {
            root.left = insert(root.left, val);
        } else if (val > root.val) {
            root.right = insert(root.right, val);
        }
        // val == root.val 时这里简单忽略（不插入重复值）
        return root;
    }

    // 前序遍历：根 -> 左 -> 右
    public static void preorder(TreeNode root) {
        if (root == null) return;
        System.out.print(root.val + " ");
        preorder(root.left);
        preorder(root.right);
    }

    // 中序遍历：左 -> 根 -> 右
    public static void inorder(TreeNode root) {
        if (root == null) return;
        inorder(root.left);
        System.out.print(root.val + " ");
        inorder(root.right);
    }

    // 后序遍历：左 -> 右 -> 根
    public static void postorder(TreeNode root) {
        if (root == null) return;
        postorder(root.left);
        postorder(root.right);
        System.out.print(root.val + " ");
    }

    public static void main(String[] args) {
        int[] vals = {5, 3, 7, 2, 4, 6, 8};
        TreeNode root = null;
        for (int v : vals) {
            root = insert(root, v);
        }

        System.out.print("前序遍历: ");
        preorder(root);
        System.out.println();

        System.out.print("中序遍历: ");
        inorder(root);
        System.out.println();

        System.out.print("后序遍历: ");
        postorder(root);
        System.out.println();
    }
}
```

### 期望输出

```text
前序遍历: 5 3 2 4 7 6 8 
中序遍历: 2 3 4 5 6 7 8 
后序遍历: 2 4 3 6 8 7 5 
```

---

## 费曼式讲解

### 1. 二叉树遍历顺序
- 前序：**先看根，再看左，最后看右** → 适合“拷贝整棵树结构”
- 中序：**先看左，再看根，最后看右** → 在 BST 上得到“有序序列”
- 后序：**先看左右子树，最后看根** → 适合“删除整棵树”等场景

### 2. BST 的性质
- 每个节点的值：
  - 左子树上的所有节点值 < 根节点值
  - 右子树上的所有节点值 > 根节点值
- 因此：
  - 中序遍历 BST 时，一定会“从小到大”访问所有节点

### 3. 你必须能解释的点
- 为什么对普通二叉树做中序遍历不一定有序，但对 BST 就一定有序？
- 插入顺序不同，BST 的形状会不同，最坏情况下会退化为链表 → 查找变成 O(n)

