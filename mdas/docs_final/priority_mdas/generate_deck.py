import os
import re

def main():
    mda_dir = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas/"
    md_files = [f for f in os.listdir(mda_dir) if f.endswith(".md") and f != "Priority_MDAs_Justification_Matrix.md" and f != "temp_master_combined.md"]
    
    deck_content = """# KDEAP [16] - Proof of Concept v2
## Digital Service Architecture Programme
---

"""
    
    for filename in sorted(md_files):
        filepath = os.path.join(mda_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
            # Extract MDA Name
            mda_match = re.search(r'- \*\*Ministry/Department/Agency \(MDA\):\*\* (.*)', content)
            department_match = re.search(r'- \*\*Department:\*\* (.*)', content)
            authority_match = re.search(r'- \*\*Authority:\*\* (.*)', content)
            office_match = re.search(r'- \*\*Office:\*\* (.*)', content)
            
            mda_name = mda_match.group(1) if mda_match else filename.replace(".md", "").replace("_", " ")
            if department_match: mda_name = department_match.group(1)
            elif authority_match: mda_name = authority_match.group(1)
            elif office_match: mda_name = office_match.group(1)
            
            # Extract Process Name
            process_match = re.search(r'- \*\*Process Name:\*\* (.*)', content)
            process_name = process_match.group(1) if process_match else "Core Service Delivery"
            
            # Extract Pain Points
            pain_points_section = re.search(r'### Pain Points\n(.*?)(?=\n### |\n## )', content, re.DOTALL)
            pain_points = ""
            if pain_points_section:
                 # Get list items
                 items = re.findall(r'- (.*)', pain_points_section.group(1))
                 pain_points = "\n".join([f"  * {item}" for item in items[:3]]) # Limit to top 3
            
            # Extract Opportunities/TO-BE Narrative
            opps_section = re.search(r'### Opportunities\n(.*?)(?=\n### |\n## )', content, re.DOTALL)
            opps = ""
            if opps_section:
                items = re.findall(r'- (.*)', opps_section.group(1))
                opps = "\n".join([f"  * {item}" for item in items[:3]])

            deck_content += f"""## {mda_name}
### {process_name}

**Current Pain Points:**
{pain_points}

**Digital Transformation (TO-BE):**
{opps}

---

"""

    with open("/Users/mac/ictapoc/mdas/docs_final/priority_mdas/KDEAP_PoC_v2_Deck.md", "w") as out_f:
        out_f.write(deck_content)
        
    print("Deck generated at /Users/mac/ictapoc/mdas/docs_final/priority_mdas/KDEAP_PoC_v2_Deck.md")

if __name__ == "__main__":
    main()
