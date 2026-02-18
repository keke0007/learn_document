/**
 * Promise 示例
 * 演示 Promise 的各种用法和实现
 */

// 1. Promise 基本使用
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        const success = Math.random() > 0.5;
        if (success) {
            resolve('Success');
        } else {
            reject('Error');
        }
    }, 1000);
});

promise
    .then(value => {
        console.log(value); // Success
    })
    .catch(error => {
        console.error(error); // Error
    });

// 2. Promise 链式调用
fetch('/api/users')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        return fetch(`/api/users/${data[0].id}`);
    })
    .then(response => response.json())
    .then(user => console.log(user))
    .catch(error => console.error(error));

// 3. Promise.all - 并行执行多个 Promise
const promises = [
    fetch('/api/users'),
    fetch('/api/posts'),
    fetch('/api/comments')
];

Promise.all(promises)
    .then(responses => Promise.all(responses.map(r => r.json())))
    .then(([users, posts, comments]) => {
        console.log({ users, posts, comments });
    })
    .catch(error => {
        console.error('One of the promises failed:', error);
    });

// 4. Promise.race - 竞态，返回最先完成的
Promise.race([
    fetch('/api/slow-endpoint'),
    new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 5000)
    )
])
    .then(response => response.json())
    .catch(error => console.error(error));

// 5. Promise.allSettled - 等待所有 Promise 完成
Promise.allSettled([
    Promise.resolve('Success'),
    Promise.reject('Error'),
    Promise.resolve('Another Success')
])
    .then(results => {
        results.forEach((result, index) => {
            if (result.status === 'fulfilled') {
                console.log(`Promise ${index}:`, result.value);
            } else {
                console.log(`Promise ${index}:`, result.reason);
            }
        });
    });

// 6. async/await
async function fetchUser() {
    try {
        const response = await fetch('/api/users');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const userResponse = await fetch(`/api/users/${data[0].id}`);
        const user = await userResponse.json();
        console.log(user);
        return user;
    } catch (error) {
        console.error('Error fetching user:', error);
        throw error;
    }
}

// 7. 简化版 Promise 实现
class MyPromise {
    constructor(executor) {
        this.state = 'pending';
        this.value = undefined;
        this.reason = undefined;
        this.onFulfilledCallbacks = [];
        this.onRejectedCallbacks = [];
        
        const resolve = (value) => {
            if (this.state === 'pending') {
                this.state = 'fulfilled';
                this.value = value;
                this.onFulfilledCallbacks.forEach(fn => fn());
            }
        };
        
        const reject = (reason) => {
            if (this.state === 'pending') {
                this.state = 'rejected';
                this.reason = reason;
                this.onRejectedCallbacks.forEach(fn => fn());
            }
        };
        
        try {
            executor(resolve, reject);
        } catch (error) {
            reject(error);
        }
    }
    
    then(onFulfilled, onRejected) {
        return new MyPromise((resolve, reject) => {
            const handleFulfilled = () => {
                try {
                    if (typeof onFulfilled === 'function') {
                        const result = onFulfilled(this.value);
                        resolve(result);
                    } else {
                        resolve(this.value);
                    }
                } catch (error) {
                    reject(error);
                }
            };
            
            const handleRejected = () => {
                try {
                    if (typeof onRejected === 'function') {
                        const result = onRejected(this.reason);
                        resolve(result);
                    } else {
                        reject(this.reason);
                    }
                } catch (error) {
                    reject(error);
                }
            };
            
            if (this.state === 'fulfilled') {
                handleFulfilled();
            } else if (this.state === 'rejected') {
                handleRejected();
            } else {
                this.onFulfilledCallbacks.push(handleFulfilled);
                this.onRejectedCallbacks.push(handleRejected);
            }
        });
    }
    
    catch(onRejected) {
        return this.then(null, onRejected);
    }
    
    static resolve(value) {
        return new MyPromise(resolve => resolve(value));
    }
    
    static reject(reason) {
        return new MyPromise((_, reject) => reject(reason));
    }
}

// 使用示例
const myPromise = new MyPromise((resolve, reject) => {
    setTimeout(() => {
        resolve('Success');
    }, 1000);
});

myPromise.then(value => {
    console.log(value); // Success
});
