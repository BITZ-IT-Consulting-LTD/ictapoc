import re
import os

files = [
    "mdas/docs_final/priority_mdas/Breakout_Room_1_High_Impact_Large_Registries.md",
    "mdas/docs_final/priority_mdas/Breakout_Room_2_Coordination_Culture_Specialised.md",
    "mdas/docs_final/priority_mdas/Breakout_Room_3_Policy_Economy_Foundational.md"
]

for file_path in files:
    with open(file_path, "r") as f:
        content = f.read()

    # The files already have links like [Name](./filename.md)
    # The user wants to "include the actual name of the MDA as a link to the document Process"
    # This might mean they want me to double check that the link text matches the document title,
    # or just confirming that the links in the previous message were rendered correctly.
    # Looking at the previous output, the files *do* have links. Let's just output the exact markdown
    # representation so the user can see them, or verify if the links are broken.
    
    # Wait, the user said "updat the .md to include the actual name of the MDA as a link to the document Process"
    # Let me check if the ones I added had the exact same link structure.
    # Yes:
    # - **[Internal Security and National Administration](./Internal_Security_and_National_Administration___Service_Delivery.md)**: Manages governance...
    
    print(f"--- {file_path} ---")
    lines = content.split('\n')
    for line in lines:
        if line.startswith("- **["):
            print(line)

