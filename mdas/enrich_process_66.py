
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-seventh process (index 66)
process = data['processes'][66]

# Populate fields
process['executive_summary'] = "The Kenya Urban Roads Authority (KURA) is a statutory body established under the Kenya Roads Act, 2007. Its primary mandate is the management, development, rehabilitation, and maintenance of national urban trunk roads across Kenya, including all national trunk roads that traverse urban areas. KURA aims to improve mobility, safety, and the overall quality of urban infrastructure, thereby supporting socio-economic development and enhancing the quality of life in urban centers."
process['process_overview']['process_objective'] = "To develop, rehabilitate, and maintain urban road networks to enhance mobility, accessibility, and safety; to effectively manage road projects and coordinate urban road network planning; to provide various online services to stakeholders, such as requests for road cutting and roadside development; and to play a pivotal role in transforming urban mobility, driving socio-economic development, and enhancing the overall quality of life in urban areas through sustainable road infrastructure."
process['process_overview']['policy_legal_context'].append("Established under the Kenya Roads Act, 2007, which provides the legal framework for its mandate and functions. Its responsibilities were expanded in 2016 to include all national trunk roads that traverse urban areas. KURA operates under the Ministry of Roads and Transport and aligns its activities with national urban development policies and plans aimed at decongesting urban areas and improving connectivity.")
process['stakeholders'].append({"stakeholder": "Urban Road Users (Motorists, Pedestrians, Cyclists)", "role": "Primary beneficiaries of improved urban road networks and road safety initiatives", "responsibilities": "(INFERRED) Adhering to traffic laws, utilizing road infrastructure responsibly, providing feedback."})
process['stakeholders'].append({"stakeholder": "Urban Residents / Businesses", "role": "Directly affected by urban road development and maintenance; beneficiaries of enhanced connectivity", "responsibilities": "(INFERRED) Engaging with urban planning, contributing to local economy."})
process['stakeholders'].append({"stakeholder": "Public Transport Operators (Matatus, Buses)", "role": "Rely on urban roads for service delivery; affected by road conditions and traffic management", "responsibilities": "(INFERRED) Providing transport services, complying with traffic regulations."})
process['stakeholders'].append({"stakeholder": "Construction Companies", "role": "Contractors engaged in urban road construction, rehabilitation, and maintenance projects", "responsibilities": "(INFERRED) Delivering quality road works, adhering to contractual terms, ensuring safety standards."})
process['stakeholders'].append({"stakeholder": "Consulting Engineers", "role": "Provide technical expertise in urban road design, supervision, and project management", "responsibilities": "(INFERRED) Ensuring technical integrity, compliance with design specifications."})
process['stakeholders'].append({"stakeholder": "County Governments (especially urban centers)", "role": "Partners in local infrastructure development, urban planning, and traffic management", "responsibilities": "(INFERRED) Collaborating on urban road development plans, providing local support for projects."})
process['stakeholders'].append({"stakeholder": "National Government (Ministry of Roads and Transport)", "role": "Parent Ministry providing policy direction, funding, and oversight", "responsibilities": "(INFERRED) Formulating national transport policies, allocating resources for urban road development."})
process['stakeholders'].append({"stakeholder": "Kenya National Highways Authority (KeNHA)", "role": "Manages national trunk roads; coordinates on interconnecting networks, including those traversing urban areas", "responsibilities": "(INFERRED) Collaborating on integrated road network planning, ensuring smooth transitions between road classes."})
process['stakeholders'].append({"stakeholder": "Kenya Rural Roads Authority (KeRRA)", "role": "Manages rural road networks; coordinates on interconnecting networks", "responsibilities": "(INFERRED) Collaborating on integrated road network planning, ensuring smooth transitions between road classes."})
process['stakeholders'].append({"stakeholder": "Utilities Providers (Water, Electricity, Internet)", "role": "Require access to road reserves for infrastructure installation and maintenance", "responsibilities": "(INFERRED) Coordinating works with KURA, minimizing disruption to roads."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical support for urban road infrastructure projects", "responsibilities": "(INFERRED) Funding projects, sharing technical expertise for sustainable urban mobility."})

process['as_is_narrative'] = "(INFERRED) KURA's operations involve a strategic approach to planning, designing, and implementing urban road projects, including new construction, widening, and rehabilitation of existing networks. It undertakes traffic management studies and implements measures to improve urban traffic flow and reduce congestion. A key aspect of KURA's work is the continuous maintenance of urban roads through routine patching, drain clearing, and street lighting maintenance to ensure safety and serviceability. KURA also processes and issues permits for activities affecting road reserves, such as road cutting for utility installations and developments adjacent to urban roads, ensuring compliance with regulations. The Authority collects extensive data on urban traffic patterns, road conditions, and accident hotspots to inform its planning and enhance road safety. KURA actively collaborates with county governments, urban planners, other road agencies, and public transport stakeholders to develop integrated urban transport solutions that support sustainable urban development, improve accessibility, and contribute to a better quality of life for urban dwellers."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kura.go.ke/",
    "https://ecitizen.go.ke/", # Provided context
    "https://saraka.info/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-seventh process enriched and combined_data.json updated.")
