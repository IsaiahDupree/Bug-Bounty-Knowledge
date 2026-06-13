# Reporting & Disclosure

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Helper code:** `bbkit.report.Finding / render`  ·  **Test:** `tests/test_bbkit.py::test_report_render_has_required_sections`
```bash
pytest tests/test_bbkit.py -k report_render_has_required_sections
```

**Books:** Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen

---

## How the shelf describes it

### Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen — as "Origin IP Disclosure"

- **Idea**: Revealing the original IP behind WAFs or proxies (CWE-200).
- **Where it Lives**: Components protected by WAFs or reverse proxies.
- **How to FIND/TEST it**: Use `whois`, `amass` for ASN identification.
- **Proof-of-Impact Approach**: Access to service via discovered IP address.
- **Impact & CWE**: Low severity but leads to potential vulnerabilities like XSS.
- **Remediation**: Strengthen network security configurations.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._