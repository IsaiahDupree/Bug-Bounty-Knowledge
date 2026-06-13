# Code Injection Attacks

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi

---

## How the shelf describes it

### Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi

- **Idea**: Untrusted data executing as commands (e.g., SQL injection).
- **CWE**: CWE-94 (Code Injection).
- **Where It Lives**: Web applications, APIs.
- **How to Find & Test**: Inspect input fields and URLs for vulnerabilities.
- **Proof-of-Impact Approach**: Simulate injection without damaging data integrity.
- **Impact & Severity**: High; can lead to unauthorized access.
- **Remediation**: Input validation and use of parameterized queries.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._