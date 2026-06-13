# Weak Cipher

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** My First Bug Bounty

---

## How the shelf describes it

### My First Bug Bounty

- **Idea**: Use of outdated cryptographic algorithms.
- **Where It Applies**: Encryption methods.
- **How to Find & Test**: Check for cipher support using tools like SSL Labs.
- **Proof-of-Impact Approach**: Show that communication can be intercepted using weak ciphers.
- **Impact & CWE**: High impact; CWE-327.
- **Remediation**: Disable weak ciphers and enforce strong ones.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._