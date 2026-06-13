# Bug Bounty Knowledge — Index

AI-extracted technique references from **12 bug-bounty / web-security books** (model `gpt-4o-mini`). For AUTHORIZED testing + responsible disclosure. Each links to its full notes in `books/`.

## Books
- **[A bug bounty hunting journey](books/a-bug-bounty-hunting-journey-0fed.md)** — 7 techniques: Account Enumeration, SMS Spamming, Reflected XSS (Cross-Site Scripting), Client-Side Template Injection, SQL Injection, CSRF (Cross-Site Request Forgery), CORS Misconfiguration
- **[Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards](books/bug-bounty-decoded-unraveling-the-mysteries-of-eth-4a75.md)** — 7 techniques: SQL Injection (SQLi), Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Broken Authentication, Sensible Data Exposure, Security Misconfigurations, Broken Access Control
- **[Bug Bounty Field Manual](books/bug-bounty-field-manual-b80e.md)** — 4 techniques: SQL Injection, Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Server-Side Request Forgery (SSRF)
- **[Bug Bounty from Scratch A comprehensive guide to discovering vulnerabilities and succeeding in c...](books/bug-bounty-from-scratch-a-comprehensive-guide-to-d-2db4.md)** — 7 techniques: Business Logic Flaws, Advanced Persistent Threats (APT), Code Injection Attacks, Cross-Site Scripting (XSS), SQL Injection (SQLi), Directory Enumeration, Insecure Direct Object Reference (IDOR)
- **[Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities In Web Sites And Applications](books/bug-bounty-hunting-for-web-security-find-and-explo-16f6.md)** — 9 techniques: Cross-Site Scripting (XSS), SQL Injection (SQLi), Cross-Site Request Forgery (CSRF), Command Injection, File Upload Vulnerability, Header Injection, URL Redirection, XML External Entity (XXE) Injection …
- **[Bug Bounty Playbook v1](books/bug-bounty-playbook-v1-5b36.md)** — 8 techniques: Hard-Coded Credentials, Misconfigured Storage Buckets, Open Ports/Services, XML External Entity Injection (XXE), Cross-Site Scripting (XSS), Server-Side Request Forgery (SSRF), Cross-Site Request Forgery (CSRF), Unauthenticated API Access
- **[Corporate Cybersecurity Identifying Risks and the Bug Bounty Program](books/corporate-cybersecurity-identifying-risks-and-the-2001.md)** — 8 techniques: Denial of Service (DoS) / Distributed Denial of Service (DDoS), Social Engineering Attacks, Brute Force Attacks, Account and Email Enumeration, Clickjacking, SQL Injection, Open Redirect, Directory Traversal
- **[Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Penetration Testers and OSINT Aggressors](books/enumerating-esoteric-attack-surfaces-recon-for-bug-69e2.md)** — 8 techniques: Horizontal Domain Enumeration, CIDR Enumeration, Origin IP Disclosure, NoSQL Injection, Dorks, Secrets Exposure, Certificate Transparency Monitoring, Content Security Policy (CSP) Misconfigurations
- **[[Journal of Database Management 2020-jan vol. 31 iss. 1] Bug Bounty Marketplaces and Enabling Responsible Vulnerability Disclosure{Subramanian, Hemang Chamakuzhi_ Malladi, Suresh}(2020 January)[10.4018_JDM.2020010103]{85229289} libgen.li](books/journal-of-database-management-2020-jan-vol-31-iss-6658.md)** — 2 techniques: Cross-Site Scripting (XSS), SQL Injection
- **[My First Bug Bounty](books/my-first-bug-bounty-08c6.md)** — 8 techniques: CORS Misconfiguration, Open Redirection, CRLF Injection, CSRF, Server-Side Request Forgery (SSRF), Weak Cipher, Missing Security Headers, Content Security Policy Not Implemented
- **[Redefining Hacking A Comprehensive Guide to Red Teaming and Bug Bounty Hunting in an AI-driven World](books/redefining-hacking-a-comprehensive-guide-to-red-te-adc6.md)** — 13 techniques: Phishing via Man-in-the-Middle (MitM), RFID Badge Cloning, Physical Bypass Techniques, Credential Harvesting, Local Privilege Escalation, Network-based Privilege Escalation, Web Shells, Command and Control (C2) Channels …
- **[The secret of bug hunting. Bug bounty automation with python](books/the-secret-of-bug-hunting-bug-bounty-automation-wi-80f0.md)** — 5 techniques: Sensitive Data Exposure, Debug Mode Exposure, Misconfigured Jenkins Instances, Default Credentials in SonarQube, S3 Bucket Exposure

