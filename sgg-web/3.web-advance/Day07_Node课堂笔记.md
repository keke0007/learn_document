# Day07 Node 课堂笔记

## 1 内置模块

Noode 当中的模块分为三种：内置模块，第三方模块以及自定义模块。 不论哪一种模块，在使用时都必须先引入模块。

### 1.1 path 模块

- `path.join([path1][, path2][, ...])` 用于连接路径。该方法的主要用途在于，会正确使用当前系统的路径分隔符，Unix系统是"`/`"，Windows系统是"`\`"。
- `path.isAbsolute(path)` 判断参数 **path** 是否是绝对路径。
- `path.dirname(p)` 返回路径中目录的部分 。
- `path.basename(p[, ext])` 返回路径中的最后一部分，文件名部分。
- `path.extname(p)` 返回路径中文件的后缀名。
- `path.resolve()` 将路径或者路径片段序列化为绝对路径 (常用)。



### 1.2 fs 模块

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

```js
fs.mkdir(newDir, {recursive:true},err => {
    if (err) {
        console.log('创建目录失败：', err.message);
    } else {
        console.log('创建目录成功！');
    }
});

// 异步方式 创建目录 递归方式创建多级目录 
fs.mkdir(newDir, {recursive:true},err => {
    if (err) {
        console.log('创建目录失败：', err.message);
    } else {
        console.log('创建目录成功！');
    }
});

// 同步方式 创建目录
try {
    fs.mkdirSync(newDir);
    // fs.mkdirSync(newDir,{recursive:true});  递归方式创建多级目录
} catch (err) {
    console.log('目录创建失败：', err.message);
}
```

#### ⑥ 删除目录

```js
// 异步方式 删除空目录
fs.rmdir(dirname01, err => {
    if (err) {
        console.log('删除失败：', err.message);
    } else {
        console.log('删除成功！');
    }
});

// 异步方式 删除非空目录使用递归方式
fs.rmdir(dirname02, {recursive: true}, err => {
    if (err) {
        console.log('删除失败：', err.message);
    } else {
        console.log('删除成功！');
    }
});

// 同步方式 删除目录
try {
    fs.rmdirSync(dirname01);
    console.log('删除成功！');
} catch (err) {
    console.log('删除失败：', err.message);
}
```

#### ⑦ 读取目录

```js
// 异步方式 读取目录
fs.readdir(dirname, (err, data) => {
    if (err) {
        console.log('读取失败：', err.message);
    } else {
        for (let basename of data) {
            // console.log(basename);
            console.log(path.resolve(dirname, basename));
        }
    }
});

// 同步方式 读取目录
try {
    const files = fs.readdirSync(dirname);
    console.log(files);
} catch (err) {
    console.log('读取失败：', err);
}
```

#### ⑧ 判断文件或目录是否存在

```js
// 异步方式 判断文件或目录是否存下
fs.access(file02, err => {
    if (err) {
        console.log('文件不存在！');
    } else {
        console.log('文件存在！');
    }
});

// 同步方式
try {
    fs.accessSync(file02);
    console.log('文件存在！');
} catch {
    console.log('文件不存在！');
}
```

#### ⑨ 判断是文件还是目录

```js
fs.stat(file02, (err, stats) => {
    if (err) {
        console.log('错误：', err.message);
    } else {
        console.log('是否是目录：', stats.isDirectory());
        console.log('是否是文件：', stats.isFile());
    }
})

// 同步方式
try {
    const stats = fs.statSync(file01)
    console.log(file01);
    console.log('是否是目录：', stats.isDirectory());
    console.log('是否是文件：', stats.isFile());
    console.log('');
} catch (err) {
    console.log('错误：', err,message);
}
```

#### ⑩ 流式读写文件

**流式读取文件内容：**

```js
// 创建文件读取流
const rs = fs.createReadStream(file);

rs.on('data', chunk => {
    console.log(chunk);
});

rs.on('end', () => {
    console.log('读取完毕！');
});

rs.on('error', () => {
    console.log('读取出错！');
});
```

**流式写文件：**

```js
// 创建写入流
const ws = fs.createWriteStream(file);

ws.on('close', () => {
    console.log('写入完毕！');
});

for (let i = 0; i < 100000; i ++) {
    ws.write(`${i} ${Math.random()} ${Date.now()} \n`);
}

ws.close();
```

**流式复制文件：**

```js
// 创建读取流
const rs = fs.createReadStream(originFile);
// 创建写入取流
const ws = fs.createWriteStream(targetFile);

rs.pipe(ws);
```

