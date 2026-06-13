# Cross-Site Scripting (XSS)

_Aggregated from **8** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Helper code:** `bbkit.encoders.html_entities / case_permute (filter-evasion analysis)`  ·  **Test:** `tests/test_bbkit.py::test_encoders`
```bash
pytest tests/test_bbkit.py -k encoders
```

**Books:** A bug bounty hunting journey, Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards, Bug Bounty Field Manual, Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I, Bug Bounty Playbook v1, Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi, Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty, [Journal of Database Management 2020-jan vol. 31 iss. 1] Bug Bounty Ma

---

## How the shelf describes it

### A bug bounty hunting journey — as "Reflected XSS (Cross-Site Scripting)"

- **Idea**: Injecting scripts in user inputs to manipulate application outputs.
- **Where it Applies**: Web application inputs and outputs.
- **How to Find & Test**: Check for reflected inputs in HTTP responses.
- **Proof-of-Impact Approach**: Trigger a benign JavaScript alert to show exploitation.
- **Impact & CWE**: High severity; CWE-79: Improper Neutralization of Input During Web Page Generation.
- **Remediation**: Sanitize and encode user inputs.

### Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards

- **Idea**: Injecting malicious scripts into web pages.
- **Where it Applies**: User input forms and display areas in web applications.
- **How to Find & Test**: Inject payloads in fields to check for execution of scripts.
- **Proof-of-Impact Approach**: Use alerts to show script execution in the user's browser context.
- **Impact & CWE**: High impact (CWE-79), can lead to session hijacking.
- **Remediation**: Enforce output encoding and input validation.

### Bug Bounty Field Manual

- **Idea**: Injecting malicious scripts into web pages viewed by other users.
- **Where it Applies**: Web applications that fail to sanitize user-generated content.
- **How to Find & Test**: Input `<script>alert(1)</script>` in inputs and observe whether it gets executed.
- **Proof-of-Impact Approach**: Show script execution without causing harm (e.g., alert pop-up).
- **Impact & CWE**: Can lead to session hijacking; CWE-79.
- **Remediation**: Use content security policies and escape outputs.

### Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi

- **Idea**: Injecting malicious scripts into web pages executed by users.
- **CWE**: CWE-79.
- **Where It Lives**: Web applications.
- **How to Find & Test**: Test input fields for reflected output with malicious scripts.
- **Proof-of-Impact Approach**: Craft benign scripts to show potential data theft.
- **Impact & Severity**: Medium to high; user data risk.
- **Remediation**: Implement CSP and sanitize outputs.

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I

- **Idea**: Injecting malicious scripts into web pages viewed by other users. 
- **Where It Applies**: User input fields like forums and login forms.
- **How to Find & Test**: Utilize tools like Burp Suite to test for XSS through input fields. Inject test scripts (e.g., `<script>alert("XSS")</script>`).
- **Proof-of-Impact Approach**: Trigger an alert box using injected JavaScript to demonstrate the vulnerability.
- **Impact & CWE**: Can lead to session hijacking (CWE-79).
- **Remediation**: Ensure user input is properly sanitized and encoded.

### Bug Bounty Playbook v1

- **Idea**: Allows execution of malicious scripts in users' browsers.
- **Where It Applies**: Web applications that render unsanitized user inputs.
- **How to Find & Test**: Identify user input fields to inject script payloads.
- **Proof-of-Impact**: Demonstrate script execution via alerts or similar methods.
- **Impact & CWE**: High; CWE-79 (Improper Neutralization of Input).
- **Remediation**: Implement input sanitization and output encoding.

### [Journal of Database Management 2020-jan vol. 31 iss. 1] Bug Bounty Ma

- **Idea**: Injection of malicious scripts into web pages viewed by users.
- **Where it Applies**: Web applications that accept and render untrusted data.
- **How to Find & Test**: Look for input fields and URL parameters that reflect user input. Use scripts to see if they execute in the browser.
- **Proof-of-Impact Approach**: Demonstrate script execution in a controlled environment without causing disruption.
- **Impact & CWE**: Can lead to session hijacking, phishing, and data theft; relates to CWE-79.
- **Remediation**: Implement proper input validation and output encoding.

### Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty

- **Idea**: Injecting scripts into web pages for execution.
- **Impact & CWE**: High risk of data breach (CWE-79).

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._