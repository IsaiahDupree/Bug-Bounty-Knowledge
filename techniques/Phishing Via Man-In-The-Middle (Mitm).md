# Phishing Via Man-In-The-Middle (Mitm)

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty

---

## How the shelf describes it

### Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty

- **Idea**: Capturing credentials/session cookies to bypass MFA.
- **Attack Surface**: Credential submission pages, authentication forms on targeted websites.
- **How to Find & Test**:
  - Look for common login forms.
  - Monitor for script loads from suspicious origins.
  - Check for phishlets or redirectors in network requests.
- **Proof-of-Impact Approach**: Capture a session cookie post-authentication without exposing user details.
- **Impact & CWE**: High impact; Unauthorized account access (CWE-287).
- **Remediation**: Implement strict CSP and resilient MFA configurations.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._