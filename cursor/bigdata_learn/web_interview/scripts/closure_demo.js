/**
 * 闭包示例
 * 演示闭包的各种应用场景
 */

// 1. 闭包实现私有变量
function createCounter() {
    let count = 0;
    
    return {
        increment: function() {
            count++;
            return count;
        },
        decrement: function() {
            count--;
            return count;
        },
        getCount: function() {
            return count;
        }
    };
}

const counter1 = createCounter();
const counter2 = createCounter();

console.log(counter1.increment()); // 1
console.log(counter1.increment()); // 2
console.log(counter2.increment()); // 1（独立的闭包）

// 2. 闭包实现函数柯里化
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        } else {
            return function(...nextArgs) {
                return curried.apply(this, args.concat(nextArgs));
            };
        }
    };
}

function add(a, b, c) {
    return a + b + c;
}

const curriedAdd = curry(add);
console.log(curriedAdd(1)(2)(3)); // 6
console.log(curriedAdd(1, 2)(3)); // 6

// 3. 闭包实现模块化模式
const Module = (function() {
    let privateVar = 0;
    
    function privateMethod() {
        return privateVar;
    }
    
    return {
        getPrivateVar: function() {
            return privateMethod();
        },
        setPrivateVar: function(value) {
            privateVar = value;
        },
        publicMethod: function() {
            return 'This is a public method';
        }
    };
})();

// 4. 闭包在循环中的应用
// 问题：循环中使用闭包
for (var i = 0; i < 5; i++) {
    setTimeout(function() {
        console.log(i); // 输出 5 次 5
    }, 100);
}

// 解决方案1：使用立即执行函数
for (var i = 0; i < 5; i++) {
    (function(j) {
        setTimeout(function() {
            console.log(j); // 输出 0, 1, 2, 3, 4
        }, 100);
    })(i);
}

// 解决方案2：使用 let
for (let i = 0; i < 5; i++) {
    setTimeout(function() {
        console.log(i); // 输出 0, 1, 2, 3, 4
    }, 100);
}

// 5. 闭包实现缓存（Memoization）
function memoize(fn) {
    const cache = {};
    
    return function(...args) {
        const key = JSON.stringify(args);
        
        if (cache[key]) {
            console.log('Cache hit');
            return cache[key];
        }
        
        console.log('Cache miss');
        const result = fn.apply(this, args);
        cache[key] = result;
        return result;
    };
}

function expensiveFunction(n) {
    console.log('Computing...');
    return n * n;
}

const memoizedFunction = memoize(expensiveFunction);
console.log(memoizedFunction(5)); // Computing... 25
console.log(memoizedFunction(5)); // Cache hit 25
