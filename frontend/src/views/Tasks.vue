<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Tasks</span>
        <h2 style="margin-top:12px">任务中心</h2>
      </div>
      <RouterLink class="button primary" to="/image-tools">创建图片任务</RouterLink>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="table-card">
      <table class="table">
        <thead>
          <tr><th>ID</th><th>类型</th><th>状态</th><th>积分</th><th>进度</th><th>结果</th><th>错误信息</th><th>时间</th></tr>
        </thead>
        <tbody>
          <tr v-for="job in items" :key="job.id">
            <td>{{ job.id }}</td>
            <td>{{ job.job_type }}</td>
            <td><span class="badge" :class="job.status">{{ job.status }}</span></td>
            <td>{{ job.credit_cost }}</td>
            <td><div class="progress"><span :style="{ width: `${job.progress}%` }"></span></div></td>
            <td>
              <a v-if="job.result_file?.public_url" :href="job.result_file.public_url" target="_blank">查看结果</a>
              <span v-else>-</span>
            </td>
            <td>{{ job.error_message || '-' }}</td>
            <td>{{ formatTime(job.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { jobApi } from '../api'

const items = ref([])
const error = ref('')
const formatTime = (value) => value ? new Date(value).toLocaleString() : '-'

onMounted(async () => {
  try {
    items.value = (await jobApi.list()).items
  } catch (err) {
    error.value = err.message
  }
})
</script>
