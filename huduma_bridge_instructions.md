# Huduma Bridge Integration & Usage Instructions

## Overview
The **Huduma Bridge** is the authoritative connectivity layer for citizen-centric services in the GOS (Government Operation System). It provides a standardized interface for interacting with various MDA (Ministry, Department, and Agency) backends using the **ICTA POC Framework**.

## Integration Architecture
The bridge operates on a **Zero-Trust** model, requiring every request to be:
1. **Authenticated**: via ICTA-issued JWT 2.0.
2. **Authorized**: via the Security & Trust Layer (RBAC).
3. **Consented**: requires valid Citizen Consent token.

## Standard Workflow Step Configuration
When configuring an **Automated API Call** in the Workflow Step Manager, follow these patterns:

### 1. Identity Validation (IPRS)
- **URL**: `HUB_BRIDGE/IPRS/verify`
- **Method**: `POST`
- **Payload Structure**:
```json
{
  "id_number": "{{citizen.id_number}}",
  "data_required": ["names", "dob", "status"]
}
```

### 2. Document Archival (EDRM)
- **URL**: `HUB_BRIDGE/EDRM/store`
- **Method**: `PUT`
- **Payload Structure**:
```json
{
  "request_id": "{{request.id}}",
  "mda_code": "{{mda.code}}",
  "document_type": "PDF",
  "file_stream": "BASE64_DATA"
}
```

## Error Handling
The Huduma Bridge returns standard HTTP status codes:
- **200/201**: Success.
- **401**: Authentication Refused (Check Token).
- **403**: Consent Missing or Revoked.
- **429**: Rate limit exceeded (KESEL Throttling).

## Best Practices
- **Idempotency**: Always include `request_id` to prevent duplicate processing.
- **Logging**: All Bridge interactions are automatically logged in the **Audit Logs** tab for compliance.
- **Retry Logic**: Implement exponential backoff for 5xx Gateway errors.
