# 案例4：Vue 样式作用域与命名规范（Scoped / BEM）

## 案例目标
理解 Vue 中样式的作用域问题，以及如何避免样式冲突：
- **Scoped CSS**：组件样式隔离
- **BEM 命名规范**：Block__Element--Modifier
- **CSS Modules**：另一种隔离方案（进阶）

## 验证文件
- `vue_css/data/03_vue_component_example.vue`（含 scoped 样式）

## Scoped CSS（费曼式讲解）

### 一句话讲明白
`<style scoped>` 让样式“只作用于当前组件”，不会影响其他组件。

### 原理（简化理解）
Vue 会给每个元素和样式选择器加上一个唯一的 `data-v-xxx` 属性，实现隔离。

### 最小示例
```vue
<template>
  <div class="card">
    <h3>标题</h3>
  </div>
</template>

<style scoped>
.card {
  padding: 1rem;
}
/* 这个 .card 不会影响其他组件的 .card */
</style>
```

## BEM 命名规范（费曼式讲解）

### 一句话讲明白
BEM = Block（块）__ Element（元素）-- Modifier（修饰符），用命名避免样式冲突。

### 命名规则
- **Block**：独立的功能块（如 `user-card`）
- **Element**：块内的元素（如 `user-card__avatar`、`user-card__name`）
- **Modifier**：状态/变体（如 `user-card--highlighted`）

### 最小示例
```vue
<template>
  <div class="user-card user-card--highlighted">
    <img class="user-card__avatar" src="..." />
    <h3 class="user-card__name">张三</h3>
    <p class="user-card__email">zhangsan@example.com</p>
  </div>
</template>

<style scoped>
.user-card {
  padding: 1rem;
}

.user-card--highlighted {
  border: 2px solid #3498db;
}

.user-card__avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
}

.user-card__name {
  font-size: 1.2rem;
}
</style>
```

## 期望效果（对照验证）

查看 `03_vue_component_example.vue`：
- 样式使用 `scoped`，不会污染全局
- 类名清晰（`.user-card`、`.avatar`、`.info`）
- 使用 Flexbox 实现卡片布局

## 选择建议

- **Scoped**：Vue 项目默认推荐，简单直接
- **BEM**：大型项目、多人协作时更清晰
- **CSS Modules**：需要更严格的隔离时使用

## 常见坑
- **Scoped 内使用全局选择器**：需要用 `:global()` 或 `<style>`（无 scoped）
- **BEM 命名过长**：适度即可，不要过度嵌套
- **忘记 scoped**：导致样式泄露到其他组件
