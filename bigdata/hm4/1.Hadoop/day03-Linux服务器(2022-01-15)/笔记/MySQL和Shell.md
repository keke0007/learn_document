## MySQl的安装

### 安装方式

1. 在线安装

   ```shell
   #需要联网，MySQL的版本是默认的
   yum -y install mysql-server mysql-client
   ```

2. rpm包安装

 ```shell
 #不需要联网，很多配置自动生成
 rpm -ivh MySQL-client-5.6.42-1.el7.x86_64.rpm
 ```

3. **离线安装**

   ```shell
   #不需要联网，所有的配置都可以手动设置
   tar  -zxvf mysql-5.7.29-linux-glibc2.12-x86_64.tar.gz -C /export/server/
   ```

### 注意事项

1. MySQL在安装之前必须给虚拟机保存快照

2. 在输入临时密码时，方式如下

   ```sql
   /export/server/mysql-5.7.29/bin/mysql -uroot -p  
   然后回车,将临时密码复制，在CRT中进行右键粘贴
   ```

   

## Shell编程

### 为什么要学习Shell编程

1. 在大数据后期，大数据开发的代码需要封装到脚本中，自动化执行，这里就可以使用Shell脚本来完成

2. 大数据开发大致流程

   ![image-20220115143207338](image\image-20220115143207338.png)

3. 当封装完shell脚本之后，可以使用一些调度框架（AirFlow、Azkaban、Oozie）来使用这些脚本完成自动化调度

### Shell是什么

1. Shell是一门脚本语言（简单），属于解释性语言
2. Shell脚本语言需要由解释器来解释执行，默认的解释器是Bash

### Shell入门

```shell
#!/bin/bash  #该语句可以升序，默认解释器就是 /bin/bash
echo 'Hello World!'
```

+ 解释
  + shell文件名可以有后缀（.sh），也可以没有后缀
  + shell除了第一行的#之外，在任何地方#就是注释
  + echo 其实等于与 System.out.println() 和 print

### Shell的运行方式

+ 方式一：sh  执行脚本

  ```shell
  sh hello.sh  #这种方式不需要脚本文件有可执行权限
  ```

+ 工作目录执行

  ```shell
  cd /export/data/shell/
  chmod +x hello.sh 
  ./hello.sh  #这种方式不需要脚本文件有可执行权限
  ```

+ 绝对路径执行（推荐）

  ```shell
  /export/shell/hello.sh   #这种方式不需要脚本文件有可执行权限
  ```

### 变量-用户变量

 解释：变量就是存放变化数据的符号

#### 变量的分类

+ 用户变量：用户自己定义的变量符号
+ 系统变量：系统已经定义的变量，在整个Linux系统起作用
+ 特殊变量

#### 变量的数据类型

+ 字符串类型
+  数字类型（属于特殊的字符串类型）

#### 变量的定义格式

```shell
变量名=变量值  #注意，"="左右两侧不能有空格。
```

#### 变量的赋值方式

+ 直接赋值

  ```shell
  username="lft"
  ```

+ 从键盘赋值

  ```shell
  read username
  ```

+ 执行命令的结果赋值

  ```shell
  str=$(pwd)
  str=$(ll)
  str=$(ps -ef)
  
  str=`pwd`  #这里不是引号，是tab键上边的符号
  str=`ll`
  str=`ps -ef`
  ```

#### 变量的访问

+ 方式1

  ```shell
  echo $username
  ```

+ 方式2

  ```shell
  echo ${username}xxx  #如果后边还有其他的字符，则必须使用该方式
  ```

#### 只读变量

如果你定义了一个变量，不想让这个变量被再次赋值，则可以标记为只读变量

```shell
readonly username
```

#### 删除变量

 定义了一个用户变量之后， 默认的作用域是从变量定义开始到脚本结束，如果想让这个变量的空间提前释放，则可以用unset来设置

```shell
unset username
```

### 变量-环境变量

#### 介绍

+ 环境变量都是Linux系统已经好的变量
+ 每一个环境变量都有特殊的含义，PWD，
+ 环境变量的变量名都是大写字母
+ 我们也可以自己定义环境变量： /etc/profile

