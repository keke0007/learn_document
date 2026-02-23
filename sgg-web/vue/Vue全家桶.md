# 一- 了解 Vue3 

> 官方文档: https://cn.vuejs.org/

## 1-1- 了解相关信息

> - 2年多开发, 100+位贡献者, 2600+次提交, 600+次PR(Pulll Request)
> - Vue3支持vue2的大多数特性
> - 更好的支持Typescript

## 1-2- 性能提升

> - 打包大小减少41%
> - 初次渲染快55%, 更新渲染快133%
> - 内存减少54%
> - 重写虚拟DOM的实现和Tree-Shaking

## 1-3- Composition API

> - 也称组合 API
> - setup
> - ref 和 reactive
> - computed 和 watch
> - 新的生命周期函数
> - 自定义hooks函数

## 1-4- 其它新增特性

> -  Teleport - 瞬移组件的位置
> -  Suspense - 异步加载组件的loading界面
> -  全局API的修改

## 1-5- vscode插件

* 安装https://blog.csdn.net/hebiwen95/article/details/126268585

# 二- 安装脚手架

* 命令

  ```shell
  vue create first
  ```

* 选择手动安装，在原来基础上选择typescript,一路回车即可！

# 三- 分析脚手架文件

## 3-1- 差异

* vue.config.js (与原来相同)

  ```js
  const {defineConfig} = require('@vue/cli-service')
  module.exports = defineConfig({
  	transpileDependencies: true,
  	lintOnSave:false,// 关闭语法检查
  	devServer:{
  		open:true,// 自动打开浏览器
  		port:80,// 指定端口号
  		host:"zhangpeiyue.com",// 指定host
  	}
  })
  
  ```

* 入口文件main.ts:src->main.ts

  ```ts
  // 在Vue3中不需要实例化Vue
  // 可以通过createApp创建单页面应用的一个对象,类型是一个函数。
  import {createApp} from "vue";
  // console.log(createApp);// 是一个函数
  // 引入根组件App,根组件不允许省略扩展名.vue(main.ts中不支持省略.vue)
  import App from "@/App.vue";
  // 运行该函数必须指定一个根组件。
  // 该函数返回的是一个对象，称该对象为app对象。
  
  // 方式一
  // const app = createApp(App);
  // console.log(app);// 输出的app对象只是一个普通对象
  // 指定挂载的容器。(将id为app的标签作为应用的容器)
  // app.mount("#app");
  
  // 方式二
  createApp(App).mount("#app");
  
  ```

* src->App.vue

  ```vue
  <template>
      <!-- Vue3中可以拥有多个根元素   -->
      <h3>App组件1</h3>
      <h3>App组件2</h3>
      <h3>App组件3</h3>
  </template>
  
  <script>
  import {defineComponent} from "vue";
  // defineComponent作用对类型的推断辅助。由于ts拥有推断机制，所以也可以省略。
  export default defineComponent({
      name:"App"
  })
  </script>
  
  <style scoped>
  
  </style>
  ```

* 

## 3-2- 在Vu3中使用Vue2语法

* src->App.vue

  ```vue
  <template>
      <h3>App组件</h3>
      <p>{{ num }}</p>
      <p>{{ arr }}</p>
      <button @click="num++">{{ num }}</button>
      <button @click="changeNum">{{ num }}</button>
      <button @click="changeNum2(100)">{{ num }}</button>
      <p>{{sum}}</p>
      <hr/>
      <button @click="isShow=!isShow">{{isShow}}</button>
      <Child v-if="isShow"></Child>
      <p v-for="item in arr" :key="item">{{item}}</p>
  </template>
  
  <script>
  // 支持Vue2的基本语法,不支持销毁生命周期钩子函数
  import Child from "@/components/Child";
  const arr = [1, 2, 3, 4, 5];
  export default {
      name: "App",
      components: {Child},
      data() {
          return {
              num: 1,
              arr,
              isShow:true
          }
      },
      computed:{
          sum(){
              // return this.arr.length;
              return this.arr.reduce((sum,item)=>{
                  sum+=item;
                  return sum;
              },0)
          }
      },
      methods: {
          changeNum() {
              // 1  false
              // console.log(this.num,this.arr===arr);
              this.num++;
              this.arr.push(this.arr.length + 1);
          },
          changeNum2(n) {
              this.num += n;
          }
      },
      // 挂载阶段
      beforeCreate() {
          console.log("1-beforeCreate");
      },
      created(){
          console.log("2-created");
      },
      beforeMount() {
          console.log("3-beforeMount");
      },
      mounted(){
          console.log("4-mounted");
      },
      // 更新
      beforeUpdate() {
          console.log("1-beforeUpdate");
      },
      updated() {
          console.log("2-updated");
      }
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3>Child</h3>
  </template>
  
  <script>
  export default {
      name: "Child",
      beforeDestroy() {
          console.log("1-beforeDestroy");
      },
      destroyed() {
          console.log("2-destroyed");
      }
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

  

# 四- 组合式API

## 4-1- setup(配置钩子函数)

> setup是组合API的入口。

* 基本使用:App.vue

  ```vue
  <template>
      <h3>App</h3>
      <p>userName:{{userName}}</p>
      <p>age:{{age}}</p>
      <button @click="age++">{{age}}</button>
      <button @click="changeAge">changeAge{{age}}</button>
  </template>
  <script>
      import {defineComponent} from "vue";
  
      export default defineComponent({
          beforeCreate() {
              console.log("beforeCreate");
          },
          // 1- setup是一个钩子函数。
          // 2- 在beforeCreate之前执行。
          // 3- this指向的undefined.
          // 4- setup如果要使用return进行返回，要求必须是一个对象
          // 5- setup不允许设置为async函数。
          // 6- 返回对象的属性可以直接被模板调用
          // 7- 如果data与setup拥有相同名的数据，那么以setup为准
          // 8- data中的数据是响应式的，而setup中的数据不是响应式。
          data(){
              return {
                  age:100,
                  userName:"lisi->data"
              }
          },
          setup(){
              return {
                  age:10,
                  userName:"zhangsan->setup",
                  changeAge(){
                      this.age+=2;
                      console.log("changeAge",this.age)
                  }
              }
          }
      })
  </script>
  <style>
  
  </style>
  ```

## 4-2- 响应组合式API-ref

### 4-2-1- 基本使用-App.vue

```vue
<template>
    <h3>App</h3>
    <p>count:{{count}}</p>
    <button @click="suibian">{{count}}</button>
    <hr/>
    <p>{{obj}}</p>
    <button @click="obj.userName+='!'">更改userName</button>
    <button @click="changeAge">更改userName</button>
</template>
<script lang="ts">
    import {defineComponent,ref} from "vue";

    export default defineComponent({
        setup(){
            // setup是组合API的入口
            // 1- 可以通过ref实现数据的响应式。
            // 2- ref需要通过import {ref} from "vue"导入
            // 3- ref是一个函数。
            // 4- 返回的是一个拥有value属性的RefImpl的实例对象。
            // 5- ref接收的值即是ref函数返回的RefImpl的实例对象的value属性值。
            // 6- 常见操作：ref在setup中调用，其调用结果作为setup返回对象的属性。
            // 7- setup返回的对象中的属性值如果是RefImpl的实例，那么在模块中可以直接被解包。
            //    解包：可以不需要写 RefImpl实例.value,可以直接书写实例即可。
            //         比如实例为count,在模板中可以直接写count
            //    在setup中不会被解包，必须要写.value
            // 8- ref可以接收任意类型的数据，并实现响应式。
            // 9- 如果ref接收的是一个非原始类型，那么其底层用的是reactive.(下午详聊)
            // 10- 在模板中事件监听中可以直接操作refImpl属性，在script中必须要使用.value
            // const num = ref();
            // console.log(num.value);// undefined

            let count = ref(100);
            let obj = ref({
                userName:"zhangsan",
                age:12
            })
            console.log(count.value);
            return {
                count,
                obj,
                suibian(){
                    // console.log("suibian")
                    // this.count = 200;// 可以实现响应式
                    count.value = 200;// 可以实现响应式
                },
                changeAge(){
                    obj.value.age+=10;
                    // 基本数据类型-ref接收的类型
                    console.log("count",count);
                    // 引用类型-ref接收的类型
                    console.log("obj",obj)
                }
            }

        }
    })
</script>
```

### 4-2-2- ref响应式的原理

* Object.defineProperty

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
  	<meta charset="UTF-8">
  	<title>Title</title>
  </head>
  <body>
  
  </body>
  <script>
  	// 1- defineProperty是属性Object对象下的函数。
  	// 2- 接收三个参数：第一个参数是操作的对象，第二个参数是拦截的属性名字，第三个参数是描述对象。
  	// 1- get
  	// const obj = {
  	// 	userName:"zhangsan"
  	// };
  	// Object.defineProperty(obj,"userName",{
  	// 	// 获取时（输出，赋值，比较）可以被调用,返回值即为调用的结果
  	// 	get(){
  	// 		console.log("get")
  	// 	}
  	// });
  	// // 输出
  	// console.log(obj.userName);// undefined
  	// // 比较
  	// if(obj.userName === "zhangsan"){
  	// 	console.log("ok");
  	// }else{
  	// 	console.log("no");
  	// }
  	// // 赋值
  	// const userName = obj.userName;
  	// console.log(userName);// undefined
  	// function fn(userName){
  	// 	console.log(userName);// undefined
  	// }
  	// fn(obj.userName);
  	
  	
  	// 2- set
  	const obj = {
  		userName:"zhangsan"
  	}
  	let value = obj.userName;
  	Object.defineProperty(obj,"userName",{
  		// 读取时
  		get(){
  			return "《"+value+"》";
  		},
  		// 设置时执行，接收的参数即是最新赋予的值。
  		set(v){
  			// console.log("set",v);
  			value = v;
  		}
  	});
  	// obj.userName = "lisi";
  	// console.log(obj.userName);// 《lisi》
  	console.log(obj.userName);//
  	
  </script>
  </html>
  ```

  

