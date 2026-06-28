<template>
  <section class="hero-grid">
    <div>
      <span class="eyebrow fade-up">Welcome back</span>
      <h1 class="fade-up delay-1">登录工作台</h1>
      <p class="lead fade-up delay-2">使用邮箱或手机号和密码登录，进入积分、任务、文件和后台管理闭环。</p>
    </div>
    <form class="card form fade-up delay-3" @submit.prevent="submit">
      <div class="field">
        <label>邮箱 / 手机号</label>
        <input v-model="account" class="input" autocomplete="username" placeholder="you@example.com" />
      </div>
      <div class="field">
        <label>密码</label>
        <input v-model="password" class="input" type="password" autocomplete="current-password" />
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <button class="button primary" :disabled="loading" type="submit">{{ loading ? '登录中...' : '登录' }}</button>
      <RouterLink class="button ghost" to="/signup">还没有账号，去注册</RouterLink>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { authApi } from '../api'

const router = useRouter()
const route = useRoute()
const account = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await authApi.login({ account: account.value, password: password.value })
    router.push(route.query.next || '/dashboard')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
