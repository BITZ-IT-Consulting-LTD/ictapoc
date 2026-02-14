
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-seventh process (index 46)
process = data['processes'][46]

# Populate fields
process['executive_summary'] = "The Kenya Broadcasting Corporation (KBC) is a state corporation established by an Act of Parliament (CAP 221 of the Laws of Kenya). It is mandated to provide independent, impartial, objective, informative, educative, and entertaining public broadcasting services in English, Kiswahili, and various local languages, thereby contributing to national development, cultural preservation, and the well-being of Kenyans."
process['process_overview']['process_objective'] = "To deliver high-quality, diverse programming across radio, television, and digital platforms; to increase public understanding of government development policies and strategies; to promote effective communication and national cohesion; and to serve as a vital tool for national development by upholding independence, impartiality, and public service broadcasting principles."
process['process_overview']['policy_legal_context'].append("Established by an Act of Parliament (CAP 221 of the Laws of Kenya). Operates under the Ministry of Information, Communications and the Digital Economy, with its functions aligned with national broadcasting policies and regulations, including those enforced by the Communications Authority of Kenya.")
process['stakeholders'].append({"stakeholder": "Kenyan Public / Citizens", "role": "Primary audience and beneficiaries of KBC's broadcasting services", "responsibilities": "(INFERRED) Consuming diverse content, providing feedback, engaging in national discourse."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Information, Communications and the Digital Economy)", "role": "Oversight ministry providing policy direction and strategic guidance", "responsibilities": "(INFERRED) Formulating broadcasting policies, ensuring KBC fulfills its public mandate."})
process['stakeholders'].append({"stakeholder": "Advertisers", "role": "Commercial entities utilizing KBC platforms for outreach", "responsibilities": "(INFERRED) Generating revenue for KBC, adhering to advertising standards."})
process['stakeholders'].append({"stakeholder": "Content Producers (Internal & External)", "role": "Creators of news, educational, and entertainment programs", "responsibilities": "(INFERRED) Developing high-quality content, adhering to editorial guidelines."})
process['stakeholders'].append({"stakeholder": "Journalists / Media Professionals", "role": "Contributors to news gathering, reporting, and program presentation", "responsibilities": "(INFERRED) Upholding journalistic ethics, delivering objective information."})
process['stakeholders'].append({"stakeholder": "Regulatory Bodies (e.g., Communications Authority of Kenya)", "role": "Ensuring compliance with broadcasting standards and regulations", "responsibilities": "(INFERRED) Monitoring content, enforcing licensing conditions."})
process['stakeholders'].append({"stakeholder": "Cultural / Educational Institutions", "role": "Partners in promoting national heritage and educational content", "responsibilities": "(INFERRED) Collaborating on specialized programming, utilizing KBC for dissemination."})

process['as_is_narrative'] = "(INFERRED) KBC's operations involve producing and broadcasting a wide array of content, including news, current affairs, educational programs, and entertainment, through its radio, television, and digital channels. It utilizes various linguistic platforms to reach a diverse national audience. The Corporation maintains a Quality Management System (ISO 9001:2015) to ensure service excellence and continually improves its infrastructure to leverage digital platforms, ensuring accessible and relevant content that informs, educates, and entertains the Kenyan public."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kbc.co.ke/",
    "https://ecitizen.go.ke/", # Provided context
    "https://kbc.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-seventh process enriched and combined_data.json updated.")
