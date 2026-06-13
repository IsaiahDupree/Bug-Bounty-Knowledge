# Rfid Badge Cloning

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty

---

## How the shelf describes it

### Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty

- **Idea**: Exploiting unencrypted communication for unauthorized access.
- **Where it Lives**: Access control systems with RFID badges (e.g., iClass legacy cards).
- **How to Find & Test**:
  - Look for unencrypted badge communications.
  - Use RFID sniffers to capture data.
- **Proof-of-Impact Approach**: Clone a badge by capturing credential data.
- **Impact & CWE**: High impact (CWE-202).
- **Remediation**: Use encrypted communication; secure credential management practices.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._