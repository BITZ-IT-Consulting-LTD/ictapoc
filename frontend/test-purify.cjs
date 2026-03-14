const { marked } = require('marked');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');
const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);
const html = marked.parse('# Hello\n```mermaid\ngraph TD;\n```');
console.log('Original:\n', html);
console.log('Purified:\n', DOMPurify.sanitize(html, {ADD_ATTR: ['class', 'data-processed'], ADD_TAGS: ['style']}));
