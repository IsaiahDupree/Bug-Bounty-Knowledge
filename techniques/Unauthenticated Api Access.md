# Unauthenticated Api Access

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Playbook v1

---

## How the shelf describes it

### Bug Bounty Playbook v1

- **Idea**: Exposed APIs allow unauthorized interactions.
- **Where It Applies**: Public APIs lacking authentication.
- **How to Find & Test**: Query APIs without credentials; test for access.
- **Proof-of-Impact**: Demonstrate unauthorized data retrieval.
- **Impact & CWE**: High; CWE-284 (Improper Access Control).
- **Remediation**: Secure APIs with proper authentication mechanisms.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._