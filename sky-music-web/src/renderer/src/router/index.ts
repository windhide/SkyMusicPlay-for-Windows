import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/home.vue')
  },
  {
    path: '/music',
    name: 'music',
    component: () => import('../views/music.vue')
  },
  {
    path: '/kube',
    name: 'kube',
    component: () => import('../views/kube.vue')
  },
  {
    path: '/tutorial',
    name: 'tutorial',
    component: () => import('../views/tutorial.vue')
  },
  {
    path: '/keyboard',
    name: 'keyboard',
    component: () => import('../views/tutorial_keyboard.vue')
  },
  {
    path: '/sheetPdf',
    name: 'sheetPdf',
    component: () => import('../views/sheetToPDF.vue')
  },
  {
    path: '/magicTools',
    name: 'magicTools',
    component: () => import('../views/magicTools.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
