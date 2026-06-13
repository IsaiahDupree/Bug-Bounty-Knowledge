# XXE

_Aggregated from **2** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I, Bug Bounty Playbook v1

---

## How the shelf describes it

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I — as "XML External Entity (XXE) Injection"

- **Idea**: Taking advantage of XML parsers that process external entities, potentially exposing system files.
- **Where It Lives**: Systems using XML data processing.
- **How to Find & Test**: Inspect XML handling components for DTD usage.
- **Proof-of-Impact Approach**: Inject XML payloads to retrieve sensitive files.
- **Impact & CWE**: High; can disclose sensitive system information (CWE-611).
- **Remediation**: Disable external entity processing and validate XML inputs.

### Bug Bounty Playbook v1 — as "XML External Entity Injection (XXE)"

- **Idea**: Allows reading of arbitrary files on a server through malicious XML entities.
- **Where It Applies**: Applications that process XML.
- **How to Find & Test**: Inject external entities in XML submissions to retrieve sensitive files.
- **Proof-of-Impact**: Read critical files (e.g., `/etc/passwd`) through injection.
- **Impact & CWE**: High; CWE-611 (XML External Entity Reference).
- **Remediation**: Disallow external entity processing in XML parsers.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._