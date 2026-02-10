import axios from 'axios';
import { useAuthStore } from '../store/auth';
import router from '../router';

const setupInterceptors = (apiInstance) => {
  apiInstance.interceptors.request.use(
    (config) => {
      const authStore = useAuthStore();
      if (authStore.token) {
        config.headers.Authorization = `Bearer ${authStore.token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  apiInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const authStore = useAuthStore();
      const originalRequest = error.config;

      // If error status is 401 and it's not a login or refresh request
      if (error.response.status === 401 && !originalRequest._retry && !originalRequest.url.includes('/token/')) {
        originalRequest._retry = true; // Mark request as retried

        try {
          // Attempt to refresh token
          await authStore.refreshToken();
          // Retry the original request with the new token
          return apiInstance(originalRequest);
        } catch (refreshError) {
          // If refresh fails, log out and redirect to login
          authStore.logout();
          router.push('/login');
          return Promise.reject(refreshError);
        }
      }
      return Promise.reject(error);
    }
  );
};

export default setupInterceptors;