* 内置构造函数Proxy

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
  	<meta charset="UTF-8">
  	<title>Title</title>
  </head>
  <body>
  
  </body>
  <script>
  	// 1- Proxy是一个内置构造函数
  	// console.log(Proxy);// ƒ Proxy() { [native code] }
  	
  	// 2- 接收两个参数，第一个参数是一个对象(目标对象)，第二个参数是描述对象
  	let obj = {
  		userName:"zhangsan"
  	};
  	// p是Proxy实例,相当于对obj进行了一个深度复制。
  	// 所有对obj的操作可以通过p来进行。即是代理。
  	const p = new Proxy(obj,{
  		// 当获取p的属性时执行。
  		// 第一个参数是目标对象
  		// 第二个参数是操作的属性名
  		// 第三个参数是Proxy实例p
  		get(target,key,proxy){
  			console.log("proxy->get->userName",target===obj);// proxy->get->userName true
  			console.log("proxy->get->key",key);// proxy->get->key userName
  			console.log("proxy->get->proxy",proxy===p);// proxy->get->proxy true
  			return "《"+target[key]+"》";
  		},
  		// 当修改p属性时执行。
  		// 第一个参数是目标对象target
  		// 第二个参数是操作的属性名key
  		// 第三个参数是要修改的值
  		// 第四个参数是Proxy实例p
  		set(target,key,newValue,proxy){
  			console.log("proxy-set->target",target===obj);// proxy-set->target true
  			console.log("proxy-set->key",key);// proxy-set->key userName
  			console.log("proxy-set->newValue",newValue);// proxy-set->newValue lisi
  			console.log("proxy-set->proxy",proxy===p);// proxy-set->proxy true
  			target[key] = newValue;
  		}
  	});
  	// console.log(obj.userName,p.userName);
  	// obj.userName = "lisi";
  	// p.userName = "lisi";
  	
  	console.log(p.userName);// 《zhangsan》
  	
  	p.userName = "lisi";
  	console.log(p.userName);// 《lisi》
  	
  </script>
  </html>
  ```

  

* 实现ref响应式

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
  	<meta charset="UTF-8">
  	<title>Title</title>
  </head>
  <body>
  	<h3></h3>
  	<p></p>
  	<hr/>
  	<button>点我</button>
  </body>
  <script>
  	// 1- ref是一个函数
  	// 2- ref可以接收任意类型的数据
  	// 3- ref可以获取到一个RefImpl实例
  	// 4- RefImpl实例中拥有属性value
  	// 5- ref接收的是一个基本数据类型是通过defineProperty实现的响应式
  	// 6- 如果ref接收的是一个引用类型，那么返回的RefImpl实例中的value值是proxy
  	function RefImpl(value){
  		if(typeof value === "object"){
  			// 将value设置为目标对象
  			this.value = new Proxy(value,{
  				get(target,key){
  					// console.log("get");
  					return target[key];
  				},
  				set(target,key,newValue){
  					target[key] = p.innerText = newValue;
  				}
  			})
  		}else{
  			let _value = value;
  			Object.defineProperty(this,"value",{
  				get(){
  					// console.log("get");
  					return _value;
  				},
  				set(v){
  					// console.log("set",v);
  					h3.innerText=_value = v;
  				}
  			})
  		}
  		
  	}
  	
  	const ref = function(value){
  		return new RefImpl(value);
  	}
  	const h3 = document.querySelector("h3");
  	const p = document.querySelector("p");
  	const btn = document.querySelector("button");
  	const count = ref(10);
  	const obj = ref({
  		userName:"zhangsan"
  	})
  	h3.innerText = count.value;
  	p.innerText = obj.value.userName;
  	btn.onclick = function(){
  		count.value++;
  		obj.value.userName+="!";
  		// console.log(count.value)
  	}
  	
  	
  </script>
  </html>
  ```

### 4-2-3- ref与普通元素结合使用

```vue
<template>
    <div>
        <h3 ref="h3Ref">ref</h3>
        <input value="100" ref="userName" type="text">
    </div>
</template>
<script setup lang="ts">
import {onMounted, ref} from "vue";
// 与普通标签结合使用：在标签中作用ref属性，其值为ref对象。
//                 那么当组件挂载完成后得到的value值为真实DOM元素。
const userName = ref<HTMLInputElement | number>(1);
const h3Ref = ref();
console.log(userName.value);// 还未实现挂载，所以值为初始的1
onMounted(()=>{
    console.log("mounted",userName.value===document.querySelector("input"));
    console.log("mounted",(document.querySelector("input") as  HTMLInputElement).value);
    console.log("mounted",(userName.value as  HTMLInputElement).value);
    console.log("mounted",h3Ref.value.innerText)
})
</script>
```



### 4-2-4- ref与v-for结合使用

```vue
<template>
    <div>
        <p ref="pRef" v-for="item in arr" :key="item">{{item}}</p>
    </div>
</template>
<script setup lang="ts">
import {onMounted, ref} from "vue";
// ref与v-for结合使用得到的是一个数组，数组内的元素是真实的DOM
let arr = [1, 2, 3, 4, 5, 6];
let pRef = ref();
console.log(pRef.value);
onMounted(function(){
    // console.log("mounted",pRef.value)
    for(let index = 0;index<pRef.value.length;index++){
        if(index % 2 === 1){
            pRef.value[index].style.color="red";
        }else  pRef.value[index].style.color="green";
    }
})
</script>
```



### 4-2-5- ref与组件结合使用

* src->App.vue

  ```vue
  <template>
      <h3>与组件结合使用</h3>
      <button @click="childRef.setCount(200)">更改子组件中的count</button>
      <hr/>
      <child ref="childRef"/>
  
  </template>
  <script setup lang="ts">
  import {onMounted, ref} from "vue";
  import Child from "./components/Child.vue";
  // ref与组件结合使用，可以获取组件proxy实例。
  const childRef = ref();
  
  onMounted(function(){
      console.log(childRef.value)
  })
  </script>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <div>Child</div>
      <p @click="setCount(50)">count:{{count}}</p>
  </template>
  
  <script setup lang="ts">
     import {ref} from "vue";
  
     let a = 1;
     let count = ref(100);
     let setCount = function(n:number){
         count.value = n;
     }
     // 如果要在组件外部使用当前组件的数据状态，必须暴露。
     defineExpose({a,count,setCount})
  </script>
  
  <style scoped>
  
  </style>
  ```

  

## 4-3- 响应组合式API-reactive

### 4-3-1- 基本使用

```vue
<template>
    <h3>reactive组合API</h3>
    <button @click="count++">{{count}}</button>
    <hr/>
    <p>{{obj.userName}}</p>
    <p>{{obj.age}}</p>
    <button @click="obj.userName+='!'">修改userName</button>
    <button @click="obj.age++">修改age</button>
    <button @click="objHandler">修改userName以及age</button>
</template>
<script lang="ts">
    import {defineComponent,ref,reactive} from "vue";
    // reactive也可以实现数据的响应式。
    // 1- reactive也是来自于vue
    // 2- reactive是一个函数
    // 3- reactive接收的是一个对象。
    // 4- reactive返回的是一个Proxy实例。
    // 5- 常用：在setup中声明并返回,在模板中可以直接使用，在script中可以对其进行修改并实现响应式。
    export default defineComponent({
        name:"App",
        setup(){
            const count = ref(1);
            // setup中声明
            const obj = reactive({
                userName:"zhangsan",
                age:12
            })
            return {
                count,
                // 返回
                obj,
                objHandler(){
                    obj.userName+="!";
                    obj.age ++;
                }
            }
        }
    })
</script>
```

### 4-3-2- reactive的原理

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Title</title>
</head>
<body>
	<h3></h3>
	<button>点我</button>
</body>
<script>
	const btn = document.querySelector("button");
	const h3 = document.querySelector("h3");
	// 1- reactive是一个函数
	// 2- 返回一个Proxy实例
	// 3- 接收的是一个对象
	function reactive(value){
		return new Proxy(value,{
			get(target,key){
				return target[key];
			},
			set(target,key,newValue){
				h3.innerText = target[key] = newValue;
			}
		})
	}
	const obj = reactive({
		age:100
	})
	h3.innerText = obj.age;
	btn.onclick = function(){
		obj.age++;
		console.log(obj.age);
	}
</script>
</html>
```

### 4-3-3- ref以及reactive的区别

> 相同点：都是函数，都是来自于vue,都可以实现响应式。
>
> 不同点：
>
> * 数据定义方面：
>   * ref常用于声明基本数据类型
>   * reactive用于声明引用类型（对象，数组）
>   * 注意：ref也可以声明引用类型。ref声明的引用类型的本质是通过reactive创建的。
> * 响应原理方面：
>   * ref是通过Object.defineProperty实现的（基本类型）。引用类型是通过reactive创建的。
>   * reactive是通过Proxy内置构造函数实现的。
> * 使用方面：
>   * ref在模块中不需要value,在JS中需要写value
>   * reactive不需要value.

### 4-3-4- ref以及reactive需要注意的地方

```vue
<template>
    <h3>App</h3>
    <p @click="num++">num:{{ num }}</p>
    <p @click="count++">ref->count:{{ count }}</p>
    <p @click="setCount(2)">ref->count:{{ count }}</p>
    <p @click="obj.age++">reactive->obj.age:{{ obj.age }}</p>
    <p @click="upObjAge">reactive->obj.age:{{ obj.age }}</p>
    <p @click="upInfoAge">ref->info.age:{{ info.age }}</p>
</template>

<script setup lang="ts">
// 注意1：如果通过reactive创建了一个引用类型的数据，那么如果在使用时，
//       直接更改其引用地址，那么不会进行响应。
// 注意2：如果通过ref创建了数据状态，只要将其value值设置为引用类型，那么在使用时其value的数据类型均是proxy实例。
// 可以通过ref,以及reactive实现响应式。
import {ref,reactive} from "vue";
// 可以渲染，但不支持响应式
let num = 100;
// ref
let count = ref<number>(1);
let info = ref({
    age:90
})
// reactive
let obj = reactive({
    age:100
});
const setCount = (n:number)=> {
    count.value += n;
}
const upObjAge = function(){
    // 如果通过reactive创建了一个引用类型的数据，那么如果在使用时，
    // 直接更改其引用地址，那么不会进行响应。
    // obj = {
    //     age:200
    // };

    // obj = reactive({
    //     age:200
    // })


    console.log(obj);
}
function upInfoAge(){
    // info.value.age++;

    info.value = {
        age:87
    };

    // 如果通过ref创建了数据状态，只要将其value值设置为引用类型，那么在使用时其value的数据类型均是proxy实例。
    console.log(info)
}
</script>

<style scoped>

</style>
```

### 4-3-5- ref实现原理

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Title</title>
</head>
<body>
	<h3></h3>
	<button>点我</button>
</body>
<script>
	const h3 = document.querySelector("h3");
	const btn = document.querySelector("button");
	function reactive(value){
		return new Proxy(value,{
			get(target,key){
				return target[key];
			},
			set(target,key,newValue){
				h3.innerText = target[key] = newValue;
			}
		})
	}
	function RefImpl(value){
		let _value = value;
		// 为当前实例的属性value增加拦截
		Object.defineProperty(this,"value",{
			// 返回值即是该实例下value的值
			get(){
				return _value;
			},
			set(v){
				if(typeof v === "object")
				{
					_value = reactive(v);
					h3.innerText = _value.age;
				}
				
			}
		});
		if(typeof value === "object")
			this.value = reactive(value);
	}
	function ref(value){
		return new RefImpl(value);
	}
	let count = ref({
		age:100
	});
	console.log(count);
	h3.innerText = count.value.age;
	btn.onclick = function(){
		// count.value = {
		// 	age:900
		// }
		// console.log(count.value)
		
		count.value.age = 80;
	}
</script>
</html>
```



## 4-4- setup语法糖

