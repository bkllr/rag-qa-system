<template>
  <div class="source-card" :class="{ expanded }">
    <div class="source-header" @click="expanded = !expanded">
      <div class="source-info">
        <span class="source-badge" :class="scoreClass">{{ scorePercent }}</span>
        <span class="source-filename" :title="source.filename">{{ displayName }}</span>
      </div>
      <span class="source-toggle">{{ expanded ? '▾' : '▸' }}</span>
    </div>
    <div class="source-body" v-show="expanded">
      <pre class="source-content">{{ source.content }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  source: {
    type: Object,
    required: true,
  },
})

const expanded = ref(false)

const scorePercent = computed(() => {
  return `${Math.round((props.source.score || 0) * 100)}%`
})

const scoreClass = computed(() => {
  const s = props.source.score || 0
  if (s >= 0.8) return 'score-high'
  if (s >= 0.6) return 'score-mid'
  return 'score-low'
})

const displayName = computed(() => {
  const name = props.source.filename || '未知'
  // 截取文件名部分
  const parts = name.replace(/\\/g, '/').split('/')
  return parts[parts.length - 1]
})
</script>

<style scoped>
.source-card {
  margin-top: 6px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background: #fafbfc;
  transition: border-color 0.2s;
}
.source-card.expanded {
  border-color: #93c5fd;
}

.source-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  cursor: pointer;
  user-select: none;
  font-size: 13px;
}
.source-header:hover {
  background: #f0f4f8;
}

.source-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.source-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}
.source-badge.score-high {
  background: #d1fae5;
  color: #065f46;
}
.source-badge.score-mid {
  background: #fef3c7;
  color: #92400e;
}
.source-badge.score-low {
  background: #fee2e2;
  color: #991b1b;
}

.source-filename {
  color: #4b5563;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.source-toggle {
  color: #9ca3af;
  font-size: 14px;
  flex-shrink: 0;
}

.source-body {
  padding: 0 12px 10px;
}

.source-content {
  margin: 0;
  padding: 10px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.6;
  color: #374151;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
}
</style>