#### 查看所有的环境变量

```shell
env
```

####  常见的环境变量

```shell
PATH 决定了shell将到哪些目录中寻找命令或程序 
HOME 当前用户主目录 
HOSTNAME　指主机的名称 
PWD 当前用户的所在路径
```

#### 如何访问环境变量

```shell
echo $PWD
echo $PATH
```

#### 如何定义环境变量

1. vi /etc/profile ,在文件末尾加上要定义的环境变量

   ```shell
   export SERVICE_HOST=www.itcast.cn
   ```

2.  将/etc/profile保存退出

3.  source /etc/profile 让配置生效

4. 查看自定义环境变量

   ```sql
   env
   ```

5. 使用环境变量

   ```shell
   echo $SERVICE_HOST
   ```

### 变量-特殊变量 

特殊变量主要用于脚本的传参

| **变量** | **解释**                                     |
| -------- | -------------------------------------------- |
| $#       | 命令行参数的个数                             |
| $n       | $1表示第一个参数，$2表示第二个参数，以此类推 |
| $0       | 当前程序的名称                               |
| $?       | 前一个命令或许或函数的返回码                 |
| $*       | 以“参数1 参数2 。。。”形式保存所有参数       |

### 字符串

#### 字符串的表达方式

+ 第一种： hello
+ 第二种:   'hello'
+ 第三种:   "hello"  (推荐)

#### 不同表达方式的区别

结论：推荐大家使用双引号

```shell
str=hello
str='hello'
str="hello"


str2='I am ${str}'   #单引号不会解释字符串中包含的变量
str2=I am ${str}"  #双引号引号可以解释字符串中包含的变量
```

#### 字符串的处理

+ 求字符串长度

  ```shell
  #!/bin/bash
  string="jobs"
  echo ${#string}   # 输出结果: 4
  ```

+ 对字符串进行截取

  ```shell
  #!/bin/bash
  string="敢于亮剑决不后退"
  echo ${string:2:4}    # 输出结果为: 亮剑剑决  从索引（从0开始）为2的字符开始截取，截取4个字符
  ```

### 算术运算符

+ 计算-方式1

   ```shell
   echo `expr 3 + 2`  # + 变量必须留空格，否则报错
   echo `expr 3 \* 2` # * 是乘法 ，必须转义
   echo `expr 3 % 1` # 
   
   a=3
   b=2
   echo `expr $a + $b`
   ```

+ 计算-方式2 （推荐）

```shell
echo $((3+2))  #  +两边不用留空格
echo $((3*2)) # * 是乘法 ，不用转义
echo $((3%2)) # 

a=3
b=2
echo $(($a+$b))
echo $((a+b)) #$可以省略
```

+ 计算-方式3（推荐）

```shell
echo $[3+2]  # +两边不用留空格
echo $[3*2] # *是乘法 ，不用转义
echo $[3%2] #

a=3
b=2
echo $[$a+$b]
echo $[a+b] #$可以省略
```

+ 数值的比较

```shell
==  #比较两个数是否相同
!=  #比较两个数字是否不同
```

### 流程控制语句

#### if语句 - if

+ 方式1

```shell
#!/bin/bash
if [ $(ps -ef | grep -c "ssh") -gt 1 ]
then 
 echo "true" 
fi
```

+ 方式2

```shell
#!/bin/bash
if [ $(ps -ef | grep -c "ssh") -gt 1 ] ; then  #将if和then放在一行上，中间用分号隔开
 echo "true" 
fi
```

### if语句-if else

+ 方式1

```shell
#!/bin/bash
read -p "Enter your age(1-100）：" age  #-p是输入的提示信息，提示信息和输入是在同一行进行
if [ $age -ge 18 ]
then
     echo '已经成年！'
else
     echo '未成年!'
fi
```

+ 方式2

```shell
#!/bin/bash
read -p "Enter your age(1-100）：" age  #-p是输入的提示信息，提示信息和输入是在同一行进行
if test $age -ge 18  #这里的test就等价于 []
then
     echo '已经成年！'
else
     echo '未成年!'
fi
```

### if语句-if elif else

