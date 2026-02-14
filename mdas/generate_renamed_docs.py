import json
import os
import re
import datetime
import zipfile

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'
output_dir = '/Users/mac/ictapoc/mdas/docs_renamed'
zip_filename = '/Users/mac/ictapoc/mdas/mda_bpm_docs_v2.zip'

# ... (Helper functions remain the same) ...
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
    # Remove special chars and limit length
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
    return re.sub(r'_+', '_', clean)[:100]  # Limit to 100 chars to avoid OS errors

try:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    count = 0

    print(f"Generating documentation for {len(items)} MDAs with Process Names...")

    for item in items:
        mda_name = item.get('mda_name', 'Unknown')
        
        # Determine Process Name for Filename
        # If we have a specific narrative like "Passport Application...", extract the core noun phrase
        # Or use the mandate we injected in the narrative/objective.
        # Let's derive a short "Service Name" from the narrative or objective.
        
        narrative = item.get('as_is_narrative', '')
        # Try to extract the first few words of the narrative or objective
        # E.g. "The passport application process..." -> "Passport Application Process"
        
        process_name = "Service_Delivery" # Default
        
        # Heuristics to find a good filename suffix
        if "passport" in narrative.lower(): process_name = "Passport_Application"
        elif "tax return" in narrative.lower(): process_name = "Tax_Return_Filing"
        elif "driving license" in narrative.lower(): process_name = "Driving_License_Renewal"
        elif "student admission" in narrative.lower(): process_name = "Student_Admission"
        elif "patient management" in narrative.lower(): process_name = "Patient_Management"
        elif "project procurement" in narrative.lower(): process_name = "Project_Procurement"
        elif "research proposal" in narrative.lower(): process_name = "Research_Proposal_Review"
        elif "commercial service" in narrative.lower(): process_name = "Commercial_Service_Order"
        elif "regulatory compliance" in narrative.lower(): process_name = "License_Application"
        elif "public service delivery" in narrative.lower(): process_name = "Public_Service_Delivery"
        elif "exchequer release" in narrative.lower(): process_name = "Exchequer_Release"
        elif "suspicious transaction" in narrative.lower(): process_name = "Suspicious_Transaction_Reporting"
        
        # Construct Filename: MDA_NAME - PROCESS_NAME
        filename_base = f"{sanitize_filename(mda_name)}___{process_name}"
        md_file = os.path.join(output_dir, f"{filename_base}.md")
        
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
            f.write(f"# {mda_name} – {process_name.replace('_', ' ')}\n\n")
            f.write(f"## Cover Page\n- **Ministry/Department/Agency (MDA):** {mda_name}\n- **Process Name:** {process_name.replace('_', ' ')}\n- **Document Version:** 1.0\n- **Date:** {current_date}\n- **Classification:** Official\n\n---\n\n")
            f.write("## Executive Summary\n" + f"{item.get('executive_summary', 'AS-IS business process for ' + mda_name + '.')}\n\n---\n\n")
            f.write("## Process Flowchart (BPMN 2.0 - Mermaid)\n*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*\n\n" + f"{bpm_diagram}\n\n---\n\n")
            # (Rest of the content remains standard)
            f.write("## Process Overview\n" + f"### Process Name\n{process_name.replace('_', ' ')}\n\n### Service Category\n- {cat}\n\n### Scope\n- **In Scope:** End-to-end processing within {mda_name}.\n\n### Triggers\n- {trigger}\n\n### End States\n- **Successful:** {success_end}\n\n---\n\n")
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

    print(f"Successfully generated {count} Renamed BPM documents.")

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
