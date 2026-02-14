import json
import os
import re
import datetime
import zipfile

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'
output_dir = '/Users/mac/ictapoc/mdas/docs'
zip_filename = '/Users/mac/ictapoc/mdas/mda_bpm_docs.zip'

# ... (Helper functions remain the same: get_service_category, get_trigger, etc.) ...
# Repeating concise versions for the script context
def get_service_category(mda_name):
    if any(x in mda_name.upper() for x in ["UNIVERSITY", "HOSPITAL", "IMMIGRATION", "REGISTRATION", "PERSONS"]): return "G2C (Government to Citizen)"
    if any(x in mda_name.upper() for x in ["AUTHORITY", "BOARD", "COMMISSION", "CORPORATION", "COMPANY", "REVENUE"]): return "G2B (Government to Business)"
    return "G2C/G2B"

def get_trigger(mda_name, steps):
    if steps and len(steps) > 0: return f"Submission of application/request by {steps[0].get('actor', 'Applicant')}."
    return "Submission of request for service."

def get_end_states(iod):
    outputs = iod.get('outputs', [])
    success = ", ".join(outputs) if outputs else "Service delivered successfully."
    return success, "Application rejected due to non-compliance."

def get_policy_context(mda_name):
    return f"The {mda_name} Act; The Constitution of Kenya 2010; Data Protection Act 2019."

def get_decision_points(steps):
    dps = []
    count = 1
    for step in steps:
        desc = step.get('description', '').lower()
        if any(x in desc for x in ["verify", "review", "approve", "inspect", "validate", "assess"]):
            dps.append({"id": f"DP-{count:02}", "step": step.get('step_number'), "decision": f"Does the application meet the {desc.split(' ')[0]} criteria?", "rule": "IF criteria met, THEN proceed. ELSE reject/request correction."})
            count += 1
    if not dps: dps.append({"id": "DP-01", "step": "N/A", "decision": "Verification", "rule": "Standard verification."})
    return dps

def get_mermaid_bpmn(steps):
    if not steps: return ""
    mermaid = "```mermaid\ngraph TD\n    Start((Start)) --> S1\n"
    steps_by_actor = {}
    for s in steps:
        a = s.get('actor', 'Unknown')
        if a not in steps_by_actor: steps_by_actor[a] = []
        steps_by_actor[a].append(s)
    for actor, actor_steps in steps_by_actor.items():
        clean_actor = re.sub(r'[^a-zA-Z0-9]', '', actor)
        mermaid += f"    subgraph {clean_actor} [{actor}]\n"
        for s in actor_steps:
            sid = f"S{s.get('step_number')}"
            desc = s.get('description', '').replace('"', "'")
            if len(desc) > 50: desc = desc[:50] + "..."
            mermaid += f"        {sid}[\"{desc}\"]\n"
        mermaid += "    end\n"
    for i in range(len(steps) - 1):
        mermaid += f"    S{steps[i].get('step_number')} --> S{steps[i+1].get('step_number')}\n"
    if steps: mermaid += f"    S{steps[-1].get('step_number')} --> End((End))\n"
    mermaid += "```"
    return mermaid

try:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    count = 0

    print(f"Generating documentation for {len(items)} MDAs...")

    for item in items:
        mda_name = item.get('mda_name', '')
        # FILTER REMOVED: Processing ALL items now
        
        slug = re.sub(r'[^a-zA-Z0-9]', '_', mda_name).lower()
        md_file = os.path.join(output_dir, f"{slug}_bpm.md")
        
        iod = item.get('inputs_outputs_dependencies', {})
        steps = item.get('as_is_steps', [])
        pains = item.get('pain_points_bottlenecks_risks', [])
        opps = item.get('digitization_opportunities', [])
        
        cat = get_service_category(mda_name)
        trigger = get_trigger(mda_name, steps)
        success_end, fail_end = get_end_states(iod)
        policy = get_policy_context(mda_name)
        dps = get_decision_points(steps)
        bpm_diagram = get_mermaid_bpmn(steps)

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# STANDARD BPM TEMPLATE – {mda_name}\n\n")
            f.write(f"## Cover Page\n- **Ministry/Department/Agency (MDA):** {mda_name}\n- **Process Name:** {item.get('process_overview', {}).get('process_objective', 'Service Delivery')}\n- **Document Version:** 1.0\n- **Date:** {current_date}\n- **Classification:** Official\n\n---\n\n")
            f.write("## Executive Summary\n" + f"{item.get('executive_summary', 'AS-IS business process for ' + mda_name + '.')}\n\n---\n\n")
            f.write("## Process Flowchart (BPMN 2.0 - Mermaid)\n*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*\n\n" + f"{bpm_diagram}\n\n---\n\n")
            f.write("## Process Overview\n" + f"### Process Name\n{item.get('process_overview', {}).get('process_objective', 'Service Delivery')}\n\n### Service Category\n- {cat}\n\n### Process Objective\n- {item.get('process_overview', {}).get('process_objective', 'N/A')}\n\n### Scope\n- **In Scope:** End-to-end processing within {mda_name}.\n- **Out of Scope:** External agency approvals.\n\n### Triggers\n- {trigger}\n\n### End States\n- **Successful:** {success_end}\n- **Unsuccessful:** {fail_end}\n\n### Policy Context\n- {policy}\n\n---\n\n")
            f.write("## Stakeholders\n| Stakeholder | Role | Responsibilities |\n|---|---|---|\n")
            actors = set(s.get('actor', 'Officer') for s in steps)
            for actor in actors: f.write(f"| {actor} | Process Actor | Performs actions as defined in steps. |\n")
            f.write("\n---\n\n")
            f.write("## Inputs & Outputs\n" + f"- **Inputs:** {', '.join(iod.get('inputs', []))}\n- **Outputs:** {', '.join(iod.get('outputs', []))}\n\n---\n\n")
            f.write("## Detailed Process (AS-IS)\n| Step | Role | Action | Tool | Notes |\n|---|---|---|---|---|\n")
            for step in steps:
                tool = "Digital" if "portal" in step.get('description', '').lower() else "Manual"
                f.write(f"| {step.get('step_number')} | {step.get('actor')} | {step.get('description')} | {tool} | |\n")
            f.write("\n---\n\n")
            f.write("## Pain Points & Opportunities\n### Pain Points\n")
            for p in pains: f.write(f"- {p}\n")
            f.write("\n### Opportunities\n")
            for o in opps: f.write(f"- {o}\n")
            f.write("\n---\n\n")
            f.write("## KPIs\n| KPI | Baseline | Target |\n|---|---|---|\n| Turnaround Time | 30 Days | 5 Days |\n| CSAT | 50% | 90% |\n")

        count += 1

    print(f"Successfully generated {count} BPM documents.")

    # Create ZIP
    print(f"Zipping files to {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('_bpm.md'):
                    zipf.write(os.path.join(root, file), arcname=file)
    
    print(f"Done. Zip archive created at: {zip_filename}")

except Exception as e:
    print(f"Error: {e}")