```shell
#!/bin/bash 
read -p "请输入a的值:"   a

read -p "请输入b的值:"  b
if [ $a -eq $b ]
then
        echo "a 等于 b" 
elif [ $a -gt $b ]
then
        echo "a 大于 b" 
elif [ $a -lt $b ]
then
        echo "a 小于 b" 
else
        echo "没有符合的条件" 
fi
```

#### if的特殊写法

```shell
#以下两种方式等价
#方式1
[ -n "$pid" ] && kill -9 $pid
test -n "$pid"  && kill -9 $pid

#方式2
if [-n "$pid" ]
then
 kill -9 $pid
fi

#!/bin/bash
[ -e "hello.sh" ] && rm -fr hello.sh   #如果前边成立，则会执行后边的操作
test -e "hello.sh"  && rm -fr hello.sh  #如果前边成立，则会执行后边的操作
test ! -e "hello.sh"  || rm -fr hello.sh #如果前边不成立，则会执行后边的操作


#未解决问题
if modprobe sunrpc || strstr "$(cat /proc/filesystems)" rpc_pipefs; then

```

### for循环

+ 格式1

  ```shell
  #1、打印/root目录下所有文件的名字
  #!/bin/bash  
  for file in $(ls /root)
  do 
          echo $file  
  done
  ```

+ 格式2

  ```shell
  #!/bin/bash
  s=0
  #从1加到100
  for(( i=1;i<=100;i=i+1))
  #定义循环100次
  do
   #每次循环给变量s赋值
   #s=$((s+i))  #传统写法
   let s+=1     #一种简写（和其他高级语言接轨）
  done
  #输出从1加到100的和
  echo "The sum of 1+2+..+100 is : $s"
  ```

  ### while循环

  案例1

  ```shell
  #!/bin/bash
  num=1
  while [ $num -le 5 ]    # [] 需要使用   -le  推荐
  #while (( $num <= 5 ))    # (()) 需要使用 <=
  do
      echo $num
      #num=$((num+1))      #传统写法
      let num++            #一种简写（和其他高级语言接轨）
  done
  ```

###     死循环

+ while的死循环

  ```shell
  #!/bin/bash
  while :
  do
   echo "hello world"
   sleep 1  #休眠1秒钟
  done
  ```

+ for的死循环

  ```shell
  #!/bin/bash
  
  for((;;))  ; do   #for和do可以放在同一行
   echo "hello world"
   sleep 1
  done
  ```

### case语句

```shell
#!/bin/bash
echo '输入 1 到 4 之间的数字:'

echo '你输入的数字为:'
read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;                  #两个分号
    2)  echo '你选择了 2'
    ;;
    3)  echo '你选择了 3'
    ;;
    4)  echo '你选择了 4'
    ;;
    *)  echo '你没有输入 1 到 4 之间的数字'
    ;;
esac  #结束关键字
```

### 跳出循环

+ break

  ```shell
  #跳出本层循环
  #!/bin/bash
  
  while :
  do
      echo -n "输入 1 到 5 之间的数字:"   #### -n表示不换行输出
  
      read  aNum
  
      case $aNum in
          1|2|3|4|5) echo "你输入的数字为 $aNum!"     ###case的穿透
          ;;
          *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
              break                                 ###跳出while循环，不是跳出break
          ;;
      esac
  done
  ```

+ continue

  ```shell
  #跳出本次循环
  #!/bin/bash
  while :
  
  do
  
      echo -n "输入 1 到 5 之间的数字: "
      read aNum
      case $aNum in
          1|2|3|4|5) echo "你输入的数字为 $aNum!"
          ;;
          *) echo "你输入的数字不是 1 到 5 之间的!"
              continue          ### 跳到循环开始的地方
              echo "游戏结束"    ###该语句永远无法执行
          ;;
      esac
  done
  ```

  ### 函数

  ####  格式

  ```shell
  [ function ] funname()  # function关键字可以省略 ，不管有没有形参，函数名后的后边都写()
  {
      action;        #函数体
      [return int;]  #return不是返回函数的返回值，返回的是函数的执行状态码（只能是整数）
  }
  ```

  #### 入门案例

+ 没有参数，没有返回值

