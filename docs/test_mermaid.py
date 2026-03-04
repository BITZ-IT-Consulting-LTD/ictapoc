import os
import re

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"

def check_mermaid(content, filename):
    blocks = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
    issues = set()
    for block in blocks:
        lines = block.split('\n')
        for i, line in enumerate(lines):
            # check if there is an unquoted string after a shape
            # usually ID[Text] or ID(Text) or ID{Text} or ID>Text] or ID((Text))
            # Let's just find anything like `[` followed by text without `"` containing `(` or `)`
            
            # remove inline styles
            l = re.sub(r'style\s+.*', '', line)
            l = re.sub(r'classDef\s+.*', '', l)
            l = re.sub(r'class\s+.*', '', l)
            
            if "%%" in l or line.strip().startswith('style '):
                continue
            
            # find labels like [...], (...), {...} etc.
            # but wait, mermaid has a lot of shapes: [(...)] [[...]] etc.
            # let's look for matching brackets that contain `(` or `)` or `[` or `]` or `<` or `>` and don't have `"` 
            m_list = re.findall(r'(\[|\(|\{|\>)([^"\]\)\}]+)(\]|\)|\})', l)
            for begin, text, end in m_list:
                if re.search(r'[\(\)\[\]]', text) or "<br" in text.lower():
                    # might be an issue
                    # check if the text is entirely enclosed in quotes? regex didn't allow quotes
                    issues.add(line.strip())
                    
    return issues

for file in os.listdir(dir_path):
    if not file.endswith(".md"): continue
    path = os.path.join(dir_path, file)
    with open(path, "r") as f:
        content = f.read()
    issues = check_mermaid(content, file)
    if issues:
        print(f"--- {file} ---")
        for iss in issues:
            print(iss)

