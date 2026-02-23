# Day05 Git 课堂笔记

## 回顾

```
1. 初始化配置 git安装完成之后只需要初始化配置
   git config --global user.name '用户名'
   git config --global user.email '用户名'
   
2. 仓库初始化 每个项目初始化一次
   git init
	
3. 添加到暂存区
   git add 文件名
   git add -A

4. 提交到版本库
   git commit -m '提交信息'
   git commit -am '提交信息'

5. 查看状态
   git status

6. 查看具体修改的信息
   git diff
   git diff --cached

7. 撤销工作区的修改（工作区修改，未添加到暂存区）
   git restore 文件名
   git restore .

8. 撤销暂存区(已经添加到暂存区)
   git restore --staged 文件名
   git restore --staged .
```



## 1 历史版本回滚

### 1.1 查看历史版本号

```bash
git log		# 查看提交记录
git log -n	# 查看最近的 n 次提交几次，n 是个数字
git log --oneline	# 每次提交记录只用一行显示
```

如果需要查看被回滚掉的提交的版本号：

```bash
git reflog
```

### 1.2 通过指定版本号回滚

```bash
git reset --hard <commitID>
```

> **注意：**
>
> 进行版本回退时，不需要使用完整的哈希字符串(版本号，CommitID)，前七位即可。
>
> 版本切换之前，要提交当前的代码状态到仓库。

### 1.3 快捷回滚

```bash
git reset --hard HEAD^    # 恢复到上个版本
git reset --hard HEAD^^    # 恢复到上上个版本
git reset --hard HEAD^^^    # 恢复到上上上个版本
```



## 2 Git 忽略文件

### 2.1 被忽略的文件

哪些文件需要被 git 忽略：

1. 忽略操作系统自动生成的文件，比如缩略图等；
2. 忽略编译生成的中间文件、可执行文件等，也就是如果一个文件是通过另一个文件自动生成的，那自动生成的文件就没必要放进版本库，比如 Java 编译产生的`.class`文件；
3. 忽略你自己的带有敏感信息的配置文件，比如存放口令的配置文件。

### 2.2 设置忽略文件 `.gitignore`

忽略文件的文件名是 `.gitignore` 的文件, 文件内可以设置项目的忽略规则。

忽略文件可以放在项目中的任意目录中，放在哪个目录作用范围就是哪个目录； 一般忽略文件会放在项目的根目录下。

### 2.3 忽略文件的语法

可以用`git check-ignore` 命令检查 `.gitignore`文件格式是否正确。

`.gitignore` 文件的格式规则如下：

1. 空格不匹配任意文件，可作为分隔符，可用反斜杠转义。
2. `#` 开头的文件表示注释，可以使用反斜杠进行转义。
3. `!` 开头的模式表示否定，该文件将会再次被包含，如果排除了该文件的父级目录，则使用 `!` 也不会再次被包含。可以使用反斜杠进行转义。
4. `/` 结束的模式只匹配目录以及在该目录路径下的内容。
5. `/` 开始的模式匹配当前目录下的，（`.gitignore` 文件所在的目录）
6. `**` 匹配多级目录，可在开始，中间，结束。
7. `*` 匹配任意数量的任意字符串。
8. `?` 通用匹配单个字符。
9. `[]` 通用匹配单个字符列表。

### 2.4 忽略文件配置示例

```
# 此为注释 
# 忽略所有的 .a 文件
*.a

# 但跟踪所有的 lib.a，即便你在前面忽略了 .a 文件
!lib.a

# 只忽略当前目录下的 TODO 文件，而不忽略子目录下的 TODO 文件
/TODO

# 忽略任何目录下名为 build 的文件夹
build/

# 忽略 doc/notes.txt，但不忽略 doc/server/arch.txt
doc/*.txt

# 忽略 doc/ 目录及其所有子目录下的 .pdf 文件
doc/**/*.pdf
```

### 2.5 忽略已经提交到版本库的文件

对于已经加入到版本库的文件，可以在版本库中删除该文件

```bash
git rm --cached 文件名
```

然后在 `.gitignore` 中配置忽略。

最后执行 `git add` 和 `git commit` 提交即可。



## 3 Git 分支

### 3.1 分支介绍

分支并非 Git 的专利，几乎所有的版本控制系统都以某种形式支持分支。

使用分支意味着你可以把你的工作从开发主线上分离开来，以免影响开发主线。

![分支](images/分支.jpg)

### 3.2 分支操作

> **注意：** 在进行分支操作之前，一定一定要把工作区都提交了！！！

#### ① 创建分支

```bash
git branch 分支名
```

会根据当前所在的分支进行创建。

#### ② 切换分支

```bash
git switch 分支名
# 或者
git checkout 分支名
```

#### ③ 创建并切换到该分支

```bash
git switch -c 分支名
# 或者
git checkout -b 分支名
```

#### ④ 查看分支

```bash
git branch
```

#### ⑤ 重命名分支

```bash
git branch -m 分支名 新的名字
```

#### ⑥ 删除分支

```bash
git branch -d 分支名
```

#### ⑦ 合并分支

如果把 A 分支合并到 B 分支上，先切换到 B 分支上。

```bash
git merge 分支名		# 把指定的分支合并到当前分支
```

### 3.3 合并分支解决冲突

当多个分支修改同一个文件后，合并分支的时候就会产生冲突。冲突的解决非常简单，将内容修改为最终想要的结果，然后继续执行 `git add` 与 `git commit` 就可以了。

