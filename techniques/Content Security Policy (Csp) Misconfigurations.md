# Content Security Policy (Csp) Misconfigurations

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen

---

## How the shelf describes it

### Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen

- **Idea**: Misconfigured CSP headers may expose to XSS (CWE-693).
- **Where it Lives**: HTTP response headers with CSP.
- **How to FIND/TEST it**: Fetch CSP headers using `curl`.
- **Proof-of-Impact Approach**: Analyze loaded domains.
- **Impact & CWE**: Vulnerable to XSS; high risk of data leak.
- **Remediation**: Regular CSP audits and adjustments.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._