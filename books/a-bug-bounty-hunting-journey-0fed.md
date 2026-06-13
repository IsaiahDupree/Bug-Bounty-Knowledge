# A bug bounty hunting journey

> **AI-generated research summary** (model: `gpt-4o-mini`, map-reduce over 7 excerpts). Original study notes — vulnerability classes, techniques, and methodology extracted for AUTHORIZED testing + responsible disclosure, **not** the book's verbatim text and **not** weaponized exploits.
>
> **Source book:** thehackerish - A bug bounty hunting journey - libgen.li.pdf

---

```markdown
# Technique Reference from "A Bug Bounty Hunting Journey"

## Overview
"A Bug Bounty Hunting Journey" provides insights into the world of ethical hacking through bug bounty programs, focusing on the methodologies and techniques used to identify vulnerabilities in web applications. The book emphasizes practical approaches that leverage both automated tools and manual testing techniques, bridging the gap between theory and real-world application.

## Techniques & Vulnerability Classes

### Account Enumeration
- **Idea**: Identifying valid usernames based on differences in response messages during login attempts.
- **Where it Applies**: Authentication flow of web applications.
- **How to Find & Test**: Analyze response messages for discrepancies between valid and invalid usernames.
- **Proof-of-Impact Approach**: Document differences in error messages to demonstrate enumeration risk.
- **Impact & CWE**: Medium severity; CWE-203: Information Exposure Through Discrepancy.
- **Remediation**: Implement generic error messages to reduce information leakage.

### SMS Spamming
- **Idea**: Exploiting SMS functionalities to send unsolicited messages.
- **Where it Applies**: SMS-related features in web applications.
- **How to Find & Test**: Monitor HTTP requests for phone number manipulation and observe SMS behavior.
- **Proof-of-Impact Approach**: Alter fields to demonstrate unsolicited SMS being sent.
- **Impact & CWE**: Medium severity; CWE-20: Improper Input Validation.
- **Remediation**: Implement rate limiting on SMS functionalities.

### Reflected XSS (Cross-Site Scripting)
- **Idea**: Injecting scripts in user inputs to manipulate application outputs.
- **Where it Applies**: Web application inputs and outputs.
- **How to Find & Test**: Check for reflected inputs in HTTP responses.
- **Proof-of-Impact Approach**: Trigger a benign JavaScript alert to show exploitation.
- **Impact & CWE**: High severity; CWE-79: Improper Neutralization of Input During Web Page Generation.
- **Remediation**: Sanitize and encode user inputs.

### Client-Side Template Injection
- **Idea**: Injecting JavaScript into front-end frameworks.
- **Where it Applies**: Frameworks like AngularJS that use client-side templates.
- **How to Find & Test**: Manipulate user input that is embedded in templates.
- **Proof-of-Impact Approach**: Demonstrate a script execution through template manipulation.
- **Impact & CWE**: High severity; CWE-20: Improper Input Validation.
- **Remediation**: Validate and sanitize all user inputs.

### SQL Injection
- **Idea**: Injecting SQL commands through user inputs or API endpoints.
- **Where it Applies**: Web application APIs (e.g., `/api/accounts/`).
- **How to Find & Test**: Check unsanitized user inputs in SQL queries.
- **Proof-of-Impact Approach**: Manipulate a parameter to extract data from the database.
- **Impact & CWE**: High impact; CWE-89: SQL Injection.
- **Remediation**: Use parameterized queries and input validation.

### CSRF (Cross-Site Request Forgery)
- **Idea**: Allowing unauthorized actions on behalf of a user through unprotected endpoints.
- **Where it Applies**: Web applications lacking anti-CSRF tokens.
- **How to Find & Test**: Test features without CSRF protections.
- **Proof-of-Impact Approach**: Execute actions using crafted requests that leverage the absence of protections.
- **Impact & CWE**: High severity; CWE-352: Cross-Site Request Forgery.
- **Remediation**: Implement anti-CSRF tokens for all state-changing requests.

### CORS Misconfiguration
- **Idea**: Misconfigured CORS settings allowing unauthorized resource access.
- **Where it Applies**: Microservices and APIs with lax CORS policies.
- **How to Find & Test**: Check HTTP response headers for misconfigured CORS settings.
- **Proof-of-Impact Approach**: Demonstrate unauthorized access to resources.
- **Impact & CWE**: Medium severity; CWE-693: CORS Misconfiguration.
- **Remediation**: Enforce strict CORS policies across all API endpoints.

## Recon & Methodology
- **Workflow**: Start with comprehensive reconnaissance (subdomain enumeration, feature exploration) before testing for vulnerabilities.
- **Enumeration**: Use tools (e.g., amass, recon-ng) to map the target’s attack surface.
- **Automation Tips**: Use scripts to automate repetitive tasks, allowing more time for manual testing.

## Tooling
- **Burp Suite**: Intercept and analyze HTTP requests, test for vulnerabilities.
- **OWASP ZAP**: Security scanner for web applications.
- **amass**: Subdomain enumeration tool.
- **Recon-ng**: Framework for information gathering, automates common checks.
- **Foca**: Analyzes file metadata for sensitive information.
- **Nmap**: Scans live services and identifies open ports.
- **Wfuzz/ffuf**: Tools for directory brute-forcing.
- **TheHarvester**: Gathers emails, subdomains, public information.
- **grep**: Searches source code for specific patterns like SQL queries.
- **Google Dorking**: For reconnaissance via search engine queries.

## Reporting & Disclosure
The book frames reporting in a structured way that emphasizes clarity and thoroughness, ensuring all findings are documented with potential impacts and suggested remediations. Ethical considerations are highlighted, stressing the need for responsible disclosure practices to protect users and organizations.

## Transferable Takeaways
- Focus on minimizing information exposure (e.g., generic error responses).
- Always validate and sanitize user inputs to prevent various injection attacks.
- Pay attention to authentication flows for account enumeration vulnerabilities.
- Implement rigorous testing methodologies to avoid common pitfalls.
- Acknowledge the importance of ongoing learning and adaptation as security landscapes evolve.
- Some techniques may become outdated; continuously refine your toolkit and methodologies based on recent findings and emerging technologies.
```