```shell
#!/bin/bash

function demoFun(){
  echo "Hello World"
}

#调动函数
demoFun
```

+ 没有参数，有返回状态码

  ```shell
  #!/bin/bash
  funWithReturn(){
  
      echo "这个函数会对输入的两个数字进行相加运算..."
  
      echo "输入第一个数字: "
  read aNum
  
      echo "输入第二个数字: "
  
      read anotherNum
      echo "两个数字分别为 $aNum 和 $anotherNum !"
  
      echo "两个数的和为:$((aNum+anotherNum))"
      return 100  ###返回函数的执行状态码 (范围：0-255 ， 0表示成功，非0就表示失败)
  }
  
  funWithReturn ###调用函数
    
  echo "函数的返回状态码：$?"   ###获取函数的返回状态码
  ```

+ 有返回值的方法

  ```shell
  #!/bin/bash
  funWithReturn(){
    s=0
    for((i=1;i<=100;i++))
    do
      let s+=i
    done
    
    echo $s  ###函数的返回值通过这个echo返回，当有返回值时，函数内部只能有一个echo
  }
  
  result=$(funWithReturn)  ###调用有返回值的函数，返回值赋给result
  #funWithReturn
  
  echo "函数的返回值：${result}"
  echo "函数的返回状态码：$?"
  ```

+ 有参数，又有返回值

  ```shell
  #!/bin/bash
  funWithReturn(){
    s=0
    for((i=$1;i<=$2;i++))
    do
      let s+=i
    done
    echo $s
  }
  
  result=$(funWithReturn $1 $2)
  #funWithReturn
  
  echo "函数的返回值：${result}"
  echo "函数的返回状态码：$?"
  
  
  ###执行脚本
  sh  test31.sh 10 20 # $1就是10 $2就是20
  ```

  ### 数组的操作

+ 定义数组

```shell
#!/bin/bash

my_array=("A" "B" "C" "D")

#我们也可以使用下标来定义数组:

array_name[0]=value0

array_name[1]=value1

array_name[2]=value2
```

+ 获取数组中的所有元素和长度

  ```shell
  #!/bin/bash
  my_array[0]="A"
  my_array[1]="B"
  my_array[2]="C"
  my_array[3]="D"
  
  #获取数组元素
  echo "数组的元素为: ${my_array[*]}"
  echo "数组的元素为: ${my_array[@]}" #两种方式等价
  
  #获取数组长度
  echo "数组元素个数为: ${#my_array[*]}"
  echo "数组元素个数为: ${#my_array[@]}"
  
  ```

+  遍历数组

  ```shell
  #!/bin/bash
  
  my_arr=('AA BB' 'CC')  
  my_arr_num=${#my_arr[*]}  #获取数组长度
  for((i=0;i<my_arr_num;i++));
  do
    echo "----------------- ------------"
    echo ${my_arr[$i]}  # 通过索引获取每一个元素
  done
  ```

  



### 脚本的相互调用

脚本之间可以进行导入

+ demo0.sh

  ```shell
  #!/bin/bash
  
  func1(){
    echo "Hello World0"
  }
  ```

+ demo1.sh

  ```shell
  #!/bin/bash
  #定义数组
  array=("AA" "BB" "CC" "DD")
  
  #定义方法
  func1(){
    echo "Hello World1"
  }
  ```

+ demo2.sh

  ```shell
  #!/bin/bash
  
  ######方式1############
  #. /export/shell/demo1.sh          #导入demo1.sh脚本-绝对路径(推荐)
  #. ./demo1.sh                      #导入demo1.sh脚本-相对路径
  
  ######方式2############
  #source ./demo1.sh                 #导入demo1.sh脚本-相对路径
  
  ######调入多个脚本######
  source /export/shell/demo0.sh      #导入demo0.sh脚本-绝对路径
  source /export/shell/demo1.sh      #导入demo1.sh脚本-绝对路径
  
  my_arr_num=${#array[*]}  #获取数组长度
  for((i=0;i<my_arr_num;i++));
  do
    echo "----------------- ------------"
    echo ${array[$i]}  # 通过索引获取每一个元素
  done
  
  func1 #当多个脚本中有同名函数，则导入方式是就近原则
  ```

  