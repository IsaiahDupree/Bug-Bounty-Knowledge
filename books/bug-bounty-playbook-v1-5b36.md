# Bug Bounty Playbook v1

> **AI-generated research summary** (model: `gpt-4o-mini`, map-reduce over 16 excerpts). Original study notes — vulnerability classes, techniques, and methodology extracted for AUTHORIZED testing + responsible disclosure, **not** the book's verbatim text and **not** weaponized exploits.
>
> **Source book:** Alex Thomas, Ghostlulz - Bug Bounty Playbook v1 (2019) - libgen.li.pdf

---

# Technique Reference from Bug Bounty Playbook v1

## Overview
The "Bug Bounty Playbook v1" serves as a comprehensive guide for bounty hunters, detailing various techniques to identify vulnerabilities across diverse technologies and platforms. It emphasizes a systematic approach, covering the reconnaissance phase, exploitation methods, and responsible disclosure practices.

## Techniques & Vulnerability Classes

### Hard-Coded Credentials
- **Idea**: Credentials hard-coded in source code repositories that can be exploited.
- **Where It Applies**: Source code repositories (e.g., GitHub).
- **How to Find & Test**: Search specific repositories with the company's name for hard-coded secrets.
- **Proof-of-Impact**: Demonstrate access by logging in to sensitive services using found credentials.
- **Impact & CWE**: High; CWE-798 (Use of Hardcoded Credentials).
- **Remediation**: Secure management of credentials and environment variables.

### Misconfigured Storage Buckets
- **Idea**: Publicly accessible cloud storage allowing unauthorized access to sensitive data.
- **Where It Applies**: Cloud Storage (e.g., AWS S3 buckets).
- **How to Find & Test**: Use Google Dorking and manual searches for misconfigurations.
- **Proof-of-Impact**: Access and retrieve sensitive files from exposed storage.
- **Impact & CWE**: High; CWE-552 (Content Exposure).
- **Remediation**: Implement proper access controls for storage solutions.

### Open Ports/Services
- **Idea**: Exposed services on IPs, potentially vulnerable to exploitation.
- **Where It Applies**: Web applications and IPs with open ports.
- **How to Find & Test**: Conduct port scans using tools like Nmap to identify open ports.
- **Proof-of-Impact**: Showcase potential exploitability based on identified services.
- **Impact & CWE**: Variable; CWE-200 (Information Exposure), CWE-889 (Insecure Service).
- **Remediation**: Regularly assess and minimize exposed services.

### XML External Entity Injection (XXE)
- **Idea**: Allows reading of arbitrary files on a server through malicious XML entities.
- **Where It Applies**: Applications that process XML.
- **How to Find & Test**: Inject external entities in XML submissions to retrieve sensitive files.
- **Proof-of-Impact**: Read critical files (e.g., `/etc/passwd`) through injection.
- **Impact & CWE**: High; CWE-611 (XML External Entity Reference).
- **Remediation**: Disallow external entity processing in XML parsers.

### Cross-Site Scripting (XSS)
- **Idea**: Allows execution of malicious scripts in users' browsers.
- **Where It Applies**: Web applications that render unsanitized user inputs.
- **How to Find & Test**: Identify user input fields to inject script payloads.
- **Proof-of-Impact**: Demonstrate script execution via alerts or similar methods.
- **Impact & CWE**: High; CWE-79 (Improper Neutralization of Input).
- **Remediation**: Implement input sanitization and output encoding.

### Server-Side Request Forgery (SSRF)
- **Idea**: Forces an application to make HTTP requests to internal services.
- **Where It Applies**: Applications accepting user-defined URLs.
- **How to Find & Test**: Manipulate URL inputs to access internal resources.
- **Proof-of-Impact**: Access internal application data by targeting localhost or internal services.
- **Impact & CWE**: High; CWE-918 (Server-Side Request Forgery).
- **Remediation**: Validate and sanitize URL inputs.

### Cross-Site Request Forgery (CSRF)
- **Idea**: Causes a user's browser to execute unauthorized actions.
- **Where It Applies**: Applications with authenticated state changes.
- **How to Find & Test**: Check forms lacking anti-CSRF tokens.
- **Proof-of-Impact**: Perform actions like changing user account details by tricking a user.
- **Impact & CWE**: High; CWE-352 (Cross-Site Request Forgery).
- **Remediation**: Implement anti-CSRF tokens.

### Unauthenticated API Access
- **Idea**: Exposed APIs allow unauthorized interactions.
- **Where It Applies**: Public APIs lacking authentication.
- **How to Find & Test**: Query APIs without credentials; test for access.
- **Proof-of-Impact**: Demonstrate unauthorized data retrieval.
- **Impact & CWE**: High; CWE-284 (Improper Access Control).
- **Remediation**: Secure APIs with proper authentication mechanisms.

## Recon & Methodology
- Use tools for DNS resolution and subdomain enumeration.
- Conduct automated scans with tools like Nmap and Burp Suite for known vulnerabilities.
- Utilize Google Dorks for targeted searches (e.g., for sensitive documents).
- Implement reconnaissance workflows that include asset discovery and verification.

## Tooling
- **Nmap**: Network scanning and open port identification.
- **Burp Suite**: Web application security testing, including manual and automated scanning.
- **Amass**: Asset discovery tool for subdomain enumeration.
- **GoBuster**: Directory brute-forcing tool to discover hidden endpoints.
- **Shodan**: Search engine for discovering exposed devices and services.
- **GitDumper, svn-extractor**: Tools for retrieving exposed source code.
  
## Reporting & Disclosure
The book emphasizes the importance of clear and concise reports that outline vulnerability findings, potential impact, and remediation suggestions. Ethical considerations are highlighted, urging researchers to avoid unnecessary disruption during testing and to adhere to a responsible disclosure policy.

## Transferable Takeaways
- **Vulnerability Assessment**: Regularly audit for hard-coded secrets, misconfigurations, and exposed access points.
- **Enumeration Techniques**: Use structured methodologies for asset discovery and vulnerability identification.
- **Remediation Best Practices**: Focus on secure coding practices, access controls, and regular security patches.
- **Automation**: Leverage existing tools to automate reconnaissance and testing while validating findings to reduce false positives.
