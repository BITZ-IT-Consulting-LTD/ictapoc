
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-eighth process (index 57)
process = data['processes'][57]

# Populate fields
process['executive_summary'] = "The Kenya National Bureau of Statistics (KNBS) is Kenya's principal agency for the collection, compilation, analysis, publication, and dissemination of official statistical data. Established by the Statistics Act of 2006, it plays a critical role in coordinating the National Statistical System (NSS) and ensuring adherence to statistical standards, thereby providing reliable data for evidence-based policy formulation, planning, and decision-making for national development."
process['process_overview']['process_objective'] = "To collect, compile, analyze, publish, and disseminate integrated, reliable, and timely statistical information on various socio-economic sectors (e.g., health, economy, poverty, foreign investment); to coordinate, monitor, and supervise the National Statistical System (NSS) to ensure coherence and quality; to establish standards and promote best practices in statistical production and dissemination; to conduct national censuses and surveys, including the Population and Housing Census; to maintain a comprehensive national socio-economic database; and to collaborate with county governments and other institutions in the production of official statistics."
process['process_overview']['policy_legal_context'].append("Established by the Statistics Act of 2006, which provides its legal framework and mandates its functions. Operates as a Semi-Autonomous Government Agency under the State Department for Planning. Its work is guided by national development agendas like Vision 2030 and international statistical principles.")
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, and Agencies", "role": "Primary users of official statistics for policy formulation and program implementation", "responsibilities": "(INFERRED) Utilizing data for planning, collaborating with KNBS on sectoral statistics."})
process['stakeholders'].append({"stakeholder": "Policy Makers", "role": "Utilize statistical data to formulate and evaluate national and sectoral policies", "responsibilities": "(INFERRED) Relying on evidence-based data, engaging with KNBS for policy relevant statistics."})
process['stakeholders'].append({"stakeholder": "Researchers / Academia", "role": "Utilize KNBS data for academic research, analysis, and further studies", "responsibilities": "(INFERRED) Conducting studies, contributing to knowledge generation."})
process['stakeholders'].append({"stakeholder": "International Organizations (e.g., UN, World Bank, IMF)", "role": "Users of Kenyan statistics for global reporting, development assistance, and economic analysis", "responsibilities": "(INFERRED) Accessing national data, collaborating on statistical capacity building."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in statistical production and users of data for county-level planning", "responsibilities": "(INFERRED) Collecting local data, utilizing national statistics for county development."})
process['stakeholders'].append({"stakeholder": "Media", "role": "Disseminators of statistical information to the general public", "responsibilities": "(INFERRED) Reporting on official statistics accurately, raising public awareness."})
process['stakeholders'].append({"stakeholder": "General Public", "role": "Beneficiaries of transparent and accessible data for informed decision-making", "responsibilities": "(INFERRED) Accessing public data, engaging in civic discourse informed by statistics."})
process['stakeholders'].append({"stakeholder": "Businesses / Private Sector", "role": "Users of statistical data for market analysis, strategic planning, and investment decisions", "responsibilities": "(INFERRED) Utilizing economic data, contributing data to surveys where applicable."})
process['stakeholders'].append({"stakeholder": "Civil Society Organizations", "role": "Advocacy groups and development partners using statistics for program design and monitoring", "responsibilities": "(INFERRED) Using data for advocacy, monitoring development outcomes."})

process['as_is_narrative'] = "(INFERRED) KNBS's operations involve designing and conducting a wide range of national surveys (e.g., economic, demographic, social) and the decennial Population and Housing Census. It meticulously processes, analyzes, and interprets large datasets, ensuring data quality and statistical integrity. The Bureau is responsible for publishing numerous statistical reports, yearbooks, and economic surveys that provide a comprehensive picture of Kenya's socio-economic landscape. It maintains a robust national statistical database, which serves as a central repository for official data. KNBS also plays a pivotal role in strengthening statistical capacity across various government entities and county governments by providing technical assistance, training, and setting statistical standards. Furthermore, it actively engages in disseminating statistical information through its website, publications, and public outreach programs to promote evidence-based planning and decision-making across all sectors of society."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://knbs.or.ke/",
    "https://afro.co.ke/", # Provided context
    "https://wikipedia.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-eighth process enriched and combined_data.json updated.")
