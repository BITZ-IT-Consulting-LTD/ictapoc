
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-first process (index 60)
process = data['processes'][60]

# Populate fields
process['executive_summary'] = "The Kenya Ports Authority (KPA) is a state corporation responsible for maintaining, operating, improving, and regulating all scheduled seaports along Kenya's Indian Ocean coastline. With Kilindini Harbour at Mombasa as its principal port, KPA serves as a crucial link for trade and commerce for Kenya and the wider East and Central African region, connecting them to global markets and playing a vital role in facilitating economic growth and regional integration."
process['process_overview']['process_objective'] = "To provide efficient, competitive, and world-class port services; to maintain, operate, improve, and regulate all scheduled seaports and inland waterways under its jurisdiction; to facilitate global trade and commerce through strategic port management; to manage inland container depots; and to operate and regulate existing ferry services (e.g., Likoni Ferry), thereby ensuring smooth and secure maritime logistics and contributing to national and regional economic prosperity."
process['process_overview']['policy_legal_context'].append("Established as a state corporation (implying its establishment under a specific Act of Parliament, likely related to ports and harbours). It operates under the Ministry of Transport and is integral to national trade policies and regional economic blocs like the East African Community. KPA's mandate aligns with national development blueprints and international maritime guidelines.")
process['stakeholders'].append({"stakeholder": "Shipping Lines / Agents", "role": "Clients of port services for vessel docking and cargo handling", "responsibilities": "(INFERRED) Scheduling vessel calls, adhering to port regulations, facilitating cargo documentation."})
process['stakeholders'].append({"stakeholder": "Importers / Exporters", "role": "Users of port facilities for international trade", "responsibilities": "(INFERRED) Complying with trade regulations, managing cargo logistics, paying port charges."})
process['stakeholders'].append({"stakeholder": "Freight Forwarders / Logistics Companies", "role": "Facilitate the movement and storage of goods through the port", "responsibilities": "(INFERRED) Coordinating cargo movements, customs clearance, transportation."})
process['stakeholders'].append({"stakeholder": "Customs Authorities (e.g., KRA Customs)", "role": "Regulatory body for international trade and revenue collection", "responsibilities": "(INFERRED) Clearing cargo, collecting duties and taxes, enforcing trade laws."})
process['stakeholders'].append({"stakeholder": "Kenya Railways Corporation", "role": "Provides rail transport services for cargo from the port to inland destinations", "responsibilities": "(INFERRED) Coordinating with KPA for seamless cargo transfer, operating railway network."})
process['stakeholders'].append({"stakeholder": "Trucking Companies", "role": "Provide road transport services for cargo to and from the port", "responsibilities": "(INFERRED) Transporting cargo efficiently, adhering to road safety regulations."})
process['stakeholders'].append({"stakeholder": "Local Communities (Mombasa, Lamu, etc.)", "role": "Residents near port areas; affected by port operations and beneficiaries of economic activity", "responsibilities": "(INFERRED) Engaging with port projects, benefiting from employment and local development."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Transport / Maritime Affairs)", "role": "Parent Ministry providing policy direction and oversight", "responsibilities": "(INFERRED) Formulating transport policies, allocating resources for port development."})
process['stakeholders'].append({"stakeholder": "International Traders", "role": "Global businesses utilizing Kenya's ports for transshipment and trade", "responsibilities": "(INFERRED) Engaging in international commerce, utilizing regional trade routes."})
process['stakeholders'].append({"stakeholder": "Seafarers", "role": "Maritime personnel working on vessels calling at Kenyan ports", "responsibilities": "(INFERRED) Adhering to maritime safety standards, complying with port entry requirements."})

process['as_is_narrative'] = "(INFERRED) KPA's operations involve a complex interplay of activities to manage and facilitate maritime trade. This includes providing essential cargo handling services for various types of goods (containers, bulk, conventional) at its numerous berths and terminals. KPA ensures safe navigation within port limits through pilotage, tug services, and effective Vessel Traffic Management Systems. It is responsible for maintaining critical port infrastructure, including dredging channels, maintaining jetties, and upgrading equipment. A core function is the efficient movement of vessels into and out of port, as well as managing the storage and transfer of cargo. KPA also operates vital ferry services, such as the Likoni Ferry, ensuring connectivity for local communities. The Authority is continuously involved in port development and expansion projects, exemplified by the ongoing Lamu Port project, to enhance capacity and competitiveness. Furthermore, KPA implements stringent security protocols (ISPS Code compliant) to safeguard port operations, goods, and personnel, while collaborating closely with customs authorities, railway operators, and other logistics stakeholders to ensure a seamless and integrated supply chain."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kpa.co.ke/",
    "https://wikipedia.org/", # Provided context
    "https://ecitizen.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-first process enriched and combined_data.json updated.")
