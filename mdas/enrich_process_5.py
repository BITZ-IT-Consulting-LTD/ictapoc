
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixth process (index 5)
process = data['processes'][5]

# Populate fields
process['executive_summary'] = "The Kenya Revenue Authority (KRA) is the principal government agency responsible for the assessment, collection, and accounting of all government revenues. Established in 1995, it advises on tax policy, enforces compliance, and facilitates trade through customs and border control, utilizing digital platforms like iTax for taxpayer services."
process['process_overview']['process_objective'] = "To efficiently and effectively mobilize government revenue and facilitate trade by fostering compliance with tax and customs laws in Kenya."
process['process_overview']['policy_legal_context'].append("Established on July 1, 1995, by an Act of Parliament (Chapter 469 of the laws of Kenya). Operates under the legislative framework of various tax and customs laws, and advises the government on tax policy.")
process['stakeholders'].append({"stakeholder": "Kenyan Taxpayers (Individuals and Businesses)", "role": "Primary source of government revenue; subjects of tax compliance", "responsibilities": "(INFERRED) Filing tax returns, paying taxes, complying with tax laws."})
process['stakeholders'].append({"stakeholder": "Government of Kenya", "role": "Beneficiary of collected revenue; recipient of tax policy advice", "responsibilities": "(INFERRED) Utilizing revenue for public services, setting fiscal policy."})
process['stakeholders'].append({"stakeholder": "International Traders", "role": "Users of customs and border control services", "responsibilities": "(INFERRED) Complying with import/export regulations, paying duties."})
process['stakeholders'].append({"stakeholder": "Ministry of Finance", "role": "Oversight and policy-setting body for revenue administration", "responsibilities": "(INFERRED) Collaborating on fiscal strategy, receiving policy advice from KRA."})

process['as_is_narrative'] = "(INFERRED) KRA's operations involve assessing various taxes and duties, collecting revenue through multiple channels including digital platforms like iTax, enforcing compliance through audits and investigations, managing customs processes (e.g., import/export clearance via iCMS), and providing taxpayer education and support."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = ["https://kra.go.ke/", "https://pfmr.go.ke/", "https://en.wikipedia.org/wiki/Kenya_Revenue_Authority"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixth process enriched and combined_data.json updated.")
