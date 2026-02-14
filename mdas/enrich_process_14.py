
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifteenth process (index 14)
process = data['processes'][14]

# Populate fields
process['executive_summary'] = "The Ministry of Investment, Trade and Industry in Kenya is dedicated to driving economic recovery, growth, and transformation. It achieves this by promoting and facilitating domestic and foreign investments, enhancing trade opportunities, and fostering industrial development through initiatives like Special Economic Zones, Export Processing Zones, and value addition programs."
process['process_overview']['process_objective'] = "To promote and facilitate domestic and foreign investments into the Kenyan economy, develop and manage industrial infrastructure, promote exports and market access for Kenyan goods, and encourage value addition in key sectors to secure Kenya's economic future and contribute to national development."
process['process_overview']['policy_legal_context'].append("Mandate derived from its role in formulating, coordinating, and implementing National Industrialization, Private Sector, and Investment Policies, regulatory frameworks, and legislation. Key policies include the Special Economic Zones Policy and industrial property rights policies. (INFERRED: This implies a legislative basis for investment promotion, trade, and industrial development in Kenya.)")
process['stakeholders'].append({"stakeholder": "Domestic and Foreign Investors", "role": "Key contributors to economic growth through capital and job creation", "responsibilities": "(INFERRED) Investing in Kenya, adhering to investment regulations, creating employment."})
process['stakeholders'].append({"stakeholder": "Manufacturers/Industries", "role": "Producers of goods and services; beneficiaries of industrial development policies", "responsibilities": "(INFERRED) Engaging in value addition, contributing to industrial growth, adhering to quality standards."})
process['stakeholders'].append({"stakeholder": "Traders/Exporters", "role": "Entities involved in domestic and international trade of Kenyan goods and services", "responsibilities": "(INFERRED) Promoting Kenyan products, adhering to trade regulations, exploring new markets."})
process['stakeholders'].append({"stakeholder": "SMEs (Small and Medium Enterprises)", "role": "Significant contributors to employment and economic activity; beneficiaries of enterprise development initiatives", "responsibilities": "(INFERRED) Innovating, growing their businesses, contributing to local economies."})
process['stakeholders'].append({"stakeholder": "International Trade Organizations", "role": "Partners in promoting fair and open international trade", "responsibilities": "(INFERRED) Collaborating on trade agreements, providing technical assistance."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in developing County Aggregation and Industrial Parks (CAIPs)", "responsibilities": "(INFERRED) Collaborating on industrialization initiatives, providing local support."})


process['as_is_narrative'] = "(INFERRED) The Ministry operates by formulating investment and trade policies, facilitating investment through a One-Stop Investment Center, developing and overseeing industrial parks and special economic zones, promoting exports and market access, mobilizing resources for strategic projects, implementing local content policies, and championing automation and re-engineering of government business processes to improve ease of doing business."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from government-related sources) / medium (inferred legal basis, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://investmentpromotion.go.ke/",
    "https://parliament.go.ke/", # Though not primary, provided useful context in search
    "https://nipashebiz.co.ke/" # Though not primary, provided useful context in search
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifteenth process enriched and combined_data.json updated.")
