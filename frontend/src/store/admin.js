import { defineStore } from 'pinia';
import api from '../services/api';

export const useAdminStore = defineStore('admin', {
    state: () => ({
        users: [],
        usersPagination: {
            count: 0,
            next: null,
            previous: null
        },
        roles: [],
    }),
    actions: {
        async fetchUsers(params = { page: 1, search: '' }) {
            try {
                const response = await api.get('/users/', { params });
                if (response.data.results) {
                    this.users = response.data.results;
                    this.usersPagination = {
                        count: response.data.count,
                        next: response.data.next,
                        previous: response.data.previous
                    };
                } else {
                    this.users = response.data;
                }
            } catch (error) {
                console.error('Failed to fetch users:', error);
            }
        },
        async fetchRoles() {
            try {
                const response = await api.get('/roles/');
                this.roles = response.data;
            } catch (error) {
                console.error('Failed to fetch roles:', error);
            }
        },
        async deleteUser(userId) {
            try {
                await api.delete(`/users/${userId}/`);
                this.users = this.users.filter(u => u.id !== userId);
            } catch (error) {
                console.error('Failed to delete user:', error);
            }
        }
    }
});