### 1.3 url 模块

```js
// 解析网址 用法一
const urlData = url.parse(siteAddress);
console.log(urlData);
console.log(urlData.query);
console.log('');

// 解析网址 用法二
const urlInfo = new url.URL(siteAddress);
console.log(urlInfo);
console.log(urlInfo.searchParams);
```

### 1.4 querystring 模块

```js
const qs = require('querystring');

qs.parse(字符串);  	// 将查询字符串解析成对象
qs.stringify(对象)  // 将对象转为查询字符串的形式
```





## 2 异常处理语法

### 2.1 Error 对象

```js
new Error('错误的信息');
```

### 2.2 throw 主动抛出错误

```js
// throw 100;
// throw 'Hello World';
throw new Error('高小乐 is not defined');
```

### 2.3 try catch 结构

```js
try {
    // 系统报错  调用不存在的函数
    getInfo();

    // 主动抛出的错误
    // throw new Error('xiaole is not defiend');
} catch (err) {
    console.log('捕获到错误：', err.errno, err.message);
}
```

```js
1. try 里面的错误会被 catch 捕获，不论是代码错误还是主动抛出，捕获到错误之后由程序员处理，系统不会报错
2. try catch 不论是否抛出错误，都不影响后面的语句的执行
3. try 内部，错误后面的语句不会执行
```





## 3 JSON 数据格式以及处理

### 3.1 什么是`JSON`数据格式

`JSON`全称是 `JavaScript Object Notation` (JavaScript 对象表示法) ,是一种轻量级的数据交换格式。

`JSON` 的语法与 `JS` 定义数组和对象的语法存在如下的区别：

```
1. json 中的字符串必须使用双引号
2. json 中的属性名必须使用双引号包裹
3. json 中的最后一个属性不能有逗号
4. json 中的属性值不能是表达式
```

### 3.2 JS 中的 JSON 对象

- `JSON.stringify(obj/arr)`	将对象或数组转为 json 格式的字符串。

