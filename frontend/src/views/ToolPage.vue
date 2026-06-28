<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">{{ eyebrow }}</span>
        <h2 style="margin-top:12px">{{ title }}</h2>
        <p class="muted">{{ note }}</p>
      </div>
      <RouterLink class="button ghost" to="/upload">上传素材</RouterLink>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="success">{{ message }}</p>
    <div class="grid cols-3">
      <div v-for="tool in tools" :key="tool.type" class="card">
        <span class="eyebrow">{{ tool.cost }} 积分</span>
        <h3 style="margin-top:14px">{{ tool.name }}</h3>
        <p class="muted" style="margin:10px 0 16px">{{ tool.type }}</p>
        <div class="field">
          <label>选择文件</label>
          <select v-model="selected[tool.type]" class="select">
            <option value="">请选择</option>
            <option v-for="file in filteredFiles" :key="file.id" :value="file.id">
              {{ file.original_name }}
            </option>
          </select>
        </div>
        <button class="button primary" style="margin-top:14px" :disabled="loading || !selected[tool.type]" @click="create(tool)">
          {{ loading ? '创建中...' : '创建任务' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { fileApi, jobApi } from '../api'

const props = defineProps({
  title: String,
  eyebrow: String,
  note: String,
  tools: Array,
  fileType: String,
})

const files = ref([])
const selected = reactive({})
const error = ref('')
const message = ref('')
const loading = ref(false)
const filteredFiles = computed(() => files.value.filter((file) => file.file_type === props.fileType))

async function loadFiles() {
  try {
    files.value = (await fileApi.list()).items
  } catch (err) {
    error.value = err.message
  }
}

async function create(tool) {
  error.value = ''
  message.value = ''
  loading.value = true
  try {
    const data = await jobApi.create({ source_file_id: selected[tool.type], job_type: tool.type })
    message.value = `任务 ${data.job.id} 已成功，扣除 ${data.job.credit_cost} 积分，当前余额 ${data.wallet.balance}。`
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(loadFiles)
</script>
