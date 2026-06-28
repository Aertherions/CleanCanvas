<template>
  <section class="hero-grid">
    <div>
      <span class="eyebrow fade-up">Create account</span>
      <h1 class="fade-up delay-1">注册 Clean Creation</h1>
      <p class="lead fade-up delay-2">第一版注册后积分为 0，通过 mock 充值获得积分，再创建处理任务。</p>
    </div>
    <form class="card form fade-up delay-3" @submit.prevent="submit">
      <div class="field">
        <label>邮箱 / 手机号</label>
        <input v-model="account" class="input" autocomplete="username" placeholder="creator@example.com" />
      </div>
      <div class="field">
        <label>密码</label>
        <input v-model="password" class="input" type="password" autocomplete="new-password" />
      </div>
      <div class="field">
        <label>确认密码</label>
        <input v-model="confirmPassword" class="input" type="password" autocomplete="new-password" />
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
      <button class="button primary" :disabled="loading" type="submit">{{ loading ? '注册中...' : '注册' }}</button>
      <RouterLink class="button ghost" to="/login">已有账号，去登录</RouterLink>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { authApi } from '../api'

const router = useRouter()
const account = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

async function submit() {
  error.value = ''
  success.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = '两次密码不一致。'
    return
  }
  loading.value = true
  try {
    await authApi.register({
      account: account.value,
      password: password.value,
      confirm_password: confirmPassword.value,
    })
    success.value = '注册成功，正在跳转登录。'
    setTimeout(() => router.push('/login'), 700)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
