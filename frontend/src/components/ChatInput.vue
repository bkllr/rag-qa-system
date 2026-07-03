<template>
  <div class="chat-input">
    <textarea
      ref="textareaRef"
      v-model="text"
      class="input-textarea"
      :placeholder="placeholder"
      :disabled="disabled"
      rows="1"
      @keydown="handleKeydown"
      @input="autoResize"
    ></textarea>
    <button
      class="send-button"
      :disabled="disabled || !text.trim()"
      @click="handleSend"
    >
      <span v-if="!disabled">发送</span>
      <span v-else class="spinner"></span>
    </button>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const emit = defineEmits(['send'])

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
  placeholder: {
    type: String,
    default: '输入你的技术问题，按 Enter 发送...',
  },
})

const text = ref('')
const textareaRef = ref(null)

function handleSend() {
  const question = text.value.trim()
  if (!question || props.disabled) return
  emit('send', question)
  text.value = ''
  nextTick(() => {
    autoResize()
  })
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

function autoResize() {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 150) + 'px'
}
</script>

<style scoped>
.chat-input {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  padding: 14px 18px;
  background: #fff;
  border-top: 1px solid #e5e7eb;
}

.input-textarea {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  outline: none;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
  max-height: 150px;
}
.input-textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.input-textarea:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

.send-button {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 64px;
  height: 40px;
  padding: 0 16px;
  border: none;
  border-radius: 10px;
  background: #3b82f6;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, opacity 0.2s;
}
.send-button:hover:not(:disabled) {
  background: #2563eb;
}
.send-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
