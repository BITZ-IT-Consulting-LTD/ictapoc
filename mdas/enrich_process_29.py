import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirtieth process (index 29)
process = data['processes'][29]

# Populate fields
process['executive_summary'] = "The Judiciary of Kenya is one of the three State organs established under the Constitution, serving as an independent custodian of justice. Its primary role is to exercise judicial authority, delivering justice in line with the Constitution and other laws, resolving disputes justly, protecting rights and liberties, and facilitating the rule of law."
process['process_overview']['process_objective'] = "To administer justice fairly and impartially, interpret the Constitution and laws, protect human rights and freedoms, resolve legal disputes, promote alternative dispute resolution mechanisms, and foster social and political stability and national socio-economic development through judicial processes and decisions."
process['process_overview']['policy_legal_context'].append("Established under Chapter 10, Article 159 of the Constitution of Kenya. Its functions and powers are outlined in various Articles of the Constitution (e.g., Article 165 for the High Court) and other national legislation. It acts as a guardian of the Constitution and ensures that laws conform to it.")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Seekers of justice, litigants, and beneficiaries of an impartial legal system", "responsibilities": "(INFERRED) Engaging in legal processes, respecting court decisions, upholding laws."})
process['stakeholders'].append({"stakeholder": "Legal Professionals (Lawyers, Prosecutors)", "role": "Actors in the legal system representing parties and presenting cases", "responsibilities": "(INFERRED) Providing legal representation, upholding professional ethics, assisting in justice administration."})
process['stakeholders'].append({"stakeholder": "Superior Courts (Supreme Court, Court of Appeal, High Court, ELC, ELRC)", "role": "Highest judicial bodies responsible for constitutional interpretation and final appeals", "responsibilities": "(INFERRED) Hearing cases, setting legal precedents, upholding the rule of law."})
process['stakeholders'].append({"stakeholder": "Subordinate Courts (Magistrates Courts, Kadhi's Courts, etc.)", "role": "Lower courts handling a wide range of legal matters", "responsibilities": "(INFERRED) Hearing cases, applying laws, adhering to judicial principles."})
process['stakeholders'].append({"stakeholder": "Legislature (Parliament)", "role": "Body responsible for lawmaking, which the Judiciary interprets and applies", "responsibilities": "(INFERRED) Enacting clear and just laws, respecting judicial independence."})
process['stakeholders'].append({"stakeholder": "Executive (Government)", "role": "Body responsible for law enforcement and implementation of government policies", "responsibilities": "(INFERRED) Enforcing court orders, respecting the rule of law."})

process['as_is_narrative'] = "(INFERRED) The Judiciary operates through a structured court system, hearing and determining various legal disputes (civil, criminal, constitutional), interpreting constitutional and statutory law, protecting human rights, promoting alternative dispute resolution, compiling and disseminating case law, and overseeing the entire hierarchy of courts to ensure access to justice and uphold the rule of law across Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (constitutional mandates, functions from official sources) / medium (inferred legal frameworks, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://judiciary.go.ke/",
    "https://kenyaplax.com/", # Though not primary, provided useful context in search
    "https://deborahwando.co.ke/" # Though not primary, provided useful context in search
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirtieth process enriched and combined_data.json updated.")