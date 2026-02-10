<template>
  <div class="bg-white p-6 rounded-lg shadow mt-4">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
      <div>
        <h3 class="text-xl font-bold text-gray-900">Authoritative Service Registry</h3>
        <div class="text-sm text-gray-500 bg-gray-100 px-3 py-0.5 rounded-full border inline-block mt-1">
          Connected to KESEL & Huduma Bridges
        </div>
      </div>
      <div class="relative w-full md:w-80">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search endpoints by name, URL, or category..." 
          class="block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        <span class="absolute right-3 top-2 text-gray-400">🔍</span>
      </div>
    </div>

    <p class="text-gray-600 mb-8 max-w-3xl">
      The following services are authoritative system endpoints available for use in <strong>Automated API Call</strong> workflow steps. 
      Use these to integrate with national registries, document archives, and external government systems.
    </p>

    <div v-if="filteredRegistry.length > 0" class="grid grid-cols-1 gap-6">
      <div v-for="service in filteredRegistry" :key="service.id" class="border rounded-xl overflow-hidden hover:border-indigo-300 transition-colors shadow-sm bg-slate-50">
        <div class="p-4 bg-white border-b flex justify-between items-center">
          <div>
            <h4 class="text-lg font-bold text-gray-800">{{ service.name }}</h4>
            <span class="text-xs font-mono text-gray-400 uppercase tracking-tighter">{{ service.category }}</span>
          </div>
          <span :class="service.status === 'online' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-2 py-1 text-xs font-bold rounded uppercase">
            {{ service.status }}
          </span>
        </div>
        
        <div class="p-4 space-y-4">
          <p class="text-sm text-gray-600">{{ service.description }}</p>
          
          <div class="bg-slate-900 rounded-lg p-3 overflow-x-auto">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold text-indigo-400 uppercase">Endpoint URL</span>
              <button @click="copyToClipboard(service.url)" class="text-[10px] text-gray-400 hover:text-white underline">Copy URL</button>
            </div>
            <code class="text-indigo-300 text-sm font-mono">{{ service.url }}</code>
          </div>

          <div>
             <h5 class="text-xs font-bold text-gray-500 uppercase mb-2">Documentation / Expected Payload</h5>
             <pre class="bg-white border rounded p-3 text-xs font-mono text-gray-700 overflow-x-auto">{{ JSON.stringify(service.payload, null, 2) }}</pre>
          </div>

          <div class="flex space-x-4 pt-2">
            <div v-for="(detail, label) in service.details" :key="label">
              <span class="text-[10px] uppercase font-bold text-gray-400 block">{{ label }}</span>
              <span class="text-sm text-gray-700">{{ detail }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
      <p class="text-gray-500 italic">No authoritative services found matching your search.</p>
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
