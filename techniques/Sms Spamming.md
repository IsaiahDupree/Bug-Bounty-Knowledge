# Sms Spamming

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** A bug bounty hunting journey

---

## How the shelf describes it

### A bug bounty hunting journey

- **Idea**: Exploiting SMS functionalities to send unsolicited messages.
- **Where it Applies**: SMS-related features in web applications.
- **How to Find & Test**: Monitor HTTP requests for phone number manipulation and observe SMS behavior.
- **Proof-of-Impact Approach**: Alter fields to demonstrate unsolicited SMS being sent.
- **Impact & CWE**: Medium severity; CWE-20: Improper Input Validation.
- **Remediation**: Implement rate limiting on SMS functionalities.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._