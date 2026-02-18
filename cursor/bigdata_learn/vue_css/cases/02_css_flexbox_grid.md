# 案例2：CSS Flexbox 与 Grid（现代布局的核心）

## 案例目标
掌握两种现代布局方案：
- **Flexbox**：一维布局（横向/纵向）
- **Grid**：二维布局（行列网格）

## 验证文件
- `vue_css/data/01_basic_layout.html`（Flexbox 示例）
- `vue_css/data/02_grid_layout.html`（Grid 示例）

## Flexbox 核心属性（费曼式讲解）

### 一句话讲明白
Flexbox 就是“把一堆元素排成一行或一列，并且能控制它们怎么对齐、怎么分配空间”。

### 关键属性速查

#### 容器属性（父元素）
- `display: flex`：开启 Flexbox
- `flex-direction: row/column`：主轴方向（横向/纵向）
- `justify-content: center/space-between/space-around`：主轴对齐
- `align-items: center/stretch/flex-start`：交叉轴对齐
- `gap: 1rem`：子元素间距（现代浏览器）

#### 子元素属性
- `flex: 1`：占据剩余空间
- `flex-grow: 1`：允许放大
- `flex-shrink: 0`：不允许缩小
- `align-self: center`：单独控制对齐

### 最小示例
```css
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.item {
  flex: 1; /* 每个 item 平分空间 */
}
```

## Grid 核心属性（费曼式讲解）

### 一句话讲明白
Grid 就是“把页面切成网格，每个元素可以占据一个或多个格子”。

### 关键属性速查

#### 容器属性
- `display: grid`：开启 Grid
- `grid-template-columns: repeat(3, 1fr)`：3 列，每列等宽
- `grid-template-rows: auto`：行高自动
- `gap: 1rem`：行列间距
- `grid-template-areas`：命名区域（进阶）

#### 子元素属性
- `grid-column: span 2`：占据 2 列
- `grid-row: span 2`：占据 2 行
- `grid-area: header`：使用命名区域

### 最小示例
```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.card {
  /* 自动填充网格 */
}
```

## 期望效果（对照验证）

### Flexbox 示例（01_basic_layout.html）
- Header、Body、Footer 纵向排列
- Body 内 Sidebar 和 Main 横向排列
- Main 占据剩余空间（`flex: 1`）

### Grid 示例（02_grid_layout.html）
- 3 列卡片网格（桌面端）
- 移动端自动变为 1 列（`@media`）

## 选择建议（什么时候用哪个）

- **Flexbox**：导航栏、表单行、卡片内部布局、垂直居中
- **Grid**：整体页面布局、卡片网格、复杂表单、杂志式布局

## 常见坑
- **Flexbox 嵌套过深**：性能会下降，Grid 可能更合适。
- **Grid 列数写死**：用 `repeat(auto-fit, minmax(200px, 1fr))` 更灵活。
- **忘记 `gap`**：用 `margin` 控制间距不如 `gap` 简洁。
