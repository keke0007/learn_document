# Day06 Node 课堂笔记

官方网站地址： https://nodejs.org/en/	中文网站地址 ：http://nodejs.cn/

## 1 Node 概述

### 1.1 什么是Node.js

 Node.js，也称 Node，是一个基于 `Chrome V8` 引擎的 JavaScript 运行环境（宿主），与浏览器是等价的。 

### 1. 2 什么学习 Node.js

```
1. 基于 Node 进行后端开发，前端工程师秒变全栈工程师。
2. 前端可以实现工程化开发，前端自动化工具、模块化打包工具gulp、webpack以及 vue、react 的脚手架工具都是基于 Node 运行的。
3. 以开发很多小工具，如自动化脚本，爬虫程序等。
4. 可以开发桌面应用，框架 Electron、ReactNative等
```

### 1.3 什么是后端开发

- 前端是运行在客户端上的代码， 也单指WEB前端，运行在客户端浏览器上的代码
- 后端是运行在服务器端的程序，主要实现业务逻辑，数据库读取等功能

### 1.4 Node.js 的特点

* 单线程
* 非阻塞 I/O (non-blocking I/O)
* 事件驱动 （event-driven）



## 2 安装和使用

### 2.1 下载地址

官方网站 https://nodejs.org/en/download/

中文网站 http://nodejs.cn/download/

历史版本下载 https://npm.taobao.org/mirrors/node/

### 2.2 版本选择

注意区分 LTS 版本与 Current 版本的不同，我们推荐安装 LTS 版本。

LTS 为长期稳定版（long term service），对于追求稳定性的企业级项目来说，推荐安装 LTS 版本的 Noode.js。

Current 为新特性尝鲜版，对热衷于尝试新特性的用户来说，可以安装 Current 版本的 Node.js，但是，Current 版本中可能存在隐藏的 Bug 或安全漏洞，因此不推荐在企业级项目中使用 Current 版本的

### 2.3 REPL 方式运行

##### 进入REPL

命令行或终端运行 node ，就进入了 repl 模式

##### 退出REPL

.exit 或者 按两下 `ctrl+c` 或者 `ctrl+d`

##### REPL命令

- `ctrl + c` - 按下两次 - 退出 Node REPL。
- `ctrl + d` - 退出 Node REPL.
- 向上/向下键 - 查看输入的历史命令*
- `tab` 键 - 列出当前变量（对象）
- `.help` - 列出使用命令
- `.break` - 退出多行表达式
- `.clear` - 退出多行表达式
- `.save filename` - 保存当前的 Node REPL 会话到指定文件
- `.load filename` - 载入当前 Node REPL 会话的文件内容。

### 2.4 脚本方式运行

```bash
node JS脚本文件地址
```

### 3.5 命令行工具

#### ① windows 平台

```
cmd
powershell
gitbash
```

#### ② macOS 平台

```
终端
```

#### ③ vscode 内置的终端工具

```
鼠标放在目录上，右键菜单，选择在“在集中终端中打开”
```



## 3 内置常量

```
__dirname		获取JS脚本所在目录的绝对路径
__filename		获取JS脚本自己的绝对路径
```



## 4 Buffer

### 4.1 Buffer 介绍

Buffer 是一个和数组类似的对象，不同是 Buffer 是专门用来保存二进制数据的。

**特点：**

- 大小固定：在创建时就确定了，且无法调整。
- 性能较好：直接对计算机的内存进行操作。
- 每个元素大小为 1 字节（byte）。

**字节单位：**

```
1 Byte = 8 bit；
1 KB = 1024 Byte;
1 MB = 1024 KB;
1 GB = 1024 MB;
1 TB = 1024 GB;
...
```

### 4.2 创建 Buffer

```js
Buffer.alloc(10);        // <Buffer 00 00 00 00 00 00 00 00 00 00>

Buffer.alloc(2,"a");    // <Buffer 61 61>

Buffer.alloc(2,257);    // <Buffer 01 01>

Buffer.from("abcdefghik");    // <Buffer 61 62 63 64 65 66 67 68 69 6b>
Buffer.from([1, 2, 3]);        // <Buffer 01 02 03>
```

**alloc 和 allocUnsafe 的区别：**

```
不安全创建 Buffer.allocUnsafe(size)： 返回一个指定大小的 Buffer 实例，但是它不会被初始化，所以该方法比 alloc() 要快得多，但可能包含的旧数据。
```

### 4.3 读写 Buffer

```js
const b = Buffer.from("abcdefghik");
b[7];
b.toString();
b.forEach((item, index)=>{
    console.log(item, index);
});
```

