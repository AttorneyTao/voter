import { createRouter, createWebHistory } from 'vue-router';
import VotePage from '../components/VotePage.vue';
import AdminPage from '../components/AdminPage.vue';
import LoginPage from '../components/LoginPage.vue';
// 导入其他页面组件



const routes = [
  {
    path: '/',
    name: 'Vote',
    component: VotePage,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminPage,
    meta: { requiresAuth: true }
    // 可以添加路由守卫进行身份验证
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  // 定义其他路由
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});
// 添加全局前置守卫
router.beforeEach((to, from, next) => {
  // 检查即将访问的路由是否被标记为需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已经登录
    const isAuthenticated = localStorage.getItem('auth');
    if (!isAuthenticated) {
      // 如果用户未登录，重定向到登录页面
      next({ name: 'Login' });
    } else {
      // 如果用户已登录，允许访问
      next();
    }
  } else {
    // 对于不需要认证的路由，直接允许访问
    next();
  }
});
export default router;
