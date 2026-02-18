# Vue + CSS 示例运行说明

## 1) HTML 文件（可直接在浏览器打开）

`vue_css/data/` 目录下的 `.html` 文件：
- 直接用浏览器打开即可查看效果
- 无需任何构建工具

## 2) Vue 组件文件（需要 Vue 项目环境）

`vue_css/data/03_vue_component_example.vue` 需要在 Vue 项目中使用：

### 使用 Vue CLI
```bash
vue create my-project
cd my-project
# 将 .vue 文件复制到 src/components/
npm run serve
```

### 使用 Vite
```bash
npm create vue@latest my-project
cd my-project
# 将 .vue 文件复制到 src/components/
npm run dev
```

### 在父组件中使用
```vue
<template>
  <div>
    <UserCard 
      :user="userData" 
      @view-detail="handleViewDetail"
    />
  </div>
</template>

<script>
import UserCard from './components/UserCard.vue'

export default {
  components: {
    UserCard
  },
  data() {
    return {
      userData: {
        id: 1,
        name: '张三',
        email: 'zhangsan@example.com',
        role: '开发者',
        avatar: 'https://via.placeholder.com/60'
      }
    }
  },
  methods: {
    handleViewDetail(id) {
      console.log('查看用户:', id)
    }
  }
}
</script>
```
