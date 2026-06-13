# Html Injection

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

---

## How the shelf describes it

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

- **Idea**: Inject arbitrary HTML code into web applications, possibly leading to XSS.
- **Where It Lives**: Input fields in web applications.
- **How to Find & Test**: Inject HTML tags into input fields and check the output.
- **Proof-of-Impact Approach**: Verify if injected HTML is rendered on the page.
- **Impact & CWE**: Moderate to high; could lead to trust issues (CWE-79).
- **Remediation**: Sanitize and encode all user inputs.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._