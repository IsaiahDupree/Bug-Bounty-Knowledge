# IDOR / Broken Access Control

_Aggregated from **3** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards, Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi, Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty

---

## How the shelf describes it

### Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards — as "Broken Access Control"

- **Idea**: Poorly enforced authorization mechanisms leading to unauthorized access.
- **Where it Applies**: Resource-sensitive operations in web apps.
- **How to Find & Test**: Attempt direct object references with lower permissions.
- **Proof-of-Impact Approach**: Access restricted resources meant for higher-privilege users.
- **Impact & CWE**: High impact (CWE-284).
- **Remediation**: Enforce robust access controls and regular testing.

### Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi — as "Insecure Direct Object Reference (IDOR)"

- **Idea**: Unauthenticated access to objects via identifiers.
- **CWE**: CWE-648.
- **Where It Lives**: Web applications with sensitive resources.
- **How to Find & Test**: Manipulate object identifiers in requests.
- **Proof-of-Impact Approach**: Access restricted resources by altering parameters.
- **Impact & Severity**: High; significant risk of unauthorized access.
- **Remediation**: Proper authorization checks.

### Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty — as "Local Privilege Escalation"

- **Idea**: Gaining higher privileges on systems post-initial access.
- **Impact & CWE**: Unauthorized access to sensitive data (CWE-264).

### Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty — as "Network-based Privilege Escalation"

- **Idea**: Exploiting network vulnerabilities for privilege escalation.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._