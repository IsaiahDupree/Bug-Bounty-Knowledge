# SSTI

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** A bug bounty hunting journey

---

## How the shelf describes it

### A bug bounty hunting journey — as "Client-Side Template Injection"

- **Idea**: Injecting JavaScript into front-end frameworks.
- **Where it Applies**: Frameworks like AngularJS that use client-side templates.
- **How to Find & Test**: Manipulate user input that is embedded in templates.
- **Proof-of-Impact Approach**: Demonstrate a script execution through template manipulation.
- **Impact & CWE**: High severity; CWE-20: Improper Input Validation.
- **Remediation**: Validate and sanitize all user inputs.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._