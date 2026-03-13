<template>
  <div class="card overflow-hidden border-0 shadow-xl rounded-2xl u-bg-white">
    <div class="u-p-6 u-border-b u-border-slate-100 u-flex u-justify-between u-items-start">
      <div>
        <h2 class="u-text-xl u-font-black u-text-main u-uppercase u-tracking-widest">{{ artifact?.title }}</h2>
        <p class="u-text-xs u-text-muted u-mt-1 u-font-medium">{{ artifact?.description || 'No description provided.' }}</p>
      </div>
      <span class="badge" :class="statusClass">{{ statusLabel }}</span>
    </div>
    
    <div class="u-p-6 u-bg-slate-50/50">
      <div class="u-grid u-grid-cols-2 md:u-grid-cols-4 u-gap-6">
        <div>
          <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-1">Artifact Type</div>
          <div class="u-text-sm u-font-bold u-text-main flex items-center gap-2">
            <i class="bi bi-tag-fill u-text-primary"></i>
            {{ artifact?.artifact_type?.name || 'General' }}
          </div>
        </div>
        <div>
          <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-1">Phase</div>
          <div class="u-text-sm u-font-bold u-text-main flex items-center gap-2">
            <i class="bi bi-diagram-3-fill u-text-info"></i>
            {{ artifact?.phase?.name || 'N/A' }}
          </div>
        </div>
        <div>
          <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-1">Owner MDA</div>
          <div class="u-text-sm u-font-bold u-text-main flex items-center gap-2 uppercase">
            <i class="bi bi-building-fill u-text-slate-400"></i>
            {{ artifact?.mda_owner?.name || 'N/A' }}
          </div>
        </div>
        <div>
          <div class="u-text-[10px] u-font-black u-text-muted u-uppercase u-tracking-widest u-mb-1">Last Updated</div>
          <div class="u-text-sm u-font-bold u-text-main flex items-center gap-2">
            <i class="bi bi-clock-history u-text-warning"></i>
            {{ getRelativeTime(artifact?.updated_at) }}
          </div>
        </div>
        <div v-if="artifact?.submission_deadline">
          <div class="u-text-[10px] u-font-black text-red-500 u-uppercase u-tracking-widest u-mb-1">Submission Deadline</div>
          <div class="u-text-sm u-font-black text-red-600 flex items-center gap-2">
            <i class="bi bi-calendar-check-fill"></i>
            {{ new Date(artifact.submission_deadline).toLocaleDateString() }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  artifact: {
    type: Object,
    default: () => ({})
  }
});

const statusClass = computed(() => {
  const map = {
    'draft': 'badge--secondary',
    'reviewed': 'badge--warning',
    'validated': 'badge--primary',
    'final': 'badge--success',
    'archived': 'badge--danger'
  };
  return map[props.artifact?.status] || 'badge--secondary';
});

const statusLabel = computed(() => {
  const status = props.artifact?.status;
  if (!status) return 'Unknown';
  return status.charAt(0).toUpperCase() + status.slice(1);
});

const formatCategory = (cat) => {
  if (!cat) return 'Other';
  return cat.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
};

const getRelativeTime = (dateString) => {
  if (!dateString) return 'Never';
  return new Date(dateString).toLocaleString();
};
</script>
