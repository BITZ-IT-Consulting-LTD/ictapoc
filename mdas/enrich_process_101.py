
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and second process (index 101)
process = data['processes'][101]

# Populate fields
process['executive_summary'] = "The Capital Markets Authority (CMA) Kenya is an independent public agency established in 1989 by the Capital Markets Act Cap 485A. Its dual mandate is to regulate and facilitate the development of orderly, fair, and efficient capital markets in Kenya. CMA's primary responsibility is to protect the interests of investors, government, employees, issuers of securities, and market intermediaries. By ensuring market integrity, transparency, and investor confidence, CMA plays a vital role in mobilizing and allocating capital resources to finance long-term productive investments for Kenya's economic growth and development."
process['process_overview']['process_objective'] = "To license and supervise all capital market intermediaries, including stockbrokers, investment banks, fund managers, and collective investment schemes; to ensure the proper conduct of all licensed persons and market institutions; to regulate the issuance of capital market products, including bonds, shares, Exchange Traded Funds (ETFs), and Real Estate Investment Trusts (REITs), as well as market activities like online forex trading; to promote market development through research on new products and institutions, fostering product innovation, supporting institutional capacity development, and stimulating robust market infrastructure; to educate investors and raise public awareness to enhance financial literacy; to protect investors' interests from financial loss and ensure market integrity, including operating a compensation fund; to oversee trading activity on the Nairobi Securities Exchange (NSE) and enforce compliance with disclosure standards; to develop a framework to facilitate the use of electronic commerce for the advancement of capital markets in Kenya; and to enforce compliance with capital market laws and regulations, including imposing fines, suspending or revoking licenses, investigating complaints, and pursuing prosecution for financial misconduct."
process['process_overview']['policy_legal_context'].append("Established by the Capital Markets Act Cap 485A Laws of Kenya in 1989 (inaugurated in 1990), which provides the comprehensive legal and regulatory framework for capital markets operations. CMA operates under the National Treasury and Planning and is crucial for implementing government financial sector policies, attracting both domestic and foreign investment, and ensuring market stability and investor confidence in line with national development agendas like Vision 2030 and financial inclusion strategies.")
process['stakeholders'].append({"stakeholder": "Investors (Retail, Institutional, Local, Foreign)", "role": "Primary participants in the capital markets; their interests are protected by CMA's regulatory oversight", "responsibilities": "(INFERRED) Making informed investment decisions, understanding market risks, complying with regulations."})
process['stakeholders'].append({"stakeholder": "Listed Companies / Issuers of Securities", "role": "Raise capital through the markets; subject to CMA's disclosure and listing requirements", "responsibilities": "(INFERRED) Complying with listing rules, ensuring transparent disclosures, meeting corporate governance standards."})
process['stakeholders'].append({"stakeholder": "Capital Market Intermediaries (Stockbrokers, Investment Banks, Fund Managers, Collective Investment Schemes)", "role": "Licensed entities that facilitate capital market transactions and provide services to investors and issuers", "responsibilities": "(INFERRED) Complying with licensing conditions, ethical conduct, providing professional services, adhering to regulations."})
process['stakeholders'].append({"stakeholder": "Nairobi Securities Exchange (NSE)", "role": "Facilitates trading of listed securities; licensed and supervised by CMA", "responsibilities": "(INFERRED) Operating an orderly market, enforcing listing rules, providing trading platforms."})
process['stakeholders'].append({"stakeholder": "Central Depository and Settlement Corporation (CDSC)", "role": "Provides clearing, settlement, and depository services for securities traded on the NSE; supervised by CMA", "responsibilities": "(INFERRED) Ensuring efficient settlement, maintaining investor records, safeguarding securities."})
process['stakeholders'].append({"stakeholder": "National Treasury and Planning", "role": "Parent Ministry providing policy direction, funding, and oversight to CMA", "responsibilities": "(INFERRED) Formulating fiscal and financial sector policies, allocating resources, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Central Bank of Kenya (CBK)", "role": "Monetary policy authority and bank regulator; collaborates with CMA on financial system stability", "responsibilities": "(INFERRED) Regulating banking sector, ensuring financial sector stability, collaborating on financial reforms."})
process['stakeholders'].append({"stakeholder": "Retirement Benefits Authority (RBA)", "role": "Regulates pension schemes; collaborates with CMA on investment guidelines for pension funds in capital markets", "responsibilities": "(INFERRED) Regulating pension sector, collaborating on investment policies."})
process['stakeholders'].append({"stakeholder": "Insurance Regulatory Authority (IRA)", "role": "Regulates insurance companies; collaborates with CMA on investment guidelines for insurance funds in capital markets", "responsibilities": "(INFERRED) Regulating insurance sector, collaborating on investment policies."})
process['stakeholders'].append({"stakeholder": "Government Agencies", "role": "May issue government securities (e.g., Treasury Bonds) or seek advice from CMA", "responsibilities": "(INFERRED) Utilizing capital markets for financing, complying with CMA regulations."})
process['stakeholders'].append({"stakeholder": "Legal Professionals", "role": "Provide legal advice to market participants and assist CMA in enforcement matters", "responsibilities": "(INFERRED) Advising clients on capital market laws, assisting in compliance and dispute resolution."})
process['stakeholders'].append({"stakeholder": "Financial Media", "role": "Disseminate market information to the public; play a role in investor education", "responsibilities": "(INFERRED) Reporting market news, educating investors, promoting transparency."})
process['stakeholders'].append({"stakeholder": "Academic Institutions", "role": "Conduct research on capital markets and provide training for market professionals", "responsibilities": "(INFERRED) Developing market-relevant curricula, providing training, conducting research."})

process['as_is_narrative'] = "(INFERRED) The Capital Markets Authority (CMA) implements its dual mandate through a rigorous and comprehensive regulatory and facilitative framework. It receives, vets, and issues licenses to various capital market intermediaries, including stockbrokers, investment banks, fund managers, and collective investment schemes, ensuring they meet strict financial, operational, and ethical standards. CMA develops and enforces a robust set of rules and regulations governing the issuance and trading of diverse capital market products (e.g., equities, corporate bonds, REITs, ETFs) and approves all public offers and listings. A core operational aspect is continuous market surveillance of the Nairobi Securities Exchange (NSE) to detect, investigate, and prevent market abuse, insider trading, and other illicit activities, thereby ensuring market integrity. The Authority actively promotes market development by conducting research into new products and market structures, encouraging innovation, and supporting the enhancement of market infrastructure. Investor protection is paramount, with CMA implementing extensive investor education and public awareness programs to enhance financial literacy and market participation. It investigates complaints from investors and takes strong enforcement actions, which may include imposing fines, suspending or revoking licenses, or pursuing prosecution against individuals and entities found guilty of market misconduct. CMA also oversees a compensation fund designed to protect investors against financial losses resulting from the failure of a licensed intermediary. It collaborates closely with other financial sector regulators (e.g., Central Bank of Kenya, Retirement Benefits Authority, Insurance Regulatory Authority) to ensure systemic stability and a coordinated approach to financial regulation, and provides expert advice to the government on capital market policy reforms aimed at deepening and broadening Kenya's capital markets to support long-term economic development."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official websites and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.cmarcp.or.ke/", # Official website
    "https://policyvault.africa/", # Provided Capital Markets Act details
    "https://infoshop.org/", # Provided context
    "https://wikipedia.org/", # Provided context
    "https://saraka.info/", # Provided context
    "https://serrarigroup.com/", # Provided context
    "https://thekenyatimes.com/", # Provided context
    "https://youtube.com/", # Provided context
    "https://payatlas.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and second process enriched and combined_data.json updated.")
