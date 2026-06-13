# Recon & Enumeration

_Aggregated from **4** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** A bug bounty hunting journey, Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi, Corporate Cybersecurity Identifying Risks and the Bug Bounty Program, Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen

---

## How the shelf describes it

### A bug bounty hunting journey — as "Account Enumeration"

- **Idea**: Identifying valid usernames based on differences in response messages during login attempts.
- **Where it Applies**: Authentication flow of web applications.
- **How to Find & Test**: Analyze response messages for discrepancies between valid and invalid usernames.
- **Proof-of-Impact Approach**: Document differences in error messages to demonstrate enumeration risk.
- **Impact & CWE**: Medium severity; CWE-203: Information Exposure Through Discrepancy.
- **Remediation**: Implement generic error messages to reduce information leakage.

### Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi — as "Directory Enumeration"

- **Idea**: Discovering hidden files/resources.
- **CWE**: CWE-501.
- **Where It Lives**: Web servers and applications.
- **How to Find & Test**: Use automated tools to brute-force common directories.
- **Proof-of-Impact Approach**: Document discovered sensitive files.
- **Impact & Severity**: Can lead to unauthorized data access; must restrict directory access.
- **Remediation**: Limit accessible directories and files.

### Corporate Cybersecurity Identifying Risks and the Bug Bounty Program — as "Account and Email Enumeration"

- **Idea**: Identify valid accounts/emails through error message patterns.
- **Where It Applies**: Login portals, user account management systems.
- **How to Find & Test**: Analyze application response behaviors and timing during login attempts.
- **Proof-of-Impact Approach**: Show differences in error messages for valid vs. invalid accounts.
- **Impact & CWE**: Can lead to account takeover; CWE-203.
- **Remediation**: Generic error messages without account identification.

### Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen — as "Horizontal Domain Enumeration"

- **Idea**: Scanning for subdomains or domains owned by the organization that may be misconfigured (CWE-200).
- **Where it Lives**: Domains and subdomains of the target organization.
- **How to FIND/TEST it**: Use OSINT techniques, monitor company disclosures.
- **Proof-of-Impact Approach**: Access unintended features discovered during testing.
- **Impact & CWE**: High severity if sensitive data is exposed.
- **Remediation**: Tighten domain scopes, regularly review configurations.

### Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen — as "CIDR Enumeration"

- **Idea**: Identifying IP address ranges for potential misconfigured services or vulnerabilities.
- **Where it Lives**: IP ranges registered under Autonomous System Numbers (ASNs).
- **How to FIND/TEST it**: Identify ASN using `whois`; expand CIDRs with `prips`.
- **Proof-of-Impact Approach**: Access a service directly via discovered IP addresses.
- **Impact & CWE**: Severity is low, but risks exist for further vulnerabilities.
- **Remediation**: Improve network protection templates, review configurations.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._