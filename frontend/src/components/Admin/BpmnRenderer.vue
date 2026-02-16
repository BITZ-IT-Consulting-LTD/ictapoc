<template>
  <div class="mermaid-viewer-wrapper bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
    <div class="mb-4 flex items-center justify-center gap-6 pb-4 border-b border-gray-50">
      <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-green-500"></span><span
          class="text-[9px] uppercase font-black text-gray-400 tracking-tighter">Start</span></div>
      <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-md bg-blue-500"></span><span
          class="text-[9px] uppercase font-black text-gray-400 tracking-tighter">User Task</span></div>
      <div class="flex items-center gap-2"><span
          class="w-2.5 h-2.5 rounded-md border-2 border-dashed border-purple-500"></span><span
          class="text-[9px] uppercase font-black text-gray-400 tracking-tighter">Service Task</span></div>
      <div class="flex items-center gap-2"><span class="w-3 h-3 rotate-45 border-2 border-orange-500"></span><span
          class="text-[9px] uppercase font-black text-gray-400 tracking-tighter">Gateway</span></div>
      <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-red-500"></span><span
          class="text-[9px] uppercase font-black text-gray-400 tracking-tighter">End</span></div>
    </div>

    <div class="mermaid-container flex justify-center py-4 min-h-[200px]" ref="mermaidContainer">
      {{ definition }}
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, watch, nextTick } from 'vue';
  import mermaid from 'mermaid';

  const props = defineProps({
    steps: {
      type: Array,
      required: true
    },
    stage: {
      type: String,
      default: 'as_is'
    }
  });

  const mermaidContainer = ref(null);
  const definition = ref('');

  const generateGraph = () => {
    if (!props.steps || props.steps.length === 0) {
      definition.value = 'graph TD;\n  Start((No steps for this stage)) --> End((End))';
      return;
    }

    let graph = 'graph TD;\n';

    props.steps.forEach((step, index) => {
      const nodeId = `S${index + 1}`;
      const safeLabel = (step.description || step.step_name || 'Step').replace(/"/g, "'");
      const actor = step.actor || step.role || 'Officer';
      const isService = step.system || (step.step_type === 'api_call') || (step.bpmn_element_type === 'service_task');
      let bType = step.bpmn_element_type || (isService ? 'service_task' : 'user_task');

      // Force start/end based on position if not explicitly set
      if (index === 0 && !bType.includes('gateway')) bType = 'start_event';
      if (index === props.steps.length - 1 && !bType.includes('gateway')) bType = 'end_event';

      if (bType === 'start_event') {
        graph += `    ${nodeId}(("${safeLabel}"))\n`;
        graph += `    class ${nodeId} startEvent;\n`;
      } else if (bType === 'end_event') {
        graph += `    ${nodeId}(("${safeLabel}"))\n`;
        graph += `    class ${nodeId} endEvent;\n`;
      } else if (bType === 'exclusive_gateway' || bType === 'gateway') {
        graph += `    ${nodeId}{{"${safeLabel}"}}\n`;
        graph += `    class ${nodeId} gateway;\n`;
      } else if (bType === 'service_task') {
        graph += `    ${nodeId}[["${safeLabel}<br/>(System)"]]\n`;
        graph += `    class ${nodeId} serviceTask;\n`;
      } else {
        graph += `    ${nodeId}["${safeLabel}<br/>(${actor})"]\n`;
        graph += `    class ${nodeId} userTask;\n`;
      }

      if (index < props.steps.length - 1) {
        const nextNodeId = `S${index + 2}`;
        graph += `    ${nodeId} --> ${nextNodeId}\n`;
      }
    });

    graph += '    classDef startEvent fill:#f0fdf4,stroke:#16a34a,stroke-width:4px;\n';
    graph += '    classDef endEvent fill:#fef2f2,stroke:#dc2626,stroke-width:4px;\n';
    graph += '    classDef gateway fill:#fff7ed,stroke:#c2410c,stroke-width:2px;\n';
    graph += '    classDef userTask fill:#eff6ff,stroke:#2563eb,stroke-width:2px;\n';
    graph += '    classDef serviceTask fill:#faf5ff,stroke:#7c3aed,stroke-width:2px,stroke-dasharray: 5 5;\n';

    definition.value = graph;
  };

  const render = async () => {
    generateGraph();
    await nextTick();
    if (mermaidContainer.value) {
      mermaidContainer.value.removeAttribute('data-processed');
      mermaidContainer.value.innerHTML = definition.value;
      try {
        await mermaid.run({
          nodes: [mermaidContainer.value]
        });
      } catch (e) {
        console.error('Mermaid render error', e);
      }
    }
  };

  onMounted(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        primaryColor: '#4f46e5',
        edgeColor: '#64748b',
        fontFamily: 'Inter, sans-serif'
      }
    });
    render();
  });

  watch(() => props.steps, render, { deep: true });
</script>

<style scoped>
  .mermaid-viewer-wrapper {
    transition: all 0.3s ease;
  }

  :deep(.mermaid) {
    width: 100%;
    display: flex;
    justify-content: center;
  }
</style>
