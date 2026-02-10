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

const marked = new Marked();

// Configure mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: 'inherit',
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

const renderMermaid = async () => {
  if (!markdownBody.value) return;
  
  // Find all code blocks that might be mermaid
  // Marked adds 'language-mermaid' class to the code element
  const codeBlocks = markdownBody.value.querySelectorAll('pre code.language-mermaid');
  console.log(`Found ${codeBlocks.length} mermaid blocks.`);
  
  if (codeBlocks.length === 0) return;

  const nodes = [];

  for (const block of codeBlocks) {
    const pre = block.parentElement;
    const code = block.textContent;
    
    // Create a new div for mermaid
    const mermaidDiv = document.createElement('div');
    mermaidDiv.className = 'mermaid flex justify-center my-6';
    mermaidDiv.textContent = code;
    
    // Replace the pre block with the mermaid div
    pre.replaceWith(mermaidDiv);
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
  @apply text-3xl font-bold border-b pb-4 mb-6 text-slate-800;
}
.markdown-body h2 {
  @apply text-2xl font-semibold border-b pb-2 mb-4 mt-8 text-slate-800;
}
.markdown-body h3 {
  @apply text-xl font-semibold mb-3 mt-6 text-slate-700;
}
.markdown-body p {
  @apply mb-4 leading-relaxed text-slate-600;
}
.markdown-body ul {
  @apply list-disc pl-6 mb-4 space-y-2 text-slate-600;
}
.markdown-body blockquote {
  @apply border-l-4 border-indigo-500 pl-4 py-1 bg-slate-50 italic rounded-r-md mb-4 text-slate-700;
}
.markdown-body hr {
  @apply my-8 border-slate-200;
}
.markdown-body code {
  @apply bg-slate-100 px-1 py-0.5 rounded text-sm font-mono text-indigo-600;
}
.markdown-body pre {
  @apply bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto mb-6 shadow-md;
}
.markdown-body table {
  @apply min-w-full border-collapse mb-6;
}
.markdown-body th {
  @apply bg-slate-100 border p-2 text-left font-semibold;
}
.markdown-body td {
  @apply border p-2;
}
.mermaid-chart svg {
  @apply max-w-full h-auto shadow-sm p-4 bg-white rounded-lg border;
}
</style>
