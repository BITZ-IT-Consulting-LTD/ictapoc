# Test & Validation Plan

## Project: Repeatable Government Services Platform (Production-Centric POC)

---

## 1. Purpose
This document outlines the **test strategy and validation plan** for the POC to ensure that all workflows, service configurations, and roles function correctly in a production-like environment.

---

## 2. Test Scope
- Service request submission and validation
- Workflow execution (manual and auto steps)
- SLA monitoring and escalation
- Notifications (in-app and email)
- Role-based access control
- MDA and service configuration management
- Audit logging and traceability

---

## 3. Test Environment
- Dockerized backend and frontend
- PostgreSQL database with sample data
- Redis for background tasks
- Sample service configurations (JSON/YAML)
- Simulated citizen, officer, and supervisor users

---

## 4. Test Cases

### 4.1 Service Request Submission
| Test Case ID | Description | Steps | Expected Result |
|--------------|-------------|-------|----------------|
| TC-001 | Submit valid request | Citizen fills form and submits | Request created with status RECEIVED |
| TC-002 | Submit invalid request | Missing required fields | Validation fails, audit log records VALIDATION_FAILED |

### 4.2 Workflow Execution
| Test Case ID | Description | Steps | Expected Result |
|--------------|-------------|-------|----------------|
| TC-003 | Auto-processing step | Step configured as auto_process | Step executed automatically, audit log updated |
| TC-004 | Manual step by Officer | Officer notified, approves request | Request moves to next workflow step, audit logged |
| TC-005 | SLA breach | Step not actioned in SLA time | Request escalated, notification sent, audit logged |

### 4.3 Notifications
| Test Case ID | Description | Steps | Expected Result |
|--------------|-------------|-------|----------------|
| TC-006 | Citizen receives update | Workflow step completed | Notification sent and received by citizen |
| TC-007 | Officer receives pending task | Manual step assigned | Notification sent to officer |

### 4.4 Role-Based Access Control
| Test Case ID | Description | Steps | Expected Result |
|--------------|-------------|-------|----------------|
| TC-008 | Officer access restriction | Attempt to modify service config | Access denied |
| TC-009 | Admin full access | Modify service config | Access granted, changes persisted |

### 4.5 MDA and Service Configuration Management
| Test Case ID | Description | Steps | Expected Result |
|--------------|-------------|-------|----------------|
| TC-010 | Register new MDA | Admin adds MDA with roles | MDA available, roles assigned |
| TC-011 | Add new service | Admin configures new service workflow | Service added, available for request submission |

### 4.6 Audit Logging
| Test Case ID | Description | Steps | Expected Result |
|--------------|-------------|-------|----------------|
| TC-012 | Log all actions | Perform request submission, workflow steps | Audit logs record each action with timestamp, actor, and status |

---

## 5. Metrics for Validation
- Workflow completion rate
- SLA compliance rate
- Number of validation errors per service
- Notification delivery rate
- Audit log completeness
- Role-based access enforcement

---

## 6. Assumptions
- Sample service configurations and MDAs are sufficient to validate core workflows
- Test users simulate real-world roles
- Dockerized environment accurately mirrors production

---

## 7. Acceptance Criteria
- All test cases pass successfully
- SLA breaches trigger escalations correctly
- Notifications are received by intended users
- Audit logs capture all critical actions
- Role-based access control enforced
- System ready for demonstration or further production scaling

