<template>
  <div class="stack fade-up">
    <div class="section-head">
      <div>
        <span class="eyebrow">Admin</span>
        <h2 style="margin-top:12px">管理后台</h2>
        <p class="muted">只有 Django staff / superuser 可以访问。</p>
      </div>
      <a class="button ghost" href="http://127.0.0.1:8000/admin/" target="_blank">打开 Django Admin</a>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="success">{{ message }}</p>

    <div v-if="stats" class="grid cols-4">
      <div v-for="(value, key) in stats" :key="key" class="metric">
        <span class="muted">{{ key }}</span>
        <strong>{{ value }}</strong>
      </div>
    </div>

    <form class="card form" @submit.prevent="adjust">
      <h3>手动调整积分</h3>
      <div class="grid cols-3">
        <div class="field">
          <label>用户</label>
          <select v-model="adjustForm.user_id" class="select">
            <option value="">选择用户</option>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }} · {{ user.credits }}积分</option>
          </select>
        </div>
        <div class="field">
          <label>调整数量</label>
          <input v-model.number="adjustForm.amount" class="input" type="number" placeholder="例如 100 或 -20" />
        </div>
        <div class="field">
          <label>说明</label>
          <input v-model="adjustForm.description" class="input" placeholder="admin_adjust" />
        </div>
      </div>
      <button class="button primary" :disabled="loading">提交调整</button>
    </form>

    <AdminTable title="用户" :columns="['id','username','email','credits','is_admin']" :items="users" />
    <AdminTable title="订单" :columns="['order_no','user_id','amount_yuan','credits','status','paid_at']" :items="orders" />
    <AdminTable title="积分流水" :columns="['user_id','type','amount','before_balance','after_balance','description']" :items="ledger" />
    <AdminTable title="文件" :columns="['id','user_id','original_name','file_type','size']" :items="files" />
    <AdminTable title="任务" :columns="['id','user_id','job_type','status','credit_cost','progress']" :items="jobs" />
  </div>
</template>

<script setup>
import { defineComponent, h, onMounted, reactive, ref } from 'vue'
import { adminApi } from '../api'

const stats = ref(null)
const users = ref([])
const orders = ref([])
const ledger = ref([])
const files = ref([])
const jobs = ref([])
const error = ref('')
const message = ref('')
const loading = ref(false)
const adjustForm = reactive({ user_id: '', amount: 0, description: 'Admin adjustment' })

async function load() {
  try {
    const data = await adminApi.overview()
    stats.value = data.stats
    users.value = data.users
    orders.value = data.orders
    ledger.value = data.ledger
    files.value = data.files
    jobs.value = data.jobs
  } catch (err) {
    error.value = err.message
  }
}

async function adjust() {
  error.value = ''
  message.value = ''
  loading.value = true
  try {
    const data = await adminApi.adjustCredits(adjustForm)
    message.value = `${data.user.username} 当前积分 ${data.wallet.balance}。`
    await load()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(load)

const AdminTable = defineComponent({
  props: { title: String, columns: Array, items: Array },
  setup(props) {
    return () => h('section', { class: 'stack' }, [
      h('h3', props.title),
      h('div', { class: 'table-card' }, [
        h('table', { class: 'table' }, [
          h('thead', [h('tr', props.columns.map((column) => h('th', column)))]),
          h('tbody', (props.items || []).map((item) =>
            h('tr', { key: `${props.title}-${item.id || item.order_no}` },
              props.columns.map((column) => h('td', String(item[column] ?? '-'))),
            ),
          )),
        ]),
      ]),
    ])
  },
})
</script>