* src->App.vue

  ```vue
  <template>
      <h3>setup语法糖</h3>
      <p>{{num}}</p>
      <button @click="changeNum">修改num,修改不了，因为直接定义的数据不支持响应式</button>
      <hr/>
      <p @click="count++">{{count}}</p>
      <button @click="setCount">修改count</button>
      <hr/>
      <p>{{obj.userName}}</p>
      <button @click="obj.userName+='!'">修改obj->userName</button>
  </template>
  
  <script setup lang="ts">
      // 之前的写法可以将Vue2语法与Vue3语法结合使用。如果使用语法糖只支持Vue3
      // 语法糖即是在script标签中增加setup
      // 之前要在setup函数中定义数据，然后返回。
      // 在语法糖中可以直接定义数据，直接定义的数据可以在模板中直接使用。
      // 注意：如果语法糖写法与过去的写法同时出现（出现两个script）,语法糖写法优先
      import {reactive, ref} from "vue";
  
      let num = 100;
      let count = ref(9);
      let obj = reactive({
          userName:"zhangsan"
      })
      const changeNum = function(){
          num++;
      }
      const setCount = function(){
          count.value+=2;
      }
  </script>
  <script lang="ts">
  export default {
      setup(){
          
          return {
              num:102
          }
      }
  }
  </script>
  
  ```


## 4-5- 生命周期组合式API

* src->App.vue

  ``` vue
  <template>
      <h3>生命周期组合API--->{{count}}</h3>
      <button @click="count++">更改count</button>
      <hr/>
      <button @click="isRender=!isRender">销毁子组件</button>
      <Child v-if="isRender"></Child>
  </template>
  <script lang="ts" setup>
  import {onBeforeMount,onUpdated, onBeforeUpdate, onMounted, ref} from "vue";
  // 直接将组件引用即可使用
  import Child from "./components/Child.vue";
  
  const count = ref(100);
  const isRender = ref(true);
  console.log("立即调用。可以替换之前的beforeCreate以及created");
  
  // 当这个钩子被调用时，组件已经完成了其响应式状态的设置，但还没有创建 DOM 节点。它即将首次执行 DOM 渲染过程
  // onBeforeMount(function () {
  //     console.group("********onBeforeMount:注册一个钩子，在组件被挂载之前被调用。**************")
  //     console.log("onBeforeMount->count",count.value);// onBeforeMount->count 100
  //     console.log("onBeforeMount->h3",document.querySelector("h3"));// onBeforeMount->h3 null
  //     console.groupEnd();
  // });
  //
  // onMounted(function () {
  //     console.group("********onMounted:注册一个回调函数，在组件挂载完成后执行。。**************")
  //     console.log("onMounted->count",count.value);// onMounted->count 100
  //     console.log("onMounted->h3",(document.querySelector("h3") as HTMLHeadingElement).innerText);// onMounted->h3 生命周期组合API--->100
  //     console.groupEnd();
  // });
  //
  // onBeforeUpdate(function(){
  //     console.group("********onBeforeUpdate:注册一个钩子，在组件即将因为响应式状态变更而更新其 DOM 树之前调用。**************")
  //     console.log("onBeforeUpdate->count",count.value);// onBeforeUpdate->count 101
  //     console.log("onBeforeUpdate->h3",(document.querySelector("h3") as HTMLHeadingElement).innerText);// onBeforeUpdate->h3 生命周期组合API--->100
  //     console.groupEnd();
  // })
  //
  // onUpdated(function(){
  //     console.group("********onUpdated:注册一个回调函数，在组件因为响应式状态变更而更新其 DOM 树之后调用。。**************")
  //     console.log("onUpdated->count",count.value);// onUpdated->count 101
  //     console.log("onUpdated->h3",(document.querySelector("h3") as HTMLHeadingElement).innerText);// onUpdated->h3 生命周期组合API--->101
  //     console.groupEnd();
  // })
  
  
  </script>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <div>
          <h4>Child</h4>
      </div>
  </template>
  
  <script setup lang="ts">
  import {onBeforeUnmount, onBeforeUpdate, onUnmounted} from "vue";
  let userName = "zhangpeiyue";
  onBeforeUnmount(function(){
      // 当这个钩子被调用时，组件实例依然还保有全部的功能。
      console.group("********onBeforeUnmount:注册一个钩子，在组件实例被卸载之前调用。。**************")
      console.log("onBeforeUnmount->userName",userName);// zhangpeiyue
      console.log("onBeforeUnmount->h3",document.querySelector("h4"));// Child
      console.groupEnd();
  })
  onUnmounted(function(){
      console.group("********onUnmounted:注册一个回调函数，在组件实例被卸载之后调用。。**************")
      console.log("onUnmounted->userName",userName);// zhangpeiyue
      console.log("onUnmounted->h3",document.querySelector("h4"));// Child
      console.groupEnd();
  })
  </script>
  
  <style scoped>
  
  </style>
  ```

## 4-6- 计算属性-computed

* src->App.vue

  ```vue
  <template>
      <h3>计算属性-只读</h3>
      <p @click="count++">count--->{{count}}</p>
      <p>userName--->{{userName}}</p>
      <p>age--->{{age}}</p>
      <p>方案一：函数-->{{getInfo()}}</p>
      <p>方案二：拼接-->{{"今年"+userName+","+age+"岁了"}}</p>
      <p>方案三：计算属性-->{{getInfoCom}}</p>
      <p>方案三：计算属性-->{{getInfoCom}}</p>
      <p>方案三：计算属性-->{{getInfoCom}}</p>
      <p>方案三：计算属性-->{{getInfoCom}}</p>
      <button @click="age++">点我更改age</button>
      <button @click="userName+='!'">点我更改userName</button>
      <hr/>
      <h3>计算属性-读写</h3>
      <p @click="count+=2">count-->{{count}}</p>
      <p>countCom->{{countCom}}</p>
      <button @click="countCom=300">修改计算属性的值</button>
  </template>
  <script setup lang="ts">
      import {ref,computed} from "vue";
      const count = ref(100);
      const age = ref(1);
      const userName = ref("zhangsan");
  
      // getInfo函数的返回结果，只受userName,以及age的影响，
      // 但是更新了数据count,由于模板中调用了该函数，所以该函数依然会被执行，哪怕结果没有任何变化。
      const getInfo = function(){
          console.log("getInfo");
          return "今年"+userName.value+","+age.value+"岁了"
      }
      // 计算属性：
      // 1- 引入组合API->computed
      // 2- computed接收一个回调函数
      // 3- 将computed函数的返回结果赋值给常量,变量
      // 4- 模板中可以直接渲染计算属性。
      // 5- 计算属性拥有缓存功能，只有所依赖的数据不发生改变，计算属性对应的函数不会再次执行。
      // 6- 模板中如果使用了计算属性，那么在初次渲染时，会执行。
      // 创建一个只读的计算属性（接收函数）
      const getInfoCom = computed(function(){
          console.log("getInfoCom")
          return "今年"+userName.value+","+age.value+"岁了"
      })
      // 创建一个读写的计算属性(对象)
      const countCom = computed({
          // 返回值即是计算属性的值
          get(){
              return count.value*2;
          },
          // 当设置计算属性值时调用。接收的参数是修改的值
          set(v:number){
             count.value = v/2;
          }
      })
  </script>
  ```

  

## 4-7- 侦听-watch

```vue
<template>
    <h3>watch</h3>
    <p>ref->count->{{ count }}</p>
    <p>reactive->info->{{ info }}</p>
    <button @click="count++">更改ref->count</button>
    <br/>
    <button @click="info.age++">更改reactive->info->age</button>
    <button @click="info.userName+='!'">更改reactive->info->userName</button>
    <button @click="info.arr.push(info.arr.length+1)">更改reactive->info->arr</button>
    <button @click="info.arr[1]=90">更改reactive->info->arr->下标</button>
    <button @click="stopWatch">停止侦听</button>
</template>
<script setup lang="ts">
// watch:可以针听一个或多个数据，如果侦听的数据发生变化，会执行指定的函数。
import {reactive, ref, watch} from "vue";
// count可以被称为：响应式ref对象|ref对象|ref
const count = ref(1);
// info可以被称为：响应式代理对象|响应式reactive对象|数据源代理对象
const info = reactive({
    userName: "zhangsan",
    age: 12,
    arr: [1, 2, 3, 4]
})
// 1- 侦听ref
// 第一个参数是侦听的数据。第二个参数是回调函数。第三个参数是一个配置对象。
// 当侦听的数据发生改变，那么会执行回调函数。
// watch的返回值是一个函数，通过调用该函数可以停止侦听(当数据发生改变，那么不会再次执行回调函数)。

// const stopWatch = watch(count,(newValue,oldValue)=> {
//     console.log("watch", newValue, oldValue)
// },{
//     // 立即调用，如果立即调用那么oldValue的值是undefined.
//     immediate:true
// })

// 2- 侦听数据代理对象
// const stopWatch = watch(info,(newValue,oldValue)=>{
//     console.log("侦听数据代理对象",newValue===oldValue)
// },{
//     immediate:true
// });

// 3- 侦听一个函数，该函数返回一个数据
// 函数要有一个返回值，返回值可以依赖一个或多个数据，当返回值发生改变以后会被侦听到。
// const stopWatch = watch(()=>count.value+info.age,(newValue,oldValue)=>{
//     console.log("侦听一个函数",newValue,oldValue)
// },{
//     immediate:true
// })

// 主要应用于侦听代理对象中的某个属性的变化
// 如果返回的是一个引用类型，引用类型的地址没有发生改变不会被侦听，如果被侦听需要增加deep:true
const stopWatch = watch(()=>info.age,(newValue,oldValue)=>{
    console.log("侦听一个函数",newValue,oldValue)
},{
    // deep:true,
    immediate:true
})

// 4- 侦听数组，数组内可以是所有的响应式数据
// newValue是更改后的数据，oldValue是更改前的数据。
// newValue以及oldValue类型是数组。数组中分别为对应数组的更改前以及更改后的值
// const stopWatch = watch([info,count],(newValue,oldValue)=>{
//     // newValue:[info更改后的值，count更改后的值]
//     // oldValue:[info更改前的值，count更改前的值]
//     console.log("侦听数组",newValue,oldValue)
// },{
//     immediate:true
// })

</script>
```



## 4-8- watchEffect

