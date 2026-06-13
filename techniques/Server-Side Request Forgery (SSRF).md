# Server-Side Request Forgery (SSRF)

_Aggregated from **3** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Field Manual, Bug Bounty Playbook v1, My First Bug Bounty

---

## How the shelf describes it

### Bug Bounty Field Manual

- **Idea**: Forcing a server to make requests to internal or external resources.
- **Where it Applies**: Services that take URLs as parameters without validation.
- **How to Find & Test**: Supply crafted URLs that point to internal services.
- **Proof-of-Impact Approach**: Illustrate potential access to internal endpoints without causing disruption.
- **Impact & CWE**: Can lead to data exposure; CWE-918.
- **Remediation**: Validate and sanitize URL inputs.

### Bug Bounty Playbook v1

- **Idea**: Forces an application to make HTTP requests to internal services.
- **Where It Applies**: Applications accepting user-defined URLs.
- **How to Find & Test**: Manipulate URL inputs to access internal resources.
- **Proof-of-Impact**: Access internal application data by targeting localhost or internal services.
- **Impact & CWE**: High; CWE-918 (Server-Side Request Forgery).
- **Remediation**: Validate and sanitize URL inputs.

### My First Bug Bounty

- **Idea**: Exploiting a server's ability to make requests to arbitrary domains.
- **Where It Applies**: Web applications and APIs.
- **How to Find & Test**: Modify host headers to test for untrusted requests.
- **Proof-of-Impact Approach**: Demonstrate unauthorized requests being sent to internal services.
- **Impact & CWE**: High impact; CWE-918.
- **Remediation**: Validate and sanitize user input that controls server requests.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._