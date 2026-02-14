
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-third process (index 32)
process = data['processes'][32]

# Populate fields
process['executive_summary'] = "The State Department of Medical Services in Kenya, operating under the Ministry of Health, is committed to shaping healthcare and ensuring the well-being of citizens. Its mandate includes setting medical services policy, providing curative health services, and managing health policy and administration, alongside supporting medical research."
process['process_overview']['process_objective'] = "To formulate and implement medical services policy, provide curative health services, manage health policy and administration, coordinate national health referral services, develop cancer management policies, and support medical research to enhance the health and well-being of all Kenyans."
process['process_overview']['policy_legal_context'].append("Operates within the broader legal framework of the Ministry of Health. This includes acts governing public health, medical practice (e.g., Medical Practitioners and Dentists Act), pharmacy and poisons control (e.g., Pharmacy and Poisons Act), and general health policy. (INFERRED: This legislative landscape underpins its functions.)")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens (Patients)", "role": "Primary beneficiaries of medical services and healthcare policies", "responsibilities": "(INFERRED) Seeking healthcare, adhering to medical advice, participating in public health initiatives."})
process['stakeholders'].append({"stakeholder": "Healthcare Providers (Doctors, Nurses, Hospitals, Clinics)", "role": "Deliverers of medical services", "responsibilities": "(INFERRED) Providing quality healthcare, adhering to medical ethics, complying with health regulations."})
process['stakeholders'].append({"stakeholder": "Medical Research Institutions", "role": "Collaborators in advancing medical knowledge and healthcare solutions", "responsibilities": "(INFERRED) Conducting research, informing policy, developing new treatments."})
process['stakeholders'].append({"stakeholder": "Pharmacy and Poisons Board", "role": "Regulatory body for pharmacy and medicines control", "responsibilities": "(INFERRED) Ensuring quality and safety of medicines, regulating pharmaceutical practice."})
process['stakeholders'].append({"stakeholder": "Ministry of Health", "role": "Parent Ministry providing overall policy direction and oversight", "responsibilities": "(INFERRED) Setting national health agenda, resource allocation, coordinating health sector activities."})

process['as_is_narrative'] = "(INFERRED) The State Department operates by formulating national medical services policies and standards, overseeing the provision of curative health services across various facilities, managing the administrative aspects of health policy, coordinating the national referral system for complex medical cases, developing strategies for cancer management, and supporting medical research to improve healthcare outcomes and service delivery for the Kenyan population."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://health.go.ke/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-third process enriched and combined_data.json updated.")
