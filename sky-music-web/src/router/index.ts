import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/home',
    name: 'home',
    component: () => import(/* webpackChunkName: "about" */ '../views/home.vue')
  },
  {
    path: '/music',
    name: 'music',
    component: () => import(/* webpackChunkName: "about" */ '../views/music.vue')
  },
  {
    path: '/kube',
    name: 'kube',
    component: () => import(/* webpackChunkName: "about" */ '../views/kube.vue')
  },
  {
    path: '/tutorial',
    name: 'tutorial',
    component: () => import(/* webpackChunkName: "about" */ '../views/tutorial.vue')
  },
  {
    path: '/keyboard',
    name: 'keyboard',
    component: () => import(/* webpackChunkName: "about" */ '../views/tutorial_keyboard.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
