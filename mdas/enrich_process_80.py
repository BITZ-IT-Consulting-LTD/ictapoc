
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-first process (index 80)
process = data['processes'][80]

# Populate fields
process['executive_summary'] = "The Public Procurement Regulatory Authority (PPRA) is an autonomous government agency in Kenya established under Section 8 of the Public Procurement and Asset Disposal Act, 2015. Its primary mandate is to monitor, assess, and report on the overall functioning of the public procurement and asset disposal system in Kenya. PPRA ensures that procuring entities adhere to national values, constitutional provisions, and principles of fairness, equity, transparency, competition, and cost-effectiveness, thereby promoting sustainable development and safeguarding public resources."
process['process_overview']['process_objective'] = "To monitor, assess, and review the public procurement and asset disposal system to ensure compliance with national values and constitutional provisions, and make recommendations for improvements; to develop procurement policies, regulations, and guidelines; to monitor and evaluate procurement performance to ensure compliance with procurement laws and regulations, and enforce standards by imposing sanctions for non-compliance; to investigate and resolve complaints and disputes related to procurement processes; to develop, promote, and support the training and capacity development of individuals involved in procurement and asset disposal; to provide guidance and technical support to public institutions on procurement matters; to promote the participation of disadvantaged groups (women, youth, and persons with disabilities) in public procurement through preferential policies; to promote the use of technology in procurement processes; to report to Parliament and relevant county assemblies on the functioning of the procurement system; to develop a code of ethics to guide procuring entities and bidders; to collaborate with state and non-state actors to improve public procurement and disposal; to maintain and update supplier and contractor databases, and develop standard procurement documents; and to conduct market research and procurement audits."
process['process_overview']['policy_legal_context'].append("Established under Section 8 of the Public Procurement and Asset Disposal Act, 2015 (PPAD Act, 2015), which provides the comprehensive legal framework for public procurement and asset disposal in Kenya. PPRA operates under the oversight of the National Treasury and is crucial for upholding Article 227 of the Constitution of Kenya, 2010, which mandates that public procurement systems be fair, equitable, transparent, competitive, and cost-effective. Its functions ensure adherence to international best practices in public procurement.")
process['stakeholders'].append({"stakeholder": "Procuring Entities (Government Ministries, Departments, Agencies, State Corporations, County Governments)", "role": "Organizations undertaking public procurement and asset disposal; subject to PPRA's regulations and oversight", "responsibilities": "(INFERRED) Complying with PPAD Act, ensuring fair and transparent procurement, utilizing PPRA guidelines."})
process['stakeholders'].append({"stakeholder": "Bidders / Suppliers / Contractors (Individuals and Companies)", "role": "Participants in public procurement processes; benefit from fair competition and dispute resolution mechanisms", "responsibilities": "(INFERRED) Adhering to tender requirements, competing fairly, utilizing dispute resolution channels."})
process['stakeholders'].append({"stakeholder": "Public (Taxpayers)", "role": "Ultimate beneficiaries of efficient and transparent public procurement; contribute resources to government projects", "responsibilities": "(INFERRED) Seeking accountability, benefiting from public services delivered through procurement."})
process['stakeholders'].append({"stakeholder": "Parliament / County Assemblies (for oversight)", "role": "Oversight bodies that receive reports from PPRA on the functioning of the procurement system", "responsibilities": "(INFERRED) Scrutinizing procurement reports, ensuring legislative oversight, advocating for good governance."})
process['stakeholders'].append({"stakeholder": "National Treasury", "role": "Parent Ministry providing oversight and strategic direction for public finance and procurement", "responsibilities": "(INFERRED) Policy guidance, resource allocation, ensuring fiscal responsibility."})
process['stakeholders'].append({"stakeholder": "Ethics and Anti-Corruption Commission (EACC)", "role": "Collaborates with PPRA in investigating corruption and unethical practices in public procurement", "responsibilities": "(INFERRED) Investigating corruption, promoting ethical conduct, collaborating on enforcement."})
process['stakeholders'].append({"stakeholder": "National Gender and Equality Commission", "role": "Advocates for the inclusion and participation of disadvantaged groups in public procurement", "responsibilities": "(INFERRED) Promoting equality, advising on preferential policies, monitoring inclusion."})
process['stakeholders'].append({"stakeholder": "Disadvantaged Groups (Women, Youth, Persons with Disabilities)", "role": "Target beneficiaries of preferential procurement policies aimed at economic empowerment", "responsibilities": "(INFERRED) Registering as suppliers, participating in tenders, seeking economic opportunities."})
process['stakeholders'].append({"stakeholder": "Professional Bodies (e.g., Kenya Institute of Supplies Management (KISM))", "role": "Promote professionalism and ethical conduct in procurement; collaborate with PPRA on capacity building", "responsibilities": "(INFERRED) Setting professional standards, providing training, advocating for best practices."})
process['stakeholders'].append({"stakeholder": "International Development Partners", "role": "Provide technical assistance and support for public procurement reforms", "responsibilities": "(INFERRED) Funding capacity building, sharing international best practices, advising on reforms."})

process['as_is_narrative'] = "(INFERRED) The Public Procurement Regulatory Authority (PPRA) executes its mandate through a multi-pronged approach to ensure a robust and transparent public procurement system. It develops and issues comprehensive regulations, policies, and standardized tender documents that all procuring entities must follow. PPRA continuously monitors the procurement activities of government ministries, departments, agencies, and county governments through various mechanisms, including procurement audits and performance reviews, to identify non-compliance and systemic weaknesses. It serves as an impartial body for investigating complaints and resolving disputes raised by bidders and other stakeholders concerning procurement processes, ensuring fairness and recourse. Capacity building is a key function, with PPRA designing and delivering training programs for procurement professionals, procuring entity staff, and suppliers to enhance their understanding and adherence to the PPAD Act. The Authority also provides technical support and advisory services to public institutions on complex procurement matters. PPRA actively promotes the participation of marginalized groups (women, youth, persons with disabilities) by developing and monitoring preferential procurement policies. It manages a national database of registered suppliers and contractors, and advocates for the adoption of electronic procurement systems to enhance efficiency and transparency. Through regular reporting to Parliament and other oversight bodies, PPRA ensures accountability and contributes to the ongoing reform and improvement of Kenya's public procurement and asset disposal system."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.ppra.go.ke/", # Official website
    "https://afro.co.ke/", # Provided context
    "https://majira.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-first process enriched and combined_data.json updated.")
