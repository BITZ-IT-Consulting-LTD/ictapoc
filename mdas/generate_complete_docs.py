import json
import os
import re
import datetime
import zipfile

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'
output_dir = '/Users/mac/ictapoc/mdas/docs_final'
zip_filename = '/Users/mac/ictapoc/mdas/mda_bpm_docs_complete.zip'

# ... (Helper functions from before) ...
# Copying previous helpers for context
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

def sanitize_filename(name):
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
    return re.sub(r'_+', '_', clean)[:100]

try:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    count = 0

    print(f"Generating Complete Documentation (AS-IS + TO-BE BPMN) for {len(items)} MDAs...")

    for item in items:
        mda_name = item.get('mda_name', 'Unknown')
        narrative = item.get('as_is_narrative', '')
        
        # Process Name Inference
        process_name = "Service_Delivery"
        if "passport" in narrative.lower(): process_name = "Passport_Application"
        elif "tax return" in narrative.lower(): process_name = "Tax_Return_Filing"
        elif "driving license" in narrative.lower(): process_name = "Driving_License_Renewal"
        elif "student" in narrative.lower(): process_name = "Student_Admission"
        elif "patient" in narrative.lower(): process_name = "Patient_Management"
        elif "license" in narrative.lower() or "permit" in narrative.lower(): process_name = "Licensing_and_Permitting"
        elif "loan" in narrative.lower(): process_name = "Loan_Processing"
        elif "cabinet memo" in narrative.lower(): process_name = "Cabinet_Memo_Processing"
        
        filename_base = f"{sanitize_filename(mda_name)}___{process_name}"
        md_file = os.path.join(output_dir, f"{filename_base}.md")
        
        # Data
        iod = item.get('inputs_outputs_dependencies', {})
        as_is_steps = item.get('as_is_steps', [])
        to_be_data = item.get('to_be_process', {})
        to_be_steps = to_be_data.get('steps', [])
        to_be_narrative = to_be_data.get('narrative', 'Process automation.')
        
        pains = item.get('pain_points_bottlenecks_risks', [])
        opps = item.get('digitization_opportunities', [])
        
        cat = get_service_category(mda_name)
        trigger = get_trigger(mda_name, as_is_steps)
        success_end, fail_end = get_end_states(iod)
        policy = get_policy_context(mda_name)
        dps = get_decision_points(as_is_steps)
        
        # Generate TWO diagrams
        asis_diagram = get_mermaid_bpmn(as_is_steps)
        tobe_diagram = get_mermaid_bpmn(to_be_steps)

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {mda_name} – {process_name.replace('_', ' ')}\n\n")
            f.write(f"## Cover Page\n- **Ministry/Department/Agency (MDA):** {mda_name}\n- **Process Name:** {process_name.replace('_', ' ')}\n- **Document Version:** 1.0\n- **Date:** {current_date}\n- **Classification:** Official\n\n---\n\n")
            f.write("## Executive Summary\n" + f"{item.get('executive_summary', 'AS-IS business process for ' + mda_name + '.')}\n\n---\n\n")
            
            # AS-IS Diagram
            f.write("## 1. AS-IS Process Flowchart (BPMN 2.0)\n*Current State visualization.*\n\n" + f"{asis_diagram}\n\n---\n\n")
            
            # Standard Sections
            f.write("## Process Overview\n" + f"### Process Name\n{process_name.replace('_', ' ')}\n\n### Service Category\n- {cat}\n\n### Scope\n- **In Scope:** End-to-end processing within {mda_name}.\n\n### Triggers\n- {trigger}\n\n### End States\n- **Successful:** {success_end}\n\n### Policy Context\n- {policy}\n\n---\n\n")
            f.write("## Stakeholders\n| Stakeholder | Role | Responsibilities |\n|---|---|---|\n")
            actors = set(s.get('actor', 'Officer') for s in as_is_steps)
            for actor in actors: f.write(f"| {actor} | Process Actor | Performs actions as defined in steps. |\n")
            f.write("\n---\n\n")
            f.write("## Detailed Process (AS-IS)\n| Step | Role | Action | Tool | Notes |\n|---|---|---|---|---|\n")
            for step in as_is_steps:
                tool = "Digital" if "portal" in step.get('description', '').lower() else "Manual"
                f.write(f"| {step.get('step_number')} | {step.get('actor')} | {step.get('description')} | {tool} | |\n")
            f.write("\n---\n\n")
            f.write("## Pain Points & Opportunities\n### Pain Points\n")
            for p in pains: f.write(f"- {p}\n")
            f.write("\n### Opportunities\n")
            for o in opps: f.write(f"- {o}\n")
            f.write("\n---\n\n")
            
            # TO-BE Section (Enhanced)
            f.write("## 2. TO-BE Process Flowchart (BPMN 2.0)\n*Future State visualization (Optimized).*\n\n" + f"{tobe_diagram}\n\n")
            f.write("## Future State Process (TO-BE)\n")
            f.write(f"### Narrative\n{to_be_narrative}\n\n")
            f.write("### Optimized Steps (Digital)\n| Step | Actor | Action | System |\n|---|---|---|---|\n")
            for step in to_be_steps:
                f.write(f"| {step.get('step_number')} | {step.get('actor')} | {step.get('description')} | {step.get('system', 'System')} |\n")
            f.write("\n---\n\n")
            
            f.write("## References\nDerived from official mandates.\n")

        count += 1

    print(f"Successfully generated {count} Complete BPM documents.")

    # Create ZIP
    print(f"Zipping files to {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.md'):
                    zipf.write(os.path.join(root, file), arcname=file)
    
    print(f"Done. Zip archive created at: {zip_filename}")

except Exception as e:
    print(f"Error: {e}")
