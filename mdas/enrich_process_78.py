
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-ninth process (index 78)
process = data['processes'][78]

# Populate fields
process['executive_summary'] = "The National Transport and Safety Authority (NTSA) is a Kenyan government agency established to continually improve the accessibility, safety, and reliability of the country's road transport system. NTSA provides comprehensive online and physical services for individuals, vehicles, and transport service providers, and regulates various aspects of road transport. Its core mandate involves enhancing road safety for all users, reducing road accidents and fatalities, and fostering a disciplined and efficient transport sector in Kenya."
process['process_overview']['process_objective'] = "To ensure an accessible and safe road transport system in Kenya by regulating driver and vehicle licensing, managing vehicle registration and transfers, overseeing transport service providers, and implementing road safety initiatives to reduce road accidents and fatalities; to develop and implement policies and strategies for road safety management; to conduct and coordinate research on road safety; to enforce road transport regulations and traffic laws; to provide transport safety education and awareness; and to contribute to the development of a modern, integrated, and efficient transport sector."
process['process_overview']['policy_legal_context'].append("NTSA operates under specific legislation governing road transport and safety in Kenya, primarily the National Transport and Safety Authority Act, No. 33 of 2012, which establishes its mandate, functions, and powers. It operates under the Ministry of Transport (or the relevant government ministry responsible for transport) and aligns its activities with national transport policies, road safety strategies, and international best practices in road transport management and safety.")
process['stakeholders'].append({"stakeholder": "Individual Road Users (Drivers, Passengers, Pedestrians)", "role": "Primary subjects of NTSA's safety regulations and beneficiaries of a safe road system; required to comply with traffic laws", "responsibilities": "(INFERRED) Adhering to traffic laws, obtaining proper licenses, practicing safe road behavior, reporting traffic offenses."})
process['stakeholders'].append({"stakeholder": "Vehicle Owners", "role": "Subjects of vehicle registration, inspection, and transfer regulations; responsible for vehicle roadworthiness", "responsibilities": "(INFERRED) Registering vehicles, ensuring roadworthiness through inspection, complying with ownership transfer rules, paying relevant fees."})
process['stakeholders'].append({"stakeholder": "Transport Service Providers (Operators, Dealers, Garages)", "role": "Entities regulated and licensed by NTSA to provide transport-related services (e.g., PSV operators, driving schools, vehicle inspection centers)", "responsibilities": "(INFERRED) Obtaining licenses, adhering to operational standards, ensuring vehicle safety, complying with regulations."})
process['stakeholders'].append({"stakeholder": "Organizations with Fleets", "role": "Entities managing multiple vehicles; subjects of fleet management regulations and safety standards", "responsibilities": "(INFERRED) Complying with fleet safety standards, ensuring drivers are licensed and vehicles are maintained, implementing safety policies."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Transport)", "role": "Parent Ministry providing oversight, policy direction, and strategic guidance to NTSA", "responsibilities": "(INFERRED) Policy formulation, resource allocation, strategic guidance for the transport sector."})
process['stakeholders'].append({"stakeholder": "Kenya Police Service (Traffic Department)", "role": "Collaborates with NTSA in enforcement of traffic laws and road safety regulations", "responsibilities": "(INFERRED) Enforcing traffic laws, investigating accidents, supporting NTSA operations."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local road safety initiatives, traffic management, and infrastructure development", "responsibilities": "(INFERRED) Collaborating on road safety campaigns, traffic planning, infrastructure maintenance."})
process['stakeholders'].append({"stakeholder": "Insurance Companies", "role": "Provide vehicle insurance; integrate NTSA records for policy issuance and claims processing", "responsibilities": "(INFERRED) Offering vehicle insurance, validating vehicle/driver details, processing claims."})
process['stakeholders'].append({"stakeholder": "Vehicle Manufacturers / Dealers", "role": "Involved in the supply of vehicles; affected by NTSA's vehicle standards and registration processes", "responsibilities": "(INFERRED) Ensuring vehicles meet safety standards, complying with registration requirements."})
process['stakeholders'].append({"stakeholder": "Driving Schools", "role": "Train and certify drivers; regulated and accredited by NTSA", "responsibilities": "(INFERRED) Providing quality driver training, adhering to NTSA curricula and standards."})

process['as_is_narrative'] = "(INFERRED) NTSA's operations involve a comprehensive approach to road transport management and safety. It develops and implements national road safety policies and strategies, conducts regular road safety campaigns and public awareness programs to educate all road users. NTSA provides extensive online and physical services through its Transport Integrated Management System (TIMS) portal, allowing individuals and businesses to access services such as driver licensing (including Smart Driving License issuance and renewal), vehicle registration, transfer of ownership, and payment of various transport-related fees. The Authority regulates transport service providers, including PSV operators, driving schools, and vehicle inspection centers, by issuing licenses and ensuring adherence to operational and safety standards. NTSA actively enforces traffic laws and regulations, often collaborating with the Kenya Police Service Traffic Department, and conducts conformity assessments for vehicles to ensure roadworthiness. It also regulates the use of speed limiters on public service and commercial vehicles. Through these functions, NTSA aims to reduce road accidents, manage traffic flow, and create a disciplined and efficient road transport sector that supports economic activities and ensures the safety of all road users in Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.ntsa.go.ke/", # Official website
    "https://ecitizen.go.ke/" # Provided context for online services
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-ninth process enriched and combined_data.json updated.")
