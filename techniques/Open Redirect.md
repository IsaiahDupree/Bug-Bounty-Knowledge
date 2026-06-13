# Open Redirect

_Aggregated from **2** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Corporate Cybersecurity Identifying Risks and the Bug Bounty Program, My First Bug Bounty

---

## How the shelf describes it

### Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

- **Idea**: Redirecting users to untrusted sites via manipulated URLs.
- **Where It Applies**: URL parameters in web applications.
- **How to Find & Test**: Assess input parameters for potential redirection logic.
- **Proof-of-Impact Approach**: Show redirection to a controlled domain.
- **Impact & CWE**: Can facilitate phishing attacks; CWE-601.
- **Remediation**: Validate and sanitize URL parameters.

### My First Bug Bounty — as "Open Redirection"

- **Idea**: Allows redirection to untrusted URLs, potentially leading to phishing.
- **Where It Applies**: URL parameters and links in web applications.
- **How to Find & Test**: Look for URL parameters that perform redirects; test with benign payloads.
- **Proof-of-Impact Approach**: Show potential redirect to a phishing site via exploitable parameters.
- **Impact & CWE**: Medium to high impact; CWE-601.
- **Remediation**: Validate redirect URLs against a whitelist.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._