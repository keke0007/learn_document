# 案例2：文件操作

## 案例描述
学习 Shell 脚本中的文件操作，包括文件读取、写入、复制、移动等。

## 数据准备

### 数据文件 (employees.txt)
```
1,张三,25,5000,IT
2,李四,30,8000,HR
3,王五,28,6000,IT
4,赵六,35,12000,Sales
5,孙七,27,5500,IT
```

### 数据文件 (departments.txt)
```
IT,技术部,北京
HR,人力资源部,上海
Sales,销售部,广州
```

## 脚本示例

### 1. 文件读取 (read_file.sh)
```bash
#!/bin/bash

# ============================================
# 读取整个文件
# ============================================

echo "=== 读取整个文件 ==="
content=$(cat data/employees.txt)
echo "$content"

# ============================================
# 逐行读取文件
# ============================================

echo -e "\n=== 逐行读取文件 ==="
while IFS= read -r line; do
    echo "行: $line"
done < data/employees.txt

# ============================================
# 读取指定行数
# ============================================

echo -e "\n=== 读取前3行 ==="
head -n 3 data/employees.txt

echo -e "\n=== 读取后2行 ==="
tail -n 2 data/employees.txt

# ============================================
# 按列读取（CSV）
# ============================================

echo -e "\n=== 读取CSV文件 ==="
while IFS=',' read -r id name age salary dept; do
    echo "ID: $id, 姓名: $name, 部门: $dept"
done < data/employees.txt

# ============================================
# 统计文件信息
# ============================================

echo -e "\n=== 文件统计 ==="
file="data/employees.txt"
echo "文件: $file"
echo "行数: $(wc -l < $file)"
echo "字数: $(wc -w < $file)"
echo "字符数: $(wc -c < $file)"
```

### 2. 文件写入 (write_file.sh)
```bash
#!/bin/bash

# ============================================
# 覆盖写入
# ============================================

echo "=== 覆盖写入 ==="
echo "第一行内容" > output/file1.txt
echo "第二行内容" > output/file1.txt
cat output/file1.txt

# ============================================
# 追加写入
# ============================================

echo -e "\n=== 追加写入 ==="
echo "第一行内容" > output/file2.txt
echo "第二行内容" >> output/file2.txt
echo "第三行内容" >> output/file2.txt
cat output/file2.txt

# ============================================
# Here Document
# ============================================

echo -e "\n=== Here Document ==="
cat > output/file3.txt << EOF
这是第一行
这是第二行
这是第三行
EOF
cat output/file3.txt

# ============================================
# Here String
# ============================================

echo -e "\n=== Here String ==="
cat > output/file4.txt <<< "单行内容"
cat output/file4.txt

# ============================================
# 格式化写入
# ============================================

echo -e "\n=== 格式化写入 ==="
name="张三"
age=25
city="北京"

cat > output/info.txt << EOF
姓名: $name
年龄: $age
城市: $city
EOF
cat output/info.txt
```

### 3. 文件操作命令 (file_commands.sh)
```bash
#!/bin/bash

# 创建输出目录
mkdir -p output

# ============================================
# 文件复制
# ============================================

echo "=== 文件复制 ==="
cp data/employees.txt output/employees_copy.txt
echo "复制完成"

# ============================================
# 文件移动/重命名
# ============================================

echo -e "\n=== 文件移动 ==="
mv output/employees_copy.txt output/employees_backup.txt
echo "移动完成"

# ============================================
# 创建目录
# ============================================

echo -e "\n=== 创建目录 ==="
mkdir -p output/subdir1/subdir2
echo "目录创建完成"

# ============================================
# 文件权限
# ============================================

echo -e "\n=== 文件权限 ==="
chmod +x output/file1.txt
ls -l output/file1.txt

# ============================================
# 文件查找
# ============================================

echo -e "\n=== 文件查找 ==="
find output -name "*.txt" -type f

# ============================================
# 文件删除
# ============================================

echo -e "\n=== 文件删除 ==="
rm output/file4.txt
echo "文件删除完成"

# ============================================
# 目录删除
# ============================================

echo -e "\n=== 目录删除 ==="
rm -rf output/subdir1
echo "目录删除完成"
```

### 4. 文件处理 (process_file.sh)
```bash
#!/bin/bash

# ============================================
# 文件过滤
# ============================================

echo "=== 过滤包含'IT'的行 ==="
grep "IT" data/employees.txt

# ============================================
# 文件排序
# ============================================

echo -e "\n=== 按薪资排序 ==="
sort -t',' -k4 -n data/employees.txt

# ============================================
# 去重
# ============================================

echo -e "\n=== 去重 ==="
echo -e "1\n2\n2\n3\n3\n3" | sort -u

# ============================================
# 文件合并
# ============================================

echo -e "\n=== 文件合并 ==="
cat data/employees.txt data/departments.txt > output/merged.txt
cat output/merged.txt

# ============================================
# 文件分割
# ============================================

echo -e "\n=== 文件分割 ==="
split -l 2 data/employees.txt output/part_
ls output/part_*

# ============================================
# 文件比较
# ============================================

echo -e "\n=== 文件比较 ==="
cp data/employees.txt output/employees_copy.txt
diff data/employees.txt output/employees_copy.txt
```

## 运行方式

```bash
# 创建输出目录
mkdir -p output

# 添加执行权限
chmod +x read_file.sh write_file.sh file_commands.sh process_file.sh

# 运行脚本
./read_file.sh
./write_file.sh
./file_commands.sh
./process_file.sh
```

## 预期结果

### 文件读取输出
```
=== 读取整个文件 ===
1,张三,25,5000,IT
2,李四,30,8000,HR
...

=== 读取CSV文件 ===
ID: 1, 姓名: 张三, 部门: IT
ID: 2, 姓名: 李四, 部门: HR
...
```

### 文件写入输出
```
=== 覆盖写入 ===
第二行内容

=== 追加写入 ===
第一行内容
第二行内容
第三行内容
```

## 学习要点

1. **文件读取**：cat、逐行读取、head、tail
2. **文件写入**：覆盖、追加、Here Document
3. **文件操作**：cp、mv、rm、mkdir
4. **文件处理**：grep、sort、uniq、diff
5. **文件权限**：chmod、ls -l
