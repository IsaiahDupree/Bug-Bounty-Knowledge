# File Upload

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

---

## How the shelf describes it

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I — as "File Upload Vulnerability"

- **Idea**: Allowing uploads of malicious files due to inadequate validation.
- **Where It Lives**: File upload interfaces.
- **How to Find & Test**: Look for file upload forms; test with various file types and extensions.
- **Proof-of-Impact Approach**: Upload a PHP file disguised as another file type to demonstrate potential exploitation.
- **Impact & CWE**: High, as it may lead to arbitrary code execution (CWE-434).
- **Remediation**: Implement strict server-side validations and restrictions based on file type.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._