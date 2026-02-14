
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-third process (index 72)
process = data['processes'][72]

# Populate fields
process['executive_summary'] = "The National Environment Management Authority (NEMA) is the principal agency in Kenya responsible for coordinating, monitoring, regulating, and supervising all environmental management activities. Established under specific environmental legislation, NEMA aims to ensure a clean, healthy, productive, and sustainable environment for all Kenyans by promoting sound environmental practices, integrating environmental considerations into national development policies, plans, programs, and projects, and enforcing compliance with environmental laws and regulations."
process['process_overview']['process_objective'] = "To coordinate various environmental management activities undertaken by lead agencies and promote the integration of environmental considerations into development policies, plans, programs, and projects; to spearhead the development of environmental policies, laws, regulations, standards, and guidelines, and advise the government on sound environmental management practices; to monitor and assess activities to ensure the environment is not degraded, undertaking monitoring, inspections, and compliance audits; to take stock of natural resources, their utilization, and conservation, and examine land use patterns; to undertake and coordinate research, investigations, and surveys, and disseminate environmental information; to enhance environmental education and public awareness about sound environmental management; to issue permits and licenses, including review and decision-making on Environmental Impact Assessments (EIA) and Environmental Audits (EA); to enforce environmental laws by imposing penalties for non-compliance; to advise the government on legislative measures for environmental management and the implementation of relevant international conventions, treaties, and agreements; and to initiate procedures for preventing and remedying environmental accidents."
process['process_overview']['policy_legal_context'].append("Established as the principal agency for environmental management in Kenya under the Environmental Management and Co-ordination Act (EMCA), Cap. 387, and its subsequent amendments, which provide the overarching legal framework for its operations. NEMA advises the government on environmental policy and is responsible for implementing national environmental laws and international environmental conventions to which Kenya is a signatory. It operates under the Ministry of Environment, Climate Change and Forestry (or the relevant ministry responsible for environment).")
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, and Agencies (involved in development/resource use)", "role": "Lead agencies in specific environmental sectors; subject to NEMA's coordination and regulatory oversight", "responsibilities": "(INFERRED) Integrating environmental concerns into sector plans, complying with NEMA guidelines, collaborating on environmental management."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local environmental management and enforcement of environmental regulations", "responsibilities": "(INFERRED) Implementing environmental policies at county level, managing local environmental resources, collaborating with NEMA."})
process['stakeholders'].append({"stakeholder": "Industries / Businesses", "role": "Subjects of NEMA's regulatory framework regarding pollution, waste management, and resource use", "responsibilities": "(INFERRED) Complying with environmental standards, conducting EIAs/EAs, implementing cleaner production."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Directly impacted by environmental issues and beneficiaries of environmental protection efforts", "responsibilities": "(INFERRED) Participating in environmental governance, reporting environmental degradation, practicing sustainable resource use."})
process['stakeholders'].append({"stakeholder": "Environmental Civil Society Organizations (CSOs) / NGOs", "role": "Advocates for environmental protection; partners in awareness creation and monitoring", "responsibilities": "(INFERRED) Advocating for environmental rights, conducting awareness campaigns, monitoring compliance."})
process['stakeholders'].append({"stakeholder": "Developers / Project Proponents", "role": "Required to conduct EIAs/EAs and obtain NEMA approvals for their projects", "responsibilities": "(INFERRED) Undertaking EIAs/EAs, implementing mitigation measures, complying with project conditions."})
process['stakeholders'].append({"stakeholder": "Environmental Practitioners (Consultants, Auditors)", "role": "Provide professional services for EIAs/EAs and other environmental studies", "responsibilities": "(INFERRED) Conducting professional environmental assessments, advising on compliance."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Provide scientific data and research findings to inform NEMA's policies and decisions", "responsibilities": "(INFERRED) Conducting environmental research, providing expert advice."})
process['stakeholders'].append({"stakeholder": "Academic Institutions", "role": "Contribute to environmental education and capacity building", "responsibilities": "(INFERRED) Offering environmental courses, conducting research."})
process['stakeholders'].append({"stakeholder": "International Environmental Bodies / Donors", "role": "Provide technical and financial support for environmental programs and capacity building", "responsibilities": "(INFERRED) Funding environmental projects, sharing international best practices."})
process['stakeholders'].append({"stakeholder": "General Public", "role": "Beneficiaries of a clean and healthy environment; has a right to environmental information", "responsibilities": "(INFERRED) Exercising environmental rights, participating in public hearings."})

process['as_is_narrative'] = "(INFERRED) NEMA's operations involve a comprehensive approach to environmental governance. It coordinates environmental activities across various government sectors and lead agencies to ensure a harmonized approach. A critical function is the review and approval of Environmental Impact Assessments (EIAs) for new projects and Environmental Audits (EAs) for existing facilities, leading to the issuance of licenses and permits for activities with environmental implications. NEMA monitors compliance with environmental regulations through regular inspections, surveys, and environmental quality monitoring (air, water, soil). It enforces environmental laws, often imposing fines, closure notices, or initiating legal actions against non-compliant entities. The Authority is actively involved in developing and disseminating environmental standards, guidelines, and regulations. NEMA promotes environmental education and public awareness campaigns to foster a culture of environmental responsibility and facilitates public participation in environmental decision-making processes. Furthermore, NEMA undertakes and coordinates research on environmental issues, provides advice to the government on policy matters, and acts as the national focal point for various international environmental agreements and conventions."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.nema.go.ke/", # Official website for NEMA Kenya
    "https://lin-eastafrica.com/", # Provided context
    "https://nema.go.ug/", # Provided context, differentiated for Kenya
    "https://mazingirasafi.com/", # Provided context
    "https://quora.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-third process enriched and combined_data.json updated.")
