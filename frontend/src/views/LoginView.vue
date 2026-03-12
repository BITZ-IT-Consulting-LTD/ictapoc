<template>
  <main class="login-page">
    <!-- Skip Link for Accessibility -->
    <a href="#login-form" class="skip-link">Skip to login form</a>

    <!-- Decorative Background -->
    <div class="login-page__background">
      <div class="login-page__blob login-page__blob--primary"></div>
      <div class="login-page__blob login-page__blob--success"></div>
    </div>

    <div class="login-container">
      <div class="login-card">
        <!-- Left Panel: Branding -->
        <section class="login-brand">
          <div class="login-brand__pattern"></div>

          <div class="login-brand__content">
            <header class="login-brand__header">
              <div class="login-brand__logo">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <h1 class="login-brand__title">Huduma Digital</h1>
                <p class="login-brand__subtitle">Republic of Kenya</p>
              </div>
            </header>

            <h2 class="login-brand__hero">Secure Access to Government Services</h2>
            <p class="login-brand__description">
              Access over 5,000 government services securely using your Maisha Digital ID or Government PKI credentials.
              One platform for all your civic needs.
            </p>

            <div class="login-features">
              <div class="login-feature">
                <div class="login-feature__icon login-feature__icon--success">
                  <i class="bi bi-shield-lock-fill"></i>
                </div>
                <div>
                  <div class="login-feature__title">Verified Identity</div>
                  <div class="login-feature__desc">Biometric & PKI Security</div>
                </div>
              </div>

              <div class="login-feature">
                <div class="login-feature__icon login-feature__icon--info">
                  <i class="bi bi-lightning-charge-fill"></i>
                </div>
                <div>
                  <div class="login-feature__title">Single Sign-On</div>
                  <div class="login-feature__desc">One credential for all MDAs</div>
                </div>
              </div>

              <div class="login-feature">
                <div class="login-feature__icon login-feature__icon--warning">
                  <i class="bi bi-clock-history"></i>
                </div>
                <div>
                  <div class="login-feature__title">24/7 Availability</div>
                  <div class="login-feature__desc">Access services anytime</div>
                </div>
              </div>
            </div>
          </div>

          <footer class="login-brand__footer">
            © 2026 ICT Authority • National GOK Enterprise Platform
          </footer>
        </section>

        <!-- Right Panel: Authentication -->
        <section class="login-auth" id="login-form">
          <!-- Developer Toggle -->
          <button @click="showLegacy = !showLegacy" class="dev-toggle" aria-label="Toggle developer login"
            title="Toggle Developer Login">
            <i class="bi bi-terminal"></i>
          </button>

          <!-- SSO/PKI Login Options -->
          <div v-if="!showLegacy" class="auth-options">
            <header class="auth-header">
              <h3 class="auth-title">Portal Gateway</h3>
              <p class="auth-subtitle">Select your secure authentication method</p>
            </header>

            <div class="auth-buttons">
              <!-- SSO Login -->
              <button @click="startSSOFlow" class="auth-button auth-button--primary"
                aria-label="Login with Maisha Digital ID">
                <div class="auth-button__content">
                  <div class="auth-button__icon auth-button__icon--primary">
                    <i class="bi bi-person-badge-fill"></i>
                  </div>
                  <div class="auth-button__text">
                    <div class="auth-button__title">Maisha Digital ID</div>
                    <div class="auth-button__subtitle">Citizen & Resident SSO</div>
                  </div>
                </div>
                <i class="bi bi-arrow-right auth-button__arrow"></i>
              </button>

              <!-- PKI Login -->
              <button @click="startPKIFlow" class="auth-button auth-button--secondary"
                aria-label="Login with Government PKI Smart Card">
                <div class="auth-button__content">
                  <div class="auth-button__icon auth-button__icon--secondary">
                    <i class="bi bi-cpu-fill"></i>
                  </div>
                  <div class="auth-button__text">
                    <div class="auth-button__title">Gov PKI / Smart Card</div>
                    <div class="auth-button__subtitle">Staff & Officer Token</div>
                  </div>
                </div>
                <i class="bi bi-arrow-right auth-button__arrow"></i>
              </button>
            </div>

            <!-- System Status -->
            <div class="system-status">
              <span class="badge badge--success">
                <i class="bi bi-check-circle-fill"></i> System Operational
              </span>
              <span class="system-status__separator">|</span>
              <button class="button button--ghost button--small">Registry Support</button>
            </div>

            <!-- Quick Access -->
            <div class="quick-access">
              <p class="quick-access__title">
                <i class="bi bi-lightning-fill"></i> Architectural Pilot Quick Access
              </p>
              <div class="quick-access__grid">
                <button @click="quickLogin('global.officer')" class="quick-button">Global Officer</button>
                <button @click="quickLogin('global.supervisor')" class="quick-button">Global Supervisor</button>
                <button @click="quickLogin('moh.officer')" class="quick-button">MOH Officer</button>
                <button @click="quickLogin('moe.officer')" class="quick-button">MOE Officer</button>
                <button @click="quickLogin('maggy1')" class="quick-button quick-button--full">Mock Citizen
                  (Maggy)</button>
              </div>
            </div>
          </div>

          <!-- Legacy Login Form -->
          <div v-else class="legacy-login">
            <header class="legacy-header">
              <h3 class="auth-title">Authenticator</h3>
              <button @click="showLegacy = false" class="button button--ghost button--small">
                <i class="bi bi-arrow-left"></i> Use SSO
              </button>
            </header>

            <form @submit.prevent="handleLegacyLogin" class="form">
              <div class="form__group">
                <label for="username" class="form__label form__label--required">Identity Identifier</label>
                <input id="username" type="text" v-model="username" class="form__input" required aria-required="true"
                  placeholder="UID / Registered Email">
              </div>

              <div class="form__group">
                <label for="password" class="form__label form__label--required">Security Key</label>
                <input id="password" type="password" v-model="password" class="form__input" required
                  aria-required="true" placeholder="••••••••">
              </div>

              <div v-if="errorMessage" class="status-message status-message--error" role="alert">
                <i class="bi bi-shield-exclamation" aria-hidden="true"></i>
                <span>{{ errorMessage }}</span>
              </div>

              <button type="submit" class="button button--primary w-full">
                Establish Session
              </button>

              <div class="text-center mt-4">
                <router-link to="/register" class="link link--primary">
                  Require System Credentials? <span class="link--underline">Register Account</span>
                </router-link>
              </div>
            </form>
          </div>
        </section>
      </div>
    </div>

    <!-- SSO Modal -->
    <BaseModal v-model:show="ssoModalOpen" title="Maisha Namba Identity Federation"
      subtitle="Federated authentication for GOK Digital Services" icon="bi-person-badge" size="md">
      <div class="modal-content">
        <div class="identity-list">
          <button @click="simulateSSOLogin('maggy1', 'citizen')" class="identity-card">
            <div class="identity-card__avatar identity-card__avatar--success">M</div>
            <div class="identity-card__info">
              <div class="identity-card__name">Maggy One</div>
              <div class="identity-card__meta">Verified Citizen • ID 555555</div>
            </div>
            <i class="bi bi-chevron-right identity-card__arrow"></i>
          </button>

          <button @click="simulateSSOLogin('citizen1', 'citizen')" class="identity-card">
            <div class="identity-card__avatar identity-card__avatar--success">C</div>
            <div class="identity-card__info">
              <div class="identity-card__name">Test Citizen</div>
              <div class="identity-card__meta">Registry Sample • ID 100</div>
            </div>
            <i class="bi bi-chevron-right identity-card__arrow"></i>
          </button>

          <div class="identity-divider">
            <span>Institutional Staff</span>
          </div>

          <button @click="simulateSSOLogin('officer1', 'officer')" class="identity-card">
            <div class="identity-card__avatar identity-card__avatar--info">O</div>
            <div class="identity-card__info">
              <div class="identity-card__name">Officer One</div>
              <div class="identity-card__meta">Civil Registration Specialist</div>
            </div>
            <i class="bi bi-chevron-right identity-card__arrow"></i>
          </button>
        </div>
      </div>
      <template #footer>
        <span class="modal-footer-text">
          <i class="bi bi-lock-fill"></i> Secure OpenID Connect Handshake Active
        </span>
      </template>
    </BaseModal>

    <!-- PKI Modal -->
    <BaseModal v-model:show="pkiModalOpen"
      :title="pkiPhase === 'scanning' ? 'Communicating with Smart Card...' : 'Cryptographic Proof Verified'"
      subtitle="Validating institutional private key residency" icon="bi-shield-shaded" size="sm">
      <div class="pki-container">
        <!-- Scanning Phase -->
        <div v-if="pkiPhase === 'scanning'" class="pki-scanning">
          <div class="pki-scanner">
            <div class="pki-scanner__ping"></div>
            <div class="pki-scanner__icon">
              <i class="bi bi-cpu"></i>
            </div>
          </div>
          <p class="pki-status">Reading Chip Data...</p>
        </div>

        <!-- PIN Phase -->
        <div v-if="pkiPhase === 'pin'" class="pki-pin">
          <div class="pki-success">
            <i class="bi bi-patch-check-fill"></i>
          </div>
          <p class="pki-identity">
            Identity: Officer One (MOI)<br>
            Issuer: GOK Root CA 01
          </p>

          <div class="form__group">
            <label for="pin" class="form__label text-center">Secure PIN</label>
            <input id="pin" type="password" placeholder="••••" class="form__input text-center pin-input" autofocus
              aria-label="Enter your secure PIN">
          </div>

          <button @click="verifyPinAndLogin" class="button button--primary w-full">
            Unlock & Authenticate
          </button>
        </div>
      </div>
    </BaseModal>
  </main>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '../store/auth'
  import BaseModal from '../components/Common/BaseModal.vue'

  const router = useRouter()
  const authStore = useAuthStore()

  // State
  const showLegacy = ref(false)
  const username = ref('')
  const password = ref('')
  const errorMessage = ref('')

  // Simulation State
  const ssoModalOpen = ref(false)
  const pkiModalOpen = ref(false)
  const pkiPhase = ref('scanning')

  // SSO Logic
  const startSSOFlow = () => {
    window.setTimeout(() => {
      ssoModalOpen.value = true;
    }, 300);
  }

  const simulateSSOLogin = async (simUser, role) => {
    ssoModalOpen.value = false;
    await quickLogin(simUser);
  }

  const quickLogin = async (usr) => {
    const pwd = 'Starten1@';
    await performLogin(usr, pwd);
  }

  // PKI Logic
  const startPKIFlow = () => {
    pkiModalOpen.value = true;
    pkiPhase.value = 'scanning';

    window.setTimeout(() => {
      pkiPhase.value = 'pin';
    }, 2000);
  }

  const verifyPinAndLogin = async () => {
    pkiPhase.value = 'scanning';
    pkiModalOpen.value = false;
    await performLogin('officer1', 'Starten1@');
  }

  // Core Auth
  const performLogin = async (usr, pwd) => {
    errorMessage.value = '';
    try {
      await authStore.login(usr, pwd);
      router.push('/dashboard');
    } catch (error) {
      if (error.response?.status === 401) {
        errorMessage.value = 'Authentication Failed. Please try again.';
      } else {
        errorMessage.value = 'System Error. Check connection.';
      }
      showLegacy.value = true;
    }
  }

  const handleLegacyLogin = async () => {
    await performLogin(username.value, password.value);
  }
