# Node.js 基础

Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行时。

## 模块系统

```javascript
// 导出
module.exports = { myFunc };
// 导入
const { myFunc } = require("./module");

// ES Modules
import { myFunc } from "./module.js";
```

## 文件操作

```javascript
const fs = require("fs");

// 同步
const data = fs.readFileSync("file.txt", "utf-8");

// 异步
fs.readFile("file.txt", "utf-8", (err, data) => {
    if (err) throw err;
    console.log(data);
});
```

## 包管理

```bash
npm init -y
npm install express
npm install --save-dev nodemon
```
