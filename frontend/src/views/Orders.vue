<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Orders</span>
        <h2 style="margin-top:12px">订单记录</h2>
      </div>
      <RouterLink class="button primary" to="/recharge">创建充值订单</RouterLink>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="table-card">
      <table class="table">
        <thead>
          <tr><th>订单号</th><th>金额</th><th>积分</th><th>渠道</th><th>状态</th><th>创建时间</th><th>支付时间</th></tr>
        </thead>
        <tbody>
          <tr v-for="order in items" :key="order.id">
            <td>{{ order.order_no }}</td>
            <td>{{ order.amount_yuan }} 元</td>
            <td>{{ order.credits }}</td>
            <td>{{ order.payment_channel }}</td>
            <td><span class="badge" :class="order.status">{{ order.status }}</span></td>
            <td>{{ formatTime(order.created_at) }}</td>
            <td>{{ formatTime(order.paid_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { orderApi } from '../api'

const items = ref([])
const error = ref('')
const formatTime = (value) => value ? new Date(value).toLocaleString() : '-'

onMounted(async () => {
  try {
    items.value = (await orderApi.list()).items
  } catch (err) {
    error.value = err.message
  }
})
</script>
