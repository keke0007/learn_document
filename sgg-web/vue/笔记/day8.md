一、搭建SKU管理商品的静态?

1.1SKU数据渲染出来
1.2上架与下架业务





二、深度选择器?


2.1组件内部scoped?

---scoped作用?

scoped作用是局部样式

----scoped局部样式底层怎么实现的那?

某一个组件style标签身上如果加上一个scoped导致,当前组件DOM元素(子组件的根节点)
会有相同的data-v-#hash数值！！！

scoped->data-v-hash->属性选择器实现局部样式！！！