* src->App.vue

  ```vue
  <template>
      <h3>watchEffect</h3>
      <p @click="count++">count-->{{count}}</p>
      <p @click="obj.age++">obj.age-->{{obj.age}}</p>
      <hr/>
      <button @click="isRender=!isRender">显示与隐藏</button>
      <Child v-if="isRender"/>
  </template>
  <script setup lang="ts">
  import Child from "./components/Child.vue";
  // 1- watchEffect是组合API
  // 2- watchEffect是一个函数
  // 3- watchEffect，接收一个回调函数，且该函数会被立即调用
  import {onMounted, reactive, ref, watchEffect} from "vue";
  const isRender = ref(true);
  // 一- 立即调用
  // watchEffect(function(){
  //     console.log("over");
  // })
  
  // 二- 回调函数中所依赖的数据发生改变，会执行回调函数。
  const count = ref(1);
  const obj = reactive({
      age:12
  })
  // 当count发生改变那么会执行
  // watchEffect(()=>{
  //     console.log(count.value);
  // })
  
  // 当count或obj.age发生改变，会执行回调函数。
  // watchEffect(()=>{
  //     console.log(count.value,obj.age);
  // })
  
  // 三- 清除副作用函数
  // 当所依赖的数据发生改变会执行清除副作用函数。
  // 当停止时执行。
  // 当组件被销毁时执行。
  // 不需要指定侦听的数据（不知道）
  // const stop =  watchEffect(function(onInvalidate){
  //     console.log(count.value,obj.age);
  //     onInvalidate(function(){
  //         console.log("清理副作用！")
  //     })
  // })
  // setTimeout(()=>{
  //     stop();
  // },5000)
  
  // 总结：watch与watchEffect有何不同？
  // 1- watchEffect与watch的初次执行时机不同。
  // 2- watchEffect回调函数所依赖的数据发生改变会调用，watch是指定的侦听数据发生改变才会执行。
  // 3- watchEffect无法获取修改前的值。watch可以。
  // 4- watchEffect拥有清理副作用函数。
  
  </script>
  ```

* src->components->Child.vue

  ```vue
  <template>
  <div>Child->{{num}}</div>
  </template>
  
  <script setup lang="ts">
  import {onBeforeUnmount, onMounted, ref, watchEffect} from "vue";
  const num = ref(1);
  // 应用
  watchEffect(function(onInvalidate){
      console.log("watchEffect回调函数");
      const timer = setInterval(function(){
          console.log(1111);
          num.value++;
      },1000)
      onInvalidate(function(){
          console.log("onInvalidate");
          clearInterval(timer);
      })
  })
  
  
  // let timer = -1;
  // onBeforeUnmount(function(){
  //     clearInterval(timer);
  // })
  // onMounted(function(){
  //     timer = setInterval(()=>{
  //         num.value++;
  //         console.log(11111)
  //     },1000)
  // })
  
  </script>
  
  <style scoped>
  
  </style>
  ```

  

## 4-9- nextTick

> 常识：数据发生改变，并不会立刻马上更新视图。

* 基本使用

  ```vue
  <template>
      <div>nextTick:{{count}}</div>
      <div>nextTick:{{userName}}</div>
      <button @click="changeNum">count+1</button>
  </template>
  <script setup lang="ts">
  import {onBeforeUpdate, onUpdated, ref,nextTick} from "vue";
  
  const count = ref(1);
  const userName = ref("zhangsan");
  const changeNum = async function(){
      count.value++;
      userName.value+="!";
      // 1- 回调函数
      // nextTick(function(){
      //     // 可以获取更新以后的视图信息
      //     console.log("nextTick->回调函数",(document.querySelector("div") as  HTMLDivElement).innerText)
      // })
  
      // 2- Promise
      // nextTick().then(()=>{
      //     console.log("nextTick->回调函数",(document.querySelector("div") as  HTMLDivElement).innerText)
      // })
  
      await nextTick();
      console.log("nextTick->回调函数",(document.querySelector("div") as  HTMLDivElement).innerText)
  
  
  
      // console.log("changeNum",(document.querySelector("div") as  HTMLDivElement).innerText)
  
  }
  // onBeforeUpdate(function(){
  //     console.log("onBeforeUpdate")
  // })
  // onUpdated(function(){
  //     console.log("onUpdated",(document.querySelector("div") as  HTMLDivElement).innerText);
  // })
  </script>
  ```

* 应用一

  ```vue
  <template>
      <button @click="changeIsRender">点我</button>
      <div ref="divRef" v-if="isRender"></div>
  </template>
  <script setup lang="ts">
  import {ref,nextTick} from "vue";
  const isRender = ref(false);
  const divRef = ref();
  const changeIsRender = async function(){
      isRender.value = !isRender.value;
      if(isRender.value){
          await nextTick();
          divRef.value.style.width="300px";
          divRef.value.style.height="300px";
          divRef.value.style.background = "red";
      }
  
  }
  </script>
  ```

  

* 应用二

  ```vue
  <template>
      <p ref="pRef" v-for="(item,index) in state.userList" :key="index">{{item}}</p>
  </template>
  <script setup lang="ts">
  import {ref, nextTick, reactive} from "vue";
  type TState = {
      userList:string[]
  }
  const state = reactive<TState>({
      userList: []
  });
  const pRef = ref();
  setTimeout(() => {
      const data = ["张三", "李四", "王五", "赵六"];
      state.userList = data;
      nextTick(function(){
          pRef.value.forEach((item:HTMLParagraphElement ,index:number)=>{
              if(index % 2){
                  item.style.background = "red";
              }else{
                  item.style.background = "green";
              }
          })
      })
  
  }, 3000)
  </script>
  ```

* 应用三

  ```vue
  <template>
      <div>
          <input ref="inputRef" v-if="isEdit" v-model="str" type="text">
          <span v-else>{{ str }}</span>
  
          <button @click="onEdit">{{isEdit?"完成":"编辑"}}</button>
      </div>
  </template>
  <script setup lang="ts">
  import {ref, nextTick, reactive} from "vue";
  
  let str = ref("你现在过的还好吗？");
  let isEdit = ref(false);
  let inputRef = ref();
  const onEdit = function(){
      isEdit.value = !isEdit.value;
      if(isEdit.value){
          nextTick(function(){
              inputRef.value.focus();
          })
  
      }
  }
  </script>
  ```


# 五- 路由

> * 如何搭建一个基本路由。别名，重定向。子路由。传递参数。
> * 如何搭建一个二级路由。
> * 如何传递参数。
> * 如何实现路由的跳转。

## 5-1- 搭建一个基本路由

* 下载

  ```shell
  yarn add vue-router   |    npm install vue-router
  ```

* main.ts

  ```ts
  import {createApp} from "vue";
  import App from "@/App.vue";
  import Home from "@/pages/Home/index.vue";
  import About from "@/pages/About/index.vue";
  import NotFount from "@/pages/NotFount/index.vue";
  // 1- 引入createRouter
  import {createRouter, createWebHashHistory, createWebHistory} from "vue-router"
  // 2- 配置每一个路由器的信息
  const routes = [
      {
          path: "/",
          redirect: "/home"
      }, {
          path: "/home",
          component: Home
      },
      {
          path: "/about",
          component: About
      },
      {
          // vue-router@4不支持以下代码实现404
          // path:"*",
          // component:NotFount
  
          // 需要借助params形式实结合正则实现404
          path: "/:pathMath(.*)",
          component: NotFount
      }
  ]
  // 3- 创建router
  const router = createRouter({
      // 相当于Vue2当中的mode:"history"
      history: createWebHistory(),
      // 相当于Vue2当中的mode:"hash"
      // history:createWebHashHistory(),
      routes,
      scrollBehavior() {
          return {
              left: 0,// 相当于之前的x
              top: 0// 相当于之前的y
          }
      }
  });
  // 4- 安装1
  // const app = createApp(App);
  // app.use(router);
  // app.mount("#app");
  
  // 5- 安装2-链式调用
  createApp(App).use(router).mount("#app");
  ```

## 5-2- 将路由配置信息放置在外部

* src->router->index.ts

  ```ts
  import Home from "@/pages/Home/index.vue";
  import About from "@/pages/About/index.vue";
  import NotFount from "@/pages/NotFount/index.vue";
  // 1- 引入createRouter
  import {createRouter, createWebHashHistory, createWebHistory} from "vue-router"
  // 2- 配置每一个路由器的信息
  const routes = [
      {
          path: "/",
          redirect: "/home"
      }, {
          path: "/home",
          component: Home
      },
      {
          path: "/about",
          component: About
      },
      {
          // vue-router@4不支持以下代码实现404
          // path:"*",
          // component:NotFount
  
          // 需要借助params形式实结合正则实现404
          path: "/:pathMath(.*)",
          component: NotFount
      }
  ]
  // 3- 创建router
  const router = createRouter({
      // 相当于Vue2当中的mode:"history"
      history: createWebHistory(),
      // 相当于Vue2当中的mode:"hash"
      // history:createWebHashHistory(),
      routes,
      scrollBehavior() {
          return {
              left: 0,// 相当于之前的x
              top: 0// 相当于之前的y
          }
      }
  });
  export default router;
  ```

* src->main.ts

  ```ts
  import {createApp} from "vue";
  import App from "@/App.vue";
  import router from "@/router";
  
  // 4- 安装1
  // const app = createApp(App);
  // app.use(router);
  // app.mount("#app");
  
  // 5- 安装2-链式调用
  createApp(App).use(router).mount("#app");
  ```

## 5-3- 懒加载

* src->router->index.ts

  ```ts
  import NotFount from "@/pages/NotFount/index.vue";
  // 1- 引入createRouter
  import {createRouter, createWebHashHistory, createWebHistory} from "vue-router"
  const Home = ()=>import("@/pages/Home/index.vue");
  // 2- 配置每一个路由器的信息
  const routes = [
      {
          path: "/",
          redirect: "/home"
      }, {
          path: "/home",
          component: Home
      },
      {
          path: "/about",
          component: ()=>import("@/pages/About/index.vue")
      },
      {
          // vue-router@4不支持以下代码实现404
          // path:"*",
          // component:NotFount
  
          // 需要借助params形式实结合正则实现404
          path: "/:pathMath(.*)",
          component: NotFount
      }
  ]
  // 3- 创建router
  const router = createRouter({
      // 相当于Vue2当中的mode:"history"
      history: createWebHistory(),
      // 相当于Vue2当中的mode:"hash"
      // history:createWebHashHistory(),
      routes,
      scrollBehavior() {
          return {
              left: 0,// 相当于之前的x
              top: 0// 相当于之前的y
          }
      }
  });
  export default router;
  ```

  

## 5-4- 搭建二级路由

* src->pages->Home->Message->index.vue

  ```vue
  <template>
      <div>
          <div>
              <ul>
                  <li>
                      <a href="/home/message/1">message001</a> &nbsp;&nbsp;
                      <button>push</button> &nbsp;
                      <button>replace</button>
                  </li>
                  <li><a href="/home/message/2">message002</a> &nbsp;&nbsp;<button>push
                  </button> &nbsp;<button>
                      replace
                  </button>
                  </li>
                  <li><a href="/home/message/4">message004</a> &nbsp;&nbsp;<button>push
                  </button> &nbsp;<button>
                      replace
                  </button>
                  </li>
              </ul>
              <button>前进</button>
              <button>后退</button>
          </div>
      </div>
  </template>
  
  <script lang="ts" setup>
  
  </script>
  
  <style scoped>
  
  </style>
   
  ```

* src->pages->Home->NewsList->index.vue

  ```vue
  <template>
      <h3>NewsList</h3>
  </template>
  
  <script lang="ts" setup>
  
  </script>
  
  <style scoped>
  
  </style>
   
  ```

