import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  linkActiveClass: 'active',
  history: createWebHistory('/'),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/:theaterId/shows',
      name: 'shows',
      component: () => import('@/views/ShowListView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      props: true,
    },
    {
      path: '/:showId/reviews',
      name: 'reviews',
      component: () => import('@/views/ReviewListView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      props: true,
    },
    {
      path: '/:showId/bookings',
      name: 'bookings',
      component: () => import('@/views/BookingListView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      props: true,
    },
    {
      path: '/insights',
      name: 'insights',
      component: () => import('@/views//InsightView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/show/:showId',
      name: 'show',
      component: () => import('@/views/ShowDetailView.vue'),
      meta: { requiresAuth: false, requiresAdmin: false },
      props: true,
    },
    {
      path: '/theater/:theaterId/shows',
      name: 'theater',
      component: () => import('@/views/TheaterDetailView.vue'),
      meta: { requiresAuth: false, requiresAdmin: false },
      props: true,
    },
    {
      path: '/mybookings',
      name: 'mybookings',
      component: () => import('@/views/MyBookingListView.vue'),
      meta: { requiresAuth: true, requiresAdmin: false },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true, requiresAdmin: false },
    },
    {
      path: '/myreviews',
      name: 'myreviews',
      component: () => import('@/views/MyReviewListView.vue'),
      meta: { requiresAuth: true, requiresAdmin: false },
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  await authStore.fetchUser();

  if (to.meta.requiresAuth) {
    if (authStore.isAuthenticated) {
      if (to.meta.requiresAdmin) {
        if (authStore.isAdmin) {
          next();
        } else {
          next('/');
        }
      } else {
        next();
      }
    } else {
      next('/login');
    }
  } else {
    if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
      next('/');
    } else {
      next();
    }
  }
});

export default router;
