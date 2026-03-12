import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import ServiceRequestView from '../views/ServiceRequestView.vue'
import ServiceApplicationView from '../views/ServiceApplicationView.vue'
import AdminRolesView from '../views/AdminRolesView.vue'
import ProfileView from '../views/ProfileView.vue'
import ConsentDashboard from '../views/ConsentDashboard.vue'
import LifeEventView from '../views/LifeEventView.vue'

// Repository Module
import ArtifactRegistry from '../modules/repository/pages/ArtifactRegistry.vue'
import ArtifactDetail from '../modules/repository/pages/ArtifactDetail.vue'
import RepositoryExplorer from '../modules/repository/pages/RepositoryExplorer.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/dashboard', name: 'Dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: ProfileView, meta: { requiresAuth: true } },
  { path: '/profile/consent', name: 'ConsentDashboard', component: ConsentDashboard, meta: { requiresAuth: true } },
  { path: '/service-request/:id', name: 'ServiceRequest', component: ServiceRequestView, meta: { requiresAuth: true } },
  { path: '/apply/:service_code', name: 'ServiceApplication', component: ServiceApplicationView, meta: { requiresAuth: true } },
  { path: '/life-event/:id', name: 'LifeEvent', component: LifeEventView, meta: { requiresAuth: true } },
  // Admin Routes
  { path: '/admin/roles', name: 'AdminRoles', component: AdminRolesView, meta: { requiresAuth: true, requiresAdmin: true } },

  // Repository Routes
  { path: '/repository/artifacts', name: 'ArtifactRegistry', component: ArtifactRegistry, meta: { requiresAuth: true } },
  { path: '/repository/artifacts/:id', name: 'ArtifactDetail', component: ArtifactDetail, meta: { requiresAuth: true } },
  { path: '/repository/explore/:path*', name: 'RepositoryExplorer', component: RepositoryExplorer, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  const isAuthenticated = authStore.isAuthenticated;
  const isAdmin = authStore.user?.role === 'admin';

  console.log('--- Navigation Guard ---');
  console.log('To Path:', to.path);
  console.log('Is Authenticated:', isAuthenticated);
  console.log('Auth Store User:', authStore.user);
  console.log('User Role:', authStore.user?.role);
  console.log('Is Admin:', isAdmin);
  console.log('------------------------');

  if (to.meta.requiresAuth && !isAuthenticated) {
    // If the route requires auth and the user is not authenticated, redirect to login
    next({ name: 'Login' });
  } else if (to.meta.requiresAdmin && !isAdmin) {
    // If the route requires admin and the user is not an admin, redirect to dashboard
    next({ name: 'Dashboard' });
  }
  else {
    // Otherwise, proceed
    next();
  }
});

export default router
