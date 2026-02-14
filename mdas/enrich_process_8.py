
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninth process (index 8)
process = data['processes'][8]

# Populate fields
process['executive_summary'] = "The National Police Service (NPS) of Kenya is the umbrella law enforcement body established under the Constitution to maintain law and order, protect life and property, and uphold constitutional values. It comprises the Kenya Police Service, the Administration Police Service, and the Directorate of Criminal Investigations (DCI)."
process['process_overview']['process_objective'] = "To provide professional and disciplined law enforcement services, prevent corruption, protect human rights and freedoms, train members to high standards of competence and integrity, and foster good community relations in the performance of its duties."
process['process_overview']['policy_legal_context'].append("Established under Article 243 of the Constitution of Kenya 2010. Its objectives and functions are outlined in Article 244 of the Constitution and the National Police Service Act 2011.")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Beneficiaries of security, law enforcement, and human rights protection", "responsibilities": "(INFERRED) Cooperating with law enforcement, reporting crimes, upholding laws."})
process['stakeholders'].append({"stakeholder": "Kenya Police Service", "role": "Internal component responsible for general policing duties", "responsibilities": "(INFERRED) Crime prevention, investigation, public order maintenance."})
process['stakeholders'].append({"stakeholder": "Administration Police Service", "role": "Internal component responsible for border security, critical infrastructure protection, and supporting National Government Administrative Officers", "responsibilities": "(INFERRED) Border patrols, VIP protection, security during public functions."})
process['stakeholders'].append({"stakeholder": "Directorate of Criminal Investigations (DCI)", "role": "Internal component responsible for investigating serious crimes", "responsibilities": "(INFERRED) Collecting criminal intelligence, investigating homicide, narcotics, terrorism, economic crimes."})
process['stakeholders'].append({"stakeholder": "National Police Service Commission (NPSC)", "role": "Independent body for human resource management within the NPS", "responsibilities": "(INFERRED) Recruiting, appointing, promoting, disciplining police personnel."})

process['as_is_narrative'] = "(INFERRED) The NPS operates through its various branches to prevent and detect crime, investigate serious offenses, maintain public order, provide security for government entities and functions, manage human resources within the service, and engage in community policing initiatives to build trust and cooperation."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (constitutional mandates, components, functions) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://en.wikipedia.org/wiki/National_Police_Service_(Kenya)",
    "https://npsc.go.ke/",
    "https://dci.go.ke/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninth process enriched and combined_data.json updated.")
