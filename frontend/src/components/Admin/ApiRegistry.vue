<template>
    <div class="u-flex u-flex-col u-gap-8 animate-fade-in">
    <!-- Registry Header -->
    <header class="u-flex u-flex-col md:u-flex-row u-justify-between u-items-start md:u-items-center u-gap-6">
      <div class="page__title-group">
        <h3 class="u-text-2xl u-font-black u-text-main u-mb-2">Authoritative Service Registry</h3>
        <div class="status-indicator">
          <span class="status-indicator__dot status-indicator__dot--online"></span>
          <span class="status-indicator__label u-text-muted">KESEL & Huduma Infrastructure Connected</span>
        </div>
      </div>
      <div class="toolbar__filter-group u-w-full md:u-w-96 u-shadow-sm">
        <i class="bi bi-search toolbar__filter-icon"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search endpoints, category, or url..." 
          class="toolbar__filter-input u-w-full"
        />
      </div>
    </header>

    <!-- Contextual Intelligence -->
    <div class="card u-bg-primary-soft u-border-primary/10 u-p-6 shadow-sm">
      <p class="u-text-sm u-font-medium u-text-primary-dark max-w-4xl u-mb-0">
        The following services are authoritative system endpoints available for use in <strong class="u-font-black">Automated API Call</strong> workflow steps. 
        These govern integration with national registries, document archives, and federated government systems.
      </p>
    </div>

    <!-- Endpoint Grid -->
    <div v-if="filteredRegistry.length > 0" class="u-grid u-grid-cols-1 lg:u-grid-cols-2 u-gap-6">
      <article v-for="service in filteredRegistry" :key="service.id" 
        class="card hover:u-border-primary transition-all duration-300 shadow-md group">
        <header class="card__header u-bg-page u-p-5 u-flex u-justify-between u-items-center">
          <div>
            <h4 class="u-text-base u-font-black u-text-main u-mb-1 group-hover:u-text-primary transition-colors">
              {{ service.name }}
            </h4>
            <span class="table__code-badge">{{ service.category }}</span>
          </div>
          <div class="status-indicator">
             <span class="u-text-[10px] u-font-black u-text-success u-uppercase u-tracking-widest">{{ service.status }}</span>
             <span class="status-indicator__dot status-indicator__dot--online"></span>
          </div>
        </header>
        
        <div class="card__body u-p-6 u-flex u-flex-col u-gap-6">
          <p class="u-text-sm u-text-muted u-line-clamp-2">{{ service.description }}</p>
          
          <!-- Endpoint URL Block -->
          <div class="code-block">
            <div class="code-block__header">
              <span class="code-block__label">Endpoint URL</span>
              <button @click="copyToClipboard(service.url)" class="button button--ghost button--small p-0 u-text-[10px] u-font-black u-uppercase">
                <i class="bi bi-files u-mr-1"></i> Copy
              </button>
            </div>
            <code class="code-block__content code-block__content--primary">{{ service.url }}</code>
          </div>

          <!-- Documentation Fragment -->
          <div class="u-space-y-3">
             <h5 class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest">Expected Payload Schema</h5>
             <pre class="u-bg-page u-p-4 u-rounded u-text-[11px] u-font-mono u-text-main u-border u-border-border-color u-overflow-x-auto">{{ JSON.stringify(service.payload, null, 2) }}</pre>
          </div>

          <!-- Metadata Ribbon -->
          <footer class="u-flex u-flex-wrap u-gap-6 u-pt-4 u-border-t u-border-border-color">
            <div v-for="(detail, label) in service.details" :key="label">
              <span class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-tighter u-block u-mb-1">{{ label }}</span>
              <span class="u-text-xs u-font-bold u-text-main">{{ detail }}</span>
            </div>
          </footer>
        </div>
      </article>
    </div>

    <!-- Zero State -->
    <div v-else class="card u-py-24 u-text-center u-bg-page u-border-2 u-border-dashed u-border-border-color shadow-inner">
      <div class="u-text-4xl u-mb-4">🔍</div>
      <p class="u-text-sm u-font-black u-text-muted u-uppercase u-tracking-widest">No matching authoritative services found</p>
      <button @click="searchQuery = ''" class="button button--secondary button--small u-mt-4">Clear Filters</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');

