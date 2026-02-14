
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-second process (index 81)
process = data['processes'][81]

# Populate fields
process['executive_summary'] = "The Retirement Benefits Authority (RBA) in Kenya is a regulatory body established under the Retirement Benefits Act of 1997, operating under the National Treasury. Its primary mandate encompasses the regulation, supervision, protection, and promotion of the retirement benefits sector in Kenya. RBA plays a crucial role in ensuring the security of members' savings, fostering the growth and development of the sector, and promoting public understanding and confidence in retirement planning and benefits."
process['process_overview']['process_objective'] = "To regulate and supervise the establishment and management of all retirement benefits schemes in Kenya, including licensing and registering schemes, trustees, fund managers, and administrators, and setting investment guidelines; to protect the interests of members and sponsors of retirement benefits schemes by safeguarding their savings and rights, providing a platform for resolving complaints and disputes, and enforcing penalties for non-compliance; to promote the growth and development of the retirement benefits sector through public awareness campaigns, education programs on retirement planning and financial literacy, and supporting reforms and innovations within the industry; and to advise the government on matters related to retirement benefits and implement government policies concerning the sector."
process['process_overview']['policy_legal_context'].append("Established under the Retirement Benefits Act of 1997, which provides the comprehensive legal and regulatory framework for the retirement benefits sector in Kenya. RBA operates under the oversight of the National Treasury and is crucial for implementing government policies aimed at expanding social protection, ensuring financial stability and integrity of retirement schemes, and protecting the welfare of current and future retirees. Its work aligns with national financial sector development strategies.")
process['stakeholders'].append({"stakeholder": "Retirement Benefits Scheme Members", "role": "Individuals contributing to and benefiting from retirement schemes; their savings and welfare are protected by RBA", "responsibilities": "(INFERRED) Making contributions, understanding scheme rules, seeking information, filing complaints if necessary."})
process['stakeholders'].append({"stakeholder": "Retirement Benefits Schemes (Occupational, Individual, Umbrella)", "role": "Entities established to provide retirement benefits; regulated and supervised by RBA", "responsibilities": "(INFERRED) Complying with RBA regulations, managing funds prudently, providing accurate member statements."})
process['stakeholders'].append({"stakeholder": "Scheme Trustees", "role": "Fiduciaries responsible for managing scheme assets and ensuring compliance; appointed/approved by RBA", "responsibilities": "(INFERRED) Acting in members' best interest, overseeing fund managers/administrators, ensuring compliance."})
process['stakeholders'].append({"stakeholder": "Fund Managers", "role": "Professional entities appointed to invest scheme assets; licensed by RBA", "responsibilities": "(INFERRED) Investing funds according to guidelines, providing investment reports, adhering to RBA regulations."})
process['stakeholders'].append({"stakeholder": "Scheme Administrators", "role": "Entities responsible for day-to-day administration of schemes (e.g., record-keeping, benefit processing); licensed by RBA", "responsibilities": "(INFERRED) Maintaining accurate records, processing benefits, complying with RBA rules."})
process['stakeholders'].append({"stakeholder": "Employers (Sponsors of schemes)", "role": "Establish and contribute to occupational schemes for their employees; responsible for timely remittances", "responsibilities": "(INFERRED) Establishing schemes, remitting contributions, providing information to members."})
process['stakeholders'].append({"stakeholder": "National Social Security Fund (NSSF)", "role": "Statutory pension scheme; regulated by RBA", "responsibilities": "(INFERRED) Complying with RBA regulations, managing contributions and benefits as per NSSF Act."})
process['stakeholders'].append({"stakeholder": "Financial Institutions (Banks, Investment Firms)", "role": "Serve as custodians of scheme assets and provide other financial services to the sector", "responsibilities": "(INFERRED) Safekeeping assets, providing banking services, adhering to financial regulations."})
process['stakeholders'].append({"stakeholder": "Actuaries / Consultants", "role": "Provide expert advice on scheme design, valuation, and financial soundness", "responsibilities": "(INFERRED) Providing professional advice, ensuring schemes are financially viable."})
process['stakeholders'].append({"stakeholder": "Industry Associations (e.g., Association of Pension Schemes in Kenya (APEK))", "role": "Represent the interests of retirement benefits industry stakeholders; collaborate with RBA on policy matters", "responsibilities": "(INFERRED) Advocating for members, collaborating on industry standards, providing feedback to RBA."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (National Treasury, Ministry of Labour and Social Protection)", "role": "Provides policy direction, funding, and legislative framework for the social protection sector", "responsibilities": "(INFERRED) Formulating social security policies, ensuring regulatory framework, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Other Regulatory Bodies (e.g., Central Bank of Kenya (CBK), Capital Markets Authority (CMA))", "role": "Collaborate with RBA on financial sector regulation and oversight", "responsibilities": "(INFERRED) Sharing information, coordinating regulatory efforts, ensuring financial system stability."})

process['as_is_narrative'] = "(INFERRED) The Retirement Benefits Authority (RBA) executes its mandate through a rigorous regulatory and supervisory framework. It issues licenses and approvals for the establishment of new retirement benefits schemes, as well as for key service providers such as trustees, fund managers, and scheme administrators. RBA reviews and approves scheme rules, trust deeds, and investment policies to ensure they comply with the Retirement Benefits Act and safeguard members' interests. The Authority conducts regular on-site and off-site inspections and audits of schemes and service providers to monitor compliance, assess financial soundness, and identify any irregularities. A crucial function is the investigation of complaints from scheme members and sponsors, with RBA providing a mechanism for dispute resolution and taking enforcement actions, including imposing penalties or sanctions, against non-compliant entities. RBA plays a proactive role in promoting the growth of the retirement benefits sector through continuous public education and awareness campaigns aimed at encouraging savings for retirement and improving financial literacy. It also advises the government on necessary policy and legislative changes to enhance the retirement benefits system, collects and analyzes industry data for market insights, and collaborates with other financial sector regulators like the Central Bank of Kenya and Capital Markets Authority to maintain overall financial system stability and integrity."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.rba.go.ke/", # Official website
    "https://uonbi.ac.ke/", # Provided context
    "https://chweya.com/", # Provided context
    "https://businessradar.co.ke/", # Provided context
    "https://majira.co.ke/", # Provided context
    "https://divani.co.ke/", # Provided context
    "https://thesharpdaily.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-second process enriched and combined_data.json updated.")
