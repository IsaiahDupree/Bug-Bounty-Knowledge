# Open Ports/Services

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Playbook v1

---

## How the shelf describes it

### Bug Bounty Playbook v1

- **Idea**: Exposed services on IPs, potentially vulnerable to exploitation.
- **Where It Applies**: Web applications and IPs with open ports.
- **How to Find & Test**: Conduct port scans using tools like Nmap to identify open ports.
- **Proof-of-Impact**: Showcase potential exploitability based on identified services.
- **Impact & CWE**: Variable; CWE-200 (Information Exposure), CWE-889 (Insecure Service).
- **Remediation**: Regularly assess and minimize exposed services.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._