# Clickjacking

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

---

## How the shelf describes it

### Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

- **Idea**: Deceiving users into clicking on something different from what they perceive.
- **Where It Applies**: Web applications with actionable elements (e.g., buttons).
- **How to Find & Test**: Inspect UI for exposed frames or iframes.
- **Proof-of-Impact Approach**: Show unintended actions initiated by a hidden element.
- **Impact & CWE**: Potentially unauthorized actions; CWE-1021.
- **Remediation**: Employ X-Frame-Options and frame-busting techniques.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._