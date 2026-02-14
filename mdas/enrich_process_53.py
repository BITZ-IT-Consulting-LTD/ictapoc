
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-fourth process (index 53)
process = data['processes'][53]

# Populate fields
process['executive_summary'] = "The Kenya Investment Authority (KenInvest) is a statutory body established under the Investment Promotion Act No. 6 of 2004. Its core mandate is to promote and facilitate both local and foreign investments in Kenya, acting as a one-stop center for investors, thereby improving the investment climate, fostering economic growth, and contributing to job creation and national development."
process['process_overview']['process_objective'] = "To promote Kenya as a competitive investment destination globally; to assist investors with business registration, licensing, and navigating regulatory requirements; to provide comprehensive information on investment opportunities, incentives, and the business climate; to advocate for policy reforms that enhance the investment climate; and to offer investor aftercare services to ensure successful project implementation and retention of investments."
process['process_overview']['policy_legal_context'].append("Established under the Investment Promotion Act No. 6 of 2004, which provides the legal framework for its investment promotion and facilitation activities. Operates under the relevant government ministry responsible for trade and industry, and aligns with national development blueprints like Vision 2030.")
process['stakeholders'].append({"stakeholder": "Local Investors", "role": "Individuals and entities investing domestically", "responsibilities": "(INFERRED) Complying with investment regulations, contributing to local economy."})
process['stakeholders'].append({"stakeholder": "Foreign Investors", "role": "International entities bringing capital and expertise into Kenya", "responsibilities": "(INFERRED) Adhering to Kenyan laws, transferring technology, creating employment."})
process['stakeholders'].append({"stakeholder": "Government (various ministries, especially Trade and Industry)", "role": "Policy makers and collaborators in creating a conducive investment environment", "responsibilities": "(INFERRED) Formulating investor-friendly policies, providing oversight to KenInvest."})
process['stakeholders'].append({"stakeholder": "Regulatory Bodies (e.g., BRS, KRA)", "role": "Agencies involved in business registration, taxation, and compliance", "responsibilities": "(INFERRED) Streamlining regulatory processes, collaborating with KenInvest for investor facilitation."})
process['stakeholders'].append({"stakeholder": "SMEs (Small and Medium Enterprises)", "role": "Local businesses supported by KenInvest's facilitation efforts", "responsibilities": "(INFERRED) Growing their businesses, creating local employment."})
process['stakeholders'].append({"stakeholder": "International Organizations", "role": "Partners in promoting investment, economic development, and technical assistance", "responsibilities": "(INFERRED) Collaborating on investment promotion initiatives, providing support."})
process['stakeholders'].append({"stakeholder": "Business Associations", "role": "Representing the interests of the business community and providing feedback on investment climate", "responsibilities": "(INFERRED) Advocating for members, partnering with KenInvest on business development."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in identifying and promoting investment opportunities at the county level", "responsibilities": "(INFERRED) Creating conducive local investment environments, facilitating county-level projects."})

process['as_is_narrative'] = "(INFERRED) KenInvest operates as a proactive investment promotion agency, actively marketing Kenya as an attractive investment destination through various campaigns and participation in international forums. It serves as a crucial 'one-stop shop' for investors, providing a single point of contact for information, advice, and assistance with complex licensing, registration, and regulatory procedures. The Authority collects and disseminates comprehensive data on investment opportunities, sector-specific incentives, and the overall business climate. Furthermore, KenInvest plays an advocacy role by advising the government on policy reforms to improve the ease of doing business and offers essential aftercare services to existing investors, addressing operational challenges and ensuring the long-term success and expansion of their projects in Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.invest.go.ke/",
    "https://saraka.info/", # Provided context
    "https://unido.org/", # Provided context
    "https://mfa.ir/", # Provided context
    "https://eac.int/", # Provided context
    "https://kenyaembassyparis.fr/", # Provided context
    "https://investmentkenya.com/", # Provided context
    "https://investmentpromotion.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-fourth process enriched and combined_data.json updated.")
