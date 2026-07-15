<template>
  <div class="dpi-page animate-fade-in">
    <header class="dpi-hero">
      <div class="dpi-hero__content">
        <span class="dpi-eyebrow"><i class="bi bi-grid-1x2-fill"></i> Digital Public Infrastructure</span>
        <h3>Kenya DPI Exchange</h3>
        <p>
          Trusted national rails connecting people, government agencies, and reusable public services through
          secure, standards-based exchange.
        </p>
        <div class="dpi-standards">
          <span>GEA aligned</span>
          <span>X-Road exchange</span>
          <span>NPKI secured</span>
          <span>Consent aware</span>
        </div>
      </div>
      <div class="dpi-hero__status">
        <span class="dpi-live-dot"></span>
        <div>
          <strong>National exchange operational</strong>
          <small>KeSEL and Huduma Bridge connected</small>
        </div>
      </div>
    </header>

    <section class="dpi-metrics" aria-label="DPI exchange status">
      <article>
        <span class="dpi-metric__icon dpi-tone--identity"><i class="bi bi-fingerprint"></i></span>
        <div><strong>{{ dpiRails.length }}</strong><small>Shared DPI rails</small></div>
      </article>
      <article>
        <span class="dpi-metric__icon dpi-tone--exchange"><i class="bi bi-diagram-3-fill"></i></span>
        <div><strong>{{ registry.length }}</strong><small>Reusable building blocks</small></div>
      </article>
      <article>
        <span class="dpi-metric__icon dpi-tone--payments"><i class="bi bi-shield-check"></i></span>
        <div><strong>100%</strong><small>Trusted connections</small></div>
      </article>
      <article>
        <span class="dpi-metric__icon dpi-tone--shared"><i class="bi bi-activity"></i></span>
        <div><strong>{{ onlineServices }}</strong><small>Services online</small></div>
      </article>
    </section>

    <section class="dpi-map" aria-labelledby="dpi-map-title">
      <div class="dpi-section-heading">
        <div>
          <span class="dpi-section-kicker">National exchange topology</span>
          <h4 id="dpi-map-title">Shared rails, not another silo</h4>
        </div>
        <span class="dpi-map__health"><i class="bi bi-lock-fill"></i> Trust envelope active</span>
      </div>

      <div class="dpi-topology">
        <div class="dpi-participants">
          <span class="dpi-column-label">Service channels</span>
          <article><i class="bi bi-person-fill"></i><span>Citizen & Business<small>Portals · Mobile · USSD</small></span></article>
          <article><i class="bi bi-building-fill"></i><span>Government Agencies<small>MDA systems · Counties</small></span></article>
          <article><i class="bi bi-person-workspace"></i><span>Assisted Access<small>Officers · Huduma centres</small></span></article>
        </div>

        <div class="dpi-flow" aria-hidden="true"><span></span><i class="bi bi-arrow-right"></i></div>

        <article class="dpi-exchange-hub">
          <div class="dpi-exchange-hub__rings">
            <span><i class="bi bi-share-fill"></i></span>
          </div>
          <span class="dpi-column-label">Interoperability layer</span>
          <h5>Huduma Bridge</h5>
          <p>Kenya Secure Exchange Layer</p>
          <div class="dpi-exchange-hub__tags">
            <span>API Gateway</span><span>Routing</span><span>Policy</span><span>Observability</span>
          </div>
        </article>

        <div class="dpi-flow" aria-hidden="true"><span></span><i class="bi bi-arrow-right"></i></div>

        <div class="dpi-rails">
          <span class="dpi-column-label">Foundational DPI rails</span>
          <button
            v-for="rail in dpiRails"
            :key="rail.id"
            type="button"
            class="dpi-rail"
            :class="[`dpi-rail--${rail.id}`, { 'dpi-rail--active': activeRail === rail.id }]"
            @click="toggleRail(rail.id)"
          >
            <span class="dpi-rail__icon"><i :class="rail.icon"></i></span>
            <span class="dpi-rail__body">
              <strong>{{ rail.name }}</strong>
              <small>{{ rail.description }}</small>
            </span>
            <span class="dpi-rail__count">{{ railCount(rail.id) }}</span>
          </button>
        </div>
      </div>

      <footer class="dpi-trust-envelope">
        <span><i class="bi bi-key-fill"></i> National PKI</span>
        <span><i class="bi bi-person-check-fill"></i> Federated identity</span>
        <span><i class="bi bi-check2-square"></i> Consent manager</span>
        <span><i class="bi bi-journal-check"></i> Immutable audit</span>
        <span><i class="bi bi-shield-lock-fill"></i> mTLS exchange</span>
      </footer>
    </section>

    <section class="dpi-catalogue" aria-labelledby="building-blocks-title">
      <div class="dpi-section-heading dpi-section-heading--catalogue">
        <div>
          <span class="dpi-section-kicker">Reusable public infrastructure</span>
          <h4 id="building-blocks-title">Connected building blocks</h4>
        </div>
        <div class="dpi-search">
          <i class="bi bi-search"></i>
          <input v-model="searchQuery" type="search" placeholder="Search building blocks..." aria-label="Search DPI building blocks">
        </div>
      </div>

      <div class="dpi-filters" aria-label="Filter by DPI rail">
        <button type="button" :class="{ active: activeRail === 'all' }" @click="activeRail = 'all'">All rails</button>
        <button
          v-for="rail in dpiRails"
          :key="`filter-${rail.id}`"
          type="button"
          :class="[{ active: activeRail === rail.id }, `dpi-filter--${rail.id}`]"
          @click="activeRail = rail.id"
        >
          <i :class="rail.icon"></i> {{ rail.shortName }}
        </button>
      </div>

      <div v-if="filteredRegistry.length" class="dpi-building-grid">
        <article v-for="service in filteredRegistry" :key="service.id" class="dpi-building-block">
          <header>
            <span :class="`dpi-building-block__icon dpi-tone--${service.rail}`"><i :class="railById(service.rail).icon"></i></span>
            <div class="dpi-building-block__title">
              <span>{{ railById(service.rail).name }}</span>
              <h5>{{ service.name }}</h5>
            </div>
            <span class="dpi-online"><i></i>{{ service.status }}</span>
          </header>

          <p>{{ service.description }}</p>

          <div class="dpi-endpoint">
            <span>{{ service.details.Protocol }}</span>
            <code>{{ service.url }}</code>
            <button type="button" :aria-label="`Copy ${service.name} endpoint`" @click="copyToClipboard(service)">
              <i :class="copiedId === service.id ? 'bi bi-check2' : 'bi bi-copy'"></i>
            </button>
          </div>

          <footer>
            <span><small>Authentication</small>{{ service.details.Auth }}</span>
            <span><small>Typical latency</small>{{ service.details.Latency }}</span>
            <details>
              <summary>Payload schema <i class="bi bi-chevron-down"></i></summary>
              <pre>{{ JSON.stringify(service.payload, null, 2) }}</pre>
            </details>
          </footer>
        </article>
      </div>

      <div v-else class="dpi-empty-state">
        <i class="bi bi-search"></i>
        <strong>No building blocks match this view</strong>
        <button type="button" @click="clearFilters">Show all DPI rails</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  activeTab: {
    type: String,
    default: 'API Gateway'
  }
});

