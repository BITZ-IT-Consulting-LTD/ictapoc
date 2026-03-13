import os
import re
import subprocess
import hashlib

# Configuration
input_dir = '.'
output_docx = 'Priority_MDAs_Blueprints_Combined_With_Diagrams.docx'
image_dir = 'temp_images'
master_md = 'temp_master_combined.md'

if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Pattern to find mermaid blocks
mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)

def render_mermaid(content):
    # Create a hash of the content for a unique filename
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    mmd_file = os.path.join(image_dir, f"{content_hash}.mmd")
    png_file = os.path.join(image_dir, f"{content_hash}.png")
    
    if not os.path.exists(png_file):
        with open(mmd_file, 'w') as f:
            f.write(content)
        
        try:
            # Use mmdc to render
            subprocess.run(['mmdc', '-i', mmd_file, '-o', png_file, '-b', 'transparent'], 
                           check=True, capture_output=True)
        except Exception as e:
            print(f"Error rendering mermaid: {e}")
            return None
            
    return png_file

# Files to process in order
files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
# Put matrix first
if 'Priority_MDAs_Justification_Matrix.md' in files:
    files.remove('Priority_MDAs_Justification_Matrix.md')
    files = ['Priority_MDAs_Justification_Matrix.md'] + sorted(files)

with open(master_md, 'w') as master:
    for filename in files:
        if filename == master_md:
            continue
            
        print(f"Processing {filename}...")
        with open(filename, 'r') as f:
            content = f.read()
        
        # Replace mermaid blocks with image links
        def replace_func(match):
            mermaid_content = match.group(1)
            img_path = render_mermaid(mermaid_content)
            if img_path:
                return f"\n\n![Process Flow]({img_path})\n\n"
            return match.group(0) # Fallback to code block if rendering fails
            
        processed_content = mermaid_pattern.sub(replace_func, content)
        
        master.write(f"\n\n# Source: {filename}\n\n")
        master.write(processed_content)
        master.write("\n\n---\n\n")

# Convert to DOCX using pandoc
print("Converting to DOCX...")
try:
    subprocess.run(['pandoc', master_md, '-o', output_docx], check=True)
    print(f"Success! Created {output_docx}")
except Exception as e:
    print(f"Pandoc conversion failed: {e}")

# Cleanup
# os.remove(master_md)
