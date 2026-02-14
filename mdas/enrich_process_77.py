
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-eighth process (index 77)
process = data['processes'][77]

# Populate fields
process['executive_summary'] = "The National Social Security Fund (NSSF) is a statutory public institution in Kenya mandated to provide social security protection to all workers, encompassing both the formal and informal sectors. Established initially as a Provident Fund in 1965, NSSF transitioned into a Pension Scheme in 2014 following the enactment of the NSSF Act, No. 45 of 2013. Its core purpose is to guarantee basic compensation in cases of permanent disability, provide assistance to needy dependents in the event of death, and offer a monthly life pension upon retirement. Beyond these direct benefits, NSSF also mobilizes domestic savings, aids in poverty reduction, fosters financial inclusion, and helps decrease the national dependency ratio."
process['process_overview']['process_objective'] = "To register eligible individuals for social security across all sectors; to efficiently receive and manage contributions from its members and their employers; to oversee the funds of the scheme to ensure their sustainability, growth, and proper investment; to process and disburse various benefits, including retirement, survivor, and invalidity benefits, to eligible members or their dependents in a timely manner; to guarantee basic compensation in cases of permanent disability; to provide assistance to needy dependents in the event of a member's death; to offer a monthly life pension upon retirement to ensure income security; to mobilize domestic savings for national development; to aid in poverty reduction by providing a social safety net; to foster financial inclusion by reaching out to the informal sector; and to decrease the dependency ratio by encouraging self-reliance in old age."
process['process_overview']['policy_legal_context'].append("Initially established in 1965 as a Provident Fund, NSSF transitioned into a Pension Scheme in 2014 following the enactment of the NSSF Act, No. 45 of 2013, which provides the current legal framework for its operations. NSSF operates under the Ministry of Labour and Social Protection (or the relevant government ministry responsible for social protection) and is guided by national social security policies and labor laws aimed at expanding social protection coverage and ensuring the well-being of Kenyan workers and their families.")
process['stakeholders'].append({"stakeholder": "Kenyan Workers (Formal and Informal Sectors)", "role": "Members of NSSF; contributors to the fund and beneficiaries of its schemes", "responsibilities": "(INFERRED) Registering with NSSF, making regular contributions, understanding their benefits."})
process['stakeholders'].append({"stakeholder": "Employers (Public and Private Sector)", "role": "Responsible for remitting employee contributions to NSSF and ensuring compliance", "responsibilities": "(INFERRED) Registering with NSSF, deducting and remitting contributions promptly, complying with NSSF Act."})
process['stakeholders'].append({"stakeholder": "Beneficiaries / Dependents of Members", "role": "Receive survivor benefits in the event of a member's death", "responsibilities": "(INFERRED) Submitting claims, providing required documentation."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (Ministry of Labour and Social Protection, National Treasury)", "role": "Provides policy direction, oversight, and legislative framework for NSSF", "responsibilities": "(INFERRED) Formulating social security policies, ensuring regulatory compliance, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Retirement Benefits Authority (RBA)", "role": "Regulates and supervises retirement benefits schemes in Kenya, including NSSF", "responsibilities": "(INFERRED) Ensuring NSSF compliance with RBA regulations, protecting members' interests."})
process['stakeholders'].append({"stakeholder": "Trade Unions / Worker Associations", "role": "Represent workers' interests; engage with NSSF on member welfare and policy issues", "responsibilities": "(INFERRED) Advocating for members, collaborating on social security policy, educating members."})
process['stakeholders'].append({"stakeholder": "Employer Federations", "role": "Represent employers' interests; engage with NSSF on employer compliance and policy", "responsibilities": "(INFERRED) Advising members on NSSF compliance, collaborating on policy."})
process['stakeholders'].append({"stakeholder": "Financial Institutions (for investments)", "role": "Managed by NSSF for the investment of scheme funds", "responsibilities": "(INFERRED) Providing investment opportunities, managing funds prudently, adhering to investment guidelines."})
process['stakeholders'].append({"stakeholder": "Pension Scheme Managers", "role": "Provide technical expertise in pension scheme administration and management", "responsibilities": "(INFERRED) Advising NSSF on best practices, ensuring efficient administration."})
process['stakeholders'].append({"stakeholder": "International Social Security Organizations", "role": "Provide benchmarks, technical support, and best practices for social security systems", "responsibilities": "(INFERRED) Sharing knowledge, collaborating on social protection initiatives."})

process['as_is_narrative'] = "(INFERRED) The NSSF operates through a continuous cycle of member registration, contribution management, fund investment, and benefit disbursement. It actively registers new members from both formal and informal sectors, providing them with unique membership numbers. Employers are responsible for deducting and remitting monthly contributions for their employees, while self-employed individuals make voluntary contributions. NSSF has robust systems for receiving, accurately recording, and reconciling these contributions. The accumulated funds are strategically invested in various financial instruments (e.g., government securities, real estate, equities) under strict regulatory guidelines to ensure capital preservation, long-term sustainability, and growth for members' benefits. NSSF manages a comprehensive claims processing system for different benefit types (age, invalidity, survivor, withdrawal), verifying eligibility and disbursing payments to members or their dependents. It conducts extensive public awareness and education campaigns to inform workers and employers about their rights and obligations under the NSSF Act. NSSF also collaborates with government agencies, labor unions, and employer federations to expand social security coverage, particularly among the informal sector, and to ensure adherence to regulatory guidelines set by bodies like the Retirement Benefits Authority (RBA). Digitization of services (e.g., online registration, mobile payments) is an ongoing effort to enhance efficiency and accessibility."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.nssf.or.ke/", # Official website
    "https://mygov.go.ke/", # Provided context
    "https://ecitizen.go.ke/", # Provided context
    "https://sokodirectory.com/", # Provided context
    "https://cytonn.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-eighth process enriched and combined_data.json updated.")
