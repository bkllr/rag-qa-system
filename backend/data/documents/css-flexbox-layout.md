# CSS Flexbox 布局详解

Flexbox 是 CSS3 的一维布局模型。

## 容器属性

```css
.container {
    display: flex;
    flex-direction: row;       /* 主轴方向 */
    justify-content: center;   /* 主轴对齐 */
    align-items: center;       /* 交叉轴对齐 */
    gap: 16px;                 /* 间距 */
    flex-wrap: wrap;           /* 换行 */
}
```

## 项目属性

```css
.item {
    flex: 1;         /* flex-grow */
    align-self: flex-end;
    order: 2;
}
```

## 常见布局
- 水平居中: justify-content: center
- 垂直居中: align-items: center
- 两端对齐: justify-content: space-between