* src->pages->Home->index.vue

  ```vue
  <template>
      <h2>Home组件内容</h2>
      <div>
          <ul class="nav nav-tabs">
              <li><router-link to="/home/newsList" class="list-group-item">News</router-link></li>
              <li><router-link to="/home/message" class="list-group-item" >Message</router-link>
              </li>
          </ul>
          <router-view/>
      </div>
  </template>
  ```

  

* src->router->index.ts

  ```ts
     {
          path: "/home",
          component: Home,
          children:[
              {
                  path:"/home",
                  redirect:"/home/newsList"
              },
              {
                  path:"/home/message",
                  component:()=>import("@/pages/Home/Message/index.vue")
              },
              {
                  path:"/home/newsList",
                  component:()=>import("@/pages/Home/NewsList/index.vue")
              }
          ]
      }
  ```

## 5-5- 渲染Message列表

* 下载

  ```shell
  cnpm install axios
  ```

* src->pages->Home->Message->index.vue

  ```vue
  <template>
      <div>
          <div>
              <ul>
                  <li v-for="item in state.films" :key="item.filmId">
                      <a href="/home/message/1">{{item.name}}</a> &nbsp;&nbsp;
                      <button>push</button> &nbsp;
                      <button>replace</button>
                  </li>
              </ul>
              <button>前进</button>
              <button>后退</button>
          </div>
      </div>
  </template>
  
  <script lang="ts" setup>
  import {onMounted, reactive} from "vue";
  import axios from "axios";
  let state = reactive({
      films:[]
  })
  onMounted(function(){
      // https://m.maizuo.com/gateway?cityId=310100&pageNum=1&pageSize=10&type=1&k=6086743
      axios.get('https://m.maizuo.com/gateway?cityId=310100&pageNum=1&pageSize=3&type=1&k=6086743',{
          headers:{
              "X-Client-Info":'{"a":"3000","ch":"1002","v":"5.2.1","e":"16923264631851757969801217","bc":"310100"}',
              "X-Host":"mall.film-ticket.film.list"
          }
      }).then(value=>{
          // console.log(value.data.data.films);
          state.films = value.data.data.films;
      })
  
  })
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

## 5-6- 三级路由

* src->pages->Home->Message->Detail->index.vue

  ```vue
  <template>
      <h3>Detail</h3>
  </template>
  
  <script lang="ts" setup>
  
  </script>
  
  <style scoped>
  
  </style>
   
  ```

* src->router->index.ts

  ```ts
  		{
              path:"/home/message",
              component:()=>import("@/pages/Home/Message/index.vue"),
              children:[
                  {
                      path:"/home/message/:filmId",
                      component:()=>import("@/pages/Home/Message/Detail/index.vue")
                  }
              ]
  		}
  ```

## 5-7- 优化路由

* src->router->index.ts

  ```ts
  import NotFount from "@/pages/NotFount/index.vue";
  // 1- 引入createRouter
  import {createRouter, createWebHashHistory, createWebHistory} from "vue-router"
  // 2- 配置每一个路由器的信息
  const renderCom = function(name:string){
      return ()=>import("@/pages/"+name+"/index.vue");
  }
  const routes = [
      {
          path: "/",
          redirect: "/home"
      }, {
          path: "/home",
          component: renderCom("Home"),
          children:[
              {
                  path:"/home",
                  component:renderCom("Home/NewsList")
              },
              {
                  path:"/home/message",
                  component:renderCom("Home/Message"),
                  children:[
                      {
                          path:"/home/message/:filmId",
                          component:renderCom("Home/Message/Detail")
                      }
                  ]
              }
          ]
      },
      {
          path: "/about",
          component:renderCom("About")
      },
      {
          // vue-router@4不支持以下代码实现404
          // path:"*",
          // component:NotFount
  
          // 需要借助params形式实结合正则实现404
          path: "/:pathMath(.*)",
          component:renderCom("NotFount")
      }
  ]
  // 3- 创建router
  const router = createRouter({
      // 相当于Vue2当中的mode:"history"
      history: createWebHistory(),
      // 相当于Vue2当中的mode:"hash"
      // history:createWebHashHistory(),
      routes,
      // linkExactActiveClass:"active",
      // linkActiveClass:"active",
      scrollBehavior() {
          return {
              left: 0,// 相当于之前的x
              top: 0// 相当于之前的y
          }
      }
  });
  
  // console.log("router",router);
  export default router;
  ```

  

## 5-7- 三级数据渲染-传递参数

* src->pages->Home->Message->index.vue

  ```vue
  <template>
      <ul>
          <li v-for="item in state.films" :key="item.filmId">
              <router-link :to="{
                  path:'/home/message/'+item.filmId
              }">{{item.name}}</router-link> &nbsp;&nbsp;
              <button>push</button> &nbsp;
              <button>replace</button>
          </li>
      </ul>
      <button>前进</button>
      <button>后退</button>
      <hr/>
      <router-view></router-view>
  </template>
  ```

  

  

* src->pages->Home->Message->Detail->index.vue

  ```vue
  <template>
      <h3>{{state.film.name}}</h3>
      <p>{{state.film.synopsis}}</p>
  </template>
  
  <script lang="ts" setup>
  // 1- 在模板中可以直接使用$route
  // 2- 在script标签中无法使用$route，如何解决？
  // 方案一
  // import $router from "@/router";
  // console.log($router.currentRoute.value.params.filmId);
  
  // 方案二
  // import {useRouter} from "vue-router";
  // import router from "@/router"
  // const $router = useRouter();
  // console.log($router===router);// true
  // console.log($router.currentRoute.value.params.filmId)
  
  // 方案三
  // import {useRoute} from "vue-router";
  // const $route = useRoute();
  // console.log($route.params.filmId)
  
  import {onMounted, reactive, watch} from "vue";
  import {onBeforeRouteUpdate, useRoute} from "vue-router";
  import axios from "axios";
  const $route = useRoute();
  const state = reactive({
      film:{}
  })
  // 获取数据方案一
  // const getway = async function(filmId:string){
  //     const {data:{data:{film}}} =await axios.get("https://m.maizuo.com/gateway?filmId="+filmId+"&k=7345366",{
  //         headers:{
  //             "X-Client-Info":'{"a":"3000","ch":"1002","v":"5.2.1","e":"16923264631851757969801217","bc":"310100"}',
  //             "X-Host":"mall.film-ticket.film.info"
  //         }
  //     })
  //     state.film = film;
  // }
  // onBeforeRouteUpdate(async function(to,from,next){
  //     await getway(to.params.filmId as string)
  //     next();
  // })
  // onMounted(function(){
  //     getway($route.params.filmId as string)
  // })
  
  // 获取数据方案二- watch
  watch(()=>$route.params.filmId,async (filmId)=>{
      const {data:{data:{film}}} =await axios.get("https://m.maizuo.com/gateway?filmId="+filmId+"&k=7345366",{
          headers:{
              "X-Client-Info":'{"a":"3000","ch":"1002","v":"5.2.1","e":"16923264631851757969801217","bc":"310100"}',
              "X-Host":"mall.film-ticket.film.info"
          }
      })
      state.film = film;
  },{
      immediate:true
  })
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

## 5-8- 编程式导航

