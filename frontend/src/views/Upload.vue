<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Upload</span>
        <h2 style="margin-top:12px">上传素材</h2>
        <p class="muted">支持小图片和演示视频文件，MVP 限制 5MB。</p>
      </div>
      <RouterLink class="button ghost" to="/files">文件中心</RouterLink>
    </div>

    <div class="card upload-zone" :class="{ active: dragging }" @dragover.prevent="dragging = true" @dragleave.prevent="dragging = false" @drop.prevent="dropFile">
      <input ref="input" hidden type="file" accept="image/*,video/*" @change="pickFile" />
      <span class="eyebrow">Drag & drop</span>
      <h3 style="margin-top:14px">{{ file ? file.name : '拖拽文件到这里，或点击选择' }}</h3>
      <p class="muted" style="margin-top:10px">上传前必须确认内容为本人原创、已授权或拥有合法处理权。</p>
      <div class="actions">
        <button class="button secondary" type="button" @click="input.click()">选择文件</button>
      </div>
    </div>

    <label class="notice" style="display:flex;gap:10px;align-items:flex-start">
      <input v-model="consent" type="checkbox" />
      我确认上传的内容为本人原创、已授权或拥有合法处理权。
    </label>

    <div v-if="progress > 0" class="progress"><span :style="{ width: `${progress}%` }"></span></div>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="uploaded" class="success">上传成功：{{ uploaded.original_name }}。你可以进入图片工具或视频工具创建任务。</p>
    <div class="actions">
      <button class="button primary" :disabled="!file || !consent || loading" @click="upload">
        {{ loading ? '上传中...' : '上传' }}
      </button>
      <RouterLink class="button ghost" to="/image-tools">去图片工具</RouterLink>
      <RouterLink class="button ghost" to="/video-tools">去视频工具</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { fileApi } from '../api'

const input = ref(null)
const file = ref(null)
const consent = ref(false)
const dragging = ref(false)
const progress = ref(0)
const uploaded = ref(null)
const loading = ref(false)
const error = ref('')

function setFile(candidate) {
  error.value = ''
  uploaded.value = null
  if (!candidate) return
  if (candidate.size > 5 * 1024 * 1024) {
    error.value = '文件超过 5MB，请先压缩。'
    return
  }
  file.value = candidate
}

function pickFile(event) {
  setFile(event.target.files?.[0])
}

function dropFile(event) {
  dragging.value = false
  setFile(event.dataTransfer.files?.[0])
}

async function upload() {
  error.value = ''
  progress.value = 4
  loading.value = true
  try {
    uploaded.value = (await fileApi.upload(file.value, consent.value, (value) => { progress.value = value })).file
    progress.value = 100
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.upload-zone {
  cursor: pointer;
  border-style: dashed;
}
.upload-zone.active {
  border-color: rgba(179,92,46,0.45);
  background: rgba(255,253,247,0.92);
}
</style>
