import router from '@/router';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const authToken = localStorage.getItem('auth_token');
    if (authToken) {
      config.headers['Authentication-Token'] = authToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// // Response interceptor
// api.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   async (error) => {
//     const originalRequest = error.config;

//     if (error.response.status === 401 && originalRequest && !originalRequest._retry) {
//       originalRequest._retry = true;

//       try {
//         const authToken = localStorage.getItem('auth_token');
//         const response = await axios.post('http://127.0.0.1:5000/api/refresh', {
//           auth_token: authToken
//         });

//         api.defaults.headers.common['Authentication-Token'] = response.data.auth_token;

//         return api(originalRequest);
//       } catch (error) {
//         router.push('/login');
//         return Promise.reject(error);
//       }
//     }

//     return Promise.reject(error);
//   }
// );

export default api;
