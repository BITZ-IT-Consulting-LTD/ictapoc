import os
import re
import subprocess
import shutil

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"
out_dir = os.path.join(dir_path, "exported_mermaids")

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

total_exported = 0
failed = []

for filename in files:
    # Skip some files that are just combinations or matrices
    if filename in ["temp_master_combined.md", "Priority_MDAs_Justification_Matrix.md"]:
        continue
        
    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    blocks = re.split(r'```mermaid', content)
    if len(blocks) <= 1:
        continue
        
    # Clean up the filename to get just the MDA name
    mda_name = filename.replace("___Service_Delivery.md", "").replace("___Passport_Application.md", "")
    
    for i in range(1, len(blocks)):
        block_text = blocks[i].split('```')[0].strip()
        preceding_text = blocks[i-1][-300:].lower() 
        
        label = f"diagram_{i}"
        if "as-is" in preceding_text or "current state" in preceding_text or "current process" in preceding_text:
            label = "AS_IS"
        elif "to-be" in preceding_text or "future state" in preceding_text or "future process" in preceding_text:
            label = "TO_BE"
            
        out_name = f"{mda_name}_{label}.png"
        out_path = os.path.join(out_dir, out_name)
        
        temp_mmd = os.path.join(dir_path, "temp.mmd")
        with open(temp_mmd, "w", encoding="utf-8") as f:
            f.write(block_text)
            
        print(f"Exporting {out_name}...")
        try:
            subprocess.run(
                ["npx", "-y", "@mermaid-js/mermaid-cli", "-i", temp_mmd, "-o", out_path], 
                cwd="/Users/mac/ictapoc", 
                check=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
            total_exported += 1
        except subprocess.CalledProcessError as e:
            print(f"Failed to export {out_name}")
            failed.append(out_name)
            
    if os.path.exists(temp_mmd):
        os.remove(temp_mmd)

print(f"Export complete. Successfully exported {total_exported} images.")
if failed:
    print(f"Failed exports: {failed}")
