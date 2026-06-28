<template>
  <div class="app-shell">
    <header class="site-header">
      <RouterLink class="brand" to="/">
        <span class="brand-mark">C</span>
        <span>
          <strong>Clean Creation</strong>
          <small>AI Content Studio</small>
        </span>
      </RouterLink>
      <nav class="nav">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/upload">上传</RouterLink>
        <RouterLink to="/image-tools">图片工具</RouterLink>
        <RouterLink to="/video-tools">视频工具</RouterLink>
        <RouterLink to="/tasks">任务</RouterLink>
        <RouterLink to="/publish">发布预留</RouterLink>
        <RouterLink v-if="token" to="/dashboard">用户中心</RouterLink>
        <RouterLink v-if="token" to="/admin">后台</RouterLink>
      </nav>
      <div class="header-actions">
        <RouterLink v-if="!token" class="button ghost" to="/login">登录</RouterLink>
        <RouterLink v-if="!token" class="button primary" to="/signup">注册</RouterLink>
        <RouterLink v-if="token" class="button primary" to="/recharge">充值</RouterLink>
        <button v-if="token" class="button ghost" type="button" @click="logout">退出</button>
      </div>
    </header>

    <main class="page-frame">
      <RouterView />
    </main>

    <footer class="site-footer">
      <span>Clean Creation MVP</span>
      <span>仅用于原创、授权或拥有合法处理权的素材。</span>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { clearToken, getToken } from '../api'

const route = useRoute()
const router = useRouter()
const token = computed(() => {
  route.fullPath
  return getToken()
})

function logout() {
  clearToken()
  router.push('/')
}
</script>
