
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-second process (index 91)
process = data['processes'][91]

# Populate fields
process['executive_summary'] = "The Auctioneers Licensing Board is the primary regulatory body for auctioneers in Kenya, established under Section 3(1) of the Auctioneers Act, Cap 1996 of the Laws of Kenya. Its core mandate is to exercise general supervision and control over the business and practice of auctioneers, ensuring high standards of learning, professional competence, and ethical conduct within the profession. The Board plays a crucial role in maintaining public trust and ensuring fair and transparent practices in the disposal of movable and immovable property."
process['process_overview']['process_objective'] = "To set, maintain, and continuously improve the standards of learning, professional competence, and professional conduct for the provision of auctioneering services in Kenya; to determine, maintain, and enhance the standards of professional practice and ethical conduct for the auctioneering profession; to issue licenses to individuals and firms who wish to practice as auctioneers; to regulate the licensing and conduct of auctioneers; and to outline the responsibilities of auctioneers, the application process for licenses, and penalties for non-compliance with the Auctioneers Act and associated regulations."
process['process_overview']['policy_legal_context'].append("Established under Section 3(1) of the Auctioneers Act, Cap 1996 of the Laws of Kenya, which provides the comprehensive legal framework for the Board's regulatory functions over the auctioneering profession. The Board operates under the Ministry of Lands (or the relevant government ministry responsible for land, property, and justice administration) and is crucial for ensuring integrity, fairness, and transparency in processes involving the valuation and disposal of movable and immovable property through auction, thereby protecting the public interest.")
process['stakeholders'].append({"stakeholder": "Auctioneers (licensed individuals and firms)", "role": "Practicing professionals who must comply with the Board's regulations and licensing requirements", "responsibilities": "(INFERRED) Adhering to the Auctioneers Act, ethical conduct, proper execution of auction processes, maintaining professionalism."})
process['stakeholders'].append({"stakeholder": "Courts of Law (for execution of decrees and orders)", "role": "Utilize auctioneers for the execution of court orders, sale of attached property, etc.", "responsibilities": "(INFERRED) Issuing instructions to licensed auctioneers, overseeing execution processes."})
process['stakeholders'].append({"stakeholder": "Financial Institutions (Banks, Saccos)", "role": "Engage auctioneers for the recovery of debts through the sale of charged properties", "responsibilities": "(INFERRED) Appointing licensed auctioneers, complying with legal procedures for asset recovery."})
process['stakeholders'].append({"stakeholder": "Landlords (for distress for rent)", "role": "Engage auctioneers to recover rent arrears through distress for rent processes", "responsibilities": "(INFERRED) Appointing licensed auctioneers, adhering to legal procedures for rent recovery."})
process['stakeholders'].append({"stakeholder": "Clients / Public (whose property is being auctioned)", "role": "Individuals or entities whose property is subject to auction; protected by the Board's regulatory oversight", "responsibilities": "(INFERRED) Understanding auction processes, seeking fair treatment, lodging complaints if necessary."})
process['stakeholders'].append({"stakeholder": "Debtors / Property Owners", "role": "Individuals who owe debts leading to property attachment and auction; their rights are protected by due process", "responsibilities": "(INFERRED) Complying with legal notices, seeking legal advice, participating in resolution."})
process['stakeholders'].append({"stakeholder": "Lawyers", "role": "Represent clients (creditors, debtors, landlords) in matters involving auctioneers", "responsibilities": "(INFERRED) Advising clients on legal aspects of auctions, ensuring due process."})
process['stakeholders'].append({"stakeholder": "Kenya National Bureau of Statistics (KNBS) (for data on property transactions)", "role": "Collects data relevant to property transactions, which may include auction sales", "responsibilities": "(INFERRED) Collecting and disseminating statistical data relevant to the economy."})
process['stakeholders'].append({"stakeholder": "Ministry of Lands (Oversight)", "role": "Provides administrative oversight and policy guidance to the Board", "responsibilities": "(INFERRED) Formulating land policies, ensuring regulatory alignment."})

process['as_is_narrative'] = "(INFERRED) The Auctioneers Licensing Board performs a critical regulatory function to ensure the integrity and efficiency of the auctioneering profession in Kenya. Its operations commence with the rigorous process of receiving and scrutinizing applications for new auctioneer licenses and renewals. This involves vetting applicants to confirm they meet stringent criteria for qualification, professional experience, financial stability, and good conduct as prescribed by the Auctioneers Act. Upon successful vetting, the Board issues annual licenses, which are prerequisites for practicing as an auctioneer. A significant ongoing function is the development and enforcement of a comprehensive code of conduct and ethical guidelines that all licensed auctioneers must adhere to. The Board actively investigates complaints lodged by members of the public, courts, financial institutions, or other stakeholders against auctioneers regarding misconduct, malpractice, or non-compliance with the Act. Depending on the findings, the Board takes appropriate disciplinary actions, which can range from warnings and fines to suspension or revocation of licenses. It maintains an up-to-date public register of all licensed auctioneers, enhancing transparency. The Board also collaborates with relevant government agencies (e.g., Judiciary, Ministry of Lands) and professional bodies to promote continuous professional development for auctioneers and advises the government on necessary policy and legislative reforms to ensure the auctioneering profession remains responsive to economic and legal developments, thereby protecting both the public and the integrity of the process."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://parliament.go.ke/", # Provided context (Auctioneers Act)
    "https://zhiyanbao.cn/", # Provided context
    "https://uonbi.ac.ke/", # Provided context
    "https://scribd.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-second process enriched and combined_data.json updated.")
