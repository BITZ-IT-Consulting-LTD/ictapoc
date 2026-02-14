import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the twenty-eighth process (index 27)
process = data['processes'][27]

# Populate fields
process['executive_summary'] = "The State Department for Parliamentary Affairs in Kenya is mandated to coordinate the National Government's legislative agenda, facilitate seamless interaction between the Executive and Parliament, and strengthen policy coordination across Ministries, Departments, and Agencies (MDAs). It ensures effective government business and enhances accountability."
process['process_overview']['process_objective'] = "To coordinate the formulation and implementation of the government's legislative agenda, strengthen policy coordination across MDAs and stakeholders, facilitate effective interaction between the Executive and Parliament, and enhance accountability and compliance through legislative oversight and public participation in policy and legislation development."
process['process_overview']['policy_legal_context'].append("Mandate derived from Executive Order No. 2 of November 2023 and Executive Order No. 1 of January 2023. Operates within the constitutional framework governing the Executive and Legislature, and relevant national legislation that guides legislative processes and inter-branch relations. (INFERRED: This forms the legal and operational context for its liaison role.)")
process['stakeholders'].append({"stakeholder": "Parliament (National Assembly and Senate)", "role": "Legislative body; primary interface for the Department's coordination efforts", "responsibilities": "(INFERRED) Enacting laws, providing oversight of the Executive, engaging in legislative processes."})
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, and Agencies (MDAs)", "role": "Originators and implementers of government policies and legislation", "responsibilities": "(INFERRED) Formulating legislative proposals, responding to parliamentary inquiries, implementing laws."})
process['stakeholders'].append({"stakeholder": "The Executive (President, Cabinet Secretaries)", "role": "Body whose legislative agenda and policies are coordinated and presented to Parliament", "responsibilities": "(INFERRED) Driving the legislative agenda, ensuring policy implementation, engaging with Parliament."})
process['stakeholders'].append({"stakeholder": "Political Party/Coalition Leadership in Parliament", "role": "Key actors in guiding legislative processes and securing parliamentary support", "responsibilities": "(INFERRED) Facilitating legislative passage, ensuring party discipline on legislative matters."})
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Beneficiaries of legislation; participants in public participation processes", "responsibilities": "(INFERRED) Engaging in policy discussions, holding leaders accountable through legislative processes."})

process['as_is_narrative'] = "(INFERRED) The Department's operations involve leading the identification and prioritization of government legislation, liaising with MDAs to formulate legislative proposals, providing guidance on legal framework challenges, overseeing public participation in policy development, tracking the progress of legislative initiatives, monitoring Executive responses to parliamentary inquiries, and building capacity in policy and legislation making processes across government entities."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal context, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://parliamentaryaffairs.go.ke/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Twenty-eighth process enriched and combined_data.json updated.")