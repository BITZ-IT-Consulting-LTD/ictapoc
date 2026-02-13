import { defineStore } from 'pinia'
import api from '../services/api'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      const response = await api.post('/token/', { username, password })
      this.token = response.data.access
      this.refreshToken = response.data.refresh
      localStorage.setItem('access_token', this.token)
      localStorage.setItem('refresh_token', this.refreshToken)

      const userData = jwtDecode(this.token)
      // Fetch full user details
      const userResponse = await api.get(`/users/${userData.user_id}/`)
      this.user = userResponse.data
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    async refreshAccessToken() {
      if (!this.refreshToken) {
        throw new Error('No refresh token available.');
      }
      const response = await api.post('/token/refresh/', { refresh: this.refreshToken });
      this.token = response.data.access;
      localStorage.setItem('access_token', this.token);
      // No need to update user data as it's tied to the access token
    },
    logout() {
      this.token = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },
    async tryAutoLogin() {
      const accessToken = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');

      if (accessToken && refreshToken) {
        this.token = accessToken;
        this.refreshToken = refreshToken;

        try {
          const userData = jwtDecode(this.token);
          const userResponse = await api.get(`/users/${userData.user_id}/`);
          this.user = userResponse.data;
          localStorage.setItem('user', JSON.stringify(this.user));
        } catch (error) {
          console.error('Failed to auto-login or fetch user details:', error);
          this.logout(); // Log out if token is invalid or user details cannot be fetched
        }
      }
    },
    async fetchCurrentUser() {
      if (!this.token) return;
      try {
        const userData = jwtDecode(this.token);
        const userResponse = await api.get(`/users/${userData.user_id}/`);
        this.user = userResponse.data;
        localStorage.setItem('user', JSON.stringify(this.user));
      } catch (error) {
        console.error('Failed to fetch user details:', error);
      }
    }
  },
})
