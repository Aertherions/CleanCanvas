<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Credit ledger</span>
        <h2 style="margin-top:12px">积分明细</h2>
      </div>
      <RouterLink class="button primary" to="/recharge">充值</RouterLink>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="table-card">
      <table class="table">
        <thead>
          <tr><th>类型</th><th>变动</th><th>之前</th><th>之后</th><th>说明</th><th>时间</th></tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td><span class="badge">{{ item.type }}</span></td>
            <td>{{ item.amount }}</td>
            <td>{{ item.before_balance }}</td>
            <td>{{ item.after_balance }}</td>
            <td>{{ item.description }}</td>
            <td>{{ formatTime(item.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { walletApi } from '../api'

const items = ref([])
const error = ref('')
const formatTime = (value) => value ? new Date(value).toLocaleString() : '-'

onMounted(async () => {
  try {
    items.value = (await walletApi.ledger()).items
  } catch (err) {
    error.value = err.message
  }
})
</script>
