import json
import os
import re

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'
output_dir = '/Users/mac/ictapoc/mdas/docs'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    # Select representative samples
    targets = [
        "STATE DEPARTMENT FOR IMMIGRATION AND CITIZEN SERVICES",
        "KENYA REVENUE AUTHORITY (KRA)",
        "UNIVERSITY OF NAIROBI",
        "KENYATTA NATIONAL HOSPITAL",
        "NATIONAL ENVIRONMENT MANAGEMENT AUTHORITY"
    ]

    for item in items:
        mda_name = item.get('mda_name', '')
        
        # Only process targets for now (to avoid 442 files)
        if not any(t.upper() in mda_name.upper() for t in targets):
            continue

        slug = re.sub(r'[^a-zA-Z0-9]', '_', mda_name).lower()
        md_file = os.path.join(output_dir, f"{slug}.md")

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {mda_name}\n\n")
            f.write(f"**Sector:** {item.get('sector', 'N/A')}\n\n")
            
            f.write("## 1. Executive Summary\n")
            f.write(f"{item.get('executive_summary', 'N/A')}\n\n")

            f.write("## 2. Process Overview\n")
            proc_overview = item.get('process_overview', {})
            f.write(f"**Objective:** {proc_overview.get('process_objective', 'N/A')}\n\n")
            
            f.write("## 3. As-Is Process Workflow\n")
            narrative = item.get('as_is_narrative', 'N/A')
            f.write(f"*{narrative}*\n\n")
            
            steps = item.get('as_is_steps', [])
            if steps:
                f.write("| Step | Actor | Description |\n")
                f.write("|------|-------|-------------|\n")
                for step in steps:
                    f.write(f"| {step.get('step_number')} | {step.get('actor')} | {step.get('description')} |\n")
            else:
                f.write("*No detailed steps defined.*\n")
            f.write("\n")

            f.write("## 4. Key Data Elements\n")
            iod = item.get('inputs_outputs_dependencies', {})
            f.write("### Inputs\n")
            for inp in iod.get('inputs', []):
                f.write(f"- {inp}\n")
            f.write("\n")
            
            f.write("### Outputs\n")
            for out in iod.get('outputs', []):
                f.write(f"- {out}\n")
            f.write("\n")

            f.write("## 5. Pain Points & Opportunities\n")
            f.write("### Pain Points\n")
            for pain in item.get('pain_points_bottlenecks_risks', []):
                f.write(f"- {pain}\n")
            f.write("\n")

            f.write("### Digitization Opportunities\n")
            for opp in item.get('digitization_opportunities', []):
                f.write(f"- {opp}\n")
            f.write("\n")

            f.write("---\n")
            f.write(f"*Documentation Status: {item.get('process_maturity', {}).get('documentation_status', 'N/A')}*\n")

    print(f"Documentation generated in {output_dir}")
    print("Files created:")
    for f in os.listdir(output_dir):
        if f.endswith('.md'):
            print(f"- {f}")

except Exception as e:
    print(f"Error: {e}")
