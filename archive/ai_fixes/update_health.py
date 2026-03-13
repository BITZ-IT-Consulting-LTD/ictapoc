import re

with open('priority_mdas/Ministry_of_Health___Service_Delivery.md', 'r') as f:
    content = f.read()

# Replace AS-IS flowchart
old_asis = r"### AS-IS Process Flowchart \(BPMN 2\.0\).*?class End endNode;\n```"
new_asis = """### AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Fragmented Patient Identity based on Deep Dive).*

```mermaid
graph TD
    Start((Start)) --> FacA["Patient Arrives at Facility A"]
    
    subgraph Facility_A [Facility A]
        FacA --> RegA["New Registration (Paper/Local EMR)"]
        RegA --> ID_A["Assign Local Facility ID"]
    end
    
    subgraph Facility_B [Facility B]
        ID_A --> FacB["Patient Arrives at Facility B"]
        FacB --> Search["Search Records"]
        Search --> NotFound["No Record Found"]
        NotFound --> RegB["New Registration B"]
        RegB --> ID_B["Assign New Facility ID"]
    end
    
    subgraph National_Level [MOH / National]
        ID_B --> Multiple["Multiple IDs Generated"]
        Multiple --> Fragmented["Fragmented Patient History"]
    end
    
    Fragmented --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    class Start start;
    class End endNode;
    class FacA,RegA,ID_A,FacB,Search,NotFound,RegB,ID_B,Multiple,Fragmented userTask;
```"""

content = re.sub(old_asis, new_asis, content, flags=re.DOTALL)

# Replace TO-BE flowchart
old_tobe = r"### TO-BE Process Flowchart \(BPMN 2\.0\).*?class End endNode;\n```"
new_tobe = """### TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Kenya Health Information Exchange - KHIE Architecture).*

```mermaid
graph TD
    Start((Start)) --> Scan["Biometric Scan / Maisha Namba"]
    
    subgraph Point_Of_Care [Health Facility]
        Scan --> QueryReg["Query Master Patient Index"]
        QueryReg --> Found{"Found?"}
        Found -- "No" --> Enroll["Enroll New Patient"]
        Found -- "Yes" --> Retrieve["Retrieve Existing ID"]
        Enroll --> QuerySHR
        Retrieve --> QuerySHR["Query National Shared Health Record (SHR) via X-Road"]
        QuerySHR --> ViewHist["View Unified History (Meds, Labs)"]
        ViewHist --> Consult["Clinical Consultation"]
        Consult --> Encounter["Record Encounter"]
        Encounter --> eRx["e-Prescribe & Labs"]
    end
    
    subgraph Core_KHIE [National KHIE / Huduma Bridge]
        eRx --> Push["Push Data to KHIE via API Gateway"]
        Push --> Update["Update Central SHR"]
        Update --> Claims["Trigger SHA Claims Processing"]
    end
    
    Claims --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Found gateway;
    class Scan,QueryReg,Enroll,Retrieve,ViewHist,Consult,Encounter,eRx userTask;
    class QuerySHR,Push,Update,Claims serviceTask;
```"""

content = re.sub(old_tobe, new_tobe, content, flags=re.DOTALL)

with open('priority_mdas/Ministry_of_Health___Service_Delivery.md', 'w') as f:
    f.write(content)
