import os
import re

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"

files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

issues_found = 0

for file in files:
    path = os.path.join(dir_path, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.findall(r'```mermaid(.*?)```', content, re.DOTALL)
    for i, block in enumerate(blocks):
        for line in block.split('\n'):
            line = line.strip()
            if not line or line.startswith('%') or line.startswith('style') or line.startswith('classDef') or line.startswith('class '):
                continue
            
            # Find definitions like id[Text] or id(Text) where Text does not start with "
            # and Text contains ( ) [ ] { } or <br
            # E.g. A[Get Details (System)]
            # We match id[label] where label starts with non-quote
            matches = re.findall(r'(\b[A-Za-z0-9_\-]+(?:\[|\(|\{|\{\{|>|\[\()([^"\]\)\}][^\]\)\}]*)(?:\]|\)|\}|\}\}|\]|\)\]))', line)
            
            for full_match, label in matches:
                if re.search(r'[\(\)\[\]<>]', label) or "br" in label.lower() or "br/" in label.lower():
                    print(f"{file}: {line}")
                    issues_found += 1

print(f"Total issues found: {issues_found}")
