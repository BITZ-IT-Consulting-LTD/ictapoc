import { marked } from 'marked';
import DOMPurify from 'isomorphic-dompurify';
const html = marked.parse('# Hello\n```mermaid\ngraph TD;\n```');
console.log('Original:\n', html);
console.log('Purified:\n', DOMPurify.sanitize(html, {ADD_ATTR: ['class', 'data-processed'], ADD_TAGS: ['style']}));
