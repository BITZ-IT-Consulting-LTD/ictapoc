import os
import re
import subprocess

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"
files_to_export = [
    "State_Department_of_ICT___Service_Delivery.md"
]

combined_md_path = os.path.join(dir_path, "temp_single_word_export.md")

combined_content = ""

for filename in files_to_export:
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    mda_name = "State_Department_of_ICT___Service_Delivery"
    
    blocks = content.split("```mermaid")
    new_content = blocks[0]
    
    for i in range(1, len(blocks)):
        block = blocks[i]
        split_block = block.split("```", 1)
        if len(split_block) < 2:
            new_content += "```mermaid" + block 
            continue
            
        mermaid_code = split_block[0]
        remaining_text = split_block[1]
        
        preceding_text = new_content[-300:].lower()
        label = f"diagram_{i}"
        
        if "as-is" in preceding_text or "current state" in preceding_text or "current process" in preceding_text:
            label = "AS_IS"
        elif "to-be" in preceding_text or "future state" in preceding_text or "future process" in preceding_text:
            label = "TO_BE"
            
        img_name = f"{mda_name}_{label}.png"
        img_path = f"exported_mermaids/{img_name}"
        
        # Render the image individually right now to ensure it's fully up to date!
        temp_mmd = os.path.join(dir_path, "temp.mmd")
        with open(temp_mmd, "w", encoding="utf-8") as tf:
            tf.write(mermaid_code.strip())
            
        print(f"Exporting updated {img_name}...")
        try:
            subprocess.run(
                ["npx", "-y", "@mermaid-js/mermaid-cli", "-i", temp_mmd, "-o", os.path.join(dir_path, img_path)], 
                cwd="/Users/mac/ictapoc", 
                check=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to export {img_name}")
            
        if os.path.exists(temp_mmd):
            os.remove(temp_mmd)
            
        # Add the image reference to the new content
        new_content += f"\n\n![{label} Diagram]({img_path})\n\n"
        new_content += remaining_text
        
    combined_content += new_content + "\n"
    
with open(combined_md_path, "w", encoding="utf-8") as f:
    f.write(combined_content)

output_docx = os.path.join(dir_path, "State_Department_of_ICT___Service_Delivery.docx")
output_doc = os.path.join(dir_path, "State_Department_of_ICT___Service_Delivery.doc")
print("Converting to Word document via Pandoc...")

try:
    subprocess.run(
        ["pandoc", combined_md_path, "-o", output_docx],
        cwd=dir_path,
        check=True
    )
    print(f"Successfully generated {output_docx}")

    # Generate an RTF file and name it .doc for older MS Word compatibility
    subprocess.run(
        ["pandoc", "-s", combined_md_path, "-t", "rtf", "-o", output_doc],
        cwd=dir_path,
        check=True
    )
    print(f"Successfully generated {output_doc} via RTF conversion")
except subprocess.CalledProcessError as e:
    print(f"Failed to generate Word document: {e}")

if os.path.exists(combined_md_path):
    os.remove(combined_md_path)
