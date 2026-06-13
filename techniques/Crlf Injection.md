# Crlf Injection

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** My First Bug Bounty

---

## How the shelf describes it

### My First Bug Bounty

- **Idea**: Injection of carriage return and line feed characters into HTTP headers.
- **Where It Applies**: HTTP request headers.
- **How to Find & Test**: Send crafted HTTP requests including CRLF characters.
- **Proof-of-Impact Approach**: Illustrate response splitting that can lead to additional responses being processed.
- **Impact & CWE**: High impact; CWE-113.
- **Remediation**: Sanitize inputs to prevent CRLF characters in user-controlled data.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._