
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixtieth process (index 59)
process = data['processes'][59]

# Populate fields
process['executive_summary'] = "The Kenya National Highways Authority (KeNHA) is a statutory body established under the Kenya Roads Act of 2007 and inaugurated in September 2008. Its core mandate involves the comprehensive management, development, rehabilitation, and maintenance of Kenya's national trunk road network, including Class S, A, and B roads. KeNHA aims to provide a safe, efficient, and well-maintained road infrastructure to support socio-economic development across the country."
process['process_overview']['process_objective'] = "To manage, develop, rehabilitate, and maintain national trunk roads; to plan, design, construct, and upgrade national road networks to high standards; to implement road policies and standards specifically related to national roads; to ensure the quality assurance of all road works; to enforce axle load control regulations to preserve road infrastructure; to collect and analyze data for efficient future road planning and development; and to oversee the management of weighbridge installations across the national road network."
process['process_overview']['policy_legal_context'].append("Established under the Kenya Roads Act of 2007 (inaugurated in September 2008), which provides the legal framework for its mandate and functions. Operates under the Ministry of Roads and Transport and implements national road policies in line with Kenya's Vision 2030 development agenda.")
process['stakeholders'].append({"stakeholder": "Road Users (Motorists, Pedestrians, Cyclists)", "role": "Primary beneficiaries of safe and well-maintained roads", "responsibilities": "(INFERRED) Adhering to traffic rules, respecting road infrastructure."})
process['stakeholders'].append({"stakeholder": "Transport Sector (Logistics, Public Service Vehicles - PSVs)", "role": "Industry relying on national roads for operations and business", "responsibilities": "(INFERRED) Complying with road safety regulations, contributing to economic activity."})
process['stakeholders'].append({"stakeholder": "Construction Companies", "role": "Contractors engaged in road construction, rehabilitation, and maintenance projects", "responsibilities": "(INFERRED) Adhering to contractual obligations, meeting quality standards."})
process['stakeholders'].append({"stakeholder": "Consulting Engineers", "role": "Provide technical expertise in road design, supervision, and project management", "responsibilities": "(INFERRED) Ensuring technical integrity, compliance with design specifications."})
process['stakeholders'].append({"stakeholder": "Landowners / Communities along road corridors", "role": "Affected by road development; beneficiaries of local economic activity", "responsibilities": "(INFERRED) Cooperating with land acquisition processes, providing local labor."})
process['stakeholders'].append({"stakeholder": "Ministry of Roads and Transport", "role": "Parent Ministry providing policy direction and oversight", "responsibilities": "(INFERRED) Formulating national transport policies, allocating resources."})
process['stakeholders'].append({"stakeholder": "National Transport and Safety Authority (NTSA)", "role": "Regulatory body for road safety and traffic management", "responsibilities": "(INFERRED) Enforcing traffic laws, collaborating on road safety initiatives."})
process['stakeholders'].append({"stakeholder": "Kenya Urban Roads Authority (KURA)", "role": "Manages urban road networks", "responsibilities": "(INFERRED) Coordinating with KeNHA on interconnecting road networks."})
process['stakeholders'].append({"stakeholder": "Kenya Rural Roads Authority (KeRRA)", "role": "Manages rural road networks", "responsibilities": "(INFERRED) Coordinating with KeNHA on interconnecting road networks."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local infrastructure development and planning", "responsibilities": "(INFERRED) Collaborating on integrated transport planning, local infrastructure support."})
process['stakeholders'].append({"stakeholder": "Development Partners / Donors", "role": "Provide financial and technical support for road infrastructure projects", "responsibilities": "(INFERRED) Funding projects, sharing technical expertise."})

process['as_is_narrative'] = "(INFERRED) KeNHA's operations encompass the entire lifecycle of national trunk roads, starting with strategic planning and design of new road projects and major rehabilitation works. It supervises contractors during construction and upgrading phases, ensuring adherence to engineering standards and specifications. A significant aspect of its work involves routine and periodic maintenance activities to preserve the integrity and extend the lifespan of existing national roads. KeNHA is also responsible for managing traffic flow, implementing road safety measures, and enforcing axle load limits through a network of weighbridges to prevent road damage. The Authority continuously collects and analyzes data on road usage, condition, and traffic patterns to inform future planning and investment decisions. Furthermore, KeNHA collaborates closely with other road agencies (KURA, KeRRA), government ministries, county governments, and international development partners to develop an integrated, efficient, and sustainable national road network that supports economic growth and enhances connectivity."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kenha.co.ke/",
    "https://developmentaid.org/", # Provided context
    "https://scribd.com/", # Provided context
    "https://devex.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixtieth process enriched and combined_data.json updated.")