const searchQuery = ref('');
const activeRail = ref('all');
const copiedId = ref(null);

const railForAdminView = tab => ({
  'Government Payments': 'payments',
  'Revenue & Reconciliation': 'payments',
  'Huduma Bridge': 'exchange',
  'API Gateway': 'all'
}[tab] || 'all');

watch(() => props.activeTab, tab => {
  activeRail.value = railForAdminView(tab);
  searchQuery.value = '';
}, { immediate: true });

const dpiRails = [
  {
    id: 'identity',
    shortName: 'Identity',
    name: 'Digital Identity & Trust',
    description: 'Maisha identity, authentication and consent',
    icon: 'bi bi-fingerprint'
  },
  {
    id: 'exchange',
    shortName: 'Data exchange',
    name: 'Secure Data Exchange',
    description: 'Authoritative registries through KeSEL',
    icon: 'bi bi-arrow-left-right'
  },
  {
    id: 'payments',
    shortName: 'Payments',
    name: 'Digital Payments',
    description: 'Government collections and settlement',
    icon: 'bi bi-credit-card-2-front-fill'
  },
  {
    id: 'shared',
    shortName: 'Shared services',
    name: 'Shared Service Building Blocks',
    description: 'Notifications, documents and platform hooks',
    icon: 'bi bi-boxes'
  },
  {
    id: 'orchestration',
    shortName: 'Orchestration',
    name: 'Service Orchestration',
    description: 'Workflows, schemas and dynamic forms',
    icon: 'bi bi-bezier2'
  }
];

