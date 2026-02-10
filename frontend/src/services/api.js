import axios from 'axios';
import setupInterceptors from './axios_interceptor';

const api = axios.create({
  baseURL: '/api', // Using relative URL to be proxied by Nginx
  headers: {
    'Content-Type': 'application/json',
  },
});

setupInterceptors(api);

export default api;