- `JSON.parse(json)`:`	将 json 格式的字符串转为对象或数组。



## 4 模块化

### 4.1 模块化介绍

Node 应用由模块（每一个`JS`即是一个模块）组成，采用` CommonJS `模块规范(提供了模块引入导出的规则)。每个文件就是一个模块，有自己的作用。<font color=red>在一个文件里面定义的变量、函数、类（class），都是私有的，对其他文件不可见（模块作用域）。在服务器端，模块的加载是运行时同步加载的； </font>

模块化是指解决一个复杂问题时，自顶向下逐层把系统划分成若干模块的过程，对于整个系统来说，模块是可组合，分解和更换的单元。

### 4.2 模块化特点

- 所有代码都运行在模块作用域，不会污染全局作用域。
- 模块可以多次加载，但是只会在第一次加载时运行一次，然后运行结果就被缓存了，以后再加载，就直接读取缓存结果。要想让模块再次运行，必须清除缓存。
- 模块加载的顺序，按照加载模块的代码的书写顺序。

### 4.3 模块化的好处

* 提高代码的复用性
* 提高代码的可维护性
* 可以实现按需加载

### 4.4 模块化规范

#### ① CommonJS 规范
CommonJS 是一种模块化规范，最初提出来是在浏览器以外的地方使用，并且当时命名为 ServerJS，后来为了体现它的广泛性，更名为 CommonJS，也可以简称为 CJS
Node 是 CommonJS 在服务端一个具有代表性的实现
Browserify 是 CommonJS 在浏览器端的一种实现
webpack 具备对 CommonJS 的支持与转换

#### ② AMD 规范
AMD 主要是应用于浏览器的一种模块化规范,AMD 是 Asynchronous Module Definition（异步模块定义）的缩写，它采用的是异步加载模块，事实上 AMD 的规范早于 CommonJS，但是现在 CommonJS 仍被使用，但 AMD 已经很少用了。
实现 AMD 规范的库主要是 require.js 和 curl.js

#### ③ CMD 规范
CMD 也是应用于浏览器的一种模块化规范，CMD 是 Common Module Definition（通用模块定义）的缩写，他也是采用了异步加载模块，但是它将 CommonJS 的优点吸收了过来，这个目前也很少使用了。
SeaJS 实现了 CMD 规范

### ④ ES Module 规范
ES Module 规范是 ES 提出的，是官方的模块化规范。

### 4.5 Node 中 模块的分类

Node.js中根据模块来源的不同，将模块分为了3大类，分别是：

* 内置模块（由Node.js官方提供，例如：fs,path,http）
* 自定义模块：用户创建的每个JS文件，都是自定义模块。，
* 第三方模块：由第三方开发出来的模块，并非官方提供的内置模块，也不是用户创建的自定义模块，使用前需要先下载。

Node.js 支持CommonJS 规范和ES6 模块规范



## 5 CommonJS 模块规范

### 5.1 在模块中暴露数据

1）模块内如果没有暴露数据，引人模块的时候会得到一个空对象。

2）通过给 `module.exports` 赋值，实现暴露数据。

3）通过为 `module.exports` 设置属性，暴露数据。

4）通过为 `exports` 设置属性，暴露数据。 给 `exports` 设置属性，就是给 `module.exports` 设置属性，但不能改变`exports`的引用地址，这样的话 `exports` 与 `module.exports` 就脱钩了。

### 5.2 引入模块（自定义模块）

1）自定义模块的地址需要以 `./`、  `../`  开头，这是模块文件的相对路径，相对于当前的执行的 JS 脚本的位置，不是命令行打开的目录。

2）如果模块文件的地址没有以  `./`、  `../`  开头，会被认为是内置模块或第三方模块的模块名。

3）如果模块文件扩展名是 `.js` 或者是 `.json` ，在导入的时候可以省略扩展名。如果引入模块文件时，模块路径没有扩展名，会依次查找 `.js` 文件、`.json` 文件、目录。

### 5.3 模块文件的扩展名

对于不同扩展名的模块文件，Node.js 有不同的处理方式

- 扩展名是 `.js`的模块文件： 读取文件内容并编译执行并获取模块中暴露的数据。
- 扩展名是`.json`的模块文件： 读取文件，用 `JSON.parse()` 解析返回结果作为获取的数据。
- 扩展名是`.node`的模块文件： 这是 c/c++ 编写的扩展文件，通过 `dlopen()` 方法编译。
- 其他扩展名，文件内容会被当做 JavaScript 代码去解析。

### 5.4 整个目录作为一个模块

1）会默认加载该目录下 `package.json` 文件中 `main` 属性定义的入口文件。

2）如果没有package.json, 或者 `main` 属性对应的文件不存在，则自动找 `index.js` 、 `index.json` 作为入口文件。



## 6 ES6 模块规范

### 6.1 Node 中使用 ES 模块规范

Node.js 要求 ES6 模块采用`.mjs`后缀文件名。也就是说，只要脚本文件里面使用`import`或者`export`关键字，那么就必须采用`.mjs`后缀名。

如果不希望将后缀名改成`.mjs`，可以在项目的`package.json`文件中，指定`type`字段为`module`。

### 6.2 在模块中暴露数据

#### ① 暴露单个数据

使用 `export default` 可以在模块中暴露单个数据，注意文件中 `export default` 语句只能出现一次。

```js
export default 100;
const data = [10,20,30,40,50];
export default data;
function say() {}
function eat() {}

export default {
  say,
  eat
}
```

#### ② 暴露多个数据

使用 `export` 可以暴露多个数据，有两种写法：

```js
// 第一种写法 在声明变量的同时暴露
export const firstName = 'Lee';
export const lastName = 'KeQiang';
export const year = 1918;
export function fn() {};
export const obj = {name:'mingge',age:100}


// 第二种写法 在文件底部统一暴露（推荐）
const firstName = 'Lee';
const lastName = 'KeQiang';
const year = 1918;
function fn() {};
const obj = {name:'mingge',age:100}

export {firstName, lastName, year, fn, obj}
```

### 6.3 引入模块并使用模块中暴露的数据

#### ① 模块使用 `export default` 暴露单个数据

```js
import 变量名 from '模块地址';
```

#### ② 模块使用 `export` 暴露多个数据

```js
// 获取的变量名必须与模块暴露的变量名一致，可以多次分别获取，可以取别名
import {name, year as y} from '模块地址';
import {fn} from '模块地址';

// 可以将模块中的数据整体加载
import * as 别名 from '模块地址';
```



## 作业

```
 1. 封装容量单位转换函数，字节转为其他单位， 第二个参数指定 目标单位 0：不转换， 1：转为KB； 2:转为MB 3：转为GB 4:转为TB
 2. 将定义好的函数封装成模块，分别封装成 CommonJS 模块和 ES6 模块
```



