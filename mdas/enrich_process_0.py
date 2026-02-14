import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the first process
process = data['processes'][0]

# Populate fields
process['executive_summary'] = "The State Department for Correctional Services (Kenya) aims to be an excellent organization in correctional service. Its mission is to promote a just and secure society through efficient and effective management of offenders and administration of justice. Key core values include Professionalism, Transparency & Accountability, Integrity, Reliability, Confidentiality, Fairness, Respect for Human Dignity, and Partnerships."
process['process_overview']['process_objective'] = "To promote a just and secure society through efficient and effective management of offenders and administration of justice."
process['process_overview']['policy_legal_context'].append("The State Department for Correctional Services operates under a 'Policy Mandate' and 'Service Charter'. (INFERRED: Specific governing Acts and Regulations are implied by its mandate to administer justice and manage offenders, likely including national correctional services acts and criminal procedure codes.)")
process['stakeholders'].append({"stakeholder": "Kenya Prisons Service", "role": "Internal operational service for incarceration and rehabilitation", "responsibilities": "(INFERRED) Enforcement of correctional policies, prisoner management, rehabilitation programs."})
process['stakeholders'].append({"stakeholder": "Probation & Aftercare Service", "role": "Internal operational service for community supervision and reintegration", "responsibilities": "(INFERRED) Supervising offenders on probation, facilitating reintegration into society, providing aftercare support."})
process['stakeholders'].append({"stakeholder": "Offenders", "role": "Primary subjects of correctional services", "responsibilities": "(INFERRED) Compliance with correctional orders, participation in rehabilitation."})
process['stakeholders'].append({"stakeholder": "Society", "role": "Beneficiary of a just and secure environment", "responsibilities": "(INFERRED) Support for rehabilitation efforts, community safety."})

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mission, vision, structure) / medium (policy context, stakeholder responsibilities inferred)"
process['metadata']['source_urls'] = ["https://correctional.go.ke/"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("First process enriched and combined_data.json updated.")