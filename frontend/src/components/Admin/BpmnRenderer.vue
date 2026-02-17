<template>
  <div class="icta-mermaid-viewer shadow-premium">
    <div class="legend-bar">
      <div class="legend-item"><span class="node-dot start"></span><span class="legend-label">Start</span></div>
      <div class="legend-item"><span class="node-box user"></span><span class="legend-label">User Task</span></div>
      <div class="legend-item"><span class="node-box service"></span><span class="legend-label">Service Task</span>
      </div>
      <div class="legend-item"><span class="node-diamond gateway"></span><span class="legend-label">Gateway</span></div>
      <div class="legend-item"><span class="node-dot end"></span><span class="legend-label">End</span></div>
    </div>

    <div class="mermaid-canvas" ref="mermaidContainer">
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

    graph += '    classDef startEvent fill:#E6F6EF,stroke:#01A64E,stroke-width:3px;\n';
    graph += '    classDef endEvent fill:#FFEBEC,stroke:#EC232A,stroke-width:3px;\n';
    graph += '    classDef gateway fill:#FFFBEB,stroke:#D97706,stroke-width:2px;\n';
    graph += '    classDef userTask fill:#F0F9FF,stroke:#0284C7,stroke-width:2px;\n';
    graph += '    classDef serviceTask fill:#F5F3FF,stroke:#7C3AED,stroke-width:2px,stroke-dasharray: 5 5;\n';

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
        primaryColor: '#EC232A',
        edgeColor: '#393B3A',
        fontFamily: 'Raleway, sans-serif',
        fontSize: '12px'
      }
    });
    render();
  });

  watch(() => props.steps, render, { deep: true });
</script>

<style scoped>
  .icta-mermaid-viewer {
    background: white;
    border-radius: var(--radius-lg);
    padding: 2rem;
    border: 1px solid var(--icta-border);
    transition: all 0.3s ease;
  }

  .legend-bar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    padding-bottom: 2rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--icta-border);
    flex-wrap: wrap;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .node-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }

  .node-box {
    width: 14px;
    height: 14px;
    border-radius: 2px;
  }

  .node-diamond {
    box-sizing: border-box;
    width: 12px;
    height: 12px;
    transform: rotate(45deg);
    border: 1.5px solid;
  }

  .start {
    background: var(--icta-green);
  }

  .end {
    background: var(--icta-red);
  }

  .user {
    background: #F0F9FF;
    border: 1.5px solid #0284C7;
  }

  .service {
    background: #F5F3FF;
    border: 1.5px dashed #7C3AED;
  }

  .gateway {
    background: #FFFBEB;
    border-color: #D97706;
  }

  .legend-label {
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--icta-grey);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .mermaid-canvas {
    display: flex;
    justify-content: center;
    min-height: 250px;
  }

  :deep(.mermaid) {
    width: 100%;
  }
</style>
