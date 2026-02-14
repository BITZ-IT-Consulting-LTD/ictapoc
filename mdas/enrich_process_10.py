
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eleventh process (index 10)
process = data['processes'][10]

# Populate fields
process['executive_summary'] = "The National Treasury of Kenya is the primary government entity responsible for formulating financial and economic policies, and overseeing the effective coordination of government financial operations. Its mandate includes national budget preparation, public debt management, and resource mobilization."
process['process_overview']['process_objective'] = "To formulate, implement, and monitor macroeconomic policies; prepare the national budget; manage public debt and mobilize resources; and establish efficient, transparent financial management systems for national and county governments, ensuring accountability of public finances."
process['process_overview']['policy_legal_context'].append("Mandate derived from the Constitution of Kenya 2010 (Article 225), the Public Finance Management Act 2012 (Section 12), and various Executive Orders. Operates under a framework ensuring transparent financial management and standard financial reporting.")
process['stakeholders'].append({"stakeholder": "Kenyan Government (National and County)", "role": "Recipient and implementer of financial and economic policies; user of national budget and financial systems", "responsibilities": "(INFERRED) Adhering to fiscal policies, managing public funds according to prescribed standards."})
process['stakeholders'].append({"stakeholder": "Parliament", "role": "Approves national budget and scrutinizes public finance management", "responsibilities": "(INFERRED) Budget oversight, legislative approval of financial acts."})
process['stakeholders'].append({"stakeholder": "Kenya Revenue Authority (KRA)", "role": "Primary agency for revenue collection overseen by the Treasury", "responsibilities": "(INFERRED) Collecting taxes and duties as per KRA Act, reporting to Treasury."})
process['stakeholders'].append({"stakeholder": "Public Entities (State Corporations, Agencies)", "role": "Subjects of financial management standards and oversight", "responsibilities": "(INFERRED) Implementing financial reporting standards, managing allocated funds prudently."})
process['stakeholders'].append({"stakeholder": "International Financial Institutions", "role": "Partners in resource mobilization and public debt management", "responsibilities": "(INFERRED) Providing financial assistance, advising on economic policies."})

process['as_is_narrative'] = "(INFERRED) The National Treasury's operations involve developing macroeconomic frameworks, preparing and presenting the annual national budget, managing the government's debt portfolio, mobilizing funds from domestic and international markets, setting financial management standards for public entities, and strengthening intergovernmental fiscal relations with county governments."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (constitutional and legislative mandates from official sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://treasury.go.ke/",
    "https://afro.co.ke/", # Though not primary, provided useful context in search
    "https://devolution.go.ke/", # Though not primary, provided useful context in search
    "https://vellum.co.ke/", # Though not primary, provided useful context in search
    "https://parliament.go.ke/" # Though not primary, provided useful context in search
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eleventh process enriched and combined_data.json updated.")