---

# Cross-Book Synthesis on Bug Bounty Techniques

## Vulnerability Classes that RECUR Across the Shelf
| Vulnerability Class                  | Books That Agree                                                                 |
|-------------------------------------|----------------------------------------------------------------------------------|
| Cross-Site Scripting (XSS)          | "A Bug Bounty Hunting Journey", "Bug Bounty Decoded", "Bug Bounty Field Manual", "Bug Bounty from Scratch", "Bug Bounty Hunting For Web Security", "Bug Bounty Playbook v1", "My First Bug Bounty", "Redefining Hacking"                              |
| SQL Injection (SQLi)                | "A Bug Bounty Hunting Journey", "Bug Bounty Decoded", "Bug Bounty Field Manual", "Bug Bounty from Scratch", "Bug Bounty Hunting For Web Security", "Corporate Cybersecurity", "Journal of Database Management"                               |
| Cross-Site Request Forgery (CSRF)   | "A Bug Bounty Hunting Journey", "Bug Bounty Decoded", "Bug Bounty Field Manual", "Bug Bounty Hunting For Web Security", "Bug Bounty Playbook v1", "My First Bug Bounty"                                                            |
| Server-Side Request Forgery (SSRF)  | "Bug Bounty Field Manual", "Bug Bounty Hunting For Web Security", "Bug Bounty Playbook v1", "My First Bug Bounty"                                                                                                 |
| Insecure Direct Object Reference (IDOR) | "Bug Bounty from Scratch"                                                                                                    |
| XML External Entity (XXE)           | "Bug Bounty Hunting For Web Security", "Bug Bounty Playbook v1"                                                               |
| CORS Misconfiguration                | "A Bug Bounty Hunting Journey", "My First Bug Bounty"                                                                         |
| Security Misconfigurations           | "Bug Bounty Decoded", "Corporate Cybersecurity"                                                                                |
| Access Control / Broken Authentication| "Bug Bounty Decoded", "Bug Bounty Field Manual"                                                                               |
| Open Redirection                    | "My First Bug Bounty"                                                        |

## Distinctive or Advanced Techniques
- **Business Logic Flaws**: "Bug Bounty from Scratch"
- **Debug Mode Exposure**: "The Secret of Bug Hunting"
- **Horizontal Domain Enumeration**: "Enumerating Esoteric Attack Surfaces"
- **NoSQL Injection**: "Enumerating Esoteric Attack Surfaces"
- **S3 Bucket Exposure**: "The Secret of Bug Hunting"
- **Phishing via Man-in-the-Middle (MitM)**: "Redefining Hacking"

## Which Book to Read for What
- **Recon**: "Enumerating Esoteric Attack Surfaces" – Advanced reconnaissance techniques.
- **Web Vulnerabilities**: "Bug Bounty from Scratch" – Comprehensive guide on common and advanced web vulnerabilities.
- **Reporting**: "Bug Bounty Field Manual" – Structured approach for documenting findings responsibly.
- **Automation**: "The Secret of Bug Hunting" – Leverages Python for bug bounty automation.

## Responsible-Use Note
These notes are for **AUTHORIZED testing only** within specified scope. Always adhere to responsible disclosure practices. This document serves strictly educational purposes, not as instructions for weaponized exploits. Verify findings against current behavior before acting.
