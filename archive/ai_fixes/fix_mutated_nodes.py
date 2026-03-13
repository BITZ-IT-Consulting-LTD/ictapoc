import os
import re

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"

def fix_end_process_quotes(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        
    # We want to replace `"('Text'"))` with `(("Text"))` 
    # and `"('Text'\"))` with `(("Text"))` etc.
    # basically `("('` becomes `(("'`  or just `(("`
    # The actual pattern shown in the grep is `EndProcess("('End Process'"))`
    # Let's just use regex to fix `("('...'\"))` -> `(("..."))` universally for any node
    
    # capturing 1: the node ID, 2: inner string
    pattern = re.compile(r'(\w+)\("\(\'(.*?)\'\)"\)')
    new_content = pattern.sub(r'\1(("\2"))', content)
    
    if new_content != content:
        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Fixed mutated end nodes in: {os.path.basename(path)}")

files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

for f in files:
    path = os.path.join(dir_path, f)
    fix_end_process_quotes(path)
