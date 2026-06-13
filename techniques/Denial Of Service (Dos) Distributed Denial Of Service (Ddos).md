# Denial Of Service (Dos) / Distributed Denial Of Service (Ddos)

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

---

## How the shelf describes it

### Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

- **Idea**: Overwhelm a service to make it unavailable.
- **Where It Applies**: Web applications, APIs, and any online services.
- **How to Find & Test**: Monitor application response times during heavy loads; use automated tools to simulate attacks.
- **Proof-of-Impact Approach**: Demonstrate temporary service downtime without causing permanent damage.
- **Impact & CWE**: Can disrupt services; CWE-400.
- **Remediation**: Implement traffic monitoring and rate limiting.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._