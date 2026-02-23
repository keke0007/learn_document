## 1 本地仓库操作

### 1.1 仓库配置 仓库初始化

```bash
git config
```

```bash
git init
```

### 1.2 添加暂存和提交仓库

```bash
git add -A
```

```bash
git commit -m '提交信息'
```

### 1.3 撤销

```bash
# 未添加暂存
git restore .
git restore <文件名>
```

```bash
# 已经添加暂存  从暂存中撤销
git restore --staged .
git restore --staged <文件名>
```

### 1.4 版本回滚

```bash
# 查看提交记录
git log
git log --oneline
git log -n

# 跳转到指定版本
git reset --hard commitID

# 跳转到上n个版本
git reset --hard HEAD^
git reset --hard HEAD^^
git reset --hard HEAD^^^

# 查看被回滚掉的提交记录
git reflog
```

### 1.5 分支

```bash
# 创建分支
git brach 分支名

# 查看分支
git branch

# 切换分支
git switch 分支名
git checkout 分支名

# 创建并切换分支
git switch -c 分支名
git checkout -b 分支名

# 删除分支
git branch -d 分支名

# 重命名分支
git branch -m 分支名 新的名字

# 合并分支 先切换到目标分支
git merge 源分支名
```

### 1.6 忽略文件

```
.gitignore 文件
```

被忽略的文件，不会被添加、提交





## 2 远程仓库有关的操作

### 2.1 常见的远程仓库（代码托管平台）

```
github
gitee
```

### 2.2 登录远程仓库 验证方式

```
https	账号密码
ssh     设置公钥
```

### 2.3 本地仓库与远程仓库第一次同步

#### 本地有仓库 远程无仓库

```
1. 新建空的远程仓库并获取地址
2. 本地仓库添加提交
3. 本地仓库推送到远程
   git remoted add origin 远程仓库地址
   git push -u origin master
4. 拉取和推送
   git pull
   git push
```

#### 本地无仓库 远程有仓库

```
1. 获取远程仓库地址
2. 克隆到本地
   git clone 远程仓库地址
3. 添加提交
4. 拉取推送
   git pull
   git push
```

### 2.4 开发流程

```
1. 先 pull
2. 开发代码，频繁添加提交
3. 下班前推送 推送前先pull
   git pull
   git push
```

### 2.5 解决冲突

```
手动修改代码 再 add commit push
```



