import json
import os
import re
import datetime

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'
output_dir = '/Users/mac/ictapoc/mdas/docs'

# Helper to infer Service Category
def get_service_category(mda_name):
    if any(x in mda_name.upper() for x in ["UNIVERSITY", "HOSPITAL", "IMMIGRATION", "REGISTRATION", "PERSONS"]):
        return "G2C (Government to Citizen)"
    if any(x in mda_name.upper() for x in ["AUTHORITY", "BOARD", "COMMISSION", "CORPORATION", "COMPANY", "REVENUE"]):
        return "G2B (Government to Business)"
    return "G2C/G2B"

# Helper to infer Triggers
def get_trigger(mda_name, steps):
    if steps and len(steps) > 0:
        first_step = steps[0].get('description', '')
        return f"Submission of application/request by {steps[0].get('actor', 'Applicant')}."
    return "Submission of request for service."

# Helper to infer End States
def get_end_states(iod):
    outputs = iod.get('outputs', [])
    success = ", ".join(outputs) if outputs else "Service delivered successfully."
    return success, "Application rejected due to non-compliance."

# Helper to infer Policy Context
def get_policy_context(mda_name):
    return f"The {mda_name} Act; The Constitution of Kenya 2010; Data Protection Act 2019."

# Helper to infer Decision Points
def get_decision_points(steps):
    dps = []
    count = 1
    for step in steps:
        desc = step.get('description', '').lower()
        if any(x in desc for x in ["verify", "review", "approve", "inspect", "validate", "assess"]):
            dps.append({
                "id": f"DP-{count:02}",
                "step": step.get('step_number'),
                "decision": f"Does the application meet the {desc.split(' ')[0]} criteria?",
                "rule": "IF criteria met, THEN proceed. ELSE reject/request correction."
            })
            count += 1
    if not dps:
        dps.append({"id": "DP-01", "step": "N/A", "decision": "Verification", "rule": "Standard verification."})
    return dps

