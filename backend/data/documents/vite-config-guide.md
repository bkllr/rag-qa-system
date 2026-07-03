# Vite 构建工具配置指南

Vite 是 Vue 3 官方推荐的构建工具，提供极速的冷启动和热模块替换（HMR）。

## 创建项目

```bash
npm create vite@latest frontend -- --template vue
cd frontend
npm install
```

## 项目结构

```
frontend/
├── index.html          # 入口 HTML
├── package.json
├── vite.config.js      # Vite 配置
└── src/
    ├── main.js         # 应用入口
    ├── App.vue         # 根组件
    ├── components/     # 组件目录
    └── api/            # API 封装
```

## vite.config.js 配置

### 基本配置

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    server: {
        port: 5173,
        open: true,  // 自动打开浏览器
    }
})
```

### 开发代理配置

将 API 请求代理到后端，避免跨域问题：

```javascript
export default defineConfig({
    plugins: [vue()],
    server: {
        port: 5173,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            }
        }
    }
})
```

配置后，前端请求 `/api/chat` 会被自动转发到 `http://localhost:8000/api/chat`。

## 常用插件

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [
        vue(),
        // 其他插件...
    ],
})
```

## 开发命令

| 命令 | 说明 |
|:--|:--|
| `npm run dev` | 启动开发服务器（HMR） |
| `npm run build` | 生产构建 |
| `npm run preview` | 预览生产构建 |

## 依赖管理

```json
{
    "dependencies": {
        "vue": "^3.4.0",
        "marked": "^12.0.0",
        "highlight.js": "^11.9.0"
    },
    "devDependencies": {
        "vite": "^5.4.0",
        "@vitejs/plugin-vue": "^5.0.0"
    }
}
```

## 环境变量

Vite 支持通过 `.env` 文件管理环境变量：

```bash
# .env
VITE_API_BASE_URL=http://localhost:8000
```

```javascript
// 使用
const baseURL = import.meta.env.VITE_API_BASE_URL
```
