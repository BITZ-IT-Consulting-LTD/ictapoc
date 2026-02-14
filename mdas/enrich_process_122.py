
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and twenty-third process (index 122)
process = data['processes'][122]

# Populate fields
process['executive_summary'] = "The Ministry of Defence (MoD) of Kenya is a cabinet-level office responsible for defence-related matters and the oversight of the Kenya Defence Forces (KDF). Its primary mandate, guided by the Constitution of the Republic of Kenya, is to defend and protect the sovereignty and territorial integrity of the Republic of Kenya, ensure national security, and provide support during emergencies or disasters. The MoD aims to maintain a premier, credible, and mission-capable force deeply rooted in professionalism, contributing to regional peace and stability and supporting national development."
process['process_overview']['process_objective'] = "To defend and protect the sovereignty and territorial integrity of the Republic of Kenya from external aggression; to facilitate and support the Kenya Defence Forces (KDF) in fulfilling their constitutional mandate under Article 241 (3) (a), (b) & (c), which includes defending Kenya from external aggression, assisting civilian authority in emergencies or disasters, and restoring peace in areas of Kenya affected by unrest or instability when assigned; to provide essential civilian services such as policy development, administration, financial management, public communications, human resource management, medical, and technical support to the Defence Forces; and to contribute to regional and international peace and security through participation in peacekeeping missions and collaborative defence initiatives."
process['process_overview']['policy_legal_context'].append("The Ministry of Defence operates under the Constitution of the Republic of Kenya, 2010 (specifically Article 241 for the Kenya Defence Forces, outlining its establishment, mandate, and command), and Executive Order No. 2 of May 2013 (Revised May 2020), which defines the functions of ministries and state departments. The Ministry is led by the Cabinet Secretary, who is accountable to the President (Commander-in-Chief) and Parliament, and chairs the Defence Council, which is responsible for the overall control and direction of the Kenya Defence Forces. Its legal framework is further defined by the Kenya Defence Forces Act and various international conventions on defence and security.")
process['stakeholders'].append({"stakeholder": "Kenya Defence Forces (KDF personnel: Army, Navy, Air Force)", "role": "The professional military force responsible for national defence; overseen by MoD", "responsibilities": "(INFERRED) Defending the nation, maintaining discipline, adhering to military laws, participating in operations."})
process['stakeholders'].append({"stakeholder": "President (Commander-in-Chief)", "role": "Supreme Commander of the KDF; appoints the Cabinet Secretary for Defence", "responsibilities": "(INFERRED) Directing military operations, making strategic defence decisions, approving KDF deployments."})
process['stakeholders'].append({"stakeholder": "Parliament", "role": "Exercises oversight over the Ministry of Defence and KDF; approves defence budgets and legislation", "responsibilities": "(INFERRED) Approving defence policies, scrutinizing KDF spending, ensuring accountability."})
process['stakeholders'].append({"stakeholder": "Cabinet Secretary for Defence", "role": "Political head of the Ministry; responsible for defence policy and strategic direction; chairs the Defence Council", "responsibilities": "(INFERRED) Advising the President, formulating defence policies, overseeing MoD operations."})
process['stakeholders'].append({"stakeholder": "Defence Council", "role": "Responsible for the overall control, policy, and direction of the Kenya Defence Forces", "responsibilities": "(INFERRED) Strategic oversight, policy formulation, ensuring KDF readiness."})
process['stakeholders'].append({"stakeholder": "Citizens of Kenya", "role": "Beneficiaries of national security and protection provided by the KDF", "responsibilities": "(INFERRED) Supporting national defence, respecting KDF personnel, civic duty."})
process['stakeholders'].append({"stakeholder": "Other Government Ministries / Departments (e.g., Ministry of Interior, Foreign Affairs)", "role": "Collaborators in national security matters, disaster response, and foreign policy formulation", "responsibilities": "(INFERRED) Collaborating on security strategies, coordinating disaster relief, aligning foreign policy with defence interests."})
process['stakeholders'].append({"stakeholder": "National Police Service", "role": "Collaborates with KDF in internal security operations, particularly in restoring peace in unrest-affected areas", "responsibilities": "(INFERRED) Maintaining internal security, assisting KDF in civil support operations."})
process['stakeholders'].append({"stakeholder": "National Intelligence Service", "role": "Provides intelligence to the MoD and KDF for national security assessments and operations", "responsibilities": "(INFERRED) Gathering intelligence, advising on security threats, collaborating on national security."})
process['stakeholders'].append({"stakeholder": "Regional and International Allies / Partners (for joint operations, training, and intelligence sharing)", "role": "Collaborators in defence matters, peacekeeping missions, and capacity building", "responsibilities": "(INFERRED) Participating in joint exercises, sharing intelligence, supporting peacekeeping efforts."})
process['stakeholders'].append({"stakeholder": "Civilian Population (beneficiaries of security and disaster response)", "role": "Protected by KDF from external threats and assisted during national disasters", "responsibilities": "(INFERRED) Cooperating with KDF during emergencies, benefiting from security."})
process['stakeholders'].append({"stakeholder": "Local Communities (in areas of KDF deployment or operations)", "role": "Impacted by KDF presence; beneficiaries of civil-military cooperation activities", "responsibilities": "(INFERRED) Collaborating with KDF on community projects, providing local support."})

process['as_is_narrative'] = "(INFERRED) The Ministry of Defence (MoD) operates as the civilian oversight and policy-making body for Kenya's national security apparatus, primarily the Kenya Defence Forces (KDF). Its core operations involve formulating and implementing defence policies, strategies, and plans that guide the KDF's missions and activities. The MoD is responsible for managing the defence budget, procuring equipment, and ensuring the efficient allocation and utilization of resources to maintain KDF's operational readiness and effectiveness. The KDF, under the MoD's strategic direction, actively recruits, trains, and deploys its personnel (Army, Navy, Air Force) to safeguard Kenya's territorial integrity and national interests. This includes conducting military operations against external threats and aggressors, carrying out patrols along land and maritime borders, and securing Kenyan airspace. The KDF also participates significantly in regional and international peacekeeping missions, contributing to global security and stability. Domestically, the KDF provides crucial humanitarian assistance and disaster relief during national emergencies such as floods, droughts, or public health crises. It collaborates closely with civilian authorities, particularly the National Police Service, in internal security operations, including restoring peace in areas affected by unrest or instability, always acting in accordance with the law. The MoD fosters strategic alliances and partnerships with regional and international defence forces for joint training, capacity building, intelligence sharing, and collaborative operations. Civilian staff within the Ministry provide vital administrative, financial, human resource, medical, and technical support services to the KDF, ensuring its seamless functioning. Furthermore, the Ministry conducts intelligence gathering and analysis relevant to national security, advising the government on evolving threats and defence posture. Through these comprehensive functions, the Ministry of Defence and the KDF ensure Kenya's national security, protect its citizens, and contribute to its foreign policy objectives."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.mod.go.ke/", # Official website
    "https://wikipedia.org/", # Provided context
    "https://ecitizen.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and twenty-third process enriched and combined_data.json updated.")
