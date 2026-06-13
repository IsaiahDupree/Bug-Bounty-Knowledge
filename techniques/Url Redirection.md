# Url Redirection

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

---

## How the shelf describes it

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

- **Idea**: Attacker manipulates redirection endpoints, leading users to malicious sites.
- **Where It Lives**: Applications that perform URL redirection.
- **How to Find & Test**: Test URL parameters for unvalidated input.
- **Proof-of-Impact Approach**: Craft URLs that redirect to external sites and assess if they are followed.
- **Impact & CWE**: Can facilitate phishing attacks (CWE-601).
- **Remediation**: Employ a whitelist for redirects and validate all user inputs.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._