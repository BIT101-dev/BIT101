/*
 * @Author: flwfdd
 * @Date: 2022-05-28 01:19:14
 * @LastEditTime: 2023-10-29 16:04:15
 * @Description: 
 * _(:з」∠)_
 */
import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import { setTitle } from '@/utils/tools'
import axios from 'axios';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { keepAlive: false }
    },
    {
      path: '/user/:id',
      name: 'user',
      component: () => import('@/views/User.vue'),
      meta: { keepAlive: false }
    },
    {
      path: '/score',
      name: 'score',
      component: () => import('@/views/Score.vue')
    },
    {
      path: '/paper',
      name: 'paper',
      component: () => import('@/views/Paper.vue')
    },
    {
      path: '/paper/edit/:id',
      name: 'paper_edit',
      component: () => import('@/views/PaperEdit.vue')
    },
    {
      path: '/paper/:id',
      name: 'paper_show',
      component: () => import('@/views/PaperShow.vue')
    },
    {
      path: '/course/:id',
      name: 'course_show',
      component: () => import('@/views/CourseShow.vue')
    },
    {
      path: '/course',
      name: 'course',
      component: () => import('@/views/Course.vue')
    },
    {
      path: '/course/upload/:id',
      name: 'course_upload',
      component: () => import('@/views/CourseUpload.vue'),
      meta: { keepAlive: false }
    },
    {
      path: '/about/',
      name: 'about',
      component: () => import('@/views/About.vue'),
      meta: { keepAlive: false }
    },
    {
      path: '/schedule/',
      name: 'schedule',
      component: () => import('@/views/Schedule.vue'),
      meta: { keepAlive: false }
    },
    {
      path: '/message/',
      name: 'message',
      component: () => import('@/views/Message.vue')
    },
    {
      path: '/map/',
      name: 'map',
      component: () => import('@/views/Map.vue')
    },
    {
      path: '/gallery/',
      name: 'gallery',
      component: () => import('@/views/Gallery.vue'),
      meta: { login: true }
    },
    {
      path: '/gallery/:id',
      name: 'gallery_show',
      component: () => import('@/views/GalleryShow.vue'),
      meta: { keepAlive: false, login: true }
    },
    {
      path: '/gallery/edit/:id',
      name: 'gallery_edit',
      component: () => import('@/views/GalleryEdit.vue'),
      meta: { keepAlive: false, login: true }
    },
    {
      path: '/report/:obj',
      name: 'report',
      component: () => import('@/views/Report.vue'),
      meta: { login: true }
    },
    {
      path: '/admin/carousel/',
      name: 'admin_carousel',
      component: () => import('@/views/admin/Carousel.vue')
    },
    {
      path: '/admin/billboard/',
      name: 'admin_billboard',
      component: () => import('@/views/admin/Billboard.vue')
    },
    {
      path: '/:pathMatch(.*)',
      name: '404',
      component: () => import('@/views/404.vue')
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    else return { top: 0 }
  },
});

router.beforeEach(({ path }) => {
  // 此处只是尽快响应，设置大类标题。
  // 之后各组件可以再覆盖。

  const titleMap: Record<string, string> = {
    '': '主页',
    login: '登录',
    user: '我的',
    paper: '文章',
    course: '课程',
    score: '成绩',
    schedule: '课表',
    about: '关于',
    message: '消息',
    map: '地图',
    gallery: '话廊',
    report: '举报',
  }
  const top = path.split('/').filter(piece => piece.length > 0)[0] ?? ''
  const title = titleMap[top] ?? top
  setTitle(title)
})

export default router;
