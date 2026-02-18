# Shell 学习知识点

## 目录
1. [Shell 基础概念](#1-shell-基础概念)
2. [变量和数组](#2-变量和数组)
3. [条件判断](#3-条件判断)
4. [循环结构](#4-循环结构)
5. [函数](#5-函数)
6. [文件操作](#6-文件操作)
7. [文本处理](#7-文本处理)
8. [管道和重定向](#8-管道和重定向)
9. [正则表达式](#9-正则表达式)
10. [错误处理](#10-错误处理)
11. [案例与验证数据](#11-案例与验证数据)

---

## 1. Shell 基础概念

### 1.1 什么是 Shell
- Shell 是用户与操作系统内核之间的接口
- 命令行解释器，执行用户输入的命令
- 支持脚本编程，自动化任务

### 1.2 Shell 类型
- **Bash**：最常用的 Shell（Linux 默认）
- **sh**：POSIX Shell
- **zsh**：功能丰富的 Shell
- **fish**：用户友好的 Shell

### 1.3 Shell 脚本基础
```bash
#!/bin/bash
# 这是注释
echo "Hello World"
```

---

## 2. 变量和数组

### 2.1 变量定义和使用
```bash
# 定义变量
name="张三"
age=25

# 使用变量
echo $name
echo ${name}

# 只读变量
readonly PI=3.14

# 删除变量
unset name
```

### 2.2 特殊变量
- `$0`：脚本名称
- `$1, $2, ...`：位置参数
- `$#`：参数个数
- `$*`：所有参数
- `$@`：所有参数（带引号）
- `$?`：上一个命令的退出状态
- `$$`：当前进程 ID

### 2.3 数组
```bash
# 定义数组
arr=(1 2 3 4 5)
arr[0]=10

# 访问数组
echo ${arr[0]}
echo ${arr[@]}  # 所有元素
echo ${#arr[@]} # 数组长度
```

---

## 3. 条件判断

### 3.1 if 语句
```bash
if [ condition ]; then
    commands
elif [ condition ]; then
    commands
else
    commands
fi
```

### 3.2 条件测试
```bash
# 文件测试
[ -f file ]    # 文件存在且为普通文件
[ -d dir ]     # 目录存在
[ -r file ]    # 文件可读
[ -w file ]    # 文件可写
[ -x file ]    # 文件可执行

# 字符串测试
[ -z str ]     # 字符串为空
[ -n str ]     # 字符串非空
[ str1 = str2 ] # 字符串相等
[ str1 != str2 ] # 字符串不等

# 数值测试
[ n1 -eq n2 ]  # 相等
[ n1 -ne n2 ]  # 不等
[ n1 -gt n2 ]  # 大于
[ n1 -lt n2 ]  # 小于
[ n1 -ge n2 ]  # 大于等于
[ n1 -le n2 ]  # 小于等于
```

### 3.3 case 语句
```bash
case $var in
    pattern1)
        commands
        ;;
    pattern2)
        commands
        ;;
    *)
        commands
        ;;
esac
```

---

## 4. 循环结构

### 4.1 for 循环
```bash
# 列表循环
for i in 1 2 3 4 5; do
    echo $i
done

# C 风格循环
for ((i=1; i<=5; i++)); do
    echo $i
done

# 遍历数组
for item in ${arr[@]}; do
    echo $item
done
```

### 4.2 while 循环
```bash
while [ condition ]; do
    commands
done
```

### 4.3 until 循环
```bash
until [ condition ]; do
    commands
done
```

### 4.4 循环控制
```bash
break      # 跳出循环
continue   # 跳过本次循环
```

---

## 5. 函数

### 5.1 函数定义
```bash
function_name() {
    commands
    return value
}

# 或
function function_name() {
    commands
    return value
}
```

### 5.2 函数参数
```bash
my_function() {
    echo "第一个参数: $1"
    echo "第二个参数: $2"
    echo "参数总数: $#"
}

my_function arg1 arg2
```

### 5.3 函数返回值
```bash
my_function() {
    local result=$(($1 + $2))
    return $result
}

my_function 10 20
echo "返回值: $?"
```

---

## 6. 文件操作

### 6.1 文件读取
```bash
# 逐行读取文件
while IFS= read -r line; do
    echo "$line"
done < file.txt

# 读取文件内容
content=$(cat file.txt)
```

### 6.2 文件写入
```bash
# 覆盖写入
echo "内容" > file.txt

# 追加写入
echo "内容" >> file.txt

# Here Document
cat > file.txt << EOF
多行内容
EOF
```

### 6.3 文件操作命令
```bash
cp source dest      # 复制
mv source dest      # 移动/重命名
rm file             # 删除
mkdir dir           # 创建目录
rmdir dir           # 删除空目录
rm -r dir           # 递归删除
```

---

## 7. 文本处理

### 7.1 grep
```bash
grep pattern file           # 搜索模式
grep -i pattern file        # 忽略大小写
grep -v pattern file        # 反向匹配
grep -n pattern file        # 显示行号
grep -r pattern dir         # 递归搜索
```

### 7.2 sed
```bash
sed 's/old/new/g' file      # 替换
sed -n '1,5p' file          # 打印1-5行
sed '/pattern/d' file       # 删除匹配行
sed -i 's/old/new/g' file   # 原地修改
```

### 7.3 awk
```bash
awk '{print $1}' file       # 打印第一列
awk -F: '{print $1}' file   # 指定分隔符
awk '/pattern/ {print}' file # 模式匹配
awk '{sum+=$1} END {print sum}' file # 求和
```

### 7.4 cut
```bash
cut -d: -f1 file            # 按分隔符切分
cut -c1-5 file               # 按字符位置切分
```

---

## 8. 管道和重定向

### 8.1 管道
```bash
command1 | command2          # 管道
command1 | command2 | command3
```

### 8.2 重定向
```bash
command > file               # 标准输出重定向
command >> file              # 追加输出
command < file               # 标准输入重定向
command 2> file              # 错误输出重定向
command > file 2>&1          # 输出和错误都重定向
command &> file              # 输出和错误都重定向
```

---

## 9. 正则表达式

### 9.1 基本元字符
- `.`：匹配任意字符
- `*`：匹配前一个字符0次或多次
- `+`：匹配前一个字符1次或多次
- `?`：匹配前一个字符0次或1次
- `^`：行首
- `$`：行尾
- `[]`：字符类
- `|`：或

### 9.2 扩展正则表达式
```bash
grep -E 'pattern' file       # 使用扩展正则
egrep 'pattern' file
```

---

## 10. 错误处理

### 10.1 退出状态
```bash
command
if [ $? -eq 0 ]; then
    echo "成功"
else
    echo "失败"
fi
```

### 10.2 set 选项
```bash
set -e          # 遇到错误立即退出
set -u          # 使用未定义变量时报错
set -x          # 显示执行的命令
set -o pipefail # 管道中任何命令失败都返回失败
```

### 10.3 trap
```bash
trap 'cleanup' EXIT          # 退出时执行清理
trap 'echo "中断"' INT        # Ctrl+C 时执行
```

---

## 11. 案例与验证数据

详见以下文件：
- [案例1：基础语法](cases/basic_syntax.md)
- [案例2：文件操作](cases/file_operations.md)
- [案例3：文本处理](cases/text_processing.md)
- [案例4：系统管理](cases/system_management.md)
- [验证数据文件](data/)
