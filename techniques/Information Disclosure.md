# Information Disclosure

_Aggregated from **3** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards, Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen, The secret of bug hunting. Bug bounty automation with python

---

## How the shelf describes it

### Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards — as "Sensible Data Exposure"

- **Idea**: Storing sensitive data insecurely or transmitting it unencrypted.
- **Where it Applies**: Data storage systems and communications.
- **How to Find & Test**: Analyze data at rest and in transit for encryption.
- **Proof-of-Impact Approach**: Show exposure of sensitive information during testing.
- **Impact & CWE**: High impact (CWE-200).
- **Remediation**: Apply encryption and secure storage practices.

### Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen — as "Secrets Exposure"

- **Idea**: Finding sensitive data in code repositories.
- **Where it Lives**: GitHub, GitLab, and other repositories.
- **How to FIND/TEST it**: Search for keywords like “oauth” in repositories.
- **Proof-of-Impact Approach**: Show unauthorized access using discovered secrets.
- **Impact & CWE**: High severity; can lead to significant breaches.
- **Remediation**: Rotate exposed secrets and enforce secure coding practices.

### The secret of bug hunting. Bug bounty automation with python — as "Sensitive Data Exposure"

- **Idea**: Identify the presence of error messages that disclose sensitive information (CWE-200).
- **Where it Applies**: Web applications, especially those running in debug mode (e.g., Django).
- **How to Find & Test**: Look for specific error messages indicating debug mode, like “URLconf defined.”
- **Proof-of-Impact Approach**: Show the error message retrieved from the HTTP response to demonstrate data exposure.
- **Impact & CWE**: High impact; can lead to further exploitation. CWE-200.
- **Remediation**: Disable debug mode in production configurations.

### The secret of bug hunting. Bug bounty automation with python — as "Debug Mode Exposure"

- **Idea**: Detect if debug modes are enabled in applications like Django and Laravel.
- **Where it Applies**: Web applications built on frameworks like Django and Laravel.
- **How to Find & Test**: Use Shodan queries like `html:"URLconf defined"` for Django.
- **Proof-of-Impact Approach**: Access `/admin` endpoints to expose sensitive information.
- **Impact & CWE**: High; potential data leakage, CWE-200.
- **Remediation**: Ensure debug mode is off in production.

### The secret of bug hunting. Bug bounty automation with python — as "S3 Bucket Exposure"

- **Idea**: Identify publicly accessible S3 buckets (CWE-22).
- **Where it Applies**: Web applications using AWS for storage.
- **How to Find & Test**: Use regex to find S3 bucket URLs in JavaScript file paths.
- **Proof-of-Impact Approach**: List contents of the S3 bucket using AWS CLI.
- **Impact & CWE**: Risk of sensitive data exposure; CWE-22.
- **Remediation**: Audit and enforce private access in S3 bucket policies.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._