```
1. 有主分支和开发分支，保持同步
2. 开发购物车，基于开发分支，创建一个 shopcart 分支，在  shopcart 分支上开发
3. 开发订单模块，基于开发分支，创建 order 分支，在 order 分支上开发
4. 开发完成后，shopcart 分支和 order 分支都需要合并到开发分支；shopcart 分支、order 分支删除
5. 在开发分支上测试，解决bug，将开发分支合并到主分支
```







## 4 Git 远程仓库

### 4.1 GitHub 介绍

Hub 是一个代码仓库的托管平台，因为只支持 Git 作为唯一的版本库格式进行托管，故名 GitHub。可以创建远程中心仓库，为多人合作开发提供便利。

目前，其注册用户已经超过 350 万，托管版本数量也是非常之多，其中不乏知名开源项目 Ruby on Rails、jQuery、python等。

2018 年 6 月 4 日，微软宣布，通过 75 亿美元的股票交易收购代码托管平台 GitHub。

网址：[https://github.com](https://github.com/)

从搜索框，输入，可以查看星数十万以上，会从高到低排列

```
stars:>100000
```



### 4.2 GitHub 使用流程

#### ① 场景一： 本地有仓库 远程没有仓库

1. 在 github 上创建一个仓库

2. 获取到远程仓库的地址

3. 本地运行命令， 给仓库地址取别名为 origin

   ```sb
   git remote add origin 远程仓库地址
   ```

   ```bash
   # 仓库地址别名的其他操作
   git remote remove 名字;			# 删除
   git remote rename 名字 新名字;     # 改名
   git remove get-url 名字；		   # 查看名字对应的仓库地址
   git remove set-url 名字 地址;	   # 修改名字对应的仓库地址
   ```

4. 本地仓库提交

5. 把本地仓库推送到远程仓库 （第一次）, `-u` 的意思是记录远程仓库的地址。

   ```bash
   git push -u origin master
   ```

6. 以后如果向远程仓库推送

   ```bash
   git push master
   ```

#### ② 场景二： 本地没仓库 远程有仓库

1. 获取到远程仓库的地址

2. 本地克隆远程仓库

   ```bash
   git clone 远程仓库地址
   ```

3. 本地仓库如有修改，一定要添加并提交

4. 将本地仓库推送到远程

   ```bash
   git push
   ```

   ```bash
   git push origin 本地分支名:远程分支名
   ```
   
   

#### ③ 从远程仓库克隆之后，创建本地分支

默认从远程仓库克隆的只有主分支，如果我们需要在其他分支进行开发，只要在本地创建分支即可。

**查看所有分支：包括远程的分支**

```bash
git branch -a
```

**本地创建分支并设置对应的远程分支：**

```bash
git switch -c 分支名 origin/远程分支名
```





### 4.3 多人合作

#### ① 创建组织配置权限

```
首页 -> 右上角 `+` 号 -> new Organization
免费计划
填写组织名称和联系方式（不用使用中文名称）
邀请其他开发者进入组织（会有邮件邀请，==如收不到，请查看垃圾箱==）
配置组织权限，组织首页右侧  settings -> Member privileges -> 选择 write
```

#### ② 多人合作工作流程

**第一天上班：**

1. 获取到仓库地址，克隆到本地

2. 进行开发修改代码，添加、提交。

3. 下班之前要推送到远程仓库

   3.1 先确定所有的都提交了（commit）

   3.2 推送之前先拉取

   ```bash
   git pull
   ```
   3.3 正式推送
   
   ```bash
   git push
   ```

**以后每一天：**

1. 早上上班，拉取远程仓库

   ```bash
   git pull
   ```

2. 进行开发修改代码，添加、提交。

3. 下班之前要推送到远程仓库

   3.1 先确定所有的都提交了（commit）

   3.2 推送之前先拉取

   ```bash
   git pull
   ```
   3.3 正式推送
   
   ```bash
   git push
   ```

#### ③ 冲突解决

与合并分支类似，多个成员如果修改了同一个文件，就会出现冲突； 本地拉取文件的时候，如果远程仓库中与本地的提交有冲突，解决：修改再次提交， 再推送



### 4.4 GitHub 免密登录

1. 创建非对称加密对

   ```sh
   ssh-keygen -t rsa -C "xxx@xxx.com"
   ```

2. 文件默认存储在家目录（c:/用户/用户名/.ssh）的 .ssh 文件夹中。

   - id_rsa 私钥
   - id_rsa.pub 公钥

3. 将公钥（.pub）文件内容配置到账号的秘钥中

   首页 -> 右上角头像-> settings -> SSH and GPG keys -> new SSH Key

4. 克隆代码时，选择 ssh 模式进行克隆 （地址 在仓库首页 绿色 克隆的位置 选择 use ssh）

   ```shell
   git clone git@github.com/unclealan/team-repo-1.git
   ```

5. 克隆代码时的提醒，这里需要输入 `yes`







## 5 GitFlow - Git 开发流程

![](D:\Library\SH200910\03阶段_PC项目&jQuery&BootStrap\Day16_Git\images\GitFlow.png)



- Master 主分支。上面只保存正式发布的版本
- Hotfix 线上代码 Bug 修复分支。开发完后需要合并回Master和Develop分支。
- Feather 功能分支。当开发某个功能时，创建一个单独的分支，开发完毕后再合并到 dev 分支
- Release 分支。待发布分支，Release分支基于Develop分支创建，在这个Release分支上测试，修改Bug
- Develop 开发分支。开发者都在这个分支上提交代码




