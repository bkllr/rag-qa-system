<template>
  <div class="app">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-left">
        <span class="logo">🔍</span>
        <h1>RAG QA System</h1>
        <span class="badge">AI 技术文档智能问答</span>
      </div>
      <div class="header-right">
        <a class="header-link" href="http://localhost:8000/docs" target="_blank" title="API 文档">
          API Docs ↗
        </a>
      </div>
    </header>

    <!-- 聊天区域 -->
    <ChatWindow
      :messages="messages"
      @quickAsk="handleQuickAsk"
    />

    <!-- 输入区域 -->
    <ChatInput
      :disabled="loading"
      :placeholder="loading ? 'AI 正在思考中...' : '输入技术问题，Enter 发送'"
      @send="handleSend"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatWindow from './components/ChatWindow.vue'
import ChatInput from './components/ChatInput.vue'
import { streamChat } from './api/chat.js'

// ── 状态 ──
const messages = ref([])
const loading = ref(false)
let cancelStream = null

// ── 发送消息 ──
async function handleSend(question) {
  if (loading.value) return

  // 取消之前的请求（如果有）
  if (cancelStream) {
    cancelStream()
    cancelStream = null
  }

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: question,
  })

  // 添加 AI 占位消息（流式追加内容）
  const aiMsg = {
    role: 'assistant',
    content: '',
    sources: [],
    streaming: true,
  }
  messages.value.push(aiMsg)
  loading.value = true

  // 发起 SSE 流式请求
  cancelStream = streamChat(question, {
    onToken(token) {
      aiMsg.content += token
    },
    onSource(sources) {
      aiMsg.sources = sources
    },
    onDone() {
      aiMsg.streaming = false
      loading.value = false
      cancelStream = null
    },
    onError(err) {
      aiMsg.streaming = false
      aiMsg.content = `请求失败: ${err.message}。请确保后端服务已启动且 API Key 配置正确。`
      loading.value = false
      cancelStream = null
    },
  })
}

// ── 快捷提问 ──
function handleQuickAsk(question) {
  handleSend(question)
}
</script>

<style>
/* ── 全局重置 ── */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial,
    sans-serif;
  font-size: 15px;
  color: #1f2937;
  background: #f1f5f9;
}

#app {
  height: 100%;
}

/* ── 应用布局 ── */
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  background: #fff;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.06);
}

/* ── 顶部导航 ── */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: linear-gradient(135deg, #1e3a5f 0%, #3b82f6 100%);
  color: #fff;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-left .logo {
  font-size: 22px;
}
.header-left h1 {
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.badge {
  font-size: 11px;
  padding: 3px 10px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.header-link {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  padding: 4px 10px;
  border-radius: 6px;
  transition: background 0.2s;
}
.header-link:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* ── 滚动条美化 ── */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
