import os
import re

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"

def fix_content(content):
    # Regex to find mermaid blocks
    blocks = re.findall(r'```mermaid(.*?)```', content, re.DOTALL)
    new_content = content
    
    # We'll use a regex that matches common NodeID[Label] formats
    # capturing groups: 1=NodeID and spaces, 2=opening shape, 3=text without quotes, 4=closing shape
    # The negative lookbehind `(?<!")` and negative lookahead `(?!\")` prevents matching already quoted labels
    # but since Python re module doesn't easily support variable length lookbehind, we will just ensure 
    # the text doesn't start with quotes.
    pattern = re.compile(
        r'(^\s*[A-Za-z0-9_]+|\s+[A-Za-z0-9_]+|-->\s*[A-Za-z0-9_]+|-x\s*[A-Za-z0-9_]+|==>\s*[A-Za-z0-9_]+|-.->\s*[A-Za-z0-9_]+)'  
        r'\s*(\(\(|\{\{|\[\[|\[\(|\(\[|\[/|\[\\|\[|\(|\{|>)'
        r'([^"\]\)\}\>][^\n\]\)\}\>]+?)'
        r'(\)\)|\}\}|\]\]|\)\]|\]\)|/\]|\\\]|\]|\)|\})'
    )
    
    def repl(m):
        pre = m.group(1)
        shape_open = m.group(2)
        txt = m.group(3)
        shape_close = m.group(4)
        
        # Don't quote if it's already quoted or if it's an arrow definition somehow matching
        if txt.strip().startswith('"') and txt.strip().endswith('"'):
            return m.group(0)
            
        # We only care about quoting if it has spaces, parens, brackets, or br tags
        if re.search(r'[\(\)\[\]<>]', txt) or "br" in txt.lower() or " / " in txt or " - " in txt or " " in txt or "-" in txt:
            return f'{pre}{shape_open}"{txt}"{shape_close}'
        
        return m.group(0)

    for block in blocks:
        new_block = block
        lines = new_block.split('\n')
        new_lines = []
        for line in lines:
            line_strip = line.strip()
            # skip comments and style directives
            if not line_strip or line_strip.startswith('%') or line_strip.startswith('style') or line_strip.startswith('class') or line_strip.startswith('linkStyle'):
                new_lines.append(line)
                continue
            
            # Sub lines
            nl = pattern.sub(repl, line)
            # Apply twice in case of multiple nodes on the same line like A[foo] --> B[bar]
            nl = pattern.sub(repl, nl)
            nl = pattern.sub(repl, nl)
            
            new_lines.append(nl)
            
        new_block_str = '\n'.join(new_lines)
        if new_block_str != new_block:
            new_content = new_content.replace("```mermaid" + block + "```", "```mermaid" + new_block_str + "```")
            
    return new_content

files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
fixed_count = 0

for f in files:
    path = os.path.join(dir_path, f)
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    new_content = fix_content(content)
    if new_content != content:
        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        fixed_count += 1
        print(f"Fixed unquoted Mermaid labels in {f}")
        
print(f"Total files fixed: {fixed_count}")
