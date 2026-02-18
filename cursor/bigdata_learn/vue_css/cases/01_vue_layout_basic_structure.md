# 案例1：Vue 页面布局基本思路（组件化 + 布局容器）

## 案例目标
理解开发一个 Vue 页面的**基本布局思路**：
- 组件化拆分（Header / Sidebar / Main / Footer）
- 布局容器选择（Flexbox / Grid）
- 响应式适配（移动端优先）

## 验证文件
- `vue_css/data/01_basic_layout.html`（可直接在浏览器打开）

## Vue 组件结构示例

```vue
<template>
  <div class="app-layout">
    <AppHeader />
    <div class="app-body">
      <AppSidebar />
      <AppMain>
        <router-view />
      </AppMain>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import AppMain from './components/AppMain.vue'
import AppFooter from './components/AppFooter.vue'

export default {
  name: 'AppLayout',
  components: {
    AppHeader,
    AppSidebar,
    AppMain,
    AppFooter
  }
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-body {
  flex: 1;
  display: flex;
}

/* 响应式：移动端侧边栏收起 */
@media (max-width: 768px) {
  .app-body {
    flex-direction: column;
  }
}
</style>
```

## 布局思路（费曼式讲解）

### 1. 组件化拆分
- **为什么拆分**：就像搭积木，每个部分（Header/Sidebar/Main）独立维护，复用和测试更容易。
- **怎么拆分**：按“视觉区域 + 功能职责”切分，每个区域一个组件。

### 2. 布局容器选择
- **Flexbox**：适合“一维布局”（横向或纵向排列），比如 Header + Body + Footer 的纵向排列。
- **Grid**：适合“二维布局”（既有行又有列），比如卡片网格、复杂表单。

### 3. 响应式适配
- **移动端优先**：先写移动端样式，再用 `@media` 扩展到大屏。
- **断点选择**：常见 768px（平板）、1024px（桌面）。

## 期望效果（对照验证）

打开 `01_basic_layout.html` 应看到：
- 顶部 Header（深色背景）
- 左侧 Sidebar（深色背景）
- 右侧 Main（浅色背景，占据剩余空间）
- 底部 Footer（深色背景）
- 整体高度占满视口（100vh）

## 常见坑
- **忘记 `box-sizing: border-box`**：padding/border 会让宽度超出预期。
- **Flexbox 方向搞反**：`flex-direction: column` vs `row` 要分清。
- **响应式断点写反**：`max-width`（小于等于）vs `min-width`（大于等于）。
