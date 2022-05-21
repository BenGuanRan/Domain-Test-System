import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Signal from '../views/Signal.vue'
import Multiple from '../views/Multy.vue'
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/signal'
  },
  {
    path: '/signal',
    name: 'Signal',
    component: Signal,
    meta: {
      keepAlive: true
    }
  },
  {
    path: '/multiple',
    name: 'Multiple',
    component: Multiple,
    meta: {
      keepAlive: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
