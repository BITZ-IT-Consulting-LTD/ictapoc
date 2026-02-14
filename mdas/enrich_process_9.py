
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the tenth process (index 9)
process = data['processes'][9]

# Populate fields
process['executive_summary'] = "(INFERRED) The Cabinet Office in Kenya serves as the administrative and coordination hub supporting the Cabinet in its executive functions. It facilitates policy implementation, governmental oversight, and ensures the smooth operation of the government's highest decision-making body."
process['process_overview']['process_objective'] = "(INFERRED) To facilitate the decision-making processes of the Cabinet, ensure the coordinated implementation of government policies and programs across ministries, and provide administrative and logistical support to the President, Deputy President, and Cabinet Secretaries in their executive duties."
process['process_overview']['policy_legal_context'].append("The role and functions are derived from the Constitution of Kenya (Article 152 for the Cabinet, Article 153 for Cabinet Secretaries) and relevant executive orders outlining the structure and responsibilities of the Executive. (INFERRED: While no single Act explicitly defines 'Cabinet Office' as a separate entity, its functions are integral to constitutional governance.)")
process['stakeholders'].append({"stakeholder": "The President", "role": "Head of the Executive and Cabinet", "responsibilities": "(INFERRED) Chairing Cabinet meetings, directing government policy, overseeing executive functions."})
process['stakeholders'].append({"stakeholder": "The Deputy President", "role": "Principal assistant to the President and member of the Cabinet", "responsibilities": "(INFERRED) Assisting the President, performing assigned duties, participating in Cabinet discussions."})
process['stakeholders'].append({"stakeholder": "Attorney General", "role": "Principal legal advisor to the government and member of the Cabinet", "responsibilities": "(INFERRED) Providing legal counsel to the Cabinet, ensuring legality of government actions."})
process['stakeholders'].append({"stakeholder": "Cabinet Secretaries", "role": "Heads of Ministries, responsible for policy formulation and implementation in their sectors", "responsibilities": "(INFERRED) Presenting policy proposals to Cabinet, implementing approved policies, managing ministerial operations."})
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, and Agencies", "role": "Implementers of Cabinet decisions and policies", "responsibilities": "(INFERRED) Executing policies, providing information for Cabinet deliberations."})
process['stakeholders'].append({"stakeholder": "Parliament", "role": "Legislative body, exercises oversight over the Executive", "responsibilities": "(INFERRED) Approving legislation, scrutinizing government actions, holding Cabinet accountable."})

process['as_is_narrative'] = "(INFERRED) The Cabinet Office's operations involve coordinating the agenda for Cabinet meetings, preparing and circulating Cabinet memoranda and decisions, providing logistical support for meetings, ensuring follow-up on Cabinet directives, and facilitating communication and coordination between various government ministries and departments to achieve coherent policy implementation."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "medium (inferred from constitutional roles and general government structure, as no dedicated official website/mandate is specified for 'Cabinet Office' as a distinct MDA)"
process['metadata']['source_urls'] = [
    "https://en.wikipedia.org/wiki/Cabinet_of_Kenya",
    "https://katibainstitute.org/",
    "https://devolution.go.ke/", # Relevant for executive order context
    "https://treasury.go.ke/" # Relevant for executive order context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Tenth process enriched and combined_data.json updated.")
