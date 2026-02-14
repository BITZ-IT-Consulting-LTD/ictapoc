
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-second process (index 41)
process = data['processes'][41]

# Populate fields
process['executive_summary'] = "The Competition Authority of Kenya (CAK) is established under the Competition Act CAP 504. Its primary mandate is to enforce competition law, promote and safeguard effective competition in markets, prevent misleading market conduct, and protect consumer welfare throughout Kenya, thereby enhancing the welfare of the Kenyan people."
process['process_overview']['process_objective'] = "To promote and enforce compliance with the Competition Act; receive and investigate complaints; promote public awareness of competition law and consumer rights; control mergers and acquisitions to prevent market concentration; deter anti-competitive conduct like abuse of dominance and price fixing; and advise the government on competition and consumer welfare matters."
process['process_overview']['policy_legal_context'].append("Established under the Competition Act CAP 504, which provides the legal framework for its operations. This Act governs market conduct, mergers, and consumer protection related to competition in Kenya.")
process['stakeholders'].append({"stakeholder": "Consumers", "role": "Beneficiaries of fair competition and protection from anti-competitive practices", "responsibilities": "(INFERRED) Reporting anti-competitive practices, being aware of their rights."})
process['stakeholders'].append({"stakeholder": "Businesses / Enterprises (local and international)", "role": "Subjects of competition law; participants in the Kenyan market", "responsibilities": "(INFERRED) Complying with competition laws, engaging in fair business practices."})
process['stakeholders'].append({"stakeholder": "Individuals and Legal Entities", "role": "Complainants or subjects of investigations", "responsibilities": "(INFERRED) Providing information, cooperating with investigations."})
process['stakeholders'].append({"stakeholder": "Consumer Bodies", "role": "Advocates for consumer rights and welfare", "responsibilities": "(INFERRED) Representing consumers, collaborating with CAK on consumer protection initiatives."})
process['stakeholders'].append({"stakeholder": "Government", "role": "Recipient of policy advice on competition and consumer welfare", "responsibilities": "(INFERRED) Considering CAK's advice, enacting pro-competition policies."})
process['stakeholders'].append({"stakeholder": "Regulatory Bodies", "role": "Liaison partners on sector-specific competition issues", "responsibilities": "(INFERRED) Collaborating on regulatory frameworks, sharing information."})
process['stakeholders'].append({"stakeholder": "Acquiring / Target Firms", "role": "Parties involved in mergers and acquisitions subject to CAK review", "responsibilities": "(INFERRED) Submitting merger notifications, providing required information."})
process['stakeholders'].append({"stakeholder": "Suppliers", "role": "Affected by buyer power issues", "responsibilities": "(INFERRED) Reporting abuse of buyer power, seeking fair trading terms."})

process['as_is_narrative'] = "(INFERRED) The CAK operates by actively investigating complaints regarding anti-competitive conduct (e.g., price fixing, abuse of dominance), reviewing and approving proposed mergers and acquisitions to prevent market concentration, carrying out market inquiries and research, and providing public education on competition law. It collaborates with other regulatory bodies and advises the government on policies to foster a competitive and fair market environment, ensuring the protection of both businesses and consumers."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://cak.go.ke/",
    "https://afro.co.ke/", # Provided context
    "https://majira.co.ke/", # Provided context
    "https://cuts-nairobi.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-second process enriched and combined_data.json updated.")
