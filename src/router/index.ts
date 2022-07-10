/*
 * @Author: flwfdd
 * @Date: 2022-05-28 01:19:14
 * @LastEditTime: 2022-07-10 23:12:16
 * @Description: 
 * _(:з」∠)_
 */
import { createRouter, createWebHashHistory } from 'vue-router';

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
      component: () => import('@/views/Login.vue')
    },
    {
      path: '/user/:id',
      name: 'user',
      component: () => import('@/views/User.vue')
    },
    {
      path: '/score',
      name: 'score',
      component: () => import('@/views/Score.vue')
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
  ]
});

export default router;
