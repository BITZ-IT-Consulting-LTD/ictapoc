import os
import re
import subprocess

dir_path = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"
files_to_export = [
    "ICT_Authority___Service_Delivery.md",
    "State_Department_of_ICT.md"
]

combined_md_path = os.path.join(dir_path, "temp_word_export.md")

combined_content = ""

for filename in files_to_export:
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # The prefix logic from the previous script
    mda_name = filename.replace("___Service_Delivery.md", "").replace(".md", "")
    
    # We will replace all ```mermaid ... ``` blocks with ![Label](image_path)
    # We use a simple strategy: split by '```mermaid', and for each piece after the first, find the closing '```'
    blocks = content.split("```mermaid")
    new_content = blocks[0]
    
    for i in range(1, len(blocks)):
        block = blocks[i]
        # Split by the closing backticks
        split_block = block.split("```", 1)
        if len(split_block) < 2:
            new_content += "```mermaid" + block # Malformed
            continue
            
        mermaid_code = split_block[0]
        remaining_text = split_block[1]
        
        # Determine AS-IS vs TO-BE from preceding text in new_content
        preceding_text = new_content[-300:].lower()
        label = f"diagram_{i}"
        
        if "as-is" in preceding_text or "current state" in preceding_text or "current process" in preceding_text:
            label = "AS_IS"
        elif "to-be" in preceding_text or "future state" in preceding_text or "future process" in preceding_text:
            label = "TO_BE"
            
        img_name = f"{mda_name}_{label}.png"
        img_path = f"exported_mermaids/{img_name}"
        
        # Add the image reference to the new content
        new_content += f"\n\n![{label} Diagram]({img_path})\n\n"
        new_content += remaining_text
        
    combined_content += new_content + "\n\n<br>\n\n<hr>\n\n"
    
with open(combined_md_path, "w", encoding="utf-8") as f:
    f.write(combined_content)

# Use pandoc to convert the combined markdown to docx and rtf
output_docx = os.path.join(dir_path, "ICT_and_Authority_Service_Delivery.docx")
output_doc = os.path.join(dir_path, "ICT_and_Authority_Service_Delivery.doc")
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
