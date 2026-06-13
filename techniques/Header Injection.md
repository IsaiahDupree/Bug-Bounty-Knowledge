# Header Injection

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

---

## How the shelf describes it

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

- **Idea**: Manipulating HTTP headers through unsanitized user input.
- **Where It Lives**: Web applications using user-input for HTTP headers.
- **How to Find & Test**: Test fields accepting URL or header values for external headers.
- **Proof-of-Impact Approach**: Modify headers to redirect or alter behavior and check effects.
- **Impact & CWE**: Can lead to harmful redirects (CWE-113).
- **Remediation**: Validate and sanitize all inputs used in headers.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._