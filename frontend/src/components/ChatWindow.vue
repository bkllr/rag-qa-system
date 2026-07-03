<template>
  <div class="chat-window" ref="windowRef">
    <!-- 空状态 -->
    <div v-if="messages.length === 0" class="empty-state">
      <div class="empty-icon">💬</div>
      <h2>RAG 技术文档智能问答</h2>
      <p>基于 DeepSeek + Chroma 向量数据库的 AI 问答系统</p>
      <div class="hint-questions">
        <span class="hint-label">试试这些问题：</span>
        <button
          v-for="q in hintQuestions"
          :key="q"
          class="hint-chip"
          @click="$emit('quickAsk', q)"
        >{{ q }}</button>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="messages-container" ref="messagesRef">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        class="message"
        :class="msg.role"
      >
        <!-- 头像区域 -->
        <div class="message-avatar">
          <span v-if="msg.role === 'user'" class="avatar user-avatar">👤</span>
          <span v-else class="avatar bot-avatar">🤖</span>
        </div>

        <!-- 内容区域 -->
        <div class="message-body">
          <div class="message-role">{{ msg.role === 'user' ? '你' : 'AI 助手' }}</div>

          <!-- 用户消息：纯文本 -->
          <div v-if="msg.role === 'user'" class="message-text">{{ msg.content }}</div>

          <!-- AI 消息：Markdown 渲染 + 流式光标 -->
          <div v-else class="message-content">
            <div class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
            <span v-if="msg.streaming" class="streaming-cursor">▍</span>

            <!-- 来源引用 -->
            <div v-if="msg.sources && msg.sources.length > 0" class="sources-section">
              <div class="sources-title">📚 参考来源（{{ msg.sources.length }}）</div>
              <SourceCard
                v-for="(src, si) in msg.sources"
                :key="si"
                :source="src"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import SourceCard from './SourceCard.vue'

// ── 配置 marked ──
marked.setOptions({
  breaks: true,
  gfm: true,
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
})

// ── Props ──
defineProps({
  messages: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['quickAsk'])

// ── 快捷问题 ──
const hintQuestions = [
  '什么是 RAG？',
  'LangChain 的核心组件有哪些？',
  'FastAPI 和 Flask 有什么区别？',
  '向量数据库的工作原理是什么？',
]

// ── Refs ──
const messagesRef = ref(null)

// ── Markdown 渲染 ──
function renderMarkdown(text) {
  if (!text) return ''
  try {
    return marked.parse(text)
  } catch {
    return text
  }
}

// ── 自动滚动到底部 ──
watch(
  () => messagesRef.value?.scrollHeight,
  () => {
    nextTick(() => {
      if (messagesRef.value) {
        messagesRef.value.scrollTop = messagesRef.value.scrollHeight
      }
    })
  },
)
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f8fafc;
}

/* ── 空状态 ── */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}
.empty-icon {
  font-size: 56px;
  margin-bottom: 16px;
}
.empty-state h2 {
  font-size: 22px;
  color: #1f2937;
  margin: 0 0 8px;
}
.empty-state p {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 28px;
}

.hint-questions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 8px;
  max-width: 500px;
}
.hint-label {
  font-size: 13px;
  color: #9ca3af;
  margin-right: 4px;
}
.hint-chip {
  padding: 6px 14px;
  border: 1px solid #d1d5db;
  border-radius: 999px;
  background: #fff;
  color: #374151;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.hint-chip:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

/* ── 消息列表 ── */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
}

/* ── 消息项 ── */
.message {
  display: flex;
  gap: 12px;
  padding: 14px 24px;
  transition: background 0.15s;
}
.message.assistant {
  background: #fff;
  border-bottom: 1px solid #f3f4f6;
}
.message.user {
  background: #f8fafc;
}

.message-avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
}
.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  font-size: 18px;
}
.user-avatar {
  background: #dbeafe;
}
.bot-avatar {
  background: #ede9fe;
}

.message-body {
  flex: 1;
  min-width: 0;
}

.message-role {
  font-size: 12px;
  font-weight: 600;
  color: #9ca3af;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.message-text {
  font-size: 15px;
  color: #1f2937;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-content {
  font-size: 15px;
  color: #1f2937;
  line-height: 1.7;
}

/* ── Markdown 样式 ── */
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin: 16px 0 8px;
  color: #111827;
}
.markdown-body :deep(h1) { font-size: 1.4em; }
.markdown-body :deep(h2) { font-size: 1.2em; }
.markdown-body :deep(h3) { font-size: 1.05em; }

.markdown-body :deep(p) {
  margin: 6px 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 20px;
  margin: 6px 0;
}
.markdown-body :deep(li) {
  margin: 2px 0;
}

.markdown-body :deep(code) {
  padding: 2px 6px;
  background: #f1f5f9;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
}

.markdown-body :deep(pre) {
  margin: 10px 0;
  padding: 14px 16px;
  background: #1e293b;
  border-radius: 8px;
  overflow-x: auto;
}
.markdown-body :deep(pre code) {
  padding: 0;
  background: transparent;
  color: #e2e8f0;
  font-size: 13px;
}

.markdown-body :deep(blockquote) {
  margin: 8px 0;
  padding: 6px 14px;
  border-left: 3px solid #3b82f6;
  background: #f0f4ff;
  color: #475569;
}

.markdown-body :deep(table) {
  border-collapse: collapse;
  margin: 8px 0;
  width: 100%;
}
.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid #d1d5db;
  padding: 6px 12px;
  font-size: 13px;
  text-align: left;
}
.markdown-body :deep(th) {
  background: #f1f5f9;
  font-weight: 600;
}

.markdown-body :deep(a) {
  color: #3b82f6;
  text-decoration: none;
}
.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

/* ── 流式光标 ── */
.streaming-cursor {
  display: inline-block;
  color: #3b82f6;
  font-weight: bold;
  animation: blink 0.8s step-end infinite;
  margin-left: 2px;
}
@keyframes blink {
  50% { opacity: 0; }
}

/* ── 来源引用区域 ── */
.sources-section {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}
.sources-title {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 6px;
}
</style>