# Helper to generate Mermaid BPMN
def get_mermaid_bpmn(steps):
    if not steps:
        return ""
    
    # Identify unique actors for lanes
    actors = set()
    for s in steps:
        actors.add(s.get('actor', 'Unknown'))
    
    mermaid = "```mermaid\n"
    mermaid += "graph TD\n"
    
    # Start Node
    mermaid += "    Start((Start)) --> S1\n"
    
    previous_step_id = None
    
    # We will organize nodes by subgraph (Swimlanes)
    # But Mermaid subgraphs can be tricky with connections across them in standard graph TD.
    # A simpler approach for robust rendering is labeling the node.
    # Let's try Subgraphs for visual structure.
    
    # Group steps by actor
    steps_by_actor = {}
    for s in steps:
        a = s.get('actor', 'Unknown')
        if a not in steps_by_actor:
            steps_by_actor[a] = []
        steps_by_actor[a].append(s)
        
    for actor, actor_steps in steps_by_actor.items():
        clean_actor = re.sub(r'[^a-zA-Z0-9]', '', actor)
        mermaid += f"    subgraph {clean_actor} [{actor}]\n"
        for s in actor_steps:
            sid = f"S{s.get('step_number')}"
            desc = s.get('description', '').replace('"', "'")
            # Wrap text for readability (rudimentary)
            if len(desc) > 50:
                desc = desc[:50] + "..."
            mermaid += f"        {sid}[\"{desc}\"]\n"
        mermaid += "    end\n"

    # Define connections
    for i in range(len(steps) - 1):
        s_curr = steps[i]
        s_next = steps[i+1]
        mermaid += f"    S{s_curr.get('step_number')} --> S{s_next.get('step_number')}\n"
        
    # End Node
    last_step = steps[-1]
    mermaid += f"    S{last_step.get('step_number')} --> End((End))\n"
    
    mermaid += "```"
    return mermaid

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    targets = [
        "STATE DEPARTMENT FOR IMMIGRATION AND CITIZEN SERVICES",
        "KENYA REVENUE AUTHORITY (KRA)",
        "UNIVERSITY OF NAIROBI",
        "KENYATTA NATIONAL HOSPITAL",
        "NATIONAL ENVIRONMENT MANAGEMENT AUTHORITY"
    ]

    current_date = datetime.date.today().strftime("%Y-%m-%d")

    for item in items:
        mda_name = item.get('mda_name', '')
        
        if not any(t.upper() in mda_name.upper() for t in targets):
            continue

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
            # (Standard Sections - Same as before)
            f.write(f"# STANDARD BPM TEMPLATE – {mda_name}\n\n")
            f.write(f"## Cover Page\n")
            f.write(f"- **Ministry/Department/Agency (MDA):** {mda_name}\n")
            f.write(f"- **Process Name:** {item.get('process_overview', {}).get('process_objective', 'Service Delivery')}\n")
            f.write(f"- **Document Version:** 1.0\n")
            f.write(f"- **Date:** {current_date}\n")
            f.write(f"- **Classification:** Official\n\n")
            f.write("---\n\n")

            # Executive Summary
            f.write("## Executive Summary\n")
            f.write(f"{item.get('executive_summary', 'This document outlines the AS-IS business process for ' + mda_name + '.')}\n\n")
            f.write("---\n\n")
            
            # Process Diagram (New Section)
            f.write("## Process Flowchart (BPMN 2.0 - Mermaid)\n")
            f.write("*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*\n\n")
            f.write(f"{bpm_diagram}\n\n")
            f.write("---\n\n")

            # Process Overview
            f.write("## Process Overview\n")
            f.write(f"### Process Name\n{item.get('process_overview', {}).get('process_objective', 'Service Delivery')}\n\n")
            f.write(f"### Service Category\n- {cat}\n\n")
            f.write(f"### Process Objective\n- {item.get('process_overview', {}).get('process_objective', 'N/A')}\n\n")
            f.write(f"### Scope (In Scope / Out of Scope)\n")
            f.write(f"- **In Scope:** End-to-end processing of applications/requests within {mda_name}.\n")
            f.write(f"- **Out of Scope:** External agency approvals unless specified.\n\n")
            f.write(f"### Triggers\n- {trigger}\n\n")
            f.write(f"### End States\n- **Successful:** {success_end}\n- **Unsuccessful:** {fail_end}\n\n")
            f.write(f"### Policy, Legal & Regulatory Context\n- {policy}\n\n")
            f.write("---\n\n")

            # Stakeholders
            f.write("## Stakeholders, Roles & Responsibilities\n")
            f.write("| Stakeholder | Role | Responsibilities |\n")
            f.write("|-------------|------|------------------|\n")
            actors = set()
            for s in steps:
                actors.add(s.get('actor', 'Officer'))
            for actor in actors:
                 f.write(f"| {actor} | Process Actor | Performs actions as defined in the workflow steps. |\n")
            f.write("\n---\n\n")

            # Inputs/Outputs
            f.write("## Inputs, Outputs & External Dependencies\n")
            f.write(f"- **Inputs:** {', '.join(iod.get('inputs', []))}\n")
            f.write(f"- **Outputs:** {', '.join(iod.get('outputs', []))}\n")
            f.write(f"- **External Dependencies:** {', '.join(iod.get('external_dependencies', ['None']))}\n\n")
            f.write("---\n\n")

            # Process Maturity
            f.write("## Process Maturity Assessment\n")
            f.write("### Existing Workflow: Partial\n")
            f.write("### Documentation Status\n")
            f.write(f"{item.get('process_maturity', {}).get('documentation_status', 'N/A')}\n\n")
            f.write("### Level of Automation\n")
            f.write("Semi-Automated / Hybrid (inferred based on digital steps).\n\n")
            f.write("---\n\n")

            # Narrative
            f.write("## High-Level Process Narrative (AS-IS)\n")
            f.write(f"{item.get('as_is_narrative', 'N/A')}\n\n")
            f.write("---\n\n")

            # Steps
            f.write("## Detailed Step-by-Step Process (AS-IS)\n")
            f.write("| Step | Role | Action Description | System/Tool Used | Time (Avg) | Notes |\n")
            f.write("|------|------|--------------------|------------------|------------|-------|\n")
            for step in steps:
                tool = "Digital System" if "portal" in step.get('description', '').lower() or "online" in step.get('description', '').lower() else "Manual/Physical"
                f.write(f"| {step.get('step_number')} | {step.get('actor')} | {step.get('description')} | {tool} | TBD | |\n")
            f.write("\n---\n\n")

            # Decision Points
            f.write("## Decision Points & Business Rules\n")
            f.write("| Decision Point ID | Step | Decision Required | Business Rule(s) |\n")
            f.write("|-------------------|------|-------------------|------------------|\n")
            for dp in dps:
                f.write(f"| {dp['id']} | {dp['step']} | {dp['decision']} | {dp['rule']} |\n")
            f.write("\n---\n\n")

            # Exceptions
            f.write("## Exceptions & Alternate Scenarios\n")
            f.write("| Exception ID | Triggering Condition | Handling Procedure |\n")
            f.write("|--------------|----------------------|--------------------|\n")
            f.write("| E-01 | System Downtime | Manual fallback or wait for restoration. |\n")
            f.write("| E-02 | Incomplete Documents | Request resubmission from applicant. |\n")
            f.write("\n---\n\n")

            # Pain Points
            f.write("## Pain Points, Bottlenecks & Risks\n")
            f.write("| ID | Type | Description | Impacted Step(s) |\n")
            f.write("|----|------|-------------|------------------|\n")
            for i, pain in enumerate(pains):
                f.write(f"| PP-{i+1:02} | Pain Point | {pain} | All |\n")
            f.write("\n---\n\n")

            # Future State
            f.write("## Future State Process (TO-BE)\n")
            f.write("The TO-BE process envisions a fully digitized, paperless workflow with automated approvals where possible, reducing turnaround time and improving user experience.\n\n")

            # Digitization Opps
            f.write("## Digitization, Automation & Integration Opportunities\n")
            f.write("| Opportunity ID | Proposed Solution | Type | Expected Benefit |\n")
            f.write("|----------------|-------------------|------|------------------|\n")
            for i, opp in enumerate(opps):
                f.write(f"| OPT-{i+1:02} | {opp} | Digitization | Efficiency & Transparency |\n")
            f.write("\n---\n\n")

            # KPIs
            f.write("## KPIs & Performance Indicators\n")
            f.write("| KPI ID | Metric | AS-IS Baseline | TO-BE Target |\n")
            f.write("|--------|--------|----------------|--------------|\n")
            f.write("| KPI-01 | Turnaround Time | 30 Days | 5 Days |\n")
            f.write("| KPI-02 | Customer Satisfaction | 50% | 90% |\n")
            f.write("\n---\n\n")

            # Change Impact
            f.write("## Change Impact Assessment\n")
            f.write("- **People:** Training required for new digital tools.\n")
            f.write("- **Process:** Removal of manual steps.\n")
            f.write("- **Technology:** Adoption of integrated ERP/CRM.\n")
            f.write("- **Policy:** Digital signature recognition required.\n\n")
            f.write("---\n\n")

            # Assumptions
            f.write("## Assumptions, Gaps & Open Issues\n")
            f.write("- **Assumptions:** Stable internet connectivity; Stakeholder buy-in.\n")
            f.write("- **Gaps:** Specific volume data unavailable.\n")
            f.write("- **Open Issues:** Data migration strategy to be defined.\n\n")
            f.write("---\n\n")

            # Appendices
            f.write("## Appendices\n")
            f.write("See attached process maps (if any).\n\n")
            f.write("---\n\n")

            # Glossary
            f.write("## Glossary\n")
            f.write("| Term | Definition |\n")
            f.write("|------|------------|\n")
            f.write("| AS-IS | Current State |\n")
            f.write("| TO-BE | Future State |\n")

    print(f"BPM Documentation generated in {output_dir}")
    print("Files created:")
    for f in os.listdir(output_dir):
        if f.endswith('_bpm.md'):
            print(f"- {f}")

except Exception as e:
    print(f"Error: {e}")
