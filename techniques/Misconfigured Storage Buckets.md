# Misconfigured Storage Buckets

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Playbook v1

---

## How the shelf describes it

### Bug Bounty Playbook v1

- **Idea**: Publicly accessible cloud storage allowing unauthorized access to sensitive data.
- **Where It Applies**: Cloud Storage (e.g., AWS S3 buckets).
- **How to Find & Test**: Use Google Dorking and manual searches for misconfigurations.
- **Proof-of-Impact**: Access and retrieve sensitive files from exposed storage.
- **Impact & CWE**: High; CWE-552 (Content Exposure).
- **Remediation**: Implement proper access controls for storage solutions.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._