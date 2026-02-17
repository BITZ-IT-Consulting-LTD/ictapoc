<template>
  <div class="markdown-container bg-white p-8 rounded-xl shadow-sm border border-slate-100 max-w-none">
    <div v-if="loading" class="flex items-center justify-center p-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>
    <div v-else-if="error" class="p-4 bg-red-50 text-red-700 rounded-lg">
      {{ error }}
    </div>
    <div v-else class="prose prose-indigo max-w-none">
      <div ref="markdownBody" v-html="renderedHtml" class="markdown-body"></div>
    </div>

    <!-- Zoom Modal -->
    <Teleport to="body">
      <div v-if="showZoom"
        class="fixed inset-0 z-[10000] bg-slate-900/95 backdrop-blur-md flex flex-col items-center justify-center p-4 md:p-12 overflow-hidden"
        @click="closeZoom">
        <div class="absolute top-6 right-8 flex items-center gap-4 z-[10001]">
          <button @click.stop="downloadSvg"
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl font-bold flex items-center gap-2 shadow-2xl transition-all transform active:scale-95">
            <i class="bi bi-download"></i> Export SVG
          </button>
          <button @click="closeZoom"
            class="bg-white/10 hover:bg-white/20 text-white w-12 h-12 rounded-xl flex items-center justify-center text-2xl transition-all">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="w-full h-full flex items-center justify-center overflow-auto p-4 md:p-20 custom-scrollbar"
          @click.stop>
          <div ref="zoomContainer"
            class="zoom-content-container bg-white p-12 md:p-24 rounded-[2rem] shadow-2xl min-w-fit transition-all duration-500 ease-out transform scale-110">
            <!-- Mermaid will render here -->
            <div id="zoom-mermaid-target" class="flex justify-center"></div>
          </div>
        </div>

        <div
          class="absolute bottom-8 left-1/2 -translate-x-1/2 text-white/70 text-sm font-bold bg-white/10 px-6 py-3 rounded-full backdrop-blur-xl border border-white/10 flex items-center gap-3 animate-bounce-slow">
          <i class="bi bi-arrows-fullscreen"></i> High-Resolution Inspection Mode • Click outside to close
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
  import { ref, watch, onMounted, nextTick } from 'vue';
  import { Marked } from 'marked';
  import DOMPurify from 'dompurify';
  import mermaid from 'mermaid';

  const props = defineProps({
    url: {
      type: String,
      required: true
    }
  });

  const renderedHtml = ref('');
  const loading = ref(true);
  const error = ref(null);
  const markdownBody = ref(null);

  // Zoom Modal State
  const showZoom = ref(false);
  const zoomContainer = ref(null);
  let activeMermaidCode = '';

  const marked = new Marked();

  // Configure mermaid
  mermaid.initialize({
    startOnLoad: false,
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'Outfit, Inter, sans-serif',
    flowchart: { useMaxWidth: false, htmlLabels: true, curve: 'basis' },
    sequence: { useMaxWidth: false },
  });

  const renderMarkdown = async () => {
    if (!props.url) return;

    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(props.url);
      if (!response.ok) throw new Error('Failed to load documentation file.');
      const text = await response.text();

      // Parse Markdown
      const rawHtml = await marked.parse(text);
      // Sanitize HTML
      renderedHtml.value = DOMPurify.sanitize(rawHtml);

      loading.value = false;

      // Wait for DOM update then render mermaid
      await nextTick();
      await renderMermaid();
    } catch (err) {
      console.error('Markdown rendering error:', err);
      error.value = err.message;
      loading.value = false;
    }
  };

  const openZoom = async (code) => {
    activeMermaidCode = code;
    showZoom.value = true;

    await nextTick();

    const target = document.getElementById('zoom-mermaid-target');
    if (target) {
      try {
        // Clear previous
        target.innerHTML = '';
        // Generate a unique ID for the zoom render
        const id = 'zoom-diagram-' + Date.now();
        const { svg } = await mermaid.render(id, code);
        target.innerHTML = svg;
      } catch (e) {
        console.error('Modal mermaid rendering failed:', e);
        target.innerHTML = '<div class="text-red-500 font-bold p-8">Failed to render diagram for zoom.</div>';
      }
    }
  };

  const closeZoom = () => {
    showZoom.value = false;
    activeMermaidCode = '';
  };

  const downloadSvg = () => {
    const target = document.getElementById('zoom-mermaid-target');
    if (!target) return;

    const svg = target.querySelector('svg');
    if (!svg) return;

    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(source);

    const link = document.createElement('a');
    link.href = url;
    link.download = `GEA_Architecture_${Date.now()}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const renderMermaid = async () => {
    if (!markdownBody.value) return;

    const codeBlocks = markdownBody.value.querySelectorAll('pre code.language-mermaid');
    if (codeBlocks.length === 0) return;

    const nodes = [];

    for (const block of codeBlocks) {
      const pre = block.parentElement;
      const code = block.textContent;

      // Create a styled wrapper
      const wrapper = document.createElement('div');
      wrapper.className = 'mermaid-wrapper relative group bg-slate-50 rounded-[2rem] p-8 md:p-12 border border-slate-100 my-16 transition-all hover:shadow-2xl hover:shadow-indigo-500/10 hover:border-indigo-100';

      // Add Toolbar Button (More visible now)
      const btnContainer = document.createElement('div');
      btnContainer.className = 'absolute -top-6 right-8 z-10';

      const zoomBtn = document.createElement('button');
      zoomBtn.className = 'bg-white shadow-xl px-6 py-3 rounded-2xl text-[10px] font-black tracking-widest text-indigo-600 border border-slate-100 hover:bg-indigo-600 hover:text-white flex items-center gap-3 transform active:scale-95 transition-all group-hover:scale-105';
      zoomBtn.innerHTML = '<i class="bi bi-arrows-angle-expand text-sm"></i> INSPECT SYSTEM MODEL';

      const mermaidDiv = document.createElement('div');
      mermaidDiv.className = 'mermaid flex justify-center';
      mermaidDiv.textContent = code;

      zoomBtn.onclick = (e) => {
        e.stopPropagation();
        openZoom(code);
      };

      btnContainer.appendChild(zoomBtn);
      wrapper.appendChild(btnContainer);
      wrapper.appendChild(mermaidDiv);

      // Add Caption
      const caption = document.createElement('div');
      caption.className = 'text-center mt-8 text-[9px] uppercase tracking-[0.3em] font-black text-slate-300';
      caption.textContent = 'Decentralized Architecture Node • GEA v1.1';
      wrapper.appendChild(caption);

      pre.replaceWith(wrapper);
      nodes.push(mermaidDiv);
    }

    try {
      await mermaid.run({
        nodes: nodes,
      });
    } catch (e) {
      console.error('Mermaid rendering failed:', e);
    }
  };

  onMounted(renderMarkdown);
  watch(() => props.url, renderMarkdown);
</script>

<style>

  /* Custom styles for the markdown body to ensure it looks premium */
  .markdown-body h1 {
    @apply text-5xl font-black mb-12 text-slate-900 tracking-tight leading-tight;
  }

  .markdown-body h2 {
    @apply text-3xl font-black border-b-4 border-indigo-600/5 pb-4 mb-8 mt-20 text-slate-800 flex items-center gap-4;
  }

  .markdown-body h3 {
    @apply text-2xl font-bold mb-6 mt-12 text-slate-700;
  }

  .markdown-body p {
    @apply mb-8 leading-relaxed text-slate-600 text-xl font-light;
  }

  .markdown-body ul {
    @apply list-disc pl-8 mb-8 space-y-4 text-slate-600 text-lg;
  }

  .markdown-body blockquote {
    @apply border-l-[12px] border-indigo-600 pl-8 py-6 bg-indigo-50/20 italic rounded-r-[2rem] mb-12 text-indigo-900 font-medium text-xl;
  }

  .markdown-body hr {
    @apply my-20 border-slate-100;
  }

  .markdown-body code {
    @apply bg-indigo-50 px-2 py-1 rounded-lg text-sm font-mono text-indigo-600 font-bold;
  }

  .markdown-body pre {
    @apply bg-slate-900 text-slate-100 p-8 rounded-[2rem] overflow-x-auto mb-16 shadow-2xl border-4 border-white/5;
  }

  .markdown-body table {
    @apply min-w-full border-collapse mb-16 rounded-[2rem] overflow-hidden shadow-2xl border border-slate-100;
  }

  .markdown-body th {
    @apply bg-slate-50 border-b p-6 text-left font-black text-slate-400 uppercase text-xs tracking-[0.2em];
  }

  .markdown-body td {
    @apply border-b p-6 text-slate-600 text-lg;
  }

  /* Mermaid enhancements */
  .mermaid-wrapper svg {
    @apply h-auto max-w-full transform transition-transform duration-700;
  }

  .zoom-content-container svg {
    @apply w-auto h-auto max-w-none scale-100 transform transition-all;
  }

  /* Animations */
  @keyframes bounce-slow {

    0%,
    100% {
      transform: translate(-50%, 0);
    }

    50% {
      transform: translate(-50%, -10px);
    }
  }

  .animate-bounce-slow {
    animation: bounce-slow 3s infinite ease-in-out;
  }

  .custom-scrollbar::-webkit-scrollbar {
    @apply w-2 h-2;
  }

  .custom-scrollbar::-webkit-scrollbar-track {
    @apply bg-transparent;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    @apply bg-white/20 rounded-full hover:bg-white/40;
  }
</style>
