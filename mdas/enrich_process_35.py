
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-sixth process (index 35)
process = data['processes'][35]

# Populate fields
process['executive_summary'] = "The Agricultural Finance Corporation (AFC) Kenya is a government-owned Development Finance Institution (DFI) established under the AFC Act. Its core mandate is to assist in the development of agriculture and agricultural industries by providing loans, managerial, and technical assistance to beneficiaries in the agricultural sector, thereby supporting food security and rural livelihoods."
process['process_overview']['process_objective'] = "To provide financial support and loans for various agricultural development projects, promote food security, encourage sustainable farming practices, and offer capacity building in financial management and agribusiness best practices to boost productivity and rural development across Kenya."
process['process_overview']['policy_legal_context'].append("Established under the Agricultural Finance Corporation Act (Cap 323 of the Laws of Kenya), 1969, which provides the foundational legal framework for its operations as a Development Finance Institution (DFI) in the agricultural sector.")
process['stakeholders'].append({"stakeholder": "Farmers / Agricultural Producers", "role": "Primary recipients of AFC's loans and technical assistance", "responsibilities": "(INFERRED) Utilizing loans for agricultural development, adopting sustainable farming practices, repaying loans."})
process['stakeholders'].append({"stakeholder": "Agricultural Industries", "role": "Beneficiaries of AFC's support for agricultural development and value addition", "responsibilities": "(INFERRED) Engaging in agricultural processing, contributing to the agricultural value chain."})
process['stakeholders'].append({"stakeholder": "Rural Population", "role": "Directly and indirectly supported by AFC's efforts to develop the agricultural sector", "responsibilities": "(INFERRED) Participating in agricultural initiatives, benefiting from improved livelihoods."})
process['stakeholders'].append({"stakeholder": "Banks / Development Agencies", "role": "Collaborators in co-financing and innovative financing solutions", "responsibilities": "(INFERRED) Partnering with AFC to extend financial reach, developing joint programs."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in agricultural development and outreach at the local level", "responsibilities": "(INFERRED) Collaborating on agricultural programs, facilitating farmer access to AFC services."})
process['stakeholders'].append({"stakeholder": "Youth and Women in Agribusiness", "role": "Targeted beneficiaries of AFC's inclusive agriculture programs", "responsibilities": "(INFERRED) Participating in mentorship, utilizing targeted loans for agribusiness ventures."})

process['as_is_narrative'] = "(INFERRED) The AFC operates by processing and disbursing various types of loans to farmers and agricultural ventures for purposes such as farm equipment acquisition, livestock financing, and crop production. It also provides managerial and technical advice, conducts capacity building on financial management and agribusiness planning, and forms strategic partnerships with other financial institutions and government entities to reach underserved communities and promote sustainable agricultural practices across Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from multiple reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://developmentaid.org/",
    "https://agrifinance.org/",
    "https://saraka.info/",
    "https://agrarian.co.ke/",
    "https://theworldfolio.com/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-sixth process enriched and combined_data.json updated.")
