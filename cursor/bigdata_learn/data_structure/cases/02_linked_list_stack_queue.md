# 案例2：链表（LinkedList）与栈/队列（Stack/Queue）

## 案例目标
通过简单的链表反转与括号匹配问题，理解：
- 数组 vs 链表 的本质区别
- 栈适合“后进先出”的场景
- 队列适合“先进先出”的场景

## 一、小链表反转：理解链表结构

### 验证数据

- 文件：`data_structure/data/linked_list_values.txt`
  ```text
  10 20 30 40 50
  ```
- 目标：将单链表 `10 -> 20 -> 30 -> 40 -> 50` 反转为 `50 -> 40 -> 30 -> 20 -> 10`

### Java 代码示例：单链表反转

```java
package dsalgo;

public class LinkedListReverseDemo {

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    // 迭代反转单链表
    public static ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;

        while (curr != null) {
            ListNode next = curr.next; // 暂存后继
            curr.next = prev;          // 指针反转
            prev = curr;               // prev 前进
            curr = next;               // curr 前进
        }
        return prev;
    }

    private static void printList(ListNode head) {
        ListNode p = head;
        while (p != null) {
            System.out.print(p.val);
            if (p.next != null) System.out.print(" -> ");
            p = p.next;
        }
        System.out.println();
    }

    public static void main(String[] args) {
        // 构造链表 10 -> 20 -> 30 -> 40 -> 50
        ListNode n1 = new ListNode(10);
        ListNode n2 = new ListNode(20);
        ListNode n3 = new ListNode(30);
        ListNode n4 = new ListNode(40);
        ListNode n5 = new ListNode(50);
        n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n5;

        System.out.print("原链表: ");
        printList(n1);

        ListNode reversed = reverse(n1);
        System.out.print("反转后: ");
        printList(reversed);
    }
}
```

### 期望输出

```text
原链表: 10 -> 20 -> 30 -> 40 -> 50
反转后: 50 -> 40 -> 30 -> 20 -> 10
```

---

## 二、栈（Stack）：括号匹配问题

### 问题描述
给一个只包含 `(`、`)`、`{`、`}`、`[`、`]` 的字符串，判断括号是否成对且嵌套合法。

### 验证数据

可以自己构造几组：
- 合法：`"()[]"`、`"{[()]}"`、`"({[]})"`
- 不合法：`"(]"`、`"([)]"`、`"((("`

### Java 代码示例：有效括号

```java
package dsalgo;

import java.util.Stack;

public class StackValidParenthesesDemo {

    public static boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();

        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if ((c == ')' && top != '(') ||
                    (c == '}' && top != '{') ||
                    (c == ']' && top != '[')) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        String[] tests = {"()[]", "{[()]}", "({[]})", "(]", "([)]", "((("};
        for (String s : tests) {
            System.out.printf("%s -> %s%n", s, isValid(s));
        }
    }
}
```

### 期望输出（部分）

```text
()[] -> true
{[()]} -> true
({[]}) -> true
(] -> false
([)] -> false
((( -> false
```

---

## 费曼式讲解

### 1. 数组 vs 链表
- **数组**：一排连续格子，按下标 O(1) 随机访问，但中间插入/删除要整体移动，代价高。
- **链表**：一个个节点通过指针串起来，中间插入/删除只改指针，代价低；但按下标访问要从头走，O(n)。

### 2. 栈（Stack）
- **一句话**：后进先出，就像一摞盘子，最后放的先拿。
- 括号匹配场景：遇到左括号就压栈，遇到右括号就看栈顶能否配对。

### 3. 队列（Queue）（本案例只提概念）
- **一句话**：先进先出，就像排队买票，先来的人先被服务。
- 常见应用：任务排队、消息队列、BFS 层序遍历等。

