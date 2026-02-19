# STATE LAW OFFICE (ATTORNEY GENERAL) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** STATE LAW OFFICE (ATTORNEY GENERAL)
- **Process Name:** Marriage Registration
- **Document Version:** 1.2
- **Date:** 2026-02-19
- **Classification:** Official

---

## Executive Summary
The Office of the Attorney General (State Law Office), through the Registrar of Marriages, oversees all civil, customary, Christian, Hindu, and Islamic marriages in Kenya. It issues the **Marriage Certificate**, a vital document for spousal benefits, travel, and succession.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Manual Notice / Sheria House Queues).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Couple [Applicants]
        S1["Logs into eCitizen (Office of AG)"]
        S2["Files Notice of Marriage (21 Days)"]
        S3["Uploads IDs & Photos"]
        S4["Pays Fee (KES 600 - Notice)"]
        S5["Books Appointment Date"]
        S6["Visits Sheria House (Nairobi)"]
        S8["Signs Marriage Certificate"]
    end
    subgraph Registrar [Marriage Officer]
        S2a["Reviews Notice Application"]
        S2b["Approves Notice (if no impediment)"]
        S7["Conducts Ceremony (15 Mins)"]
        S9["Issues Certificate"]
    end
    
    S1 --> S2
    S2 --> S2a
    S2a --> S2b
    S2b --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> S9
    S9 --> End((End))
```

---

## Process Overview
### Process Name
Civil Marriage Registration (Sheria House)

### Service Category
- G2C (Government to Citizen)

### Scope
- **In Scope:** Notice of Marriage; Civil Marriage Ceremony; Issuance of Marriage Certificate.
- **Out of Scope:** Divorce (Judiciary); Customary Marriage registration (often delayed).

### Triggers
- Couple intending to marry.

### End States
- **Successful:** Issuance of Marriage Certificate.

### Policy Context
- Marriage Act, 2014.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Couple | Applicant | Files notice, attends interview/ceremony. |
| Registrar of Marriages | Officiant | Conducts civil marriage, verifies capacity to marry. |
| Witnesses (2) | Verifier | Witness the vows and sign the register. |
| Public | Objector | May file an objection (Caveat) during the 21-day notice period. |

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Couple | **Notice:** Both parties log into eCitizen, fill details (Occupation, Residence, Parents). Upload passport photos and ID copies. | eCitizen Portal | System requires both parties to have eCitizen accounts. |
| 2 | Couple | **Fee Payment:** Pays KES 600 for Notice. Wait 21 days (mandatory legal requirement). | Mobile Money | No way to expedite legally (except Special License). |
| 3 | Registrar | **Review:** Officer checks uploaded documents. If valid, Notice is "Published" (often just pinned on a notice board at Sheria House). | Physical Board | Archaic method of publication. |
| 4 | Couple | **Booking:** After 21 days, couple logs in to book a date for the ceremony. Pays KES 3,300 (Ceremony Fee). | Appointment System | Slots at Sheria House fill up fast, especially on Fridays. |
| 5 | Couple + Witnesses | **Ceremony:** On the day, arrive at Sheria House. Wait in queue. Enter Registrar's office for brief vows. | Physical Office | Often chaotic, crowded waiting rooms. |
| 6 | Registrar | **Issuance:** Parties sign the Register. Registrar issues hand-written or typed Certificate. | Manual Certificate | Risk of typos. |

---

## Pain Points & Opportunities
### Pain Points
- **Physical Presence:** Both parties must visit Sheria House for the interview/booking, even if applied online.
- **Notice Board:** Relying on a physical notice board for objections is ineffective in the digital age.
- **Delays:** Booking slots can be months away due to high demand.
- **Customary Marriages:** Registration of customary unions (traditional weddings) is complex and often ignored until death/succession disputes arise.
- **Verification:** Banks/Embassies struggle to verify manual certificates instantly.

### Opportunities
- **Digital Notice:** Publish notices online (e-Gazette/Portal) for wider visibility.
- **Remote Interview:** Conduct the pre-wedding interview via video link to save travel.
- **Decentralization:** Empower Huduma Centres in all counties to officiate marriages (currently limited).
- **Blockchain:** Immutable marriage register to prevent bigamy/fraud.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Repeatable WoG Platform).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph WoG_Platform [Civil Registry]
        S1["Checks Marital Status (Bigamy Check)"]
        S2["Publishes Online Notice (e-Gazette)"]
        S3["Waits 21 Days (Auto-Countdown)"]
    end
    subgraph Couple [Applicants]
        S4["Logs into eCitizen App"]
        S5["Jointly Signs 'Notice of Intent' (Digital Signature)"]
        S6["Receives 'License to Marry' QR Code"]
    end
    subgraph Officiant [Registrar / Pastor / Kadhi]
        S7["Scans Couple's QR Code at Venue"]
        S8["Activates 'Married' Status in Registry"]
    end
    subgraph Integrated_Systems [X-Road]
        S9["Updates Spouse Status in IPRS/NRB"]
        S10["Issues Digital Certificate"]
    end
    
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> S9
    S9 --> S10
    S10 --> End((End))
```

## Future State Process (TO-BE)
### Narrative
The process is **Decentralized** and **Secure**.
1.  **Smart Notice:** The **WoG Platform** checks the ID numbers of both parties against the central marriage database. Bigamy is flagged instantly.
2.  **Online Publication:** The "Notice of Marriage" is published on the public **e-Gazette** portal, searchable by name.
3.  **Digital License:** After 21 days, if no objection is filed online, the couple receives a secure **QR Code License** on their phone.
4.  **Universal Officiation:** Any licensed officiant (Pastor, Imam, Registrar) uses the **Government Officiant App** to scan the QR code at the wedding venue (church, garden, mosque). This "activates" the marriage in real-time.
5.  **Instant Update:** The change of status (Single -> Married) is pushed immediately to **IPRS**, linking the spouses for future services (NHIF, Pension).

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Couple | Files joint notice via eCitizen App. | eCitizen App |
| 2 | WoG Platform | Runs bigamy check and publishes notice. | Registry / e-Gazette |
| 3 | Public | Can view notice and file objection online. | Public Portal |
| 4 | Officiant | Scans QR code to finalize marriage. | Officiant App |
| 5 | Registry | Updates status and issues Digital Cert. | X-Road |

---

## References
- Marriage Act.
