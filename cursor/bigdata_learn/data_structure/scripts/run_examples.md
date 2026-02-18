# Java 数据结构与算法示例运行说明

## 1) 项目结构建议

你可以在任意 IDE（IntelliJ IDEA / Eclipse）中新建一个普通 Java 项目，将本目录下的示例代码放入 `src/` 目录：

```
src/
└── dsalgo/
    ├── ArrayBinarySearchDemo.java
    ├── LinkedListReverseDemo.java
    ├── StackValidParenthesesDemo.java
    ├── BinarySearchTreeDemo.java
    └── SortAlgorithmsDemo.java
```

## 2) 编译与运行（命令行示例）

假设你在项目根目录下：

```bash
javac -d out src/dsalgo/*.java
java -cp out dsalgo.ArrayBinarySearchDemo
```

每个 Demo 内部都自带一组小规模验证数据（也可以对照 `data_structure/data/` 下的文件）。

