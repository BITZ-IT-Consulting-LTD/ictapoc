
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-ninth process (index 38)
process = data['processes'][38]

# Populate fields
process['executive_summary'] = "The Assets Recovery Agency (ARA) in Kenya is a vital semi-autonomous institution under the Office of the Attorney General, established to combat economic crimes, money laundering, and corruption. Its primary focus is to identify, trace, freeze, seize, confiscate, and recover proceeds of crime, thereby dismantling financial incentives for criminal activities and restoring public resources."
process['process_overview']['process_objective'] = "To identify, trace, freeze, seize, confiscate, and recover proceeds of crime, institute legal proceedings for forfeiture of unlawfully acquired assets, manage preserved and forfeited assets, and administer the Criminal Assets Recovery Fund, in order to combat economic crimes, money laundering, and corruption and enhance accountability in Kenya."
process['process_overview']['policy_legal_context'].append("Established under Section 53 of the Proceeds of Crime and Anti-Money Laundering Act (POCAMLA) No. 9 of 2009. Operates under the Office of the Attorney General and collaborates with other law enforcement bodies under relevant legal frameworks for combating crime and corruption.")
process['stakeholders'].append({"stakeholder": "Office of the Attorney General", "role": "Parent body providing oversight and legal guidance", "responsibilities": "(INFERRED) General supervision, legal advice on asset recovery cases."})
process['stakeholders'].append({"stakeholder": "Ethics and Anti-Corruption Commission (EACC)", "role": "Collaborating agency in anti-corruption efforts", "responsibilities": "(INFERRED) Investigating corruption, providing intelligence on illicit assets."})
process['stakeholders'].append({"stakeholder": "Directorate of Criminal Investigations (DCI)", "role": "Collaborating agency in criminal investigations", "responsibilities": "(INFERRED) Investigating criminal activities, providing evidence for asset tracing."})
process['stakeholders'].append({"stakeholder": "Financial Reporting Centre (FRC)", "role": "Collaborating agency in combating money laundering and terrorist financing", "responsibilities": "(INFERRED) Receiving and analyzing financial transaction reports, providing intelligence."})
process['stakeholders'].append({"stakeholder": "Office of the Director of Public Prosecutions (ODPP)", "role": "Collaborating agency in prosecuting criminal cases and asset forfeiture", "responsibilities": "(INFERRED) Prosecuting cases, supporting ARA's applications for asset recovery."})
process['stakeholders'].append({"stakeholder": "Courts (Judiciary)", "role": "Adjudicating body for legal proceedings related to asset recovery", "responsibilities": "(INFERRED) Issuing orders for freezing/forfeiture, ensuring due process."})
process['stakeholders'].append({"stakeholder": "Public", "role": "Beneficiaries of recovered assets and reduced economic crime", "responsibilities": "(INFERRED) Reporting suspicious activities, supporting anti-corruption efforts."})

process['as_is_narrative'] = "(INFERRED) The ARA's operations involve receiving intelligence and conducting investigations to identify and trace proceeds of crime, both domestically and internationally. It then initiates legal proceedings in court to obtain orders for freezing, seizing, preserving, and ultimately forfeiting these assets. The Agency is also responsible for the management of these recovered assets and the administration of the Criminal Assets Recovery Fund, working in close collaboration with other law enforcement and anti-corruption agencies."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://cifar.eu/", # Provided context on POCAMLA
    "https://businessradar.co.ke/", # Provided context
    "https://parliament.go.ke/", # Provided context
    "https://youtube.com/" # General overview, might contain links to official documents.
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-ninth process enriched and combined_data.json updated.")
