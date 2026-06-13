# Certificate Transparency Monitoring

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen

---

## How the shelf describes it

### Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen

- **Idea**: Monitoring SSL certificates for fraud.
- **Where it Lives**: SSL certificates in Certificate Transparency logs.
- **How to FIND/TEST it**: Use `crt.sh` for monitoring.
- **Proof-of-Impact Approach**: Demonstrate issuing fraudulent certificates.
- **Impact & CWE**: Can lead to man-in-the-middle attacks if misconfigured.
- **Remediation**: Regular audits of certificate usage.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._