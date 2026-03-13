import os, glob, re
md_dir = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"
files = glob.glob(os.path.join(md_dir, "*.md"))
for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f: content = f.read()
    if "Priority_MDAs" in filepath or "temp_" in filepath: continue
    
    process_match = re.search(r'\-\s*\*\*(?:Process Name|Service Name):\*\*\s*(.*)', content, re.IGNORECASE)
    if not process_match:
        print(f"FAILED PROCESS NAME: {os.path.basename(filepath)}")
        continue
    
    # check tables
    has_table = "| Step |" in content or "|Step|" in content or "| **Step** |" in content
    if not has_table:
        print(f"FAILED TABLE: {os.path.basename(filepath)}")
