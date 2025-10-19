import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/role-selection',
    name: 'RoleSelection',
    component: () => import('../views/RoleSelection.vue'),
    meta: { requiresAuth: true, requiresNoRole: true },
  },
  {
    path: '/password-reset',
    name: 'PasswordResetRequest',
    component: () => import('../views/PasswordResetRequest.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/password-reset/:uid/:token',
    name: 'PasswordResetConfirm',
    component: () => import('../views/PasswordResetConfirm.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/campaigns',
    name: 'CampaignList',
    component: () => import('../views/CampaignList.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/campaigns/create',
    name: 'CampaignCreate',
    component: () => import('../views/CampaignForm.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/campaigns/:id/edit',
    name: 'CampaignEdit',
    component: () => import('../views/CampaignForm.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/campaigns/:id',
    name: 'CampaignDetail',
    component: () => import('../views/CampaignDetail.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/my-applications',
    name: 'MyApplications',
    component: () => import('../views/MyApplications.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/applications',
    name: 'ApplicationList',
    component: () => import('../views/ApplicationList.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/applications/new',
    name: 'ApplicationCreate',
    component: () => import('../views/ApplicationForm.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/applications/:id/edit',
    name: 'ApplicationEdit',
    component: () => import('../views/ApplicationForm.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
  {
    path: '/applications/:id',
    name: 'ApplicationDetail',
    component: () => import('../views/ApplicationDetail.vue'),
    meta: { requiresAuth: true, requiresRole: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guards
router.beforeEach((to, _, next) => {
  const authStore = useAuthStore();
  
  // Initialize auth state if not already done
  if (!authStore.isAuthenticated && authStore.user === null) {
    authStore.initializeAuth();
  }
  
  const isAuthenticated = authStore.isAuthenticated;
  const hasRole = authStore.hasRole;
  
  // Redirect authenticated users away from guest-only pages
  if (to.meta.requiresGuest && isAuthenticated) {
    if (!hasRole) {
      return next('/role-selection');
    }
    return next('/dashboard');
  }
  
  // Redirect unauthenticated users to login
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }
  
  // Redirect users without role to role selection
  if (to.meta.requiresRole && !hasRole) {
    return next('/role-selection');
  }
  
  // Redirect users with role away from role selection
  if (to.meta.requiresNoRole && hasRole) {
    return next('/dashboard');
  }
  
  next();
});

export default router;
