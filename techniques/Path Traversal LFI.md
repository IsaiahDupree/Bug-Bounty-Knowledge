# Path Traversal / LFI

_Aggregated from **1** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Helper code:** `bbkit.encoders.path_traversal / double_url_encode`  ·  **Test:** `tests/test_bbkit.py::test_encoders`
```bash
pytest tests/test_bbkit.py -k encoders
```

**Books:** Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

---

## How the shelf describes it

### Corporate Cybersecurity Identifying Risks and the Bug Bounty Program — as "Directory Traversal"

- **Idea**: Accessing files outside the intended directory.
- **Where It Applies**: Web servers and file handling.
- **How to Find & Test**: Look for inputs allowing sequences like `../` to traverse directories.
- **Proof-of-Impact Approach**: Demonstrate access to sensitive files (e.g., /etc/passwd).
- **Impact & CWE**: Exposure of sensitive data; CWE-22.
- **Remediation**: Validate inputs and restrict file access.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._