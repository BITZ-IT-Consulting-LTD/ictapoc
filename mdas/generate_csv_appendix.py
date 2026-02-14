import json
import csv

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'
output_csv = '/Users/mac/ictapoc/mdas/Government_Services_List.csv'

def get_service_category(mda_name):
    if any(x in mda_name.upper() for x in ["UNIVERSITY", "HOSPITAL", "IMMIGRATION", "REGISTRATION", "PERSONS"]): return "G2C"
    if any(x in mda_name.upper() for x in ["AUTHORITY", "BOARD", "COMMISSION", "CORPORATION", "COMPANY", "REVENUE"]): return "G2B"
    return "G2C/G2B"

def get_complexity(steps):
    count = len(steps)
    if count <= 5: return "Low"
    if count <= 8: return "Medium"
    return "High"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(['MDA Name', 'Service Name', 'Service Category', 'Complexity', 'Step Count', 'Digital Maturity', 'Documentation Status'])

        count = 0
        for item in items:
            mda = item.get('mda_name', 'Unknown')
            # Extract Service Name from narrative or objective roughly
            # Or use the generic mapping we had. 
            # Ideally we'd have a specific field, but let's infer from the Objective or Steps
            
            steps = item.get('as_is_steps', [])
            process_name = "Service Delivery"
            if steps:
                # Try to guess process name from first step
                desc = steps[0].get('description', '')
                if "logs into" in desc:
                    process_name = "Digital Service Application"
                elif "visits" in desc:
                    process_name = "Manual Service Application"
            
            # Refine Process Name based on our previous specific updates
            narrative = item.get('as_is_narrative', '')
            if "passport" in narrative.lower(): process_name = "Passport Application"
            elif "tax return" in narrative.lower(): process_name = "Tax Return Filing"
            elif "driving license" in narrative.lower(): process_name = "Driving License Renewal"
            elif "student" in narrative.lower(): process_name = "Student Admission"
            elif "patient" in narrative.lower(): process_name = "Patient Management"
            elif "license" in narrative.lower() or "permit" in narrative.lower(): process_name = "Licensing & Permitting"
            elif "loan" in narrative.lower(): process_name = "Loan/Grant Processing"
            
            cat = get_service_category(mda)
            comp = get_complexity(steps)
            maturity = item.get('process_maturity', {}).get('documentation_status', 'Draft')
            
            # Infer maturity level for CSV
            level = "Level 1 (Ad-hoc)"
            if "Digital" in process_name or "logs into" in str(steps):
                level = "Level 3 (Defined/Digitized)"
            if "KRA" in mda or "NTSA" in mda or "IMMIGRATION" in mda:
                level = "Level 5 (Optimized)"

            writer.writerow([mda, process_name, cat, comp, len(steps), level, maturity])
            count += 1

    print(f"Generated Service List for {count} MDAs at {output_csv}")

except Exception as e:
    print(f"Error: {e}")
