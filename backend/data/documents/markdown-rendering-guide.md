# Markdown 渲染与代码高亮

在 Web 应用中渲染 Markdown 内容并支持代码语法高亮是常见需求。

## marked 库

`marked` 是一个快速、轻量的 Markdown 解析器：

```javascript
import { marked } from 'marked'

const markdown = `
# 标题

这是一段 **加粗** 文本。

\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`
`

const html = marked.parse(markdown)
// 输出 HTML 字符串
```

## highlight.js 代码高亮

`highlight.js` 支持 190+ 种语言的语法高亮：

```javascript
import hljs from 'highlight.js'

// 自动检测语言
const result = hljs.highlightAuto('console.log("hello")')
console.log(result.value)  // 高亮后的 HTML

// 指定语言
const result2 = hljs.highlight('def hello(): pass', { language: 'python' })
```

## 在 Vue 3 中整合

```vue
<script setup>
import { ref, watch } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const props = defineProps({
    content: String
})

const renderedHtml = ref('')

watch(() => props.content, (newVal) => {
    // 配置 marked 使用 highlight.js
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                return hljs.highlight(code, { language: lang }).value
            }
            return hljs.highlightAuto(code).value
        }
    })

    renderedHtml.value = marked.parse(newVal || '')
}, { immediate: true })
</script>

<template>
    <div class="markdown-body" v-html="renderedHtml"></div>
</template>
```

## marked 高级配置

```javascript
marked.use({
    breaks: true,      // 换行符转 <br>
    gfm: true,         // GitHub Flavored Markdown
    highlight: (code, lang) => {
        if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value
        }
        return hljs.highlightAuto(code).value
    }
})
```

## 流式 Markdown 渲染

在 LLM 流式输出场景中，内容是逐步追加的，需要实时渲染：

```javascript
const content = ref('')

// 流式接收时逐步追加
function onToken(token) {
    content.value += token
    // 实时重新渲染 Markdown
    // 注意：频繁重新渲染可能影响性能，可以加 debounce
}

// watch 自动重新渲染
watch(content, (val) => {
    renderedHtml.value = marked.parse(val)
})
```

## 代码块样式

推荐使用 `github-dark.css` 或 `atom-one-dark.css` 主题：

```javascript
import 'highlight.js/styles/github-dark.css'
```
