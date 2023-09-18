import { ref, onMounted } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import api from '@/api';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  const user = ref({});

  const isAdmin = ref(false);
  const isAuthenticated = ref(false);

  onMounted(fetchUser);

  async function register(user) {
    try {
      const response = await api.post('/register', user);

      if (response.status === 201) {
        const { auth_token } = response.data;
        localStorage.setItem('auth_token', auth_token);
        await fetchUser();
        router.push('/');
      } else {
        console.error('Registration failed');
      }
    } catch (error) {
      console.error('Registration failed', error);
    }
  }

  async function login(user) {
    try {
      const response = await api.post('/login', user);

      if (response.status === 200) {
        const { auth_token } = response.data;
        localStorage.setItem('auth_token', auth_token);
        await fetchUser();
        router.push('/');
      } else {
        console.error('Login failed');
      }
    } catch (error) {
      console.error('Login failed', error);
    }
  }

  async function fetchUser() {
    try {
      const authToken = localStorage.getItem('auth_token');
      if (authToken) {
        const response = await api.get('/user');
        if (response.status === 200) {
          user.value = response.data;
          isAuthenticated.value = true;
          isAdmin.value = user.value.roles.some(role => role.name === 'admin');
        } else {
          console.error('Failed to fetch user');
        }
      }
    } catch (error) {
      console.error('Failed to fetch user');
    }
  }

  async function logout() {
    try {
      const response = await api.post('/logout');
      localStorage.removeItem('auth_token');
      isAuthenticated.value = false;
      isAdmin.value = false;
      delete api.defaults.headers.common['Authentication-Token'];
      user.value = {};
      console.log('User object after logout:', user.value);
      router.push('/');
      location.reload();
    } catch (error) {
      console.error('Logout failed');
    }
  }

  return { user, login, register, isAuthenticated, logout, fetchUser, isAdmin };
});
