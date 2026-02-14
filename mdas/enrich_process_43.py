
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-fourth process (index 43)
process = data['processes'][43]

# Populate fields
process['executive_summary'] = "The Higher Education Loans Board (HELB) is a statutory body in Kenya, established in July 1995 by an Act of Parliament (Cap 213A) as a state corporation under the Ministry of Education. Its core mandate is to provide affordable loans, bursaries, and scholarships to Kenyan students pursuing higher education in recognized institutions, both within and outside Kenya, to ensure access to tertiary education."
process['process_overview']['process_objective'] = "To provide affordable and sustainable financing for tertiary education by mobilizing and managing funds; establishing, managing, and awarding loans, bursaries, and scholarships to needy Kenyan students; and efficiently recovering previously disbursed funds to ensure the revolving nature of the scheme and its long-term sustainability."
process['process_overview']['policy_legal_context'].append("Established in July 1995 by an Act of Parliament (Cap 213A), which provides the legal framework for its mandate of providing financing for higher education. Operates as a state corporation under the Ministry of Education.")
process['stakeholders'].append({"stakeholder": "Kenyan Students (University / College)", "role": "Primary beneficiaries of HELB's financial support for higher education", "responsibilities": "(INFERRED) Applying for loans/bursaries, utilizing funds for education, repaying loans."})
process['stakeholders'].append({"stakeholder": "Ministry of Education", "role": "Parent Ministry providing policy direction and oversight", "responsibilities": "(INFERRED) Policy formulation, strategic guidance, ensuring alignment with national education goals."})
process['stakeholders'].append({"stakeholder": "Higher Education Institutions (Universities, Colleges)", "role": "Institutions where HELB beneficiaries are enrolled", "responsibilities": "(INFERRED) Verifying student enrollment, collaborating on loan disbursement and recovery."})
process['stakeholders'].append({"stakeholder": "Employers", "role": "Partners in facilitating loan recovery through payroll deductions", "responsibilities": "(INFERRED) Deducting loan repayments from employees' salaries, remitting to HELB."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Potential partners for resource mobilization and innovative financing solutions", "responsibilities": "(INFERRED) Collaborating on funding mechanisms, providing banking services."})
process['stakeholders'].append({"stakeholder": "National Treasury", "role": "Government entity providing funding and financial oversight", "responsibilities": "(INFERRED) Allocating government funds to HELB, ensuring financial accountability."})
process['stakeholders'].append({"stakeholder": "Beneficiaries of Scholarships / Bursaries", "role": "Students receiving non-repayable financial aid", "responsibilities": "(INFERRED) Utilizing funds for educational purposes, maintaining academic performance."})

process['as_is_narrative'] = "(INFERRED) HELB operates by publicly inviting applications for loans, bursaries, and scholarships from eligible Kenyan students. It processes these applications based on established criteria (e.g., financial need, academic performance), disburses funds directly to institutions and/or student accounts, manages student loan accounts, and actively pursues loan recovery from beneficiaries upon completion of their studies through various mechanisms, including direct repayment and employer deductions. HELB also engages in resource mobilization and provides financial literacy programs."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://helb.co.ke/",
    "https://devex.com/", # Provided context
    "https://afro.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-fourth process enriched and combined_data.json updated.")
