import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    stats = {
        "missing_exec_summary": 0,
        "missing_objective": 0,
        "missing_inputs": 0,
        "missing_outputs": 0,
        "missing_pain_points": 0,
        "missing_digitization_opps": 0
    }

    for item in items:
        # Check Executive Summary
        if not item.get('executive_summary'):
            stats["missing_exec_summary"] += 1
            
        # Check Objective
        proc_overview = item.get('process_overview', {})
        if not proc_overview.get('process_objective'):
            stats["missing_objective"] += 1
            
        # Check Inputs/Outputs
        iod = item.get('inputs_outputs_dependencies', {})
        if not iod.get('inputs') or len(iod.get('inputs')) == 0:
            stats["missing_inputs"] += 1
        if not iod.get('outputs') or len(iod.get('outputs')) == 0:
            stats["missing_outputs"] += 1
            
        # Check Pain Points
        if not item.get('pain_points_bottlenecks_risks') or len(item.get('pain_points_bottlenecks_risks')) == 0:
            stats["missing_pain_points"] += 1
            
        # Check Digitization Opps
        if not item.get('digitization_opportunities') or len(item.get('digitization_opportunities')) == 0:
            stats["missing_digitization_opps"] += 1

    print("--- Field Population Analysis (Total: 442) ---")
    print(f"Missing Executive Summary: {stats['missing_exec_summary']}")
    print(f"Missing Objectives: {stats['missing_objective']}")
    print(f"Missing Inputs: {stats['missing_inputs']}")
    print(f"Missing Outputs: {stats['missing_outputs']}")
    print(f"Missing Pain Points: {stats['missing_pain_points']}")
    print(f"Missing Digitization Opps: {stats['missing_digitization_opps']}")

except Exception as e:
    print(f"Error: {e}")
