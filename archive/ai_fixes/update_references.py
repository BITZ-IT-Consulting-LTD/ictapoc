import os
import re

ref_mapping = {
    "Agriculture_and_Food_Authority___Service_Delivery.md": ["https://afa.go.ke", "Agriculture and Food Authority Act", "Desk Review"],
    "Assets_Recovery_Agency___Service_Delivery.md": ["https://ara.go.ke", "Proceeds of Crime and Anti-Money Laundering Act", "Desk Review"],
    "Athi_Water_Works_Development_Agency___Service_Delivery.md": ["https://awwda.go.ke", "Water Act 2016", "Desk Review"],
    "CABINET_OFFICE___Service_Delivery.md": ["https://cabinetoffice.go.ke", "Cabinet Handbook", "Desk Review"],
    "_CIVIL_REGISTRATION_SERVICES_CRS____Service_Delivery.md": ["https://www.immigration.go.ke", "Births and Deaths Registration Act", "Desk Review"],
    "Culture_and_Heritage___Service_Delivery.md": ["https://www.sportsheritage.go.ke", "Culture Policy", "Desk Review"],
    "Energy___Service_Delivery.md": ["https://energy.go.ke", "Energy Act 2019", "Desk Review"],
    "Government_Spokesperson___Service_Delivery.md": ["https://www.spokesperson.go.ke", "Communications Act", "Desk Review"],
    "STATE_DEPARTMENT_FOR_IMMIGRATION_AND_CITIZEN_SERVICES___Passport_Application.md": ["https://www.immigration.go.ke", "Kenya Citizenship and Immigration Act", "Desk Review"],
    "Kenya_Broadcasting_Corporation___Service_Delivery.md": ["https://www.kbc.co.ke", "Kenya Broadcasting Corporation Act", "Desk Review"],
    "Kenya_National_Qualifications_Authority___Service_Delivery.md": ["https://www.knqa.go.ke", "Kenya National Qualifications Framework (KNQF) Act", "Desk Review"],
    "Micro_Small_and_Medium_Enterprise_Development___Service_Delivery.md": ["https://www.msme.go.ke", "Micro and Small Enterprises Act", "Desk Review"],
    "Ministry_of_Health___Service_Delivery.md": ["https://www.health.go.ke", "Digital Health Act 2023", "Desk Review"],
    "National_Commission_For_Science_Technology_and_Innovation___Service_Delivery.md": ["https://www.nacosti.go.ke", "Science, Technology and Innovation Act 2013", "Desk Review"],
    "National_Environment_Management_Authority___Service_Delivery.md": ["https://www.nema.go.ke", "Environmental Management and Coordination Act (EMCA)", "Desk Review"],
    "National_Government_Coordination___Service_Delivery.md": ["https://www.interior.go.ke", "Executive Order No. 1 of 2023", "Desk Review"],
    "PUBLIC_SERVICE_COMMISION_PSC____Service_Delivery.md": ["https://www.headofpublicservice.go.ke", "Executive Order No. 1 of 2023", "Desk Review"],
    "Office_of_the_Chief_of_Staff___Service_Delivery.md": ["https://www.president.go.ke", "Executive Order No. 1 of 2023", "Desk Review"],
    "Sports_and_the_Arts___Service_Delivery.md": ["https://www.sportsheritage.go.ke", "Sports Act 2013", "Desk Review"],
    "State_Department_for_Children_Services___Service_Delivery.md": ["https://www.socialprotection.go.ke", "Children Act 2022", "Desk Review"],
    "STATE_DEPARTMENT_FOR_CORRECTIONAL_SERVICES___Service_Delivery.md": ["https://www.correctional.go.ke", "Prisons Act", "Desk Review"],
    "_REFUGEE_SERVICES___Service_Delivery.md": ["https://www.refugees.go.ke", "Refugees Act 2021", "Desk Review"],
    "State_Department_for_Special_Programmes___Service_Delivery.md": ["https://www.socialprotection.go.ke", "National Social Protection Policy", "Desk Review"],
    "Youth_Affairs___Service_Delivery.md": ["https://www.youth.go.ke", "Public Service Commission Internship Policy", "Desk Review"]
}

for filename, refs in ref_mapping.items():
    path = os.path.join('priority_mdas', filename)
    if not os.path.exists(path):
        print(f"Skipping {filename}, file not found.")
        continue
        
    with open(path, 'r') as f:
        content = f.read()
    
    ref_section = "## References\n"
    for r in refs:
        ref_section += f"- {r}\n"
    
    if "## References" in content:
        new_content = re.sub(r"## References.*", ref_section, content, flags=re.DOTALL)
    else:
        new_content = content.strip() + "\n\n" + ref_section
        
    with open(path, 'w') as f:
        f.write(new_content)
    print(f"Updated references for {filename}")

