import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '../api'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/signup', name: 'Signup', component: () => import('../views/Signup.vue') },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { requiresAuth: true } },
  { path: '/recharge', name: 'Recharge', component: () => import('../views/Recharge.vue'), meta: { requiresAuth: true } },
  { path: '/credits', name: 'Credits', component: () => import('../views/Credits.vue'), meta: { requiresAuth: true } },
  { path: '/orders', name: 'Orders', component: () => import('../views/Orders.vue'), meta: { requiresAuth: true } },
  { path: '/upload', name: 'Upload', component: () => import('../views/Upload.vue'), meta: { requiresAuth: true } },
  { path: '/image-tools', name: 'ImageTools', component: () => import('../views/ImageTools.vue'), meta: { requiresAuth: true } },
  { path: '/video-tools', name: 'VideoTools', component: () => import('../views/VideoTools.vue'), meta: { requiresAuth: true } },
  { path: '/tasks', name: 'Tasks', component: () => import('../views/Tasks.vue'), meta: { requiresAuth: true } },
  { path: '/files', name: 'Files', component: () => import('../views/Files.vue'), meta: { requiresAuth: true } },
  { path: '/admin', name: 'Admin', component: () => import('../views/Admin.vue'), meta: { requiresAuth: true } },
  { path: '/publish', name: 'PublishReserve', component: () => import('../views/PublishReserve.vue'), meta: { requiresAuth: true } },
  { path: '/about', name: 'About', component: () => import('../views/About.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !getToken()) {
    return { path: '/login', query: { next: to.fullPath } }
  }
  return true
})

export default router