const registry = ref([
  {
    id: 'huduma_oidc',
    rail: 'identity',
    name: 'Huduma Identity Federation',
    status: 'online',
    description: 'Single sign-on and federated identity for citizens, residents, officers, and government systems.',
    url: 'HUDUMA_BRIDGE/auth/oidc',
    details: { Protocol: 'OAuth 2.0 / OIDC', Auth: 'Bearer JWT', Latency: '~210ms' },
    payload: { client_id: 'ICTA_POC_OIDC', grant_type: 'authorization_code', scope: 'openid profile citizen_id' }
  },
  {
    id: 'consent_authorize',
    rail: 'identity',
    name: 'Citizen Consent Manager',
    status: 'online',
    description: 'Captures purpose-bound authorization before personal data moves between government services.',
    url: 'HUDUMA_BRIDGE/consent/authorize',
    details: { Protocol: 'REST / JSON', Auth: 'NPKI + JWT', Latency: '~90ms' },
    payload: { citizen_id: 'STRING', purpose_code: 'SERVICE_PURPOSE', data_scopes: ['IDENTITY'], expires_at: 'ISO_8601' }
  },
  {
    id: 'iprs_verify',
    rail: 'exchange',
    name: 'Population Registry Verification',
    status: 'online',
    description: 'Verifies identity attributes against IPRS and Maisha authoritative person records.',
    url: 'KESEL_BRIDGE/IPRS/verify',
    details: { Protocol: 'JSON-RPC', Auth: 'KeSEL token', Latency: '~450ms' },
    payload: { id_number: 'STRING', verification_type: 'BIO_MATCH', request_origin: 'icta-poc' }
  },
  {
    id: 'kra_pin_verify',
    rail: 'exchange',
    name: 'Taxpayer Registry Validation',
    status: 'online',
    description: 'Validates taxpayer identity, PIN status, and compliance through the KRA authoritative registry.',
    url: 'KESEL_BRIDGE/KRA/verify_pin',
    details: { Protocol: 'SOAP / WSDL', Auth: 'mTLS', Latency: '~300ms' },
    payload: { pin: 'A000000000Z', check_compliance: true }
  },
  {
    id: 'gpa_collect',
    rail: 'payments',
    name: 'Government Payment Aggregator',
    status: 'online',
    description: 'Initiates government payments across mobile money, banks, and cards using a common payment reference.',
    url: 'HUDUMA_BRIDGE/GPA/payments/initiate',
    details: { Protocol: 'REST / ISO 20022', Auth: 'mTLS + NPKI', Latency: '~180ms' },
    payload: { service_code: 'STRING', amount: 0, currency: 'KES', payer_reference: 'STRING', callback_url: 'HTTPS_URL' }
  },
  {
    id: 'gpa_status',
    rail: 'payments',
    name: 'Payment Status & Reconciliation',
    status: 'online',
    description: 'Confirms settlement and exposes an auditable transaction trail for agencies and the National Treasury.',
    url: 'HUDUMA_BRIDGE/GPA/payments/status',
    details: { Protocol: 'REST / ISO 20022', Auth: 'mTLS + NPKI', Latency: '~120ms' },
    payload: { payment_reference: 'GPA-REFERENCE', include_settlement: true }
  },
  {
    id: 'workflow_orchestrate',
    rail: 'orchestration',
    name: 'Government Workflow Engine',
    status: 'online',
    description: 'Executes reusable BPMN-aligned service journeys, decisions, human tasks, and automated registry calls.',
    url: 'HUDUMA_BRIDGE/orchestration/workflows/execute',
    details: { Protocol: 'REST / BPMN 2.0', Auth: 'NPKI + JWT', Latency: '~80ms' },
    payload: { service_code: 'STRING', workflow_version: 'ACTIVE', applicant_reference: 'STRING', input: {} }
  },
  {
    id: 'schema_forms',
    rail: 'orchestration',
    name: 'Schema & Dynamic Forms Registry',
    status: 'online',
    description: 'Publishes versioned JSON schemas that render consistent government forms across every service channel.',
    url: 'HUDUMA_BRIDGE/orchestration/schemas/resolve',
    details: { Protocol: 'REST / JSON Schema', Auth: 'Bearer JWT', Latency: '~35ms' },
    payload: { service_code: 'STRING', schema_version: 'LATEST', channel: 'WEB' }
  },
  {
    id: 'huduma_notify',
    rail: 'shared',
    name: 'Government Notification Service',
    status: 'online',
    description: 'Reusable SMS, email, and push notifications for every government service journey.',
    url: 'HUDUMA_BRIDGE/notify/send',
    details: { Protocol: 'REST / JSON', Auth: 'API key', Latency: '~50ms' },
    payload: { to: 'CITIZEN_ID', channels: ['SMS', 'PUSH'], template_id: 'REQ_APPROVED_01', variables: { status: 'STRING' } }
  },
  {
    id: 'edrms_archive',
    rail: 'shared',
    name: 'Government Document Archive',
    status: 'online',
    description: 'Stores digitally signed government records and returns a durable archival reference.',
    url: 'KESEL_BRIDGE/EDRMS/archive',
    details: { Protocol: 'REST / HTTPS', Auth: 'System-to-system', Latency: '~120ms' },
    payload: { document_type: 'CERTIFICATE', metadata: { request_id: 'STRING', issued_by: 'MDA_CODE' }, content_base64: 'BASE64' }
  },
  {
    id: 'internal_profile_update',
    rail: 'shared',
    name: 'Verified Profile Update',
    status: 'online',
    description: 'Applies verified registry attributes to a citizen profile after a successful workflow decision.',
    url: 'internal://update_profile',
    details: { Protocol: 'Native hook', Auth: 'Internal only', Latency: '<5ms' },
    payload: { fields: ['id_number', 'phone_number'], force_update: true }
  }
]);

