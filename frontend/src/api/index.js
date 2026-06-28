import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const TOKEN_KEY = 'clean_creation_token'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status
    const message =
      error.response?.data?.error ||
      (error.code === 'ECONNABORTED'
        ? '服务可能正在唤醒，请稍候再试。'
        : '请求失败，请稍后重试。')
    return Promise.reject({ status, message, raw: error })
  },
)

export const authApi = {
  register(payload) {
    return api.post('/auth/register', payload)
  },
  async login(payload) {
    const data = await api.post('/auth/login', payload)
    if (data.token) setToken(data.token)
    return data
  },
  me() {
    return api.get('/auth/me')
  },
}

export const walletApi = {
  get() {
    return api.get('/wallet')
  },
  ledger() {
    return api.get('/credits/ledger')
  },
}

export const orderApi = {
  create(amountYuan) {
    return api.post('/orders/create', { amount_yuan: amountYuan })
  },
  list() {
    return api.get('/orders')
  },
  detail(id) {
    return api.get(`/orders/${id}`)
  },
  mockPay(orderId) {
    return api.post('/payments/mock/pay', { order_id: orderId })
  },
}

export const fileApi = {
  upload(file, consent, onProgress) {
    const form = new FormData()
    form.append('file', file)
    form.append('consent', consent ? 'true' : 'false')
    return api.post('/files/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (event) => {
        if (onProgress && event.total) {
          onProgress(Math.round((event.loaded / event.total) * 100))
        }
      },
    })
  },
  list() {
    return api.get('/files')
  },
}

export const jobApi = {
  create(payload) {
    return api.post('/jobs/create', payload)
  },
  list() {
    return api.get('/jobs')
  },
}

export const adminApi = {
  overview() {
    return api.get('/admin/overview')
  },
  adjustCredits(payload) {
    return api.post('/admin/credits/adjust', payload)
  },
}

export default api
