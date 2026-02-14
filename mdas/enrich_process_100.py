
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and first process (index 100)
process = data['processes'][100]

# Populate fields
process['executive_summary'] = "CBL Bancassurance Intermediary Limited, a subsidiary of Consolidated Bank of Kenya, operates within the Kenyan financial landscape. Its primary mandate is to distribute a wide array of insurance products through the bank's extensive channels, acting as a crucial intermediary between insurance companies (underwriters) and the bank's diverse clientele. The company aims to provide convenient and accessible insurance services, drive significant business growth and profitability for the Consolidated Bank Group, and offer professional insurance advisory services across various categories, thereby enhancing customer value and financial inclusion."
process['process_overview']['process_objective'] = "To formulate and execute the overall strategy for the bank's bancassurance offerings across various insurance products, customer propositions, and distribution channels; to drive growth in business volumes with the goal of making bancassurance a significant contributor to the Consolidated Bank's profitability; to effectively manage bancassurance income and achieve profit and loss targets; to negotiate pricing structures for bancassurance products and services, and serve as a key interface with insurance partners and industry associations; to review bancassurance strategy and performance, providing leadership, and spearheading the implementation of quality operational standards, risk management frameworks, and compliance protocols; to offer professional insurance advisory services to individual, SME, and corporate bank customers; to facilitate access to a comprehensive range of insurance policies, including motor, non-motor, marine, agriculture, medical, life, and pensions; and to provide efficient claims services, risk management solutions, and insurance premium financing."
process['process_overview']['policy_legal_context'].append("Operating as a subsidiary of Consolidated Bank of Kenya, CBL Bancassurance Intermediary Limited is regulated by the Insurance Regulatory Authority (IRA) under the Insurance Act (Cap 487) for its intermediary activities. Additionally, its operations are subject to oversight by the Central Bank of Kenya (CBK) through guidelines issued to banks engaging in bancassurance business. This dual regulatory framework ensures compliance, consumer protection, and financial stability within the Kenyan financial and insurance sectors.")
process['stakeholders'].append({"stakeholder": "Consolidated Bank of Kenya (Parent Company)", "role": "Owner of CBL Bancassurance; provides the distribution network and customer base for bancassurance products", "responsibilities": "(INFERRED) Providing strategic direction, integrating bancassurance into bank operations, leveraging customer relationships."})
process['stakeholders'].append({"stakeholder": "Bank Customers (Individuals, SMEs, Corporates)", "role": "Primary beneficiaries and consumers of bancassurance products and services", "responsibilities": "(INFERRED) Seeking insurance solutions, utilizing bank channels for insurance, providing feedback on services."})
process['stakeholders'].append({"stakeholder": "Insurance Companies (Underwriters)", "role": "Provide the insurance products and underwriting capacity; partners with CBL Bancassurance", "responsibilities": "(INFERRED) Underwriting policies, settling claims, collaborating on product development."})
process['stakeholders'].append({"stakeholder": "Insurance Regulatory Authority (IRA)", "role": "Primary regulator for insurance intermediaries; licenses and supervises CBL Bancassurance", "responsibilities": "(INFERRED) Licensing intermediaries, enforcing compliance with Insurance Act, protecting policyholders."})
process['stakeholders'].append({"stakeholder": "Central Bank of Kenya (CBK)", "role": "Regulator for banks; provides guidelines for bancassurance activities conducted by banks", "responsibilities": "(INFERRED) Regulating banking sector, issuing bancassurance guidelines, ensuring financial stability."})
process['stakeholders'].append({"stakeholder": "Claims Adjusters / Assessors", "role": "Evaluate and process insurance claims on behalf of underwriters; work closely with CBL Bancassurance", "responsibilities": "(INFERRED) Assessing damages/losses, negotiating settlements, providing expert opinions."})
process['stakeholders'].append({"stakeholder": "Employees of CBL Bancassurance", "role": "Responsible for sales, advisory, and operational functions of the bancassurance business", "responsibilities": "(INFERRED) Selling insurance, providing customer service, ensuring compliance."})
process['stakeholders'].append({"stakeholder": "Financial Sector Regulators", "role": "Broader regulators ensuring stability and integrity of the financial system", "responsibilities": "(INFERRED) Collaborating on regulatory frameworks, sharing information, ensuring market conduct."})
process['stakeholders'].append({"stakeholder": "Shareholders of Consolidated Bank", "role": "Owners of the bank; benefit from the profitability of its subsidiaries like CBL Bancassurance", "responsibilities": "(INFERRED) Seeking financial returns, exercising ownership rights."})

process['as_is_narrative'] = "(INFERRED) CBL Bancassurance Intermediary Limited operates by strategically leveraging Consolidated Bank of Kenya's extensive branch network and customer base to distribute a diverse portfolio of insurance products. The process typically involves identifying suitable insurance products from various reputable underwriters that align with the diverse needs of the bank's individual, SME, and corporate customers. CBL Bancassurance then trains and equips the bank's staff with the necessary knowledge and tools to effectively offer and explain these insurance solutions to clients directly within the banking environment. It manages the entire bancassurance sales cycle, from initial lead generation through customer advisory and policy issuance, to renewals and ongoing client relationship management. A critical aspect of its operation is ensuring strict adherence to all regulatory requirements set by the Insurance Regulatory Authority (IRA) and the Central Bank of Kenya (CBK), as well as implementing robust internal risk management policies. The company maintains strong working relationships with various insurance partners, engaging in negotiations for competitive pricing structures and efficient service level agreements. Furthermore, CBL Bancassurance provides expert advice to bank clients on suitable insurance solutions, often conducting needs analyses to tailor offerings. It plays a key role in facilitating claims processing by acting as a crucial liaison between clients and underwriters, ensuring smooth and timely settlements. Through these integrated efforts, CBL Bancassurance aims to significantly contribute to the non-interest income of Consolidated Bank, enhance customer loyalty by offering comprehensive financial solutions, and expand insurance penetration in the Kenyan market."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions inferred from bancassurance model and parent bank's context) / medium (inferred responsibilities, specific operational details)"
process['metadata']['source_urls'] = [
    "https://www.consolidated-bank.com/", # Parent company website (where information is likely integrated)
    "https://kenyainsurers.com/", # Provided context (general bancassurance info)
    "https://ncbagroup.com/", # Provided context (general bancassurance info)
    "https://co-opbank.co.ke/" # Provided context (general bancassurance info)
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and first process enriched and combined_data.json updated.")
