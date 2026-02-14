
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventh process (index 6)
process = data['processes'][6]

# Populate fields
process['executive_summary'] = "The Public Service Commission (PSC) of Kenya is an independent constitutional commission responsible for effective human resource management in the public service. Its mandate includes promoting merit-based recruitment, upholding ethics, ensuring accountability, and fostering efficiency in government operations."
process['process_overview']['process_objective'] = "To manage human resources in the public service by establishing/abolishing offices, appointing/disciplining public officers, promoting constitutional values, and evaluating personnel practices to ensure an efficient, ethical, and accountable public service."
process['process_overview']['policy_legal_context'].append("Established under Article 233(1) of the Constitution of Kenya. Its functions and powers are outlined in Article 234 of the Constitution of Kenya, including promoting values and principles specified in Articles 10 and 232.")
process['stakeholders'].append({"stakeholder": "Public Servants", "role": "Individuals serving in public offices; subjects of PSC's HR management functions", "responsibilities": "(INFERRED) Adhering to codes of conduct, seeking career development within the public service."})
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, and Agencies", "role": "Public entities where PSC's human resource management mandates apply", "responsibilities": "(INFERRED) Collaborating with PSC on staffing needs, implementing PSC's recommendations."})
process['stakeholders'].append({"stakeholder": "President and Parliament", "role": "Recipients of PSC reports and recommendations on public service values and principles", "responsibilities": "(INFERRED) Reviewing PSC reports, legislating on public service matters."})
process['stakeholders'].append({"stakeholder": "Judicial Service Commission", "role": "Entity to which PSC nominates individuals", "responsibilities": "(INFERRED) Receiving nominations from PSC for certain appointments."})
process['stakeholders'].append({"stakeholder": "Salaries and Remuneration Commission", "role": "Entity to which PSC nominates individuals", "responsibilities": "(INFERRED) Receiving nominations from PSC for certain appointments."})

process['as_is_narrative'] = "(INFERRED) The PSC's operations involve setting recruitment standards, advertising vacancies, conducting interviews, making appointments, managing promotions, handling disciplinary cases, reviewing public service conditions, and providing policy advice to ensure a high-performing public service."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (constitutional mandates from legal sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = ["https://en.wikipedia.org/wiki/Public_Service_Commission_of_Kenya", "https://www.klrc.go.ke/"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventh process enriched and combined_data.json updated.")
