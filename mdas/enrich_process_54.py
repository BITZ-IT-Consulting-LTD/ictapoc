
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-fifth process (index 54)
process = data['processes'][54]

# Populate fields
process['executive_summary'] = "The Kenya Maritime Authority (KMA) is a statutory authority established under the Kenya Maritime Authority Act 2006. Its primary mandate is to regulate, coordinate, and oversee maritime affairs in the Republic of Kenya, ensuring shipping safety, promoting seafarer welfare, protecting the marine environment, and facilitating maritime trade and investment in compliance with national and international standards."
process['process_overview']['process_objective'] = "To administer and enforce the Merchant Shipping Act, 2009, and other related regulations and international maritime conventions; to manage maritime search and rescue operations; to ensure shipping safety and security; to oversee the training, recruitment, and welfare of seafarers; to investigate maritime casualties; to develop national oil spill contingency plans; to maintain and administer a national ship register; and to advise the government on all matters pertaining to maritime affairs and legislation."
process['process_overview']['policy_legal_context'].append("Established under the Kenya Maritime Authority Act 2006. Administers and enforces the Merchant Shipping Act, 2009, and other related national laws and international maritime conventions, treaties, and agreements. Operates under the relevant government ministry responsible for maritime affairs.")
process['stakeholders'].append({"stakeholder": "Ship Owners / Operators", "role": "Entities responsible for the ownership and operation of vessels", "responsibilities": "(INFERRED) Complying with maritime regulations, ensuring vessel safety and seaworthiness."})
process['stakeholders'].append({"stakeholder": "Seafarers", "role": "Personnel working on vessels; beneficiaries of KMA's welfare and training oversight", "responsibilities": "(INFERRED) Adhering to safety protocols, participating in training, maintaining certifications."})
process['stakeholders'].append({"stakeholder": "Maritime Training Institutions", "role": "Providers of education and training for seafarers and maritime professionals", "responsibilities": "(INFERRED) Delivering quality training, meeting international standards."})
process['stakeholders'].append({"stakeholder": "Port Authorities (e.g., Kenya Ports Authority - KPA)", "role": "Managers of port facilities and operations", "responsibilities": "(INFERRED) Facilitating safe navigation, enforcing port regulations, collaborating on maritime security."})
process['stakeholders'].append({"stakeholder": "Fishermen", "role": "Users of marine resources; affected by maritime safety and environmental regulations", "responsibilities": "(INFERRED) Adhering to fishing regulations, promoting marine conservation."})
process['stakeholders'].append({"stakeholder": "Environmental Agencies (e.g., NEMA)", "role": "Partners in protecting the marine environment from pollution", "responsibilities": "(INFERRED) Collaborating on environmental impact assessments, enforcing anti-pollution laws."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Transport / Maritime Affairs)", "role": "Oversight ministry providing policy direction and strategic guidance", "responsibilities": "(INFERRED) Formulating maritime policies, ensuring compliance with international obligations."})
process['stakeholders'].append({"stakeholder": "International Maritime Organization (IMO)", "role": "Global body setting international maritime standards and conventions", "responsibilities": "(INFERRED) Providing regulatory framework, promoting safe and secure shipping."})
process['stakeholders'].append({"stakeholder": "Coastal Communities", "role": "Communities residing along the coast; affected by maritime activities", "responsibilities": "(INFERRED) Participating in maritime safety awareness, promoting sustainable marine practices."})
process['stakeholders'].append({"stakeholder": "Marine Tourism Operators", "role": "Businesses offering marine-related tourism activities", "responsibilities": "(INFERRED) Complying with safety regulations, promoting responsible tourism."})

process['as_is_narrative'] = "(INFERRED) KMA conducts regular inspections of vessels for seaworthiness and compliance with safety and environmental standards, and regulates shipping in both coastal and inland waterways. It operates a Regional Maritime Rescue Co-ordination Centre (RMRCC) to manage and coordinate search and rescue operations. The Authority promotes maritime education and training by overseeing institutions and ensuring seafarer competence and welfare. KMA also actively enforces anti-pollution measures to protect the marine environment and collaborates with national and international bodies, including the IMO, to ensure Kenya's maritime sector adheres to global best practices, thereby facilitating trade, investment, and sustainable use of marine resources."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kma.go.ke/",
    "https://saraka.info/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-fifth process enriched and combined_data.json updated.")
