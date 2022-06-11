import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Signal from '../views/Signal.vue'
import Multiple from '../views/Multy.vue'
import SearchPage from '../views/SearchPage.vue'
import DisplayPage from '../views/DisplayPage.vue'
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/search'
  },
  {
    path: '/search',
    redirect: '/search/signal'
  },

  {
    path: '/search',
    name: 'SearchPage',
    component: SearchPage,
    meta: {
      keepAlive: true
    },
    children: [
      {
        path: 'signal',
        component: Signal,
        meta: {
          keepAlive: true
        }
      },
      {
        path: 'multiple',
        component: Multiple,
        meta: {
          keepAlive: true
        }
      },
    ]
  },
  {
    path: '/display',
    component: DisplayPage,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
