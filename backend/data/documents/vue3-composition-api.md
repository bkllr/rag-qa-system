# Vue 3 组合式 API 详解

Vue 3 的组合式 API（Composition API）是一种全新的组件逻辑组织方式，通过 `setup` 函数将相关逻辑聚合在一起。

## 基本结构

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const count = ref(0)

// 计算属性
const double = computed(() => count.value * 2)

// 方法
function increment() {
    count.value++
}

// 生命周期
onMounted(() => {
    console.log('组件已挂载')
})
</script>

<template>
    <button @click="increment">{{ count }} (双倍: {{ double }})</button>
</template>
```

## 响应式 API

### ref - 基本类型

```javascript
import { ref } from 'vue'

const message = ref('你好')
const count = ref(0)

// 修改值需要 .value
count.value++
message.value = '世界'
```

### reactive - 对象类型

```javascript
import { reactive } from 'vue'

const state = reactive({
    user: { name: '张三', age: 25 },
    items: [1, 2, 3],
})

// 直接访问，无需 .value
state.user.name = '李四'
state.items.push(4)
```

### computed - 计算属性

```javascript
import { ref, computed } from 'vue'

const firstName = ref('张')
const lastName = ref('三')

const fullName = computed({
    get: () => `${firstName.value}${lastName.value}`,
    set: (val) => {
        firstName.value = val[0]
        lastName.value = val.slice(1)
    }
})
```

### watch - 侦听器

```javascript
import { ref, watch } from 'vue'

const question = ref('')

watch(question, (newVal, oldVal) => {
    console.log(`问题从 "${oldVal}" 变为 "${newVal}"`)
})

// 侦听多个数据源
watch([firstName, lastName], ([newFirst, newLast]) => {
    console.log(`${newFirst} ${newLast}`)
})
```

## 生命周期钩子

| Options API | Composition API |
|:--|:--|
| beforeCreate | setup() |
| created | setup() |
| beforeMount | onBeforeMount |
| mounted | onMounted |
| beforeUpdate | onBeforeUpdate |
| updated | onUpdated |
| beforeUnmount | onBeforeUnmount |
| unmounted | onUnmounted |

## 组件通信

### Props

```vue
<!-- 子组件 -->
<script setup>
defineProps({
    title: String,
    count: { type: Number, default: 0 }
})
</script>
```

### Emits

```vue
<script setup>
const emit = defineEmits(['update', 'delete'])

function handleClick() {
    emit('update', newValue)
}
</script>
```

### 父组件使用

```vue
<template>
    <ChildComponent
        title="标题"
        :count="5"
        @update="handleUpdate"
    />
</template>
```
