# Command Injection / RCE

_Aggregated from **2** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I, Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

---

## How the shelf describes it

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I — as "Command Injection"

- **Idea**: Executing arbitrary OS commands due to improper input validation.
- **Where It Lives**: Web applications that accept user input for command execution.
- **How to Find & Test**: Input OS commands via fields and analyze response discrepancies.
- **Proof-of-Impact Approach**: Execute simple shell commands and check for changes in output.
- **Impact & CWE**: High risk as it can lead to server compromise (CWE-77).
- **Remediation**: Validate and sanitize user inputs properly.

### Corporate Cybersecurity Identifying Risks and the Bug Bounty Program — as "Brute Force Attacks"

- **Idea**: Repeatedly attempting various credential combinations to gain unauthorized access.
- **Where It Applies**: Login portals, APIs.
- **How to Find & Test**: Monitor for high volumes of failed login attempts.
- **Proof-of-Impact Approach**: Demonstrate potential account access without full credential enumeration.
- **Impact & CWE**: Account takeover risk; CWE-307.
- **Remediation**: Implement account lockout and CAPTCHA challenges.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._