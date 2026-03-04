import os
import re

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"

def fix_file(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        
    blocks = re.findall(r'```mermaid(.*?)```', content, re.DOTALL)
    new_content = content
    
    for block in blocks:
        # replace `("` with `('` and `")` with `')` inside mermaid blocks
        new_block = block.replace('("', "('").replace('")', "')")
        new_block = new_block.replace(':"', ": '").replace('"]', "']")
        
        # But wait, `"]` is used at the end of every node!
        # If I replace `"]` with `']` it breaks `Node["Text"]`!
        # Instead, I'll match ID["Text"] explicitly where Text contains quotes
        
        # Best way is to split into lines and process each node label
        lines = block.split('\n')
        new_lines = []
        for line in lines:
            line_strip = line.strip()
            if not line_strip or line_strip.startswith('%') or line_strip.startswith('style') or line_strip.startswith('class '):
                new_lines.append(line)
                continue
                
            nl = line
            # find all ["..."] 
            # we can look for `\["` followed by everything up to `"` that is followed by `\]`
            # wait, if there are interior quotes, `(.*)` is better
            matches = re.finditer(r'\["(.*?)"\]', line)
            for m in matches:
                inner_text = m.group(1)
                if '"' in inner_text:
                    fixed_text = inner_text.replace('"', "'")
                    nl = nl.replace(f'["{inner_text}"]', f'["{fixed_text}"]')
            new_lines.append(nl)
            
        new_block_str = '\n'.join(new_lines)
        if new_block_str != block:
            new_content = new_content.replace("```mermaid" + block + "```", "```mermaid" + new_block_str + "```")
            
    if new_content != content:
        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Fixed nested quotes in: {os.path.basename(path)}")

files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

for f in files:
    path = os.path.join(dir_path, f)
    fix_file(path)
