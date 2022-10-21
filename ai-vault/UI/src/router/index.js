import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/pages/Login'
import Layout from '@/pages/Layout'
import store from '@/store/index.js'
import { getAuthToken } from '@/shared/common'

Vue.use(Router)
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/app',
      component: Layout,
      children: [
        {
          path: 'home',
          name: 'home',
          component: () => import(/* webpackChunkName: "home" */ '../pages/Home.vue'),
          meta: {
            role: [1]
          }
        },
        {
          path: 'user',
          name: 'user',
          component: () => import(/* webpackChunkName: "user" */ '../pages/user/Index.vue'),
          meta: {
            role: [1]
          }
        },
        {
          path: 'ai-vault',
          name: 'ai-vault',
          component: () => import(/* webpackChunkName: "ai-vault" */ '../pages/ai-vault/Index.vue'),
          meta: {
            role: [4]
          }
        },
      ]
    },
  ]
})

export default router;

router.beforeEach((to, from, next) => {
  if(to.name !== 'login' && !store.state.login.userInfo) {
    next({
      name: 'login'
    })
  } else {
    next()
  }
  if(getAuthToken()) {
    if(to.name === 'login' || to.meta.role.includes(store.state.login.userInfo.RoleID)) {
      next();
    } else {
      next(from.path)
    }
  }
})