### 4.4 关于溢出

buffer 每个元素能表示的最大数字是 255，如果超过 255 的数字，会舍去高位（二进制）

```js
buff3[0] = 365;                    // ‭0001 0110 1101‬ 
console.log(buff3[0]);             // 109
```

### 4.5 关于中文

一个 UTF-8 的中文字符大多数情况都是占 3 个字节。





## 5 内置模块

Noode 当中的模块分为三种：内置模块，第三方模块以及自定义模块。 不论哪一种模块，在使用时都必须先引入模块。

### 5.1 模块引入方式

```js
const 变量 = require('模块');
```



### 5.2 path 模块

- `path.join([path1][, path2][, ...])` 用于连接路径。该方法的主要用途在于，会正确使用当前系统的路径分隔符，Unix系统是"`/`"，Windows系统是"`\`"。
- `path.isAbsolute(path)` 判断参数 **path** 是否是绝对路径。
- `path.dirname(p)` 返回路径中目录的部分 。
- `path.basename(p[, ext])` 返回路径中的最后一部分，文件名部分。
- `path.extname(p)` 返回路径中文件的后缀名。
- `path.resolve()` 将路径或者路径片段序列化为绝对路径 (常用)。



### 5.2 fs 模块

#### ① 文件读取

```js
// 引入模块
const fs = require('fs');
const path = require('path');

// 要读取文件的路径
const filename = path.join(__dirname, './data/a.txt');


// ----------------------------------------------------
// 异步方式 读取文件内容
/*
fs.readFile(filename, (err, data) => {
    if (err) {
        console.log('文件读取失败：', err.errno, err.code);
        return;
    }
    // console.log(data);  // Buffer 数据
    console.log(data.toString());
});
console.log('开始读取...');
*/

// 指定编码方式 直接对读取到二进制数据进行编码
fs.readFile(filename,'utf-8', (err, data) => {
    if (err) {
        console.log('文件读取失败：', err.errno, err.code);
        return;
    }
    console.log(data); 
  
});
console.log('开始读取...');


// -------------------------------------------
// 同步方式读取文件内容
// try {
//     // const data = fs.readFileSync(filename);
//     const data = fs.readFileSync(filename, 'utf-8');
//     console.log(data);
// } catch (error) {
//     console.log('文件读取失败：', error.errno, error.code);
// }
// console.log('开始读取...');

```

#### ② 文件写入

```js
// 导入模块
const fs = require('fs');
const path = require('path');


// 要写入文件的地址
// const filename = path.join(__dirname, './data/b.txt');
const filename = path.resolve('./data/b.txt');

// 要写入的内容
const data01 = '你好小乐' + Math.random() + '\n';
// const data02 = Buffer.alloc(20, 100);

// -----------------------------------------------------
// 异步f方式 写入文件
fs.writeFile(filename, data01, err => {
    if (err) {
        console.log('写入失败！', err.errno, err.code);
    } else {
        console.log('写入成功！');
    }
});



// ----------------------------------------------------------
// 同步方式 写入文件
try {
    fs.writeFileSync(filename, data01);
    console.log('写入成功！');
} catch (err) {
    console.log('写入失败！');
};


// -------------------------------------------------------------------
// 同步方式写入
try {
    for (let i = 0; i <= 10000; i ++) {
        fs.appendFileSync(filename, data01);
    }
} catch (err) {
    console.log('写入失败！');
}
```

#### ③ 文件重命名

```js
// 导入模块
const fs = require('fs');

// ---------------------------------------------------
// 重命名 将a.txt 改成 a.md
fs.rename('./data/a.txt', './data/a.md', err => {
    if (err) {
        console.log('重命名失败！');
    } else {
        console.log('重命名成功！');
    }
});


// ---------------------------------------

// 移动文件的位置
fs.rename('./data/a.md', './a.md', err => {
    if (err) {
        console.log('重命名失败！');
    } else {
        console.log('重命名成功！');
    }
});

fs.renameSync()
```

#### ④ 删除文件

```js
const fs = require('fs');

fs.unlink('./a.md', err => {
    if (err) {
        console.log('文件删除失败！');
    } else {
        console.log('文件删除成功！');
    }
})

fs.unlinkSync()
```



#### ⑤ 创建目录

#### ⑥ 删除目录

#### ⑦ 读取目录

#### ⑧ 判断文件或目录是否存在

#### ⑨ 判断是文件还是目录

#### ⑩ 流式读写文件



### 5.3 url 模块

### 5.4 querystring 模块







