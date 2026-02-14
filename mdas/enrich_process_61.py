
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-second process (index 61)
process = data['processes'][61]

# Populate fields
process['executive_summary'] = "The Kenya Railways Corporation (KRC) is a state corporation established in 1978 under the Kenya Railways Corporation Act (Cap 397) of the Laws of Kenya. KRC is mandated to provide efficient and effective railway and inland waterways transport services. It plays a pivotal role in national and metropolitan railway network development, facilitating the movement of passengers and cargo, connecting Kenya and the East and Central African region to global markets, and significantly contributing to economic growth and regional integration."
process['process_overview']['process_objective'] = "To provide efficient, safe, and reliable railway and inland waterways transport services for both passengers and cargo; to promote, facilitate, and actively participate in national and metropolitan railway network development, including the Standard Gauge Railway (SGR) and revitalization of the Meter Gauge Railway (MGR); to offer skills and technology for the railway sector; to leverage its assets for business growth and optimal resource utilization; and to develop an integrated, safe, reliable, and sustainable rail transport system that meets the evolving needs of the country and region."
process['process_overview']['policy_legal_context'].append("Established in 1978 under the Kenya Railways Corporation Act (Cap 397) of the Laws of Kenya. Its formation followed the dissolution of the East African Community, leading to independent national railway operations. KRC operates under the Ministry of Transport and aligns its operations with national development blueprints like Vision 2030 and regional integration objectives of the East African Community. It is also guided by various international railway safety and operational standards.")
process['stakeholders'].append({"stakeholder": "Passengers", "role": "Users of railway passenger services for travel and commuting", "responsibilities": "(INFERRED) Purchasing tickets, adhering to safety regulations, respecting railway property."})
process['stakeholders'].append({"stakeholder": "Cargo Owners (Importers / Exporters)", "role": "Businesses and individuals utilizing railway services for freight transport", "responsibilities": "(INFERRED) Packaging goods appropriately, complying with cargo regulations, providing timely documentation."})
process['stakeholders'].append({"stakeholder": "Kenya Ports Authority (KPA)", "role": "Key partner for intermodal transport, particularly for cargo from Mombasa Port", "responsibilities": "(INFERRED) Coordinating cargo transfer, facilitating seamless logistics from port to rail."})
process['stakeholders'].append({"stakeholder": "National Government (Ministry of Transport)", "role": "Parent Ministry providing policy direction, oversight, and funding", "responsibilities": "(INFERRED) Formulating transport policies, funding railway development projects."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in metropolitan railway development and local transport planning", "responsibilities": "(INFERRED) Collaborating on urban rail projects, integrating local transport networks."})
process['stakeholders'].append({"stakeholder": "Railway Sector Employees", "role": "Workforce involved in all aspects of railway operations, maintenance, and administration", "responsibilities": "(INFERRED) Operating trains, maintaining infrastructure, ensuring safety."})
process['stakeholders'].append({"stakeholder": "Local Communities along railway lines", "role": "Residents living near railway corridors; affected by operations and potential beneficiaries of services", "responsibilities": "(INFERRED) Respecting railway safety zones, utilizing railway services where available."})
process['stakeholders'].append({"stakeholder": "Development Partners / Financiers", "role": "Provide financial and technical support for railway infrastructure projects", "responsibilities": "(INFERRED) Funding railway expansion, sharing technical expertise."})
process['stakeholders'].append({"stakeholder": "Manufacturers / Suppliers of railway equipment", "role": "Provide locomotives, rolling stock, tracks, and other railway components", "responsibilities": "(INFERRED) Supplying quality equipment, adhering to specifications."})
process['stakeholders'].append({"stakeholder": "Road Transport Sector (for intermodal transport)", "role": "Competitors and collaborators for last-mile delivery and regional transport", "responsibilities": "(INFERRED) Providing complementary transport services, facilitating intermodal transfers."})

process['as_is_narrative'] = "(INFERRED) KRC's current operations focus on both passenger and cargo services. Passenger services include the modern Standard Gauge Railway (SGR) between Mombasa and Nairobi, and the commuter services within the Nairobi Metropolitan Area, alongside the revitalized Meter Gauge Railway (MGR) for upcountry routes. Cargo operations, a significant revenue stream, involve transporting goods, particularly from the Port of Mombasa (in coordination with KPA) to various inland container depots and destinations across the country and the wider East African region. KRC is responsible for the continuous maintenance and upgrading of its vast railway infrastructure, including tracks, bridges, stations, and rolling stock, to ensure safety and efficiency. The Corporation is actively involved in the development and expansion of new railway lines and metropolitan networks to improve connectivity and decongest urban areas. Furthermore, KRC prioritizes safety and security through strict operational protocols, invests in modern technology for train operations and signaling, and develops human capital through specialized training, all aimed at providing a seamless, reliable, and integrated transport solution for Kenya's economic growth."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.krc.co.ke/",
    "https://ecitizen.go.ke/", # Provided context
    "https://wikipedia.org/", # Provided context
    "https://developmentaid.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-second process enriched and combined_data.json updated.")
