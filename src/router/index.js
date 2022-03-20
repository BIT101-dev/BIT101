/*
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-03-19 14:35:09
 * @Description: 
 * _(:з」∠)_
 */
import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/score',
    name: 'score',
    component: () => import('../views/ScoreView.vue')
  },
  {
    path: '/my',
    name: 'my',
    component: () => import('../views/MyView.vue')
  },
  {
    path: '/course',
    name: 'course',
    component: () => import('../views/CourseView.vue')
  }
  ,
  {
    path: '/course/detail',
    name: 'course_detail',
    component: () => import('../views/CourseDetailView.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