* src->pages->Home->Message->index.vue

  ```vue
  <template>
      <ul>
          <li v-for="item in state.films" :key="item.filmId">
              <router-link :to="{
                  path:'/home/message/'+item.filmId
              }">{{item.name}}</router-link> &nbsp;&nbsp;
              <button @click="goDetail(item.filmId)">push</button> &nbsp;
              <button @click="$router.replace('/home/message/'+item.filmId)">replace</button>
          </li>
      </ul>
      <button @click="$router.forward()">前进</button>
      <button @click="$router.back()">后退</button>
      <hr/>
      <router-view></router-view>
  </template>
  
  <script lang="ts" setup>
  import {onMounted, reactive} from "vue";
  import {useRouter} from "vue-router";
  import axios from "axios";
  const $router = useRouter();
  const goDetail=(filmId:string)=>{
      $router.push('/home/message/'+filmId)
  }
  let state = reactive({
      films:[]
  })
  
  onMounted(function(){
      // https://m.maizuo.com/gateway?cityId=310100&pageNum=1&pageSize=10&type=1&k=6086743
      axios.get('https://m.maizuo.com/gateway?cityId=310100&pageNum=1&pageSize=3&type=1&k=6086743',{
          headers:{
              "X-Client-Info":'{"a":"3000","ch":"1002","v":"5.2.1","e":"16923264631851757969801217","bc":"310100"}',
              "X-Host":"mall.film-ticket.film.list"
          }
      }).then(value=>{
          // console.log(value.data.data.films);
          state.films = value.data.data.films;
      })
  
  })
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

## 5-9- 动态操作路由的方法

* src->main.ts

  ```ts
  import {createApp} from "vue";
  import App from "@/App.vue";
  import router from "@/router";
  
  // 1- getRoutes:获取所有的路由信息列表，类型是一个数组。
  // const routes = router.getRoutes();
  // console.log(routes);
  
  // 2- hasRoute:判断路由信息是否存在，接收的是路由的名字，返回的是一个布尔值
  // console.log(router.hasRoute("home"));// true
  // console.log(router.hasRoute("home2"));// false
  
  // 3- addRoute:添加路由信息
  // const renderCom = function(name:string){
  //     return ()=>import("@/pages/"+name+"/index.vue");
  // }
  // const aboutRoute = router.addRoute({
  //     path: "/about",
  //     // name:"about",
  //     component:renderCom("About")
  // })
  
  // 4- removeRoute:删除路由
  // 4-1- 方案一
  // 查看路由是否存在：
  // console.log(router.hasRoute("about"));
  // if(router.hasRoute("about")){
  //     router.removeRoute("about");
  // }
  
  // 4-2- 方案二：添加完路由之后会有一个返回值，该返回值是一个函数，调用该函数即可删除
  // aboutRoute();
  // console.log(router.getRoutes());
  
  // 扩展：将所有的路由通过方法去添加
  // 以下数据是通过接口获取过来的。
  const renderCom = function(name:string){
      return ()=>import("@/pages/"+name+"/index.vue");
  }
  const routes = [
      {
          path: "/",
          redirect: "/home"
      },
      {
          path: "/home",
          name:"home",
          component: renderCom("Home"),
          children:[
              {
                  path:"/home",
                  name:"home",
                  component:renderCom("Home/NewsList")
              },
              {
                  path:"/home/message",
                  name:"message",
                  component:renderCom("Home/Message"),
                  children:[
                      {
                          path:"/home/message/:filmId",
                          component:renderCom("Home/Message/Detail")
                      }
                  ]
              }
          ]
      },
      {
          path: "/about",
          name:"about",
          component:renderCom("About")
      },
      {
          // vue-router@4不支持以下代码实现404
          // path:"*",
          // component:NotFount
  
          // 需要借助params形式实结合正则实现404
          path: "/:pathMath(.*)",
          component:renderCom("NotFount")
      }
  ]
  // 方案一：
  // router.addRoute(routes[0]);
  // router.addRoute(routes[1]);
  // router.addRoute(routes[2]);
  // router.addRoute(routes[3]);
  
  // 方案二：
  // routes.forEach(item=>{
  //     router.addRoute(item);
  // })
  
  // 方案三：
  // router.addRoute({
  //     path: "/",
  //     redirect: "/home"
  // });
  // router.addRoute({
  //     path: "/home",
  //     name:"home",
  //     component: renderCom("Home"),
  //     children:[
  //         {
  //             path:"/home",
  //             name:"home",
  //             component:renderCom("Home/NewsList")
  //         },
  //         {
  //             path:"/home/message",
  //             name:"message",
  //             component:renderCom("Home/Message"),
  //             children:[
  //                 {
  //                     path:"/home/message/:filmId",
  //                     component:renderCom("Home/Message/Detail")
  //                 }
  //             ]
  //         }
  //     ]
  // });
  // router.addRoute( {
  //     path: "/about",
  //     name:"about",
  //     component:renderCom("About")
  // });
  // router.addRoute({
  //     // vue-router@4不支持以下代码实现404
  //     // path:"*",
  //     // component:NotFount
  //
  //     // 需要借助params形式实结合正则实现404
  //     path: "/:pathMath(.*)",
  //     component:renderCom("NotFount")
  // })
  
  // 方案四：
  router.addRoute({
      path: "/",
      redirect: "/home"
  });
  router.addRoute({
      path: "/home",
      name:"home",
      component: renderCom("Home")
  });
  // 添加二级路由:第一个参数是所在路由的名字，第二个参数是路由信息
  // 将添加的路由放置在名字为home的路由下。
  router.addRoute("home",{
      path:"/home",
      name:"newList",
      component:renderCom("Home/NewsList")
  })
  router.addRoute("home", {
      path:"/home/message",
      name:"message",
      component:renderCom("Home/Message")
  })
  router.addRoute("message",{
      path:"/home/message/:filmId",
      component:renderCom("Home/Message/Detail")
  })
  router.addRoute( {
      path: "/about",
      name:"about",
      component:renderCom("About")
  });
  router.addRoute({
      path: "/:pathMath(.*)",
      component:renderCom("NotFount")
  })
  
  
  createApp(App).use(router).mount("#app");
  ```

# 六- pinia

> Pinia符合直觉的  Vue.js 状态管理库

## 6-1- 安装

* 下载

  ```shell
  yarn add pinia
  ```

* src->store->index.ts

  ```ts
  // 创建大仓库。
  import {createPinia} from "pinia";
  export default createPinia();
  
  ```

* src->main.ts

  ```ts
  import {createApp} from "vue";
  import App from "@/App.vue";
  import store from "./store";
  createApp(App)
      .use(store)
      .mount("#app");
  ```

  

## 6-2- 采用选项式API的方案

### 6-2-1- state

* 如何定义src->store->modules->counter.ts

  ```ts
  import {defineStore} from "pinia";
  // 通过defineStore可以定义小仓库（模块）
  // defineStore返回的值一般保存至以use开头的常量中。
  // 第一个参数是模块的标识,第二个参数是配置对象
  const useCounterStore = defineStore("counter",{
      // 通过state函数可以定义状态，返回的值即是该模块中的数据状态。
      // state(){
      //     return {
      //         num:100
      //     }
      // }
      // 上方代码也可以写为：
      state:()=>({
          num:200,
          arr:[1,2,3,4,5]
      })
  });
  // 在组件可以通过运行useCounterStore函数操作该模块中的数据状态。
  export default useCounterStore;
  
  ```

* src->App.vue

  ```vue
  <template>
      <h3>练习Pinia</h3>
      <p>counter:{{counter}}</p>
      <p>counter.$id:{{counter.$id}}</p>
      <p>num:{{counter.num}}</p>
      <p>arr:{{counter.arr}}</p>
      <p>_isOptionsAPI:{{counter._isOptionsAPI}}</p>
  </template>
  
  <script lang="ts" setup>
  import useCounterStore from "@/store/modules/counter";
  const counter = useCounterStore();
  // 输出counter模块中的数据状态num
  // console.log(counter.num);
  console.log(counter)
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

### 6-2-2- actions

* src->store->modules->counter.ts

  ```ts
  import {defineStore} from "pinia";
  // 通过defineStore可以定义小仓库（模块）
  // defineStore返回的值一般保存至以use开头的常量中。
  // 第一个参数是模块的标识,第二个参数是配置对象
  const useCounterStore = defineStore("counter",{
      // 通过state函数可以定义状态，返回的值即是该模块中的数据状态。
      // state(){
      //     return {
      //         num:100
      //     }
      // }
      // 上方代码也可以写为：
      state:()=>({
          num:200,
          arr:[1,2,3,4,5]
      }),
      // 1
      actions:{
          addOne(a:number,b:number,c:number,d:number){
              console.log(a,b,c,d);
              this.num+=1;
          },
          delaySet(){
              setTimeout(()=>{
                  this.num=900
              },2000)
          }
      }
  });
  // 在组件可以通过运行useCounterStore函数操作该模块中的数据状态。
  export default useCounterStore;
  
  ```