const onlineServices = computed(() => registry.value.filter(service => service.status === 'online').length);

const filteredRegistry = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return registry.value.filter(service => {
    const matchesRail = activeRail.value === 'all' || service.rail === activeRail.value;
    const matchesQuery = !query || [service.name, service.url, service.description, service.rail]
      .some(value => value.toLowerCase().includes(query));
    return matchesRail && matchesQuery;
  });
});

const railById = id => dpiRails.find(rail => rail.id === id) || dpiRails[0];
const railCount = id => registry.value.filter(service => service.rail === id).length;

const toggleRail = id => {
  activeRail.value = activeRail.value === id ? 'all' : id;
};

const clearFilters = () => {
  activeRail.value = 'all';
  searchQuery.value = '';
};

const copyToClipboard = async service => {
  try {
    await navigator.clipboard.writeText(service.url);
    copiedId.value = service.id;
    window.setTimeout(() => {
      if (copiedId.value === service.id) copiedId.value = null;
    }, 1800);
  } catch (error) {
    console.error('Unable to copy endpoint:', error);
  }
};
</script>

<style scoped>
.dpi-page { display: flex; flex-direction: column; gap: 1.5rem; color: #172033; }
.dpi-hero { position: relative; overflow: hidden; display: flex; justify-content: space-between; gap: 2rem; padding: 2rem; border-radius: 1.5rem; color: white; background: radial-gradient(circle at 88% 15%, rgba(45, 212, 191, .28), transparent 28%), linear-gradient(135deg, #10233f, #123a58 58%, #0e5a62); }
.dpi-hero::after { content: ''; position: absolute; inset: 0; opacity: .13; background-image: linear-gradient(rgba(255,255,255,.3) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.3) 1px, transparent 1px); background-size: 32px 32px; pointer-events: none; }
.dpi-hero__content, .dpi-hero__status { position: relative; z-index: 1; }
.dpi-eyebrow, .dpi-section-kicker { display: block; margin-bottom: .55rem; color: #5eead4; font-size: .68rem; font-weight: 900; letter-spacing: .16em; text-transform: uppercase; }
.dpi-eyebrow i { margin-right: .4rem; }
.dpi-hero h3 { margin: 0 0 .5rem; color: white; font-size: clamp(1.75rem, 3vw, 2.5rem); font-weight: 900; letter-spacing: -.04em; }
.dpi-hero p { max-width: 650px; margin: 0; color: #d7e5ed; line-height: 1.65; }
.dpi-standards { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: 1.1rem; }
.dpi-standards span { padding: .32rem .65rem; border: 1px solid rgba(255,255,255,.18); border-radius: 999px; background: rgba(255,255,255,.08); color: #dceef2; font-size: .65rem; font-weight: 800; text-transform: uppercase; }
.dpi-hero__status { align-self: center; display: flex; align-items: center; gap: .75rem; min-width: 255px; padding: 1rem; border: 1px solid rgba(255,255,255,.18); border-radius: 1rem; background: rgba(4, 25, 45, .38); backdrop-filter: blur(10px); }
.dpi-live-dot { width: .7rem; height: .7rem; flex: 0 0 auto; border-radius: 50%; background: #34d399; box-shadow: 0 0 0 6px rgba(52,211,153,.14); }
.dpi-hero__status strong, .dpi-hero__status small { display: block; }
.dpi-hero__status strong { font-size: .78rem; }
.dpi-hero__status small { margin-top: .2rem; color: #a9c4d1; font-size: .65rem; }

.dpi-metrics { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .75rem; }
.dpi-metrics article { display: flex; align-items: center; gap: .75rem; padding: 1rem; border: 1px solid #e5eaf0; border-radius: 1rem; background: white; box-shadow: 0 8px 25px rgba(15, 35, 55, .04); }
.dpi-metric__icon, .dpi-building-block__icon { display: grid; place-items: center; width: 2.5rem; height: 2.5rem; flex: 0 0 auto; border-radius: .75rem; font-size: 1rem; }
.dpi-metrics strong, .dpi-metrics small { display: block; }
.dpi-metrics strong { color: #15253b; font-size: 1.2rem; font-weight: 900; }
.dpi-metrics small { color: #728096; font-size: .68rem; font-weight: 700; }
.dpi-tone--identity { color: #6d28d9; background: #f3e8ff; }
.dpi-tone--exchange { color: #0369a1; background: #e0f2fe; }
.dpi-tone--payments { color: #047857; background: #d1fae5; }
.dpi-tone--orchestration { color: #be123c; background: #ffe4e6; }
.dpi-tone--shared { color: #b45309; background: #fef3c7; }

.dpi-map, .dpi-catalogue { padding: 1.5rem; border: 1px solid #e3e9f0; border-radius: 1.5rem; background: #fff; box-shadow: 0 12px 35px rgba(15, 35, 55, .05); }
.dpi-section-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 1.35rem; }
.dpi-section-kicker { margin-bottom: .25rem; color: #0f766e; }
.dpi-section-heading h4 { margin: 0; color: #172033; font-size: 1.25rem; font-weight: 900; letter-spacing: -.025em; }
.dpi-map__health { padding: .45rem .7rem; border-radius: 999px; color: #047857; background: #ecfdf5; font-size: .65rem; font-weight: 900; text-transform: uppercase; }
.dpi-map__health i { margin-right: .3rem; }
.dpi-topology { display: grid; grid-template-columns: minmax(170px, .8fr) 50px minmax(210px, 1fr) 50px minmax(230px, 1.2fr); align-items: center; gap: .75rem; padding: 1.35rem; border: 1px solid #e8edf3; border-radius: 1.25rem; background: linear-gradient(180deg, #f8fbfd, #f4f8fa); }
.dpi-column-label { display: block; margin-bottom: .65rem; color: #8190a2; font-size: .58rem; font-weight: 900; letter-spacing: .13em; text-transform: uppercase; }
.dpi-participants { display: flex; flex-direction: column; gap: .5rem; }
.dpi-participants article { display: flex; align-items: center; gap: .65rem; padding: .7rem; border: 1px solid #dce5ec; border-radius: .8rem; background: white; }
.dpi-participants article > i { display: grid; place-items: center; width: 2rem; height: 2rem; flex: 0 0 auto; border-radius: .6rem; color: #0f766e; background: #e6fffb; }
.dpi-participants article span { font-size: .7rem; font-weight: 900; }
.dpi-participants article small { display: block; margin-top: .15rem; color: #8491a1; font-size: .58rem; font-weight: 600; }
.dpi-flow { display: flex; align-items: center; color: #2b8b8b; }
.dpi-flow span { height: 2px; flex: 1; background: linear-gradient(90deg, #bed5dc, #2b8b8b); }
.dpi-flow i { margin-left: -.1rem; }
.dpi-exchange-hub { position: relative; padding: 1.25rem; border: 1px solid #70b7bb; border-radius: 1.25rem; text-align: center; background: linear-gradient(145deg, #eafffb, #eef8ff); box-shadow: inset 0 0 0 4px rgba(255,255,255,.7), 0 12px 30px rgba(15,118,110,.1); }
.dpi-exchange-hub__rings { display: grid; place-items: center; width: 4.5rem; height: 4.5rem; margin: 0 auto .75rem; border: 1px solid #9dd5d5; border-radius: 50%; background: rgba(255,255,255,.65); box-shadow: 0 0 0 8px rgba(45, 155, 155, .07), 0 0 0 16px rgba(45, 155, 155, .04); }
.dpi-exchange-hub__rings span { display: grid; place-items: center; width: 3.1rem; height: 3.1rem; border-radius: 50%; color: white; background: linear-gradient(135deg, #0f766e, #0369a1); font-size: 1.2rem; }
.dpi-exchange-hub .dpi-column-label { margin-bottom: .55rem; color: #39737c; }
.dpi-exchange-hub h5 { margin: 0; font-size: 1rem; font-weight: 900; }
.dpi-exchange-hub p { margin: .2rem 0 .75rem; color: #5b7182; font-size: .65rem; }
.dpi-exchange-hub__tags { display: flex; flex-wrap: wrap; justify-content: center; gap: .3rem; }
.dpi-exchange-hub__tags span { padding: .25rem .42rem; border-radius: .35rem; color: #366675; background: rgba(255,255,255,.85); font-size: .52rem; font-weight: 800; }
.dpi-rails { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .5rem; }
.dpi-rails > .dpi-column-label { grid-column: 1 / -1; margin-bottom: .15rem; }
.dpi-rail { display: flex; align-items: center; gap: .55rem; min-width: 0; padding: .7rem; border: 1px solid #dee6ed; border-left: 3px solid var(--rail-color); border-radius: .8rem; text-align: left; background: white; cursor: pointer; transition: .2s ease; }
.dpi-rail:hover, .dpi-rail--active { border-color: var(--rail-color); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(20,40,60,.08); }
.dpi-rail--identity { --rail-color: #7c3aed; }.dpi-rail--exchange { --rail-color: #0284c7; }.dpi-rail--payments { --rail-color: #059669; }.dpi-rail--orchestration { --rail-color: #e11d48; }.dpi-rail--shared { --rail-color: #d97706; }
.dpi-rail--orchestration { grid-column: 1 / -1; }
.dpi-rail__icon { display: grid; place-items: center; width: 2rem; height: 2rem; flex: 0 0 auto; border-radius: .55rem; color: var(--rail-color); background: color-mix(in srgb, var(--rail-color) 11%, white); }
.dpi-rail__body { min-width: 0; flex: 1; }
.dpi-rail__body strong, .dpi-rail__body small { display: block; }
.dpi-rail__body strong { overflow: hidden; color: #243246; font-size: .66rem; font-weight: 900; text-overflow: ellipsis; white-space: nowrap; }
.dpi-rail__body small { margin-top: .15rem; color: #7d8a99; font-size: .53rem; line-height: 1.3; }
.dpi-rail__count { display: grid; place-items: center; width: 1.35rem; height: 1.35rem; flex: 0 0 auto; border-radius: 50%; color: var(--rail-color); background: color-mix(in srgb, var(--rail-color) 10%, white); font-size: .55rem; font-weight: 900; }
.dpi-trust-envelope { display: flex; flex-wrap: wrap; justify-content: center; gap: .75rem 1.5rem; margin-top: .75rem; padding: .75rem 1rem; border: 1px dashed #b9c9d5; border-radius: .8rem; color: #607385; background: #f8fafc; }
.dpi-trust-envelope span { font-size: .6rem; font-weight: 800; text-transform: uppercase; }
.dpi-trust-envelope i { margin-right: .3rem; color: #0f766e; }

.dpi-section-heading--catalogue { align-items: center; }
.dpi-search { display: flex; align-items: center; gap: .55rem; width: min(100%, 320px); padding: .65rem .8rem; border: 1px solid #dfe6ed; border-radius: .8rem; color: #7b8998; background: #f8fafc; }
.dpi-search input { min-width: 0; width: 100%; border: 0; outline: 0; color: #263448; background: transparent; font-size: .75rem; }
.dpi-filters { display: flex; flex-wrap: wrap; gap: .45rem; margin-bottom: 1rem; }
.dpi-filters button { padding: .48rem .72rem; border: 1px solid #dfe6ed; border-radius: 999px; color: #647386; background: white; font-size: .65rem; font-weight: 800; cursor: pointer; }
.dpi-filters button:hover, .dpi-filters button.active { border-color: #0f766e; color: #0f766e; background: #ecfdf5; }
.dpi-filters i { margin-right: .25rem; }
.dpi-building-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; }
.dpi-building-block { min-width: 0; padding: 1rem; border: 1px solid #e1e7ed; border-radius: 1rem; background: white; transition: .2s ease; }
.dpi-building-block:hover { border-color: #9db5c4; box-shadow: 0 10px 28px rgba(22,44,67,.07); transform: translateY(-2px); }
.dpi-building-block > header { display: flex; align-items: center; gap: .7rem; }
.dpi-building-block__title { min-width: 0; flex: 1; }
.dpi-building-block__title > span { display: block; margin-bottom: .15rem; color: #8491a1; font-size: .55rem; font-weight: 900; letter-spacing: .07em; text-transform: uppercase; }
.dpi-building-block h5 { margin: 0; overflow: hidden; color: #1d2b3e; font-size: .82rem; font-weight: 900; text-overflow: ellipsis; white-space: nowrap; }
.dpi-online { display: flex; align-items: center; gap: .25rem; color: #047857; font-size: .55rem; font-weight: 900; text-transform: uppercase; }
.dpi-online i { width: .38rem; height: .38rem; border-radius: 50%; background: #10b981; }
.dpi-building-block > p { min-height: 2.5rem; margin: .75rem 0; color: #687789; font-size: .7rem; line-height: 1.55; }
.dpi-endpoint { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: .5rem; padding: .55rem; border: 1px solid #e4e9ef; border-radius: .65rem; background: #f7f9fb; }
.dpi-endpoint > span { padding: .2rem .35rem; border-radius: .3rem; color: #0369a1; background: #e0f2fe; font-size: .48rem; font-weight: 900; text-transform: uppercase; }
.dpi-endpoint code { overflow: hidden; color: #34465b; font-size: .62rem; font-weight: 700; text-overflow: ellipsis; white-space: nowrap; }
.dpi-endpoint button { border: 0; color: #6d7b8b; background: transparent; cursor: pointer; }
.dpi-building-block > footer { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .75rem; margin-top: .75rem; }
.dpi-building-block > footer > span { color: #354458; font-size: .62rem; font-weight: 800; }
.dpi-building-block > footer small { display: block; margin-bottom: .15rem; color: #8a96a5; font-size: .5rem; font-weight: 900; text-transform: uppercase; }
.dpi-building-block details { grid-column: 1 / -1; border-top: 1px solid #edf0f4; }
.dpi-building-block summary { display: flex; justify-content: space-between; padding-top: .65rem; color: #52647a; font-size: .62rem; font-weight: 800; cursor: pointer; list-style: none; }
.dpi-building-block details[open] summary i { transform: rotate(180deg); }
.dpi-building-block pre { max-height: 220px; margin: .65rem 0 0; padding: .75rem; overflow: auto; border-radius: .65rem; color: #dbeafe; background: #172033; font-size: .6rem; }
.dpi-empty-state { display: grid; justify-items: center; gap: .6rem; padding: 3rem; border: 1px dashed #ccd6df; border-radius: 1rem; color: #718093; background: #f8fafc; }
.dpi-empty-state > i { font-size: 1.5rem; }.dpi-empty-state strong { font-size: .75rem; }.dpi-empty-state button { border: 0; color: #0f766e; background: none; font-size: .68rem; font-weight: 900; cursor: pointer; }

@media (max-width: 1100px) {
  .dpi-topology { grid-template-columns: 1fr; }
  .dpi-flow { justify-content: center; min-height: 24px; transform: rotate(90deg); }
  .dpi-flow span { max-width: 40px; }
  .dpi-participants { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .dpi-participants > .dpi-column-label { grid-column: 1 / -1; }
  .dpi-rails { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .dpi-rail--orchestration { grid-column: 1 / -1; }
}

@media (max-width: 760px) {
  .dpi-hero { flex-direction: column; padding: 1.4rem; }
  .dpi-hero__status { width: 100%; min-width: 0; }
  .dpi-metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .dpi-participants, .dpi-rails, .dpi-building-grid { grid-template-columns: 1fr; }
  .dpi-rail--orchestration { grid-column: 1; }
  .dpi-rails > .dpi-column-label { grid-column: 1; }
  .dpi-section-heading, .dpi-section-heading--catalogue { flex-direction: column; align-items: stretch; }
  .dpi-search { width: 100%; }
  .dpi-map, .dpi-catalogue { padding: 1rem; }
  .dpi-topology { padding: .9rem; }
}

@media (max-width: 420px) {
  .dpi-metrics { grid-template-columns: 1fr; }
}
</style>
