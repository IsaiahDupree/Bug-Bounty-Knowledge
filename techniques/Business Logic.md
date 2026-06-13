# Business Logic

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi

---

## How the shelf describes it

### Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi — as "Business Logic Flaws"

- **Idea**: Exploiting application functionality for unintended use (e.g., negative transactions).
- **Where It Lives**: Critical systems like databases, email servers, and payment systems.
- **How to Find & Test**: Understand critical systems, identify entry points, and look for abnormal behaviors.
- **Proof-of-Impact Approach**: Describe the flaw conceptually to demonstrate potential misuse without weaponized payloads.
- **Impact & CWE**: Potential loss of customers and reputational damage; no specific CWE mentioned.
- **Remediation**: Business process reviews and security patches.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._