const registry = ref([
  {
    id: 'huduma_oidc',
    name: 'Huduma Identity (OIDC Federation)',
    category: 'Identity',
    status: 'online',
    description: 'Unified login and identity federation for all Huduma services. Supports Single Sign-On (SSO) across government portals.',
    url: 'HUDUMA_BRIDGE/auth/oidc',
    details: {
      'Protocol': 'Oauth2/OIDC',
      'Auth': 'Bearer JWT',
      'Latency': '~210ms'
    },
    payload: {
      client_id: "ICTA_POC_OIDC",
      grant_type: "authorization_code",
      scope: "openid profile email citizen_id"
    }
  },
  {
    id: 'huduma_notify',
    name: 'Huduma G-Notify (SMS/Email Gateway)',
    category: 'Communication',
    status: 'online',
    description: 'Centralized notification engine for sending automated SMS and Email alerts to citizens regarding their service requests.',
    url: 'HUDUMA_BRIDGE/notify/send',
    details: {
      'Protocol': 'REST/JSON',
      'Auth': 'API-KEY',
      'Latency': '~50ms'
    },
    payload: {
      to: "CITIZEN_ID",
      channels: ["SMS", "PUSH"],
      template_id: "REQ_APPROVED_01",
      variables: {
        request_name: "STRING",
        status: "STRING"
      }
    }
  },
  {
    id: 'edrms_archive',
    name: 'Electronic Document Records Management System (EDRMS)',
    category: 'Archive',
    status: 'online',
    description: 'Authoritative archive for all digitized government documents and certificates. Handles long-term storage and retrieval.',
    url: 'KESEL_BRIDGE/EDRMS/archive',
    details: {
      'Protocol': 'REST/HTTPS',
      'Auth': 'System-to-System',
      'Latency': '~120ms'
    },
    payload: {
      action: "archive",
      document_type: "CERTIFICATE",
      metadata: {
        request_id: "STRING",
        citizen_id: "STRING",
        issued_by: "MDA_CODE"
      },
      content_base64: "BASE64_STRING"
    }
  },
  {
    id: 'iprs_verify',
    name: 'Integrated Population Registration System (IPRS)',
    category: 'Identity',
    status: 'online',
    description: 'Verify identity details against the national person registry using ID number or Passport number.',
    url: 'KESEL_BRIDGE/IPRS/verify',
    details: {
      'Protocol': 'JSON-RPC',
      'Auth': 'KESEL-TOKEN',
      'Latency': '~450ms'
    },
    payload: {
      id_number: "STRING",
      verification_type: "BIO_MATCH",
      request_origin: "icta-poc"
    }
  },
  {
    id: 'kra_pin_verify',
    name: 'KRA Taxpayer Validation (iTax)',
    category: 'Revenue',
    status: 'online',
    description: 'Validate Tax PIN status and compliance for businesses and individuals.',
    url: 'KESEL_BRIDGE/TAX/verify_pin',
    details: {
      'Protocol': 'SOAP/WSDL',
      'Auth': 'MTLS',
      'Latency': '~300ms'
    },
    payload: {
      pin: "A000000000Z",
      check_compliance: true
    }
  },
  {
    id: 'internal_profile_update',
    name: 'Internal Profile Update Handler',
    category: 'System',
    status: 'online',
    description: 'Internal system hook to update user profile fields after verification steps are complete.',
    url: 'internal://update_profile',
    details: {
      'Protocol': 'Native Hook',
      'Auth': 'Internal Only',
      'Latency': '<5ms'
    },
    payload: {
      fields: ["id_number", "phone_number"],
      force_update: true
    }
  }
]);

const filteredRegistry = computed(() => {
  if (!searchQuery.value) return registry.value;
  const q = searchQuery.value.toLowerCase();
  return registry.value.filter(item => 
    item.name.toLowerCase().includes(q) || 
    item.category.toLowerCase().includes(q) || 
    item.url.toLowerCase().includes(q) ||
    item.description.toLowerCase().includes(q)
  );
});

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
  alert("Endpoint URL copied to clipboard");
};
</script>
