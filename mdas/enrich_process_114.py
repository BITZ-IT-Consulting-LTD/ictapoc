
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and fifteenth process (index 114)
process = data['processes'][114]

# Populate fields
process['executive_summary'] = "Consolidated Bank of Kenya is a commercial bank regulated by the Central Bank of Kenya, providing a comprehensive range of banking services and products to individuals and businesses across the country. Its offerings encompass various account types, loan products, trade finance facilities, and modern e-banking and m-banking services. The bank aims to support economic growth, foster financial inclusion, and contribute to the stability and development of the Kenyan financial sector, while striving to achieve profitability for its stakeholders."
process['process_overview']['process_objective'] = "To provide a diverse range of personal banking products, including various account types (e.g., E-Cash, Solid Plus, Current, Dream Saver, Junior Saver, Diamond, Ace Salary Accounts) and loan products (e.g., Personal Loan, Mortgage Loan, Solid Scholar Loan, Asset Finance); to offer comprehensive business banking solutions, including deposit products and loan products (e.g., Business Term Loan, Commercial Construction Loan, Insurance Financing); to provide trade finance facilities such as Bid Bonds, Performance Bonds, Bills Discounting, and Invoice Discounting; to facilitate e-banking and m-banking services, allowing for convenient balance inquiries, fund transfers, airtime purchases, and MPESA transactions; and to act as a commercial bank, fostering economic growth and financial inclusion in Kenya by providing accessible and relevant financial services to a wide range of customers."
process['process_overview']['policy_legal_context'].append("Consolidated Bank of Kenya operates as a commercial bank regulated by the Central Bank of Kenya (CBK). Its operations are governed by the Banking Act (Cap 488) of the Laws of Kenya, the CBK Act, and other relevant prudential guidelines and circulars issued by the CBK. The bank is crucial for implementing national financial sector policies, promoting financial inclusion, and contributing to the stability and integrity of the Kenyan financial system.")
process['stakeholders'].append({"stakeholder": "Individual Customers (Savers, Borrowers)", "role": "Primary users of the bank's personal banking products and services", "responsibilities": "(INFERRED) Managing personal finances, saving, borrowing responsibly, utilizing banking services."})
process['stakeholders'].append({"stakeholder": "Business Customers (SMEs, Corporates)", "role": "Users of the bank's business banking products, loans, and trade finance facilities", "responsibilities": "(INFERRED) Managing business finances, seeking credit, utilizing trade finance, growing their businesses."})
process['stakeholders'].append({"stakeholder": "Central Bank of Kenya (CBK) (Regulator)", "role": "The primary regulatory authority for commercial banks in Kenya; ensures financial stability and compliance", "responsibilities": "(INFERRED) Licensing banks, setting prudential guidelines, monitoring financial sector, enforcing banking laws."})
process['stakeholders'].append({"stakeholder": "Kenya Deposit Insurance Corporation (KDIC)", "role": "Provides deposit insurance to protect depositors in case of bank failure", "responsibilities": "(INFERRED) Insuring deposits, resolving problem banks, protecting financial stability."})
process['stakeholders'].append({"stakeholder": "Shareholders", "role": "Owners of the bank; benefit from the bank's profitability and growth", "responsibilities": "(INFERRED) Investing in the bank, exercising ownership rights, holding management accountable."})
process['stakeholders'].append({"stakeholder": "Employees", "role": "Workforce responsible for the bank's operations, customer service, and product delivery", "responsibilities": "(INFERRED) Providing banking services, adhering to bank policies, contributing to customer satisfaction."})
process['stakeholders'].append({"stakeholder": "Correspondent Banks", "role": "International banks that facilitate cross-border transactions for Consolidated Bank", "responsibilities": "(INFERRED) Facilitating international payments, managing foreign currency transactions."})
process['stakeholders'].append({"stakeholder": "Payment Service Providers (e.g., MPESA)", "role": "Partners for mobile banking and payment services, enhancing accessibility for customers", "responsibilities": "(INFERRED) Providing mobile payment infrastructure, collaborating on digital financial services."})
process['stakeholders'].append({"stakeholder": "Government of Kenya", "role": "Owner (directly or indirectly) and key policy maker; benefits from economic growth and financial stability", "responsibilities": "(INFERRED) Setting economic policies, ensuring regulatory environment, utilizing banking services."})
process['stakeholders'].append({"stakeholder": "Bancassurance Subsidiary (CBL Bancassurance Intermediary Limited)", "role": "Provides insurance products through the bank's channels, enhancing comprehensive financial solutions", "responsibilities": "(INFERRED) Distributing insurance products, advising customers, contributing to non-interest income."})

process['as_is_narrative'] = "(INFERRED) Consolidated Bank of Kenya operates by fulfilling its mandate as a commercial bank through a diverse range of activities. It actively mobilizes deposits from individual customers, SMEs, and corporate clients through various current, savings, and call accounts, managing these funds to ensure liquidity and solvency. The bank extends credit facilities, including personal loans, mortgages, asset finance, and business term loans, to support investment and consumption across different economic sectors. It facilitates both domestic and international trade by offering a suite of trade finance products such as letters of credit, bid bonds, performance bonds, and invoice discounting, thereby supporting importers and exporters. Consolidated Bank provides modern digital banking channels, including internet banking and mobile banking (e.g., through MPESA integration), allowing customers to perform transactions like balance inquiries, fund transfers, and utility payments conveniently. Its branch network serves as a key touchpoint for customer relationship management, complemented by digital support. The bank operates under strict regulatory compliance with all requirements set by the Central Bank of Kenya (CBK), including capital adequacy, liquidity management, and asset quality standards. It participates actively in national payment systems, ensuring efficient funds transfer and settlement. Furthermore, the bank contributes to financial inclusion by targeting various customer segments with accessible and tailored banking services, while strategically managing its balance sheet to achieve sustainable profitability for its shareholders and supporting the broader economic development of Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.consolidated-bank.com/", # Official website
    "https://wikipedia.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and fifteenth process enriched and combined_data.json updated.")
