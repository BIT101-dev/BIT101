/*
 * @Author: flwfdd
 * @Date: 2022-05-28 01:19:14
 * @LastEditTime: 2023-03-30 14:28:55
 * @Description: 
 * _(:з」∠)_
 */
import { createRouter, createWebHashHistory } from 'vue-router'
import { setTitle } from '@/utils/tools'

const router = createRouter({
  history: createWebHashHistory(),
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
      meta:{keepAlive:false}
    },
    {
      path: '/user/:id',
      name: 'user',
      component: () => import('@/views/User.vue'),
      meta:{keepAlive:false}
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
      path: '/paper/show/:id',
      name: 'paper_show',
      component: () => import('@/views/PaperShow.vue')
    },
    {
      path: '/course/show/:id',
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
      meta:{keepAlive:false}
    },
    {
      path: '/about/',
      name: 'about',
      component: () => import('@/views/About.vue'),
      meta:{keepAlive:false}
    },
    {
      path: '/schedule/',
      name: 'schedule',
      component: () => import('@/views/Schedule.vue'),
      meta:{keepAlive:false}
    },
    {
      path: '/message/',
      name: 'message',
      component: () => import('@/views/Message.vue')
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
  ]
});

router.beforeEach(({ path }) => {
  // 此处只是尽快响应，设置大类标题。
  // 之后各组件可以再覆盖。

  const titleMap: Record<string, string> = {
    '': '欢迎',
    login: '登录',
    user: '我的',
    paper: '文章',
    course: '课程',
    score: '成绩',
    schedule:'课表',
    about: '关于',
    message: '消息',
  }
  const top = path.split('/').filter(piece => piece.length > 0)[0] ?? ''
  const title = titleMap[top] ?? top
  setTitle(title)
})

export default router;
