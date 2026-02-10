import { mount } from '@vue/test-utils';
import { describe, expect, it, vi } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';

// Import components to test
import LoginView from '../../views/LoginView.vue';
import DashboardView from '../../views/DashboardView.vue';
import MdaManager from '../../components/Admin/MdaManager.vue';
import ServiceConfigManager from '../../components/Admin/ServiceConfigManager.vue';
import WorkflowStepManager from '../../components/Admin/WorkflowStepManager.vue';
import FormSchemaBuilder from '../../components/Admin/FormSchemaBuilder.vue';
import ServiceApplicationView from '../../views/ServiceApplicationView.vue';
import AuditLogViewer from '../../components/AuditLogViewer.vue';

// Mock stores and API calls
vi.mock('../../services/api', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: [] })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    put: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve({ data: {} })),
  },
}));

// Mock router push
const mockRouter = {
  push: vi.fn(),
};

const routes = [
  { path: '/login', name: 'Login' },
  { path: '/dashboard', name: 'Dashboard' },
  { path: '/apply/:service_code', name: 'ServiceApplication' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe('Component Tests', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    router.push('/'); // Reset router before each test
    vi.clearAllMocks();
  });

  it('LoginView renders and submits', async () => {
    const wrapper = mount(LoginView, {
      global: {
        plugins: [router],
      },
    });
    expect(wrapper.find('h2').text()).toBe('Login');
    
    await wrapper.find('input[type="text"]').setValue('testuser');
    await wrapper.find('input[type="password"]').setValue('password');
    await wrapper.find('form').trigger('submit.prevent');

    // Expect login action to be called (mocked in auth.test.js)
    // For this test, we just check if the form submission handler is triggered
    // and if the router push is called on success.
    // This requires mocking the auth store's login method.
    const authStore = useAuthStore();
    authStore.login = vi.fn(() => Promise.resolve());
    await wrapper.vm.handleLogin();
    expect(authStore.login).toHaveBeenCalledWith('testuser', 'password');
    expect(mockRouter.push).toHaveBeenCalledWith('/dashboard');
  });

  it('DashboardView renders for citizen', async () => {
    const authStore = useAuthStore();
    authStore.user = { username: 'citizen', role: 'citizen' };
    authStore.isAuthenticated = true;

    const wrapper = mount(DashboardView, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });
    expect(wrapper.text()).toContain('Welcome, citizen!');
    expect(wrapper.text()).toContain('Available Services');
    expect(wrapper.text()).toContain('My Service Requests');
  });

  it('MdaManager renders and adds MDA', async () => {
    const wrapper = mount(MdaManager, {
      global: {
        plugins: [router],
      },
    });
    expect(wrapper.text()).toContain('Manage MDAs');
    
    await wrapper.find('input[id="mda-name"]').setValue('New MDA');
    await wrapper.find('input[id="mda-description"]').setValue('Description for New MDA');
    await wrapper.find('form').trigger('submit.prevent');

    const mdaStore = useMdaStore();
    mdaStore.createMda = vi.fn(() => Promise.resolve());
    await wrapper.vm.handleSubmit();
    expect(mdaStore.createMda).toHaveBeenCalledWith(expect.objectContaining({ name: 'New MDA' }));
  });

  it('ServiceConfigManager renders and opens edit modal', async () => {
    const serviceConfigStore = useServiceConfigStore();
    serviceConfigStore.services = [{ id: 1, service_code: 'SVC1', service_name: 'Service One', mda: 1, config: {} }];
    const mdaStore = useMdaStore();
    mdaStore.mdas = [{ id: 1, name: 'MDA One' }];

    const wrapper = mount(ServiceConfigManager, {
      global: {
        plugins: [router],
        stubs: {
          WorkflowStepManager: true, // Stub out child components
          FormSchemaBuilder: true,
        },
      },
    });
    expect(wrapper.text()).toContain('Manage Service Configurations');
    expect(wrapper.text()).toContain('Service One');

    await wrapper.find('button', { text: 'Edit' }).trigger('click');
    expect(wrapper.vm.showModal).toBe(true);
    expect(wrapper.findComponent({ name: 'WorkflowStepManager' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'FormSchemaBuilder' }).exists()).toBe(true);
  });

  it('WorkflowStepManager renders and adds step', async () => {
    const wrapper = mount(WorkflowStepManager, {
      props: { serviceConfigId: 1 },
      global: {
        plugins: [router],
      },
    });
    expect(wrapper.text()).toContain('Workflow Steps');

    await wrapper.find('input[type="number"]').setValue(1);
    await wrapper.findAll('input[type="text"]')[0].setValue('Step Name');
    await wrapper.findAll('input[type="text"]')[1].setValue('officer');
    await wrapper.findAll('input[type="text"]')[2].setValue('action');
    await wrapper.find('form').trigger('submit.prevent');

    const workflowStepStore = useWorkflowStepStore();
    workflowStepStore.createStep = vi.fn(() => Promise.resolve());
    await wrapper.vm.handleStepSubmit();
    expect(workflowStepStore.createStep).toHaveBeenCalledWith(expect.objectContaining({ step_name: 'Step Name' }));
  });

  it('FormSchemaBuilder renders and adds field', async () => {
    const wrapper = mount(FormSchemaBuilder, {
      props: {
        modelValue: {
          rules: {
            schema: {
              properties: {},
              required: [],
            },
          },
        },
      },
      global: {
        plugins: [router],
      },
    });
    expect(wrapper.text()).toContain('Form Schema Builder');

    await wrapper.findAll('input[type="text"]')[0].setValue('field_name');
    await wrapper.findAll('input[type="text"]')[1].setValue('Field Label');
    await wrapper.find('select').setValue('string');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.emitted()['update:modelValue']).toBeTruthy();
    expect(wrapper.emitted()['update:modelValue'][0][0].rules.schema.properties).toHaveProperty('field_name');
  });

  it('ServiceApplicationView renders dynamic form and submits', async () => {
    const serviceConfigStore = useServiceConfigStore();
    serviceConfigStore.services = [{
      id: 1,
      service_code: 'TEST_SVC',
      service_name: 'Test Service',
      mda: 1,
      config: {
        rules: {
          schema: {
            properties: {
              name: { type: 'string', title: 'Your Name' },
              age: { type: 'number', title: 'Your Age' },
            },
            required: ['name'],
          },
        },
      },
    }];

    const wrapper = mount(ServiceApplicationView, {
      global: {
        plugins: [router],
      },
      props: {
        service_code: 'TEST_SVC', // Pass service_code as prop for testing
      },
      // Mock route params
      mocks: {
        $route: {
          params: {
            service_code: 'TEST_SVC',
          },
        },
      },
    });

    // Wait for service data to be fetched and form to render
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick(); // Wait for watch to trigger

    expect(wrapper.text()).toContain('Test Service');
    expect(wrapper.find('label[for="name"]').text()).toBe('Your Name');
    expect(wrapper.find('label[for="age"]').text()).toBe('Your Age');

    await wrapper.find('input[id="name"]').setValue('John Doe');
    await wrapper.find('input[id="age"]').setValue(30);
    await wrapper.find('form').trigger('submit.prevent');

    const citizenStore = useCitizenStore();
    citizenStore.submitRequest = vi.fn(() => Promise.resolve());
    await wrapper.vm.handleSubmit();
    expect(citizenStore.submitRequest).toHaveBeenCalledWith('TEST_SVC', { name: 'John Doe', age: 30 });
    expect(mockRouter.push).toHaveBeenCalledWith('/dashboard');
  });

  it('AuditLogViewer renders logs', async () => {
    const auditLogStore = useAuditLogStore();
    auditLogStore.auditLogs = [
      { id: 1, timestamp: '2025-12-27T10:00:00Z', service_request: { request_id: 'req-abc' }, actor: { username: 'citizen' }, action: 'CREATED', details: 'Request created' },
    ];

    const wrapper = mount(AuditLogViewer, {
      global: {
        plugins: [router],
      },
    });
    expect(wrapper.text()).toContain('Audit Log');
    expect(wrapper.text()).toContain('req-abc');
    expect(wrapper.text()).toContain('citizen');
    expect(wrapper.text()).toContain('CREATED');
  });
});
