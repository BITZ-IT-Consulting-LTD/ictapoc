
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-third process (index 62)
process = data['processes'][62]

# Populate fields
process['executive_summary'] = "The Kenya Revenue Authority (KRA) is the principal government agency responsible for the assessment, collection, and accounting of all government revenues. Established on July 1, 1995, by an Act of Parliament (Chapter 469 of the laws of Kenya), KRA advises the government on tax policy, enforces compliance with tax and customs laws, and facilitates trade, utilizing digital platforms like iTax for taxpayer services."
process['process_overview']['process_objective'] = "To efficiently and effectively mobilize government revenue and facilitate trade by fostering compliance with tax and customs laws in Kenya; to advise the government on tax policy; to provide quality taxpayer services; and to combat tax evasion and illicit trade through robust enforcement measures."
process['process_overview']['policy_legal_context'].append("Established on July 1, 1995, by an Act of Parliament (Chapter 469 of the laws of Kenya). Operates under the legislative framework of various tax and customs laws, including the Income Tax Act, Value Added Tax Act, and East African Community Customs Management Act. It advises the National Treasury on tax policy and implements government fiscal policies.")
process['stakeholders'].append({"stakeholder": "Kenyan Taxpayers (Individuals and Businesses)", "role": "Primary source of government revenue; subjects of tax compliance and beneficiaries of public services", "responsibilities": "(INFERRED) Filing tax returns accurately and on time, paying taxes, complying with tax laws."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (National Treasury)", "role": "Beneficiary of collected revenue; recipient of tax policy advice and oversight body", "responsibilities": "(INFERRED) Utilizing revenue for public services, setting fiscal policy, providing oversight to KRA."})
process['stakeholders'].append({"stakeholder": "International Traders", "role": "Users of customs and border control services; subjects of international trade regulations", "responsibilities": "(INFERRED) Complying with import/export regulations, paying customs duties, adhering to trade facilitation rules."})
process['stakeholders'].append({"stakeholder": "Kenya Ports Authority (KPA)", "role": "Key partner in customs clearance and trade facilitation", "responsibilities": "(INFERRED) Facilitating cargo movement, coordinating with KRA on port operations."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Facilitate tax payments and provide financial services to taxpayers", "responsibilities": "(INFERRED) Processing tax payments, adhering to financial regulations."})
process['stakeholders'].append({"stakeholder": "General Public", "role": "Beneficiaries of public services funded by tax revenue", "responsibilities": "(INFERRED) Promoting tax compliance, holding government accountable for revenue use."})
process['stakeholders'].append({"stakeholder": "Kenya Bureau of Standards (KEBS)", "role": "Partner in enforcing quality standards and combating illicit trade", "responsibilities": "(INFERRED) Ensuring product quality and safety, collaborating on anti-counterfeit measures."})

process['as_is_narrative'] = "(INFERRED) KRA's operations involve the comprehensive administration of various taxes, including Income Tax, Value Added Tax (VAT), Customs and Excise Duties, and other levies. It collects revenue through multiple channels, increasingly leveraging digital platforms such as iTax for filing returns and making payments, and iCMS for customs processes. The Authority employs robust enforcement measures, including audits, investigations, and intelligence gathering, to combat tax evasion, smuggling, and illicit trade. KRA plays a crucial role in trade facilitation by streamlining customs procedures and collaborating with border agencies. Furthermore, it engages in extensive taxpayer education and awareness campaigns to foster voluntary compliance, provides taxpayer support services, and continuously advises the National Treasury on matters of tax policy to optimize revenue collection and enhance fiscal management for the country's economic development."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kra.go.ke/",
    "https://pfmr.go.ke/", # Provided context (financial management)
    "https://en.wikipedia.org/wiki/Kenya_Revenue_Authority" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-third process enriched and combined_data.json updated.")
