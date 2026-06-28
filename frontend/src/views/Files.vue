<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Files</span>
        <h2 style="margin-top:12px">文件中心</h2>
      </div>
      <RouterLink class="button primary" to="/upload">上传文件</RouterLink>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="table-card">
      <table class="table">
        <thead>
          <tr><th>文件名</th><th>类型</th><th>MIME</th><th>大小</th><th>时间</th><th>访问</th></tr>
        </thead>
        <tbody>
          <tr v-for="file in items" :key="file.id">
            <td>{{ file.original_name }}</td>
            <td>{{ file.file_type }}</td>
            <td>{{ file.mime_type }}</td>
            <td>{{ (file.size / 1024).toFixed(1) }} KB</td>
            <td>{{ formatTime(file.created_at) }}</td>
            <td><a :href="file.public_url" target="_blank">打开</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { fileApi } from '../api'

const items = ref([])
const error = ref('')
const formatTime = (value) => value ? new Date(value).toLocaleString() : '-'

onMounted(async () => {
  try {
    items.value = (await fileApi.list()).items
  } catch (err) {
    error.value = err.message
  }
})
</script>
