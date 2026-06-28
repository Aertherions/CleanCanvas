<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Workspace</span>
        <h2 style="margin-top:12px">用户中心</h2>
      </div>
      <RouterLink class="button primary" to="/recharge">充值积分</RouterLink>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="grid cols-4">
      <div class="metric"><span class="muted">账号</span><strong>{{ user?.username || '-' }}</strong></div>
      <div class="metric"><span class="muted">当前积分</span><strong :class="{ pulse: highlighted }">{{ wallet?.balance ?? 0 }}</strong></div>
      <div class="metric"><span class="muted">最近订单</span><strong>{{ orders.length }}</strong></div>
      <div class="metric"><span class="muted">最近任务</span><strong>{{ jobs.length }}</strong></div>
    </div>

    <div class="grid cols-3">
      <SummaryCard title="最近订单" :items="orders.map(o => `${o.order_no} · ${o.status} · ${o.credits}积分`)" to="/orders" />
      <SummaryCard title="最近任务" :items="jobs.map(j => `${j.job_type} · ${j.status} · -${j.credit_cost}`)" to="/tasks" />
      <SummaryCard title="最近文件" :items="files.map(f => `${f.original_name} · ${(f.size / 1024).toFixed(1)}KB`)" to="/files" />
    </div>
  </div>
</template>

<script setup>
import { defineComponent, h, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { authApi, fileApi, jobApi, orderApi } from '../api'

const user = ref(null)
const wallet = ref(null)
const orders = ref([])
const jobs = ref([])
const files = ref([])
const error = ref('')
const highlighted = ref(false)

async function load() {
  try {
    const [me, orderData, jobData, fileData] = await Promise.all([
      authApi.me(),
      orderApi.list(),
      jobApi.list(),
      fileApi.list(),
    ])
    user.value = me.user
    wallet.value = me.wallet
    orders.value = orderData.items.slice(0, 5)
    jobs.value = jobData.items.slice(0, 5)
    files.value = fileData.items.slice(0, 5)
    highlighted.value = true
    setTimeout(() => { highlighted.value = false }, 1000)
  } catch (err) {
    error.value = err.message
  }
}

onMounted(load)

const SummaryCard = defineComponent({
  props: { title: String, items: Array, to: String },
  setup(props) {
    return () => h(RouterLink, { class: 'card', to: props.to }, () => [
      h('h3', props.title),
      props.items?.length
        ? h('div', { class: 'stack', style: 'gap:8px;margin-top:14px' }, props.items.map((item) => h('p', { class: 'muted' }, item)))
        : h('p', { class: 'muted', style: 'margin-top:14px' }, '暂无记录'),
    ])
  },
})
</script>

<style scoped>
.pulse {
  color: var(--accent);
  transition: color 260ms ease;
}
</style>
