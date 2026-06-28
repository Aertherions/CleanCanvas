<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Mock payment</span>
        <h2 style="margin-top:12px">充值中心</h2>
        <p class="muted">第一版仅使用 mock 支付，不接真实支付。</p>
      </div>
      <RouterLink class="button ghost" to="/orders">订单记录</RouterLink>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="success">{{ message }}</p>
    <div class="grid cols-4">
      <div v-for="pack in packs" :key="pack.amount" class="card">
        <span class="eyebrow">mock</span>
        <h3 style="margin-top:14px">{{ pack.amount }} 元 = {{ pack.credits }} 积分</h3>
        <p class="muted" style="margin:12px 0 18px">1 人民币 = 10 积分</p>
        <button class="button primary" :disabled="loading" @click="createAndPay(pack)">
          {{ loading ? '处理中...' : '创建订单并支付成功' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { orderApi } from '../api'

const packs = [
  { amount: 10, credits: 100 },
  { amount: 30, credits: 300 },
  { amount: 100, credits: 1000 },
  { amount: 300, credits: 3000 },
]
const loading = ref(false)
const error = ref('')
const message = ref('')

async function createAndPay(pack) {
  error.value = ''
  message.value = ''
  loading.value = true
  try {
    const created = await orderApi.create(pack.amount)
    const paid = await orderApi.mockPay(created.order.id)
    message.value = `订单 ${paid.order.order_no} 已 mock 支付成功，当前积分 ${paid.wallet.balance}。`
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