* src->App.vue

  ```vue
  <template>
      <h3>练习Pinia</h3>
      <p>counter:{{counter}}</p>
      <p>模块的标识->counter.$id:{{counter.$id}}</p>
      <hr/>
      <h3>数据状态</h3>
      <p>num:{{counter.num}}</p>
      <p>arr:{{counter.arr}}</p>
      <hr/>
      <h3>是否使用了组合式API</h3>
      <p>_isOptionsAPI:{{counter._isOptionsAPI}}</p>
      <hr/>
      <h3>支持双向绑定</h3>
      <input type="text" v-model.number="counter.num">
      <hr/>
      <h3>更改数据状态方案一：直接修改</h3>
      <button @click="counter.num++">{{counter.num}}</button>
      <hr/>
      <h3>更改数据状态方案二：借助counter.$patch</h3>
      <button @click="setNum">{{counter.num}}</button>
      <hr/>
      <h3>更改数据状态方案三：actions</h3>
      <button @click="counter.addOne">{{counter.num}}</button>
      <button @click="counter.addOne(1,2,3,4)">{{counter.num}}</button>
      <button @click="actionAddOne">{{counter.num}}</button>
      <button @click="counter.delaySet">异步更新{{counter.num}}</button>
  </template>
  
  <script lang="ts" setup>
  import useCounterStore from "@/store/modules/counter";
  const counter = useCounterStore();
  // 输出counter模块中的数据状态num
  // console.log(counter.num);
  // console.log(counter)
  const setNum = function(){
      // counter.num+=2;
  
      // counter.$patch({
      //     num:counter.num+3
      // })
  
      const num = counter.num+3;
      // $patch接收一个对象，对象的属性名即是要修改的状态名，对应的属性值即是要修改的状态值。
      counter.$patch({
          num
      })
  }
  const actionAddOne = function(){
      counter.addOne(10,11,12,13);
  }
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

### 6-2-1- getters

* src->store->modules->counter.ts

  ```ts
  getters:{
      sum(){
          console.log("sum");
          const value:number = this.arr.reduce((s:number,item:number)=>{
              return s+item;
          },0)
          return value;
      }
  }
  ```

* src->App.vue

  ```vue
  <template>
      <p @click="counter.changeArr">getters->sum:{{counter.sum}}</p>
  </template> 
  ```

  

## 6-3- 采用组合式API的方案

* src->store->modules->todos.ts

  ```ts
  import {defineStore} from "pinia";
  import {computed, reactive, ref, watch} from "vue";
  const useTodosStore = defineStore("todos",()=>{
      // 响应式的ref,reactive----->state
      let taskList = ref([1,2,3,4]);
      let obj = reactive({
          userName:"zhangsan",
          age:12
      })
      // 定义的方法相当于------------>actions
      const addTaskList = function(num:number){
          taskList.value.push(num);
      }
      // 计算属性------------------->getters
      const sum = computed(()=>taskList.value.reduce((v:number,item:number)=>v=v+item,0));
      // watch
      // watch(taskList,()=>{
      //     console.log("taskList改变了")
      // },{
      //     immediate:true,
      //     deep:true
      // })
  
      watch(()=>taskList.value,()=>{
          console.log("taskList改变了")
      },{
          immediate:true,
          deep:true
      })
      // 切记一定一定一定要返回！
      return {
          taskList,
          obj,
          addTaskList,
          sum
      }
  })
  export default useTodosStore;
  ```

* src->App.vue

  ```vue
  <template>
      <h3>组合式API</h3>
      <p>{{todos}}</p>
      <p>taskList:{{todos.taskList}}</p>
      <p>sum:{{todos.sum}}</p>
      <button @click="todos.addTaskList(todos.taskList.length+1)">增加元素</button>
  </template>
  
  <script lang="ts" setup>
  import useTodosStore from "@/store/modules/todos";
  const todos = useTodosStore();
  </script>
  
  <style scoped>
  </style>
  ```

  

## 6-4- 组件外部使用store

* src->test.ts

```ts
// 1- 引入大仓库
import store from "@/store";
import useTodosStore from "@/store/modules/todos";
// 2- 传入大仓库：告知模块todos是属于哪一个大仓库下的。
const todos = useTodosStore(store);
console.log(todos.taskList);
```

* src->main.ts

  ```ts
  import "@/test";
  ```

  

# 七- 组件通讯

## 7-1- vue2父向子通过属性传递参数

* src->App.vue

  ```vue
  <template>
  <div>
      <h3>vue2->父向子传递参数通过属性进行参数的传递</h3>
      <h3>父组件</h3>
      <p>userName:{{userName}}</p>
      <p>age:{{age}}</p>
      <hr/>
      <Child :userName="userName" :age="age" hobby="1"/>
      <hr/>
      <!--  上面使用子组件的语法糖，效果相同  -->
      <Child v-bind="{userName,age,hobby:'1'}" />
  </div>
  </template>
  
  <script>
  import Child from "@/components/Child";
  export default {
      name: "App",
      components: {Child},
      data(){
          return {
              userName:"zhangsan",
              age:10
          }
      }
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

* src->components->Child.vue

  ``` vue
  <template>
      <div>
          <h3>子组件Child</h3>
          <p>props->userName->{{userName}}</p>
          <p>props->age->{{age}}</p>
          <p>props->hobby->{{hobby}}</p>
          <p>props->sex->{{sex}}</p>
          <button @click="fn">点我</button>
      </div>
  </template>
  
  <script>
  export default {
      name: "Child",
      // 1- 数组，数组内的元素是字符串，字符串即是属性的名字
      // props:["userName","age"],
      // 2- 对象：对象的属性即是接收的属性。可以对类型进行限制
      // props:{
      //     // 字符串
      //     userName:String,
      //     // 数字
      //     age:Number
      // },
      // 3- 对象
      props:{
          userName:{
              type:String
          },
          age:{
              type:Number
          },
          hobby:{
              type:String,
              required:true
          },
          sex:{
              type:String,
              default:"男"
          }
      },
      methods:{
          fn(){
              // 可以通过this获取属性，且不允许修改
              console.log(this.userName,this.age,this.hobby,this.sex);
              this.userName= 1;
          }
      }
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

## 7-2- Vue3父向子通过属性进行参数的传递

* src->App.vue  传递参数与vue2相同

  ```vue
  <template>
      <h3>Vue3父向子通过属性进行参数的传递</h3>
      <h3>父组件App</h3>
      <p>userName:{{userName}}</p>
      <p>age:{{age}}</p>
      <hr/>
      <Child :userName="userName" :age="age" hobby="学习"/>
      <hr/>
      <Child v-bind="{userName,age,hobby:'学习'}"/>
  </template>
  
  <script lang="ts" setup>
  import Child from "@/components/Child.vue";
  import {ref} from "vue";
  const userName = ref("vue3");
  const age = ref(12);
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue 接收参数需要使用defineProps

  ```vue
  <template>
      <h3>子组件Child</h3>
      <p>userName:{{ userName }}</p>
      <p>age:{{ age }}</p>
      <p>hobby:{{ hobby }}</p>
      <p>sex:{{ sex }}</p>
      <button @click="fn">点我</button>
  </template>
  
  <script lang="ts" setup>
  // defineProps有两个特点：
  // 1- 不需要引入，可以直接使用
  // 2- 指定接收的属性，指定的属性可以在模板中直接使用。
  //    在script标签中不能直接用。需要通过defineProps的返回值获取。
  
  
  
  // 1- 数组，数组的元素是字符串
  // defineProps(["userName", "age"]);
  // 2- 对象
  // defineProps({
  //     userName:String,
  //     age:Number
  // })
  // 3- 对象，对象的属性值还是对象
  const props = defineProps({
      userName:{
          type:String
      },
      age:{
          type:Number
      },
      hobby:{
          type:String,
          required:true
      },
      sex:{
          type:String,
          default:"男"
      }
  });
  const fn = function(){
      console.log(props.userName);
      console.log(props.age);
      console.log(props.hobby);
      console.log(props.sex);
      // 属性是只读的，不允许更改
      // props.userName="lisi";
  }
  </script>
  
  <style scoped>
  
  </style>
   
  ```

## 7-3- vue2自定义事件

* src->App.vue

  ```vue
  <template>
  <div>
      <h3>vue2->自定义事件</h3>
      <h3>父组件</h3>
      <button @click="changeCount(2)">{{count}}</button>
      <hr/>
      <!--  如果为在父组件中对子组件增加原生事件，子组件是无法获取到事件信息的。点击子组件无效。可以通过增加修饰符.native  -->
  <!--    <Child @click.native="changeCount(4)" :count="count" :changeCount="changeCount"/>-->
      <Child @changeCount="changeCount" :count="count" :changeCount="changeCount"/>
  </div>
  </template>
  
  <script>
  import Child from "@/components/Child";
  export default {
      name: "App",
      components: {Child},
      data(){
          return {
              count:100
          }
      },
      methods:{
          changeCount(count){
              this.count+=count;
          }
      }
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <div>
          <h3>子组件Child</h3>
          <p>count:{{count}}</p>
          <!--   子组件接收父组件传递过来的函数。当点击按钮时调用。     -->
          <button @click="changeCount(3)">调用的是接收的函数：{{count}}</button>
          <button @click="$emit('changeCount',5)">调用自定义事件：{{count}}</button>
          <button @click="fn">调用自定义事件2：{{count}}</button>
      </div>
  </template>
  
  <script>
  export default {
      name: "Child",
  
      props:["count","changeCount"],
      methods:{
          fn(){
              this.$emit("changeCount",6)
          }
      },
      mounted(){
          console.log(this)
      }
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

  

## 7-4- vue3自定义事件

* src->App.vue

  ```vue
  <template>
      <h3>Vue3父向子通过属性进行参数的传递</h3>
      <h3>父组件App</h3>
      <button @click="count++">{{count}}</button>
      <button @click="setCount(2)">{{count}}</button>
      <hr/>
      <Child @setCount="setCount" @click="setCount" :count="count" :setCount="setCount"/>
  </template>
  
  <script lang="ts" setup>
  // 注意：在vue3中没有了修饰符.native
  //      父组件向子组件设置的事件，对于子组件而言都会作为属性来处理。
  //      父@click---->子onClick
  //      父@setCount---->子onSetCount
  import Child from "@/components/Child.vue";
  import {ref} from "vue";
  const count = ref(100);
  const setCount = function(n:number){
      console.log(1)
      count.value += n;
  }
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3 @click="onSetCount(5)">子组件Child</h3>
      <button @click="setCount(3)">{{count}}</button>
      <button @click="$emits('setCount',100)">{{count}}</button>
  </template>
  
  <script lang="ts" setup>
  import {onMounted} from "vue";
  // 通过调用defineEmits可以实现vue2中的this.$emit
  const props = defineProps(["count","setCount","onClick","onSetCount"]);
  const $emits = defineEmits(["setCount"]);
  onMounted(()=>{
      // props.onClick(4);
      $emits("setCount",2)
  })
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

## 7-5- 状态提升

> 将状态放置在共有的父级中。

* src->App.vue

  ```vue
  <template>
      <h3>App组件</h3>
      <button @click="num++">{{num}}</button>
      <hr/>
      <One @setNum="setNum" :num="num"/>
      <hr/>
      <Two  @setNum="setNum" :num="num"/>
  </template>
  
  <script lang="ts" setup>
  import One from "@/components/One";
  import Two from "@/components/Two";
  import {ref} from "vue";
  const num = ref(0);
  const setNum = function(v:number=1){
      num.value += v;
  }
  
  </script>
  
  <style scoped>
  
  </style>
   
  ```

* src->components->One.vue

  ```vue
  <template>
      <h3>One</h3>
      <button @click="changeNum">{{num}}</button>
  </template>
  
  <script setup lang="ts">
  defineProps(["num"]);
  const $emit = defineEmits(["setNum"]);
  const changeNum = function(){
      $emit("setNum",2)
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

* src->components->Two.vue

  ```vue
  <template>
      <h3>Two</h3>
      <button @click="changeNum">{{num}}</button>
  </template>
  
  <script setup lang="ts">
  defineProps(["num"])
  const $emit = defineEmits(["setNum"]);
  const changeNum = function(){
      $emit("setNum",3)
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

## 7-6- vue3通过mitt完成事件总线

> vue3中没有vue2中的Vue.prototype,所以在vue3中无事件总线。

* 下载

  ```shell
  cnpm i mitt
  ```

* src->utils->index.ts

  ```ts
  import mitt from "mitt";
  export const bus = mitt();
  ```

* src->components->Two.vue

  ``` vue
  <template>
      <h3 @click="changeNum">Two1:{{num}}</h3>
      <h3 @click="bus.emit('changenum',300)">Two2:{{num}}</h3>
  </template>
  
  <script setup lang="ts">
  import {bus} from "@/utils";
  
  defineProps(["num"]);
  const changeNum = function(){
      bus.emit("changenum",200);
  }
  </script>
  
  <style scoped>
  
  </style>
  ```

* src->components->One.vue

  ```vue
  <template>
      <h3>One:{{num}}</h3>
  
  </template>
  
  <script setup lang="ts">
  import {onMounted} from "vue";
  import {bus} from "@/utils";
  
  defineProps(["num"]);
  onMounted(function(){
      bus.on("changenum",()=>{
          console.log("ONE->changenum");
          // bus.off("changenum");
      })
  })
  </script>
  
  <style scoped>
  
  </style>
  ```

* src->components->App.vue

  ```vue
  <template>
      <h3>App组件（父组件）{{num}}</h3>
      <hr/>
      <One :num="num"/>
      <hr/>
      <Two :num="num"/>
  </template>
  
  <script lang="ts" setup>
  import {onMounted, ref} from "vue";
  import {bus} from "@/utils";
  import One from "@/components/One.vue"
  import Two from "@/components/Two.vue"
  const num = ref(100);
  onMounted(function(){
      bus.on("changenum",(v)=>{
          console.log("APP->changenum",v);
          num.value = v as number;
      })
  })
  </script>
  
  <style scoped>
  </style>
  ```

  

## 7-7- v-model实现父子数据同步(vue3)

* src->App.vue

  ```vue
  <template>
      <h3>v-model数据的双向绑定</h3>
      <input v-model="userName" type="text"><span>{{userName}}</span>
      <hr/>
      <h3>vue3中实现父子组件数据同步</h3>
      <Child :value="userName" @input="setUserName"/>
      <hr/>
      <h3>v-model实现父子组件数据同步</h3>
      <!-- 1- 向子组件传递了两个属性：modelValue  onUpdate:modelValue -->
      <!-- 2- 向子组件传递了自定义事件：update:model-value -->
      <Child2 v-model="userName"/>
  
  </template>
  
  <script lang="ts" setup>
   import {ref} from "vue";
   import Child from "@/components/Child.vue"
   import Child2 from "@/components/Child2.vue"
   let userName = ref("zhangsan");
   const setUserName = function(info:string){
       console.log("setUserName",info);
       userName.value = info;
   }
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3 @click="$my('input','lisi')">我是一个子组件-Child:{{value}}</h3>
  </template>
  
  <script lang="ts" setup>
  defineProps(["value"]);
  const $my = defineEmits(["input"]);
  </script>
  
  <style scoped>
  
  </style>
   
  ```

* src->components->Child2.vue

  ```vue
  <template>
      <h3>我是子组件Child2:{{modelValue}}</h3>
      <button @click="test">onUpdate:modelValue</button>
      <button @click="test2">update:model-value</button>
  </template>
  
  <script lang="ts" setup>
  const props = defineProps(["modelValue","onUpdate:modelValue"]);
  const emit = defineEmits(["update:model-value"]);
  const test = function(){
      props["onUpdate:modelValue"]("lisi");
  }
  const test2 = function(){
      emit("update:model-value","wangwu")
  }
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

## 7-8- vue3使用多个v-model

* src->App.vue

  ```vue
  <template>
      <h3>我是父组件App{{userName}}</h3>
      <!--  将数据userName的值绑定在value属性上，但更改value的值不会影响数据。（不会响应）  -->
      <input type="text" :value="userName">
      <input type="text" v-model="userName">
      <input type="text" v-model="age">
      <hr/>
      <Child v-model:userName="userName" v-model:age="age"/>
  </template>
  
  <script lang="ts" setup>
  import Child from "@/components/Child.vue";
  import {ref} from "vue";
  let userName = ref("zhangsan");
  let age = ref(100)
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3>我是子组件Child</h3>
      <p @click="$emit('update:user-name',userName+'!')">userName:{{userName}}</p>
      <p @click="$emit('update:age',age+1)">age:{{age}}</p>
  </template>
  
  <script lang="ts" setup>
  defineProps(["userName","age"]);
  const $emit = defineEmits(["update:user-name","update:age"]);
  
  </script>
  
  <style scoped>
  </style>
  ```

  

## 7-9- sync

> 注意：vue3废弃掉了.sync。vue2中的.sync相当于vue3中的v-model

* src->App.vue

  ```vue
  <template>
      <div>
          <h3>{{userName}}</h3>
          <Child :userName.sync="userName"/>
      </div>
  
  </template>
  
  <script>
  import Child from "@/components/Child";
  export default {
      name:"App",
      components: {Child},
      data(){
          return {
              userName:"zhangsan"
          }
      }
  }
  </script>
  
  <style scoped>
  </style>
  ```

* src->component->Child.vue

  ```vue
  <template>
      <div>
          <h3 @click="$emit('update:userName','lisi')">子组件：child-->{{userName}}</h3>
      </div>
  </template>
  
  <script>
  export default {
      name:"Child",
      props:["userName"],
      mounted(){
          console.log(this)
      }
  }
  </script>
  
  <style scoped>
  </style>
  ```

## 7-10- vue2之$attrs与$listeners

* src->App.vue

  ```vue
  <template>
      <div>
          <h3>父组件App</h3>
          {{sex}}
          <hr/>
          <Child @click="fn" a="1" b="2" c="3" :sex="sex"/>
      </div>
  
  </template>
  
  <script>
  import Child from "@/components/Child";
  export default {
      name:"App",
      components: {Child},
      data(){
          return {
              sex:"男"
          }
      },
      methods:{
          fn(a,b,c,d){
              console.log('fn',a,b,c,d)
              this.sex = d;
          }
      }
  }
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <div>
          <h3>子组件Child</h3>
          <p>a:{{$attrs.a}}</p>
          <p>b:{{$attrs.b}}</p>
          <p>c:{{$attrs.c}}</p>
          <p>sex:{{$attrs.sex}}</p>
          <button @click="test"> 点我</button>
      </div>
  </template>
  
  <script>
      // 如果你在
  // 可以通过this.$attrs获取父向子传递过来的属性。
  // 可以通过this.$listeners获取父向子传递过来的自定义事件(原生不可以)。
  export default {
      name:"Child",
      methods:{
          test(){
              this.$listeners.click(1,2,3,4);
          }
      },
      mounted(){
          console.log(this);
      }
  }
  </script>
  
  <style scoped>
  </style>
  ```

  

## 7-11- vue3之useAttrs

* src->App.vue

  ```vue
  <template>
      <h3>我是父组件App{{count}}</h3>
      <hr/>
      <Child @click="fn" a="1" b="2" c="3" :count="count"/>
  </template>
  
  <script lang="ts" setup>
  import Child from "@/components/Child.vue";
  import {ref} from "vue";
  const count = ref(100);
  const fn = function(a,b,c,d){
      console.log("fn",a,b,c,d);
      count.value = a+b+c+d+count.value;
  }
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3>我是子组件Child</h3>
      <p>{{$attrs}}</p>
      <p>{{$attrs.onClick}}</p>
      <button @click="$attrs.onClick(1,2,3,4)">点我</button>
  </template>
  
  <script lang="ts" setup>
  // 模板中可以使用$attrs
  // 可以使用组合API->useAttrs
  // props的优先级高于attrs(如果在props当中声明了一个数据状态，那么attrs中不会存在与其同名的。)
  // 相较于vue2中的$attrs而言通过useAttrs获取到的不仅仅是属性也包含自定义的事件。
  // 即：useAttrs运行的结果是vue2中的$attrs与$listeners的一个结合体。
  import {useAttrs} from "vue";
  const $attrs = useAttrs();
  // const props = defineProps(["count"]);
  console.log($attrs);
  </script>
  
  <style scoped>
  </style>
  ```

  

## 7-12- vue2之$refs-$children-$parent

* src->App.vue

  ```vue
  <template>
      <div>
          <h3>父组件App：{{userName}}</h3>
          <button @click="getChildInfo">点我获取子组件信息</button>
          <hr/>
          <Child ref="child"/>
      </div>
  
  </template>
  
  <script>
  import Child from "@/components/Child";
  // 获取子组件实例方案有两种：
  // 1-$refs:可以借助ref与$refs获取真实的DOM,与组件结合使用可以获取组件实例。
  // 2-$children:获取当前组件下使用的子组件列表（数组）
  export default {
      name:"App",
      components: {Child},
      data(){
         return {
             userName:"张三"
         }
      },
      methods:{
          getChildInfo(){
              // this.$refs.child 即是子组件Child的实例。
              // console.log("getChildInfo",this.$refs.child);
              // 获取子组件数据状态
              // console.log("getChildInfo",this.$refs.child.userName)
              // 调用 子组件的方法
              // this.$refs.child.changeUserName("lisi");
  
              // console.log(this.$children[0]);
              this.$children[0].changeUserName("wangwu");
          }
      }
  }
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <div>
          <h3>子组件Child</h3>
          <p>userName:{{userName}}</p>
          <p>父组件中的userName:{{$parent.userName}}</p>
          <button @click="getParent">获取父组件实例</button>
      </div>
  </template>
  
  <script>
  // $parent:可以获取父组件实例
  export default {
      name:"Child",
      data(){
          return {
              userName:"child"
          }
      },
      methods:{
          getParent(){
              // console.log("child",this.$parent);
              this.$parent.userName="你被我修改了！";
          },
          changeUserName(v){
              this.userName = v;
          }
      }
  }
  </script>
  
  <style scoped>
  </style>
  ```

  

## 7-13- vue3之ref与$parent

* src->App.vue

  ```vue
  <template>
      <h3>我是父组件App</h3>
      <p>我是父亲，我现在的资产有：{{money}}</p>
      <button  @click="borrowByChild">向儿子借10元</button>
      <hr/>
      <Child ref="son"/>
  </template>
  
  <script lang="ts" setup>
  // 在vue3中没有$children,但是在模块中有$parent.
  import Child from "@/components/Child.vue";
  import {ref} from "vue";
  const money = ref(200);
  const son = ref();
  const borrowByChild = function(){
      // 让儿子的资产减少10元
      son.value.money -= 10;
      // 老子的资产资产加10元
      money.value+=10;
  
  }
  defineExpose({money})
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3>我是子组件Child</h3>
      <p>我还小，还是个孩子，现在的资产共{{money}}</p>
      <button @click="sendFather($parent)">给父亲100元</button>
  </template>
  
  <script lang="ts" setup>
  import {ref} from "vue";
  
  const money = ref(2000);
  const sendFather = function(parent:any){
      // 儿子减少100
      money.value-=100;
      // 父亲增加100
      parent.money+=100;
  
  }
  defineExpose({money})
  </script>
  
  <style scoped>
  </style>
  ```



## 7-14- 组合式API provide - inject

> 可以被自己直接包裹或间接包裹的组件获取到数据。
>
> 通过provide传递，通过inject接收。接收之后数据可以修改，并支持响应式。

* src->App.vue

  ```vue
  <template>
      <h3>我是父组件App(爷爷):{{token}}</h3>
      <p>age:{{age}}</p>
      <hr/>
      <Child/>
      <hr/>
      <Child2/>
  </template>
  
  <script lang="ts" setup>
  import Child from "@/components/Child.vue";
  import Child2 from "@/components/Child2.vue";
  import {ref, provide, inject} from "vue";
  const token = ref("appToken");
  // 第一个参数是标识，第二个参数是数据状态
  provide("t",token);// 提供数据，让自己所包裹的组件（可以隔代）使用。
  const age = inject("age");
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3 @click="t+='!'">我是子组件Child（儿子）:{{t}}</h3>
      <hr/>
      <One/>
  </template>
  
  <script lang="ts" setup>
  import One from "@/components/One.vue"
  import {inject, provide, ref} from "vue";
  const age = ref(100);
  const t = inject("t");
  provide("age",age);
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child2.vue

  ```vue
  <template>
      <h3>我是组件Child2:{{age}}</h3>
  </template>
  
  <script lang="ts" setup>
  import {inject} from "vue";
  const age = inject("age");
  </script>
  
  <style scoped>
  
  </style>
   
  ```

* src->components->One.vue

  ```vue
  <template>
      <h3 @click="t+='?'">One组件--孙子:{{t}}</h3>
      <p>来自于child的age:{{age}}</p>
  </template>
  
  <script lang="ts" setup>
  import {inject} from "vue";
  const t = inject("t");
  const age = inject("age");
  </script>
  
  <style scoped>
  
  </style>
   
  ```

  

## 7-15- 作用域插槽

* src->App.vue

  ```vue
  <template>
      <h3>我是父组件App</h3>
      <hr/>
  <!--    <Child :info="info">-->
  <!--        <template v-slot="props">-->
  <!--           <p :style="{-->
  <!--               background:props.suibian.done?'green':'red'-->
  <!--           }">{{props.$index}}|{{props.suibian.do}}</p>-->
  <!--        </template>-->
  <!--    </Child>-->
  
  
      <!--可以通过解构赋值的形式接收数据-->
  <!--    <Child :info="info">-->
  <!--        <template v-slot="{suibian,$index}">-->
  <!--            <p :style="{-->
  <!--               background:suibian.done?'green':'red'-->
  <!--           }">{{$index}}|{{suibian.do}}</p>-->
  <!--        </template>-->
  <!--    </Child>-->
  
  <!--    <Child :info="info">-->
  <!--        <template v-slot:default="{suibian,$index}">-->
  <!--            <p :style="{-->
  <!--               background:suibian.done?'green':'red'-->
  <!--           }">{{$index}}|{{suibian.do}}</p>-->
  <!--        </template>-->
  <!--    </Child>-->
  
  <!--    <Child :info="info">-->
  <!--        <template #default="{suibian,$index}">-->
  <!--            <p :style="{-->
  <!--               background:suibian.done?'green':'red'-->
  <!--           }">{{$index}}|{{suibian.do}}</p>-->
  <!--        </template>-->
  <!--    </Child>-->
  
      <Child :info="info">
          <template #="{suibian,$index}">
              <p :style="{
                 background:suibian.done?'green':'red'
             }">{{$index}}|{{suibian.do}}</p>
          </template>
      </Child>
  </template>
  
  <script lang="ts" setup>
  import Child from "@/components/Child.vue";
  import {ref} from "vue";
  
  const info = ref([
      {
          id: 1,
          do: "吃了一个包子！",
          done: true
      }, {
          id: 2,
          do: "扶老太太过马路！",
          done: false
      }
      , {
          id: 3,
          do: "赚了1000万！",
          done: true
      }
  ]);
  </script>
  
  <style scoped>
  </style>
  ```

* src->components->Child.vue

  ```vue
  <template>
      <h3>我是子组件Child</h3>
      <div v-for="(item,index) in info" :key="item.id">
          <slot :suibian="item" :$index="index"></slot>
      </div>
  </template>
  
  <script lang="ts" setup>
  defineProps(["info"]);
  </script>
  
  <style scoped>
  </style>
  ```

  

















































































































































































































































































