</script>

<style scoped>

  /* Login Page Layout */
  .login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-page);
    position: relative;
    overflow: hidden;
    padding: 2rem 1rem;
  }

  .login-page__background {
    position: absolute;
    inset: 0;
    overflow: hidden;
    z-index: 0;
  }

  .login-page__blob {
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.3;
    animation: float 20s ease-in-out infinite;
  }

  .login-page__blob--primary {
    top: -10%;
    left: -10%;
    background: var(--primary);
  }

  .login-page__blob--success {
    bottom: -10%;
    right: -10%;
    background: var(--success);
    animation-delay: 10s;
  }

  @keyframes float {

    0%,
    100% {
      transform: translate(0, 0) scale(1);
    }

    33% {
      transform: translate(30px, -50px) scale(1.1);
    }

    66% {
      transform: translate(-20px, 20px) scale(0.9);
    }
  }

  /* Login Container */
  .login-container {
    width: 100%;
    max-width: 1100px;
    z-index: 10;
  }

  .login-card {
    background: var(--bg-card);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-xl);
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr;
    animation: slideUp 0.6s ease-out;
  }

  @media (min-width: 768px) {
    .login-card {
      grid-template-columns: 1fr 1fr;
    }
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Brand Panel */
  .login-brand {
    background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-light) 100%);
    color: var(--text-on-dark);
    padding: 3rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    min-height: 600px;
  }

  .login-brand__pattern {
    position: absolute;
    inset: 0;
    background-image:
      radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
      radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
    opacity: 0.5;
  }

  .login-brand__content {
    position: relative;
    z-index: 1;
  }

  .login-brand__header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 3rem;
  }

  .login-brand__logo {
    width: 3.5rem;
    height: 3.5rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .login-brand__logo svg {
    width: 2rem;
    height: 2rem;
    color: white;
  }

  .login-brand__title {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
  }

  .login-brand__subtitle {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.8;
    margin: 0;
  }

  .login-brand__hero {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
  }

  .login-brand__description {
    font-size: 1rem;
    line-height: 1.7;
    opacity: 0.9;
    margin-bottom: 2.5rem;
  }

  .login-features {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .login-feature {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: var(--radius-md);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
  }

  .login-feature__icon {
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
  }

  .login-feature__icon--success {
    background: var(--success-soft);
    color: var(--success);
  }

  .login-feature__icon--info {
    background: var(--info-soft);
    color: var(--info);
  }

  .login-feature__icon--warning {
    background: var(--warning-soft);
    color: var(--warning);
  }

  .login-feature__title {
    font-weight: 700;
    font-size: 0.9375rem;
    margin-bottom: 0.25rem;
  }

  .login-feature__desc {
    font-size: 0.8125rem;
    opacity: 0.8;
  }

  .login-brand__footer {
    font-size: 0.75rem;
    opacity: 0.7;
    text-align: center;
    position: relative;
    z-index: 1;
  }

  /* Auth Panel */
  .login-auth {
    padding: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background: white;
  }

  .dev-toggle {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: var(--bg-hover);
    color: var(--text-muted);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
  }

  .dev-toggle:hover {
    background: var(--bg-active);
    color: var(--text-main);
  }

  .auth-options,
  .legacy-login {
    width: 100%;
    max-width: 400px;
  }

  .auth-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .auth-title {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--text-main);
    margin-bottom: 0.5rem;
  }

  .auth-subtitle {
    color: var(--text-muted);
    font-size: 0.9375rem;
  }

  .auth-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .auth-button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    border: 2px solid var(--border-color);
    background: white;
    cursor: pointer;
    transition: var(--transition);
    text-align: left;
    width: 100%;
  }

  .auth-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }

  .auth-button--primary:hover {
    border-color: var(--primary);
    background: var(--primary-soft);
  }

  .auth-button--secondary:hover {
    border-color: var(--secondary);
    background: var(--bg-hover);
  }

  .auth-button__content {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .auth-button__icon {
    width: 3rem;
    height: 3rem;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  .auth-button__icon--primary {
    background: var(--primary-soft);
    color: var(--primary);
  }

  .auth-button__icon--secondary {
    background: var(--bg-hover);
    color: var(--secondary);
  }

  .auth-button__title {
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 0.25rem;
  }

  .auth-button__subtitle {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.05em;
  }

  .auth-button__arrow {
    color: var(--border-color);
    font-size: 1.25rem;
    transition: var(--transition);
  }

  .auth-button:hover .auth-button__arrow {
    color: var(--primary);
    transform: translateX(4px);
  }

  /* System Status */
  .system-status {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem 0;
    border-top: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 1.5rem;
  }

  .system-status__separator {
    color: var(--border-color);
  }

  /* Quick Access */
  .quick-access {
    padding-top: 1.5rem;
  }

  .quick-access__title {
    font-size: 0.625rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .quick-access__grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }

  .quick-button {
    padding: 0.75rem 1rem;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
    background: white;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-main);
    cursor: pointer;
    transition: var(--transition);
  }

  .quick-button:hover {
    background: var(--bg-hover);
    border-color: var(--primary);
    color: var(--primary);
  }

  .quick-button--full {
    grid-column: span 2;
  }

  /* Legacy Login */
  .legacy-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
  }

  /* Identity Cards */
  .identity-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .identity-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background: white;
    cursor: pointer;
    transition: var(--transition);
    text-align: left;
    width: 100%;
  }

  .identity-card:hover {
    background: var(--bg-hover);
    border-color: var(--primary);
  }

  .identity-card__avatar {
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.25rem;
    flex-shrink: 0;
  }

  .identity-card__avatar--success {
    background: var(--success-soft);
    color: var(--success-text);
  }

  .identity-card__avatar--info {
    background: var(--info-soft);
    color: var(--info-text);
  }

  .identity-card__info {
    flex: 1;
  }

  .identity-card__name {
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 0.25rem;
  }

  .identity-card__meta {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 600;
  }

  .identity-card__arrow {
    color: var(--border-color);
    transition: var(--transition);
  }

  .identity-card:hover .identity-card__arrow {
    color: var(--primary);
    transform: translateX(4px);
  }

  .identity-divider {
    text-align: center;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 1rem 0;
    position: relative;
  }

  .identity-divider::before,
  .identity-divider::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 40%;
    height: 1px;
    background: var(--border-color);
  }

  .identity-divider::before {
    left: 0;
  }

  .identity-divider::after {
    right: 0;
  }

  /* PKI Components */
  .pki-container {
    padding: 2rem 0;
    text-align: center;
  }

  .pki-scanning,
  .pki-pin {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .pki-scanner {
    width: 5rem;
    height: 5rem;
    position: relative;
    margin-bottom: 1.5rem;
  }

  .pki-scanner__ping {
    position: absolute;
    inset: 0;
    border: 4px solid var(--primary);
    border-radius: 50%;
    opacity: 0.25;
    animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
  }

  @keyframes ping {

    75%,
    100% {
      transform: scale(2);
      opacity: 0;
    }
  }

  .pki-scanner__icon {
    position: absolute;
    inset: 0;
    background: var(--primary-soft);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: var(--primary);
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }

  .pki-status {
    font-size: 0.875rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
  }

  .pki-success {
    width: 4rem;
    height: 4rem;
    background: var(--success-soft);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: var(--success);
    margin-bottom: 1rem;
  }

  .pki-identity {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
    line-height: 1.6;
  }

  .pin-input {
    font-size: 2rem;
    letter-spacing: 1em;
    font-family: 'Courier New', monospace;
    font-weight: 700;
  }

  /* Modal Footer */
  .modal-footer-text {
    display: block;
    width: 100%;
    text-align: center;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
  }

  /* Utilities */
  .link {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-muted);
    text-decoration: none;
    transition: var(--transition);
  }

  .link--primary {
    color: var(--text-muted);
  }

  .link--primary:hover {
    color: var(--primary);
  }

  .link--underline {
    color: var(--primary);
    text-decoration: underline;
  }

  .text-center {
    text-align: center;
  }

  .w-full {
    width: 100%;
  }

  .mt-4 {
    margin-top: 1rem;
  }
</style>
