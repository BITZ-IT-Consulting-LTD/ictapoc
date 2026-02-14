
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-eighth process (index 47)
process = data['processes'][47]

# Populate fields
process['executive_summary'] = "The Kenya Broadcasting Corporation (KBC) is Kenya's national public broadcaster, established by an Act of Parliament (CAP 221 of the Laws of Kenya). Its primary mandate is to provide independent, impartial, objective, informative, educative, and entertaining broadcasting services in diverse languages, contributing to national unity, cultural preservation, and the socio-economic well-being of the Kenyan people."
process['process_overview']['process_objective'] = "To deliver high-quality, diverse, and objective programming across radio, television, and digital platforms; to increase public understanding of government development policies and strategies; to promote effective communication and national cohesion; and to serve as a vital tool for national development by upholding independence, impartiality, and public service broadcasting principles."
process['process_overview']['policy_legal_context'].append("Established by an Act of Parliament (CAP 221 of the Laws of Kenya). Operates under the Ministry of Information, Communications and the Digital Economy, with its functions aligned with national broadcasting policies and regulations, including those enforced by the Communications Authority of Kenya.")
process['stakeholders'].append({"stakeholder": "Kenyan Public / Citizens", "role": "Primary audience and beneficiaries of KBC's broadcasting services", "responsibilities": "(INFERRED) Consuming diverse content, providing feedback, engaging in national discourse."})
process['stakeholders'].append({"stakeholder": "Government (various ministries including Information, Communications and the Digital Economy)", "role": "Oversight ministry providing policy direction and strategic guidance", "responsibilities": "(INFERRED) Formulating broadcasting policies, ensuring KBC fulfills its public mandate."})
process['stakeholders'].append({"stakeholder": "Advertisers", "role": "Commercial entities utilizing KBC platforms for outreach", "responsibilities": "(INFERRED) Generating revenue for KBC, adhering to advertising standards."})
process['stakeholders'].append({"stakeholder": "Content Producers (Internal & External)", "role": "Creators of news, educational, and entertainment programs", "responsibilities": "(INFERRED) Developing high-quality content, adhering to editorial guidelines."})
process['stakeholders'].append({"stakeholder": "Journalists / Media Professionals", "role": "Contributors to news gathering, reporting, and program presentation", "responsibilities": "(INFERRED) Upholding journalistic ethics, delivering objective information."})
process['stakeholders'].append({"stakeholder": "Communications Authority of Kenya (CAK)", "role": "Regulatory body for broadcasting and telecommunications", "responsibilities": "(INFERRED) Monitoring content, enforcing licensing conditions, ensuring compliance with broadcasting standards."})
process['stakeholders'].append({"stakeholder": "Cultural / Educational Institutions", "role": "Partners in promoting national heritage and educational content", "responsibilities": "(INFERRED) Collaborating on specialized programming, utilizing KBC for dissemination."})

process['as_is_narrative'] = "(INFERRED) KBC's operations involve producing and broadcasting a wide array of content, including news, current affairs, educational programs, and entertainment, through its numerous television (e.g., KBC Channel 1, Heritage TV, Y254) and radio stations (e.g., KBC Radio Taifa, KBC English Service) in multiple languages. It also provides digital content through online platforms (live streaming, podcasts, articles) and offers commercial advertising and online services (e.g., KBC Payments, Studio Mashinani, Signet, Cositing, Matangazo). KBC maintains a Quality Management System (ISO 9001:2015) to ensure service excellence and continually improves its infrastructure to ensure accessible and relevant content that informs, educates, and entertains the Kenyan public."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kbc.co.ke/",
    "https://ecitizen.go.ke/", # Provided context
    "https://kbc.go.ke/", # Provided context
    "https://statemediamonitor.com/", # Provided context
    "https://wikipedia.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-eighth process enriched and combined_data.json updated.")
