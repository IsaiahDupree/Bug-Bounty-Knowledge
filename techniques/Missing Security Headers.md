# Missing Security Headers

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** My First Bug Bounty

---

## How the shelf describes it

### My First Bug Bounty

- **Idea**: Lack of HTTP response security headers.
- **Where It Applies**: Web server response configurations.
- **How to Find & Test**: Inspect headers using browser dev tools or curl.
- **Proof-of-Impact Approach**: Detail potential exposure to attacks like XSS.
- **Impact & CWE**: Medium impact.
- **Remediation**: Implement recommended security headers.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._