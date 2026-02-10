import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '../../store/auth';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import api from '../../services/api';

// Mock axios
vi.mock('../../services/api', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    defaults: {
      headers: {
        common: {},
      },
    },
  },
}));

// Mock jwt-decode
vi.mock('jwt-decode', () => ({
  jwtDecode: vi.fn((token) => {
    if (token === 'valid_access_token') {
      return { user_id: 1, exp: Date.now() / 1000 + 3600 };
    }
    return { user_id: 1, exp: Date.now() / 1000 - 3600 }; // Expired token
  }),
}));

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
    vi.clearAllMocks();
  });

  it('should have initial state', () => {
    const authStore = useAuthStore();
    expect(authStore.token).toBeNull();
    expect(authStore.refreshToken).toBeNull();
    expect(authStore.user).toBeNull();
    expect(authStore.isAuthenticated).toBe(false);
  });

  it('should log in a user successfully', async () => {
    api.post.mockResolvedValueOnce({
      data: { access: 'valid_access_token', refresh: 'valid_refresh_token' },
    });
    api.get.mockResolvedValueOnce({
      data: { id: 1, username: 'testuser', email: 'test@example.com', role: 'citizen' },
    });

    const authStore = useAuthStore();
    await authStore.login('testuser', 'password');

    expect(authStore.token).toBe('valid_access_token');
    expect(authStore.refreshToken).toBe('valid_refresh_token');
    expect(authStore.user).toEqual({ id: 1, username: 'testuser', email: 'test@example.com', role: 'citizen' });
    expect(authStore.isAuthenticated).toBe(true);
    expect(localStorage.getItem('access_token')).toBe('valid_access_token');
    expect(localStorage.getItem('refresh_token')).toBe('valid_refresh_token');
    expect(localStorage.getItem('user')).toBe(JSON.stringify({ id: 1, username: 'testuser', email: 'test@example.com', role: 'citizen' }));
  });

  it('should handle login failure', async () => {
    api.post.mockRejectedValueOnce(new Error('Login failed'));

    const authStore = useAuthStore();
    await expect(authStore.login('wronguser', 'wrongpass')).rejects.toThrow('Login failed');

    expect(authStore.token).toBeNull();
    expect(authStore.refreshToken).toBeNull();
    expect(authStore.user).toBeNull();
    expect(authStore.isAuthenticated).toBe(false);
    expect(localStorage.getItem('access_token')).toBeNull();
  });

  it('should refresh token successfully', async () => {
    localStorage.setItem('refresh_token', 'old_refresh_token');
    const authStore = useAuthStore();
    authStore.refreshToken = 'old_refresh_token'; // Manually set for the test

    api.post.mockResolvedValueOnce({
      data: { access: 'new_access_token' },
    });

    await authStore.refreshToken();

    expect(authStore.token).toBe('new_access_token');
    expect(localStorage.getItem('access_token')).toBe('new_access_token');
  });

  it('should handle refresh token failure', async () => {
    localStorage.setItem('refresh_token', 'invalid_refresh_token');
    const authStore = useAuthStore();
    authStore.refreshToken = 'invalid_refresh_token';

    api.post.mockRejectedValueOnce(new Error('Refresh failed'));

    await expect(authStore.refreshToken()).rejects.toThrow('Refresh failed');
    expect(authStore.token).toBeNull(); // Token should not be updated
    expect(localStorage.getItem('access_token')).toBeNull();
  });

  it('should log out a user', () => {
    localStorage.setItem('access_token', 'some_token');
    localStorage.setItem('refresh_token', 'some_refresh_token');
    localStorage.setItem('user', JSON.stringify({ username: 'test' }));
    const authStore = useAuthStore();
    authStore.token = 'some_token';
    authStore.refreshToken = 'some_refresh_token';
    authStore.user = { username: 'test' };

    authStore.logout();

    expect(authStore.token).toBeNull();
    expect(authStore.refreshToken).toBeNull();
    expect(authStore.user).toBeNull();
    expect(authStore.isAuthenticated).toBe(false);
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('refresh_token')).toBeNull();
    expect(localStorage.getItem('user')).toBeNull();
  });

  it('should try auto login successfully', () => {
    localStorage.setItem('access_token', 'auto_access_token');
    localStorage.setItem('refresh_token', 'auto_refresh_token');
    localStorage.setItem('user', JSON.stringify({ id: 2, username: 'autouser', role: 'officer' }));

    const authStore = useAuthStore();
    authStore.tryAutoLogin();

    expect(authStore.token).toBe('auto_access_token');
    expect(authStore.refreshToken).toBe('auto_refresh_token');
    expect(authStore.user).toEqual({ id: 2, username: 'autouser', role: 'officer' });
    expect(authStore.isAuthenticated).toBe(true);
  });

  it('should not auto login if tokens are missing', () => {
    localStorage.setItem('access_token', 'auto_access_token');
    // Missing refresh_token and user

    const authStore = useAuthStore();
    authStore.tryAutoLogin();

    expect(authStore.token).toBeNull();
    expect(authStore.refreshToken).toBeNull();
    expect(authStore.user).toBeNull();
    expect(authStore.isAuthenticated).toBe(false);
  });
});
