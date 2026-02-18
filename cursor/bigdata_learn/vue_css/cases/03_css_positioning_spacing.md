# 案例3：CSS 定位与间距（Position / Margin / Padding）

## 案例目标
理解 CSS 中最容易“写出来但不知道为什么这样”的部分：
- **Position**：`static/relative/absolute/fixed/sticky`
- **Margin vs Padding**：外边距 vs 内边距
- **Box Model**：盒模型（content + padding + border + margin）

## 费曼式讲解

### Position（定位）

#### 一句话讲明白
Position 决定元素“在哪里”，以及它是否“脱离文档流”。

#### 五种值
1. **`static`**（默认）：正常文档流，`top/right/bottom/left` 无效
2. **`relative`**：相对自己原来的位置偏移，仍在文档流中
3. **`absolute`**：相对最近的 `positioned` 祖先（非 static）定位，脱离文档流
4. **`fixed`**：相对视口定位，脱离文档流（常用于固定导航栏）
5. **`sticky`**：滚动到阈值时“粘住”，结合 `top` 使用

#### 最小示例
```css
/* 固定顶部导航 */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

/* 相对定位微调 */
.button {
  position: relative;
  top: -2px; /* 向上移动 2px */
}

/* 绝对定位（父元素需 relative） */
.parent {
  position: relative;
}
.child {
  position: absolute;
  top: 10px;
  right: 10px;
}
```

### Margin vs Padding（间距）

#### 一句话讲明白
- **Margin**：元素“外面”的距离（与其他元素之间的空白）
- **Padding**：元素“里面”的距离（内容与边框之间的空白）

#### 记忆技巧
想象一个盒子：
- **Padding**：盒子内壁到内容的距离（填充物）
- **Margin**：盒子外壁到其他盒子的距离（外边距）

#### 最小示例
```css
.card {
  padding: 1rem;      /* 内容与边框的距离 */
  margin: 1rem;       /* 与其他元素的距离 */
  border: 1px solid #ddd;
}
```

### Box Model（盒模型）

#### 一句话讲明白
每个元素都是一个盒子，由内到外：**content → padding → border → margin**。

#### `box-sizing` 的作用
- **`content-box`**（默认）：`width` 只包含 content，padding/border 会额外增加
- **`box-sizing: border-box`**：`width` 包含 padding + border，更符合直觉

#### 最小示例
```css
/* 推荐：全局设置 */
* {
  box-sizing: border-box;
}

.box {
  width: 200px;
  padding: 20px;
  border: 2px solid black;
  /* 实际宽度 = 200px（包含 padding + border）*/
}
```

## 期望效果（手写验证）

创建一个简单的卡片：
```html
<div class="card">
  <h3>标题</h3>
  <p>内容</p>
</div>
```

```css
.card {
  width: 300px;
  padding: 1rem;        /* 内容与边框的距离 */
  margin: 1rem auto;    /* 上下 1rem，左右居中 */
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box; /* 重要！ */
}
```

## 常见坑
- **忘记 `box-sizing: border-box`**：导致宽度超出预期
- **Margin 塌陷**：父子元素的 margin 会合并（用 padding 或 `display: flex` 解决）
- **Absolute 定位找不到参考点**：父元素必须是 `position: relative/absolute/fixed`
