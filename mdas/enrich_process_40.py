
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-first process (index 40)
process = data['processes'][40]

# Populate fields
process['executive_summary'] = "The Business Registration Service (BRS) in Kenya is a State Corporation established under the Business Registration Service Act, 2015. Its core mandate is to administer policies, laws, and other matters related to business registration, thereby improving the ease of doing business in Kenya and fostering economic growth through effective oversight of companies, partnerships, and firms."
process['process_overview']['process_objective'] = "To ensure the effective administration of laws concerning the incorporation, registration, operation, and management of companies, partnerships, and firms; to maintain comprehensive registers, data, and records of all registrations; and to provide quality business support services throughout the business lifecycle in Kenya."
process['process_overview']['policy_legal_context'].append("Established under the Business Registration Service Act, 2015. Oversees and administers laws related to companies, partnerships, limited liability partnerships, movable property security rights, insolvency, and hire purchase agreements. Operates under the Office of the Attorney General.")
process['stakeholders'].append({"stakeholder": "Entrepreneurs / Business Owners", "role": "Individuals and entities seeking to register and operate businesses in Kenya", "responsibilities": "(INFERRED) Complying with registration requirements, maintaining statutory records, fulfilling legal obligations."})
process['stakeholders'].append({"stakeholder": "Companies, Partnerships, and Firms", "role": "Legal entities whose registration, operation, and management are regulated by BRS", "responsibilities": "(INFERRED) Adhering to relevant acts, submitting annual returns, ensuring corporate governance."})
process['stakeholders'].append({"stakeholder": "Legal Professionals (Lawyers, Company Secretaries)", "role": "Assist clients with business registration and compliance matters", "responsibilities": "(INFERRED) Providing legal advice, facilitating registration processes, ensuring client compliance."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Utilize the Movable Property Security Rights Registry for collateral registration", "responsibilities": "(INFERRED) Registering security interests, conducting due diligence."})
process['stakeholders'].append({"stakeholder": "Insolvency Practitioners (Official Receivers)", "role": "Administer corporate insolvency processes and debt restructuring", "responsibilities": "(INFERRED) Managing insolvencies, ensuring fair distribution of assets."})
process['stakeholders'].append({"stakeholder": "Office of the Attorney General", "role": "Parent body providing policy advice and oversight", "responsibilities": "(INFERRED) Guiding legal frameworks, ensuring BRS operations align with national legal objectives."})
process['stakeholders'].append({"stakeholder": "Government Agencies", "role": "Collaborators in business regulation and data sharing", "responsibilities": "(INFERRED) Sharing relevant data, coordinating on business development initiatives."})

process['as_is_narrative'] = "(INFERRED) The BRS operates by receiving and processing applications for business and company registrations, maintaining various comprehensive registries including for movable property security rights and insolvency, implementing policies and guidelines related to business administration, advising the Attorney General on legislative reforms, conducting research, and providing digital services (e.g., via eCitizen) for online registration, compliance filings, business name searches, and reservations to facilitate the ease of doing business in Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website and other sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://brs.go.ke/",
    "https://capitaregistrars.co.ke/", # Provided context
    "https://globallawexperts.com/", # Provided context
    "https://cybermfukoni.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-first process enriched and combined_data.json updated.")
