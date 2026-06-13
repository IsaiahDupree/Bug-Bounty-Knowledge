# CORS Misconfiguration

_Aggregated from **2** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** A bug bounty hunting journey, My First Bug Bounty

---

## How the shelf describes it

### A bug bounty hunting journey

- **Idea**: Misconfigured CORS settings allowing unauthorized resource access.
- **Where it Applies**: Microservices and APIs with lax CORS policies.
- **How to Find & Test**: Check HTTP response headers for misconfigured CORS settings.
- **Proof-of-Impact Approach**: Demonstrate unauthorized access to resources.
- **Impact & CWE**: Medium severity; CWE-693: CORS Misconfiguration.
- **Remediation**: Enforce strict CORS policies across all API endpoints.

### My First Bug Bounty

- **Idea**: Insecure cross-origin resource sharing setups allow unauthorized resource access.
- **Where It Applies**: API endpoints and web application backends.
- **How to Find & Test**: Use tools like Corsy to identify misconfigured CORS policies.
- **Proof-of-Impact Approach**: Demonstrate unauthorized access to resources and sensitive data from a different origin.
- **Impact & CWE**: High impact; CWE-346. 
- **Remediation**: Restrict allowed origins or implement proper validation.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._