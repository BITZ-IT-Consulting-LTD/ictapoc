
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-eighth process (index 37)
process = data['processes'][37]

# Populate fields
process['executive_summary'] = "The Anti-Counterfeit Authority (ACA) Kenya is a State Corporation established under the Anti-Counterfeit Act 2008. Its primary mandate is to protect intellectual property rights and consumer rights by actively combating trade in counterfeit goods, raising public awareness, and coordinating with other organizations involved in anti-counterfeiting efforts in Kenya."
process['process_overview']['process_objective'] = "To enlighten the public on counterfeiting, combat trade in counterfeit goods, promote training programs for stakeholders, and coordinate with other organizations involved in combating counterfeiting to safeguard intellectual property rights, protect consumers, and foster a fair trading environment in Kenya."
process['process_overview']['policy_legal_context'].append("Established under the Anti-Counterfeit Act 2008, which provides the legal framework for its mandate. Operates under the Ministry of Industry, Investment and Trade.")
process['stakeholders'].append({"stakeholder": "Intellectual Property Rights Holders (e.g., brand owners)", "role": "Beneficiaries of intellectual property protection", "responsibilities": "(INFERRED) Registering IP, collaborating with ACA on enforcement."})
process['stakeholders'].append({"stakeholder": "Consumers", "role": "Victims of counterfeit goods; beneficiaries of safe and authentic products", "responsibilities": "(INFERRED) Being vigilant, reporting suspected counterfeit goods, demanding authentic products."})
process['stakeholders'].append({"stakeholder": "Law Enforcement Agencies (Police, Customs)", "role": "Partners in intelligence gathering, investigations, and seizure of counterfeit goods", "responsibilities": "(INFERRED) Enforcing anti-counterfeiting laws, conducting raids, border control."})
process['stakeholders'].append({"stakeholder": "Manufacturers", "role": "Producers of genuine goods; affected by counterfeiting", "responsibilities": "(INFERRED) Producing quality goods, collaborating on anti-counterfeiting measures."})
process['stakeholders'].append({"stakeholder": "Traders (Retailers, Wholesalers)", "role": "Distributors of goods; potential conduits for counterfeit products", "responsibilities": "(INFERRED) Ensuring authenticity of products sold, complying with anti-counterfeiting regulations."})
process['stakeholders'].append({"stakeholder": "International Anti-Counterfeiting Organizations", "role": "Collaborators in global efforts to combat counterfeiting", "responsibilities": "(INFERRED) Sharing intelligence, harmonizing strategies, providing technical support."})

process['as_is_narrative'] = "(INFERRED) The ACA operates by conducting public awareness and enlightenment campaigns on the dangers of counterfeiting, undertaking investigations and enforcement actions (including seizures of counterfeit goods) across various markets and entry points, promoting training programs for stakeholders (including law enforcement and customs officials), and coordinating with national and international organizations to combat illicit trade and protect intellectual property rights effectively."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website and other sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://aca.go.ke/",
    "https://devex.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-eighth process enriched and combined_data.json updated.")
