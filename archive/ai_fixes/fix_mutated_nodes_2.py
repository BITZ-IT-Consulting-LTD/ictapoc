import os

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"

def fix_end_process_quotes(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        
    new_content = content.replace("(\"('", "((\"").replace("'\"))", "\"))")
    
    if new_content != content:
        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Fixed mutated end nodes in: {os.path.basename(path)}")

files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

for f in files:
    path = os.path.join(dir_path, f)
    fix_end_process_quotes(path)
