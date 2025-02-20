import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home_loader',
    component: () => import('../views/home_loader.vue')
  },
  {
    path: '/home',
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
    path: '/sheetToHTML',
    name: 'sheetToHTML',
    component: () => import('../views/sheetToHTML.vue')
  },
  {
    path: '/magicTools',
    name: 'magicTools',
    component: () => import('../views/magicTools.vue')
  },
  {
    path: '/shortcut',
    name: 'shortcut',
    component: () => import('../views/shortcutKeys.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
