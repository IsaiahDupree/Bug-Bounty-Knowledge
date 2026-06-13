# CSRF

_Aggregated from **6** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** A bug bounty hunting journey, Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards, Bug Bounty Field Manual, Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I, Bug Bounty Playbook v1, My First Bug Bounty

---

## How the shelf describes it

### A bug bounty hunting journey — as "CSRF (Cross-Site Request Forgery)"

- **Idea**: Allowing unauthorized actions on behalf of a user through unprotected endpoints.
- **Where it Applies**: Web applications lacking anti-CSRF tokens.
- **How to Find & Test**: Test features without CSRF protections.
- **Proof-of-Impact Approach**: Execute actions using crafted requests that leverage the absence of protections.
- **Impact & CWE**: High severity; CWE-352: Cross-Site Request Forgery.
- **Remediation**: Implement anti-CSRF tokens for all state-changing requests.

### Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards — as "Cross-Site Request Forgery (CSRF)"

- **Idea**: Trick users into performing unintended actions on a web app.
- **Where it Applies**: Endpoints that change state based on authenticated user actions.
- **How to Find & Test**: Identify actions that lack anti-CSRF tokens.
- **Proof-of-Impact Approach**: Induce a state change without user consent (e.g., modify user settings).
- **Impact & CWE**: High impact (CWE-352).
- **Remediation**: Apply anti-CSRF tokens and SameSite cookie attributes.

### Bug Bounty Field Manual — as "Cross-Site Request Forgery (CSRF)"

- **Idea**: Trick users into executing unwanted actions on a web application where they are authenticated.
- **Where it Applies**: Applications with state-changing actions without CSRF tokens.
- **How to Find & Test**: Create a form that submits actions to test for absence of CSRF protection.
- **Proof-of-Impact Approach**: Show potential unauthorized request submission (e.g., changing user settings).
- **Impact & CWE**: Can lead to unauthorized actions; CWE-352.
- **Remediation**: Implement CSRF tokens and validate requests.

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I — as "Cross-Site Request Forgery (CSRF)"

- **Idea**: Tricking the user's browser into executing unwanted actions on a web application.
- **Where It Lives**: Forms or APIs that change user state.
- **How to Find & Test**: Look for forms without anti-CSRF tokens. Inspect HTML for hidden inputs and action URLs.
- **Proof-of-Impact Approach**: Simulate a CSRF attack by crafting a malicious request to alter user data.
- **Impact & CWE**: Can lead to unauthorized actions; high severity (CWE-352).
- **Remediation**: Implement anti-CSRF tokens and validate requests.

### Bug Bounty Playbook v1 — as "Cross-Site Request Forgery (CSRF)"

- **Idea**: Causes a user's browser to execute unauthorized actions.
- **Where It Applies**: Applications with authenticated state changes.
- **How to Find & Test**: Check forms lacking anti-CSRF tokens.
- **Proof-of-Impact**: Perform actions like changing user account details by tricking a user.
- **Impact & CWE**: High; CWE-352 (Cross-Site Request Forgery).
- **Remediation**: Implement anti-CSRF tokens.

### My First Bug Bounty

- **Idea**: Cross-site request forgery that allows unauthorized requests on behalf of authenticated users.
- **Where It Applies**: Forms and actions performing sensitive operations.
- **How to Find & Test**: Use XSRFProbe to check for missing anti-CSRF tokens.
- **Proof-of-Impact Approach**: Simulate state-changing actions as an authenticated user without consent.
- **Impact & CWE**: High impact; CWE-352.
- **Remediation**: Implement anti-CSRF tokens and enforce same-origin policies.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._