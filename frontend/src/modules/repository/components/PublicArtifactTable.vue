<template>
  <div class="card overflow-hidden border-0 shadow-xl rounded-3xl">
    <div class="table-container">
      <table class="table">
        <thead>
          <tr class="table__header-row u-bg-slate-50/50">
            <th class="table__header-cell u-py-4">Artifact Title</th>
            <th class="table__header-cell">Classification (Type)</th>
            <th class="table__header-cell">Location</th>
            <th class="table__header-cell">Owner MDA</th>
            <th class="table__header-cell u-text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="artifact in artifacts" :key="artifact.id" class="table__row hover:u-bg-slate-50/50">
            <td class="table__cell u-font-bold u-text-main">
              <div class="u-text-sm">{{ artifact.title }}</div>
              <div class="u-text-[10px] u-text-muted u-mt-1" v-if="artifact.latest_version">v{{ artifact.latest_version }} • {{ getRelativeTime(artifact.updated_at) }}</div>
            </td>
            <td class="table__cell">
              <span v-if="artifact.artifact_type" class="badge badge--info">{{ artifact.artifact_type.name }}</span>
              <span v-else class="u-text-xs u-text-muted">General</span>
            </td>
            <td class="table__cell">
              <div v-if="artifact.node" class="u-flex u-items-center u-gap-1 u-text-[10px] u-font-bold u-text-primary u-uppercase u-tracking-tighter">
                <i class="bi bi-diagram-3"></i> {{ artifact.node.full_path }}
              </div>
              <div v-else class="u-text-[9px] u-text-muted u-uppercase font-black tracking-widest">Unmapped</div>
            </td>
            <td class="table__cell">
              <span class="u-text-xs u-text-slate-500 uppercase">{{ artifact.mda_owner?.name || 'N/A' }}</span>
            </td>
            <td class="table__cell u-text-right">
              <router-link :to="`/public-repository/${artifact.id}`" class="button button--secondary button--tiny button--pill u-px-4">
                View Public Details
              </router-link>
            </td>
          </tr>
          <tr v-if="artifacts.length === 0">
            <td colspan="5" class="u-p-10 u-text-center u-text-muted u-font-bold u-uppercase u-tracking-widest u-text-[10px]">
              No public artifacts found matching criteria.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  artifacts: {
    type: Array,
    default: () => []
  }
});

const getRelativeTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString();
};
</script>