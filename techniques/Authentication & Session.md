# Authentication & Session

_Aggregated from **4** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Helper code:** `bbkit.jwt_tool.decode / analyze`  ·  **Test:** `tests/test_bbkit.py::test_jwt_decode_and_alg_none`
```bash
pytest tests/test_bbkit.py -k jwt_decode_and_alg_none
```

**Books:** Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards, Bug Bounty Playbook v1, Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty, The secret of bug hunting. Bug bounty automation with python

---

## How the shelf describes it

### Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards — as "Broken Authentication"

- **Idea**: Gain unauthorized access via brute force or session hijacking.
- **Where it Applies**: User authentication components.
- **How to Find & Test**: Test for weak password policies and session management flaws.
- **Proof-of-Impact Approach**: Access accounts using compromised credentials.
- **Impact & CWE**: High impact (CWE-287).
- **Remediation**: Enforce robust authentication processes and multi-factor authentication.

### Bug Bounty Playbook v1 — as "Hard-Coded Credentials"

- **Idea**: Credentials hard-coded in source code repositories that can be exploited.
- **Where It Applies**: Source code repositories (e.g., GitHub).
- **How to Find & Test**: Search specific repositories with the company's name for hard-coded secrets.
- **Proof-of-Impact**: Demonstrate access by logging in to sensitive services using found credentials.
- **Impact & CWE**: High; CWE-798 (Use of Hardcoded Credentials).
- **Remediation**: Secure management of credentials and environment variables.

### Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty — as "Credential Harvesting"

- **Idea**: Exploiting credential management vulnerabilities.
- **Impact & CWE**: Unauthorized access (CWE-255).

### The secret of bug hunting. Bug bounty automation with python — as "Default Credentials in SonarQube"

- **Idea**: Accessing SonarQube via known default credentials (CWE-287).
- **Where it Applies**: SonarQube instances.
- **How to Find & Test**: Shodan query `http.title:"SonarQube"`.
- **Proof-of-Impact Approach**: Login using default `admin/admin` credentials.
- **Impact & CWE**: High; administrative access risks.
- **Remediation**: Always change default credentials.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._