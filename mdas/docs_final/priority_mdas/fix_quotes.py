import os
import re

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"

def fix_inner_quotes(content):
    blocks = re.findall(r'```mermaid(.*?)```', content, re.DOTALL)
    new_content = content
    
    for block in blocks:
        new_block = block
        lines = new_block.split('\n')
        new_lines = []
        for line in lines:
            line_strip = line.strip()
            if not line_strip or line_strip.startswith('%') or line_strip.startswith('style') or line_strip.startswith('class '):
                new_lines.append(line)
                continue
                
            nl = line
            # We look for nodes in the format: NodeID["..."]
            # We match `NodeID["` then any characters except `]` or `)` up to `"]`
            # Actually we can match `(\(\(|\{\{|\[\[|\[\(|\(\[|\[/|\[\\|\[|\(|\{|>)"` 
            # and `"(\)\)|\}\}|\]\]|\)\]|\]\)|/\]|\\\]|\]|\)|\})`
            
            def repl(m):
                pre = m.group(1) # e.g. Node[
                inner = m.group(2) # e.g. Text with "quotes"
                post = m.group(3) # e.g. ]
                # remove any double quotes from inner
                inner = inner.replace('"', "'")
                return f'{pre}{inner}{post}'
            
            # This regex looks for `\["` followed by characters (not `]`) ending in `"\]`
            nl = re.sub(r'(\["|\[\("|\[\{"|>")([^\]\)\}]+?)("\]|"\)\]|"\}\]|"\])', repl, nl)
            nl = re.sub(r'(\("|\[/"|\(\[")([^\]\)\}]+?)("\)|"/\]|"\)\])', repl, nl)
            
            new_lines.append(nl)
            
        new_block_str = '\n'.join(new_lines)
        if new_block_str != new_block:
            new_content = new_content.replace("```mermaid" + block + "```", "```mermaid" + new_block_str + "```")
            
    return new_content

files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

for f in files:
    path = os.path.join(dir_path, f)
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    new_content = fix_inner_quotes(content)
    if new_content != content:
        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Fixed internal quotes in: {f}")
