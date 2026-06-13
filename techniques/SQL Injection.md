# SQL Injection

_Aggregated from **8** book(s) on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf. For AUTHORIZED testing + responsible disclosure._

**Books:** A bug bounty hunting journey, Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards, Bug Bounty Field Manual, Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I, Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi, Corporate Cybersecurity Identifying Risks and the Bug Bounty Program, Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen, [Journal of Database Management 2020-jan vol. 31 iss. 1] Bug Bounty Ma

---

## How the shelf describes it

### A bug bounty hunting journey

- **Idea**: Injecting SQL commands through user inputs or API endpoints.
- **Where it Applies**: Web application APIs (e.g., `/api/accounts/`).
- **How to Find & Test**: Check unsanitized user inputs in SQL queries.
- **Proof-of-Impact Approach**: Manipulate a parameter to extract data from the database.
- **Impact & CWE**: High impact; CWE-89: SQL Injection.
- **Remediation**: Use parameterized queries and input validation.

### Bug Bounty Decoded Unraveling the Mysteries of Ethical Hacking Rewards — as "SQL Injection (SQLi)"

- **Idea**: Manipulating input fields to execute unintended SQL queries.
- **Where it Applies**: Input fields in web applications.
- **How to Find & Test**: Look for input fields that accept unvalidated data; append SQL keywords to test for vulnerabilities.
- **Proof-of-Impact Approach**: Demonstrate unauthorized data retrieval using benign queries.
- **Impact & CWE**: High impact (CWE-89), could lead to complete database compromise.
- **Remediation**: Implement parameterized queries and input validation.

### Bug Bounty Field Manual

- **Idea**: Exploiting application vulnerabilities to execute arbitrary SQL commands.
- **Where it Applies**: Web applications with improperly sanitized user inputs.
- **How to Find & Test**: Use payloads like `' OR 1=1 --` to test input fields.
- **Proof-of-Impact Approach**: Demonstrate data extraction without causing alterations (e.g., retrieving user count).
- **Impact & CWE**: Can lead to unauthorized data access; CWE-89.
- **Remediation**: Implement prepared statements and parameterized queries.

### Bug Bounty from Scratch A comprehensive guide to discovering vulnerabi — as "SQL Injection (SQLi)"

- **Idea**: Input manipulation to execute unauthorized SQL commands.
- **CWE**: CWE-89.
- **Where It Lives**: Web applications with database interaction.
- **How to Find & Test**: Look for error messages or abnormal response times.
- **Proof-of-Impact Approach**: Use crafted queries to demonstrate potential data retrieval.
- **Impact & Severity**: High; risks data exposure.
- **Remediation**: Validate inputs and use prepared statements.

### Bug Bounty Hunting For Web Security Find And Exploit Vulnerabilities I — as "SQL Injection (SQLi)"

- **Idea**: Manipulating SQL queries through input fields, allowing unauthorized data access.
- **Where It Lives**: Database query interfaces.
- **How to Find & Test**: Check for error messages and test with SQL syntax characters (e.g., `'`).
- **Proof-of-Impact Approach**: Use crafted SQL payloads to reveal sensitive data via unauthorized queries.
- **Impact & CWE**: High severity risk of data breach (CWE-89).
- **Remediation**: Implement parameterized queries and rigorous input validation.

### Corporate Cybersecurity Identifying Risks and the Bug Bounty Program

- **Idea**: Manipulating SQL queries via input fields to retrieve or alter database data.
- **Where It Applies**: Web application input fields (e.g., forms).
- **How to Find & Test**: Look for inputs that return errors upon injection.
- **Proof-of-Impact Approach**: Demonstrate retrieving data from a crafted query.
- **Impact & CWE**: High severity, potential for data breaches; CWE-89.
- **Remediation**: Implement parameterized queries and stringent input validation.

### Enumerating Esoteric Attack Surfaces Recon for Bug Bounty Hunters, Pen — as "NoSQL Injection"

- **Idea**: Exploiting NoSQL databases through user inputs.
- **Where it Lives**: Open ports on servers (e.g., MongoDB on port 27017).
- **How to FIND/TEST it**: Use `nmap` or `masscan` for open port scanning.
- **Proof-of-Impact Approach**: Access sensitive data without compromising the target.
- **Impact & CWE**: High severity; can lead to data breaches.
- **Remediation**: Close unnecessary ports and implement authentication.

### [Journal of Database Management 2020-jan vol. 31 iss. 1] Bug Bounty Ma

- **Idea**: Manipulation of SQL queries through user inputs.
- **Where it Applies**: Any web application interfacing with a database without adequate input sanitization.
- **How to Find & Test**: Use common SQL payloads in input fields to observe error messages or altered application behavior.
- **Proof-of-Impact Approach**: Query the database for read-only actions (e.g., version number) to show data leakage without altering it.
- **Impact & CWE**: Can allow unauthorized access to sensitive data; relates to CWE-89.
- **Remediation**: Utilize parameterized queries and ORM frameworks.

---
_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, write it up with `bbkit.report`._