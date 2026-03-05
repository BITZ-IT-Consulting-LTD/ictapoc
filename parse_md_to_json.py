import os, glob, re, json
md_dir = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"
files = glob.glob(os.path.join(md_dir, "*.md"))
output = []
for f in files:
    if "Priority" in f or "temp" in f: continue
    c = open(f).read()
    
    # Process Name
    p_name = ""
    m_name = ""
    for line in c.split('\n'):
        if 'Process Name:' in line or 'Service Name:' in line:
            p_name = line.split(':')[-1].strip()
        if 'Ministry/Department/Agency' in line:
            m_name = line.split(':')[-1].strip()
    if not p_name: p_name = os.path.basename(f).replace('.md', '')
    if not m_name: m_name = "Unknown MDA"

    # Extract all tables
    tables = []
    current_table = []
    
    lines = c.split('\n')
    for line in lines:
        if '|' in line and ('Step' in line or 'Role' in line or 'Action' in line or len(current_table) > 0):
            if not line.strip().startswith('|'):
                if len(current_table) > 1: tables.append(current_table)
                current_table = []
                continue
            cols = [col.strip() for col in line.strip('|').split('|')]
            if set(cols) == {''} or all(c=='-' for x in cols for c in x): continue
            
            if len(cols) >= 3:
                current_table.append(cols)
        else:
            if len(current_table) > 1: tables.append(current_table)
            current_table = []
    
    if len(current_table) > 1: tables.append(current_table)
    
    if len(tables) > 0:
        as_is = tables[0]
        to_be = tables[1] if len(tables) > 1 else tables[0]
        output.append({
            "filename": os.path.basename(f),
            "mda_name": m_name.replace('**', ''),
            "process_name": p_name.replace('**', ''),
            "as_is": as_is,
            "to_be": to_be
        })

with open("/Users/mac/ictapoc/backend/priority_workflows.json", "w") as f:
    json.dump(output, f, indent=4)
print(f"Generated {len(output)}")
