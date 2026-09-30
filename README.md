# APTF — Automated Penetration Testing Framework

APTF (Automated Penetration Testing Framework) is a Python-based security automation framework developed as a Bachelor of Computer Applications (BCA) major project.

The framework automates multiple stages of authorized security reconnaissance and vulnerability assessment by combining commonly used penetration-testing tools into a single workflow. It collects information about a target, performs reconnaissance and security checks, and organizes the generated results into a structured directory.

The main goal of APTF is to reduce repetitive manual work during security assessments and provide a centralized workflow for reconnaissance and vulnerability analysis.

> **Important:** APTF is intended only for educational purposes and authorized security testing.

---

## Features

- Automated subdomain enumeration
- Live host discovery
- URL and endpoint collection
- Parameter analysis using GF patterns
- Port scanning
- Directory enumeration
- Vulnerability assessment
- XSS detection workflows
- CVE detection
- Automated security-tool orchestration
- Structured result organization
- Command-line based execution

---

## Workflow

                         Target Domain
                              |
                              v
                  Subdomain Enumeration
                              |
                              v
                     Host Discovery
                              |
                              v
                      URL Collection
                              |
                              v
                    Parameter Analysis
                              |
                              v
                        Port Scan
                              |
                              v
                  Directory Enumeration
                              |
                              v
                 Vulnerability Assessment
                              |
                              v
                       Results / Reports
Technologies Used
Programming and Environment
Python
Bash
Linux
Git
Security Tools
Subfinder
Assetfinder
Amass
Chaos
AlterX
Findomain
HTTPX
HTTPProbe
GAU


The framework is designed to orchestrate multiple security tools and collect their outputs as part of a single reconnaissance and assessment workflow.

Prerequisites

Before running APTF, make sure the following are available:

Linux operating system
Kali Linux or another security-focused Linux distribution
Python 3.x
Git
Required security tools installed and available in the system PATH

Some tools used by APTF are external command-line security utilities and must be installed separately.

Installation
1. Clone the Repository
git clone https://github.com/gauravthakur06/APTF-Automated-Penetration-Testing-Framework.git
2. Enter the Project Directory
cd APTF-Automated-Penetration-Testing-Framework
3. Install Python Dependencies
pip install -r requirements.txt
4. Verify Required Security Tools

Make sure the external tools required by the framework are installed and accessible from the terminal.

For example:

nmap --version
subfinder -version
nuclei -version
Usage

Start the framework using:

python recon.py

The framework will ask for the target domain:

Enter the domain to scan:

After entering an authorized target, APTF executes the configured reconnaissance and security-assessment workflow.

Example:

[*] Enumerating subdomains...
[*] Checking for subdomain takeovers...
[*] Extracting URLs...
[*] Running GF pattern analysis...
[*] Performing port scan...
[*] Performing directory enumeration...
[*] Running vulnerability tests...
[*] Generating reports...

Only scan systems, applications, and domains for which you have explicit authorization.

Output

APTF organizes scan results into directories based on the target.

Typical results may include:

outputs/
└── target-domain/
    ├── subdomains/
    ├── extracted_urls/
    ├── gf_parameters/
    ├── port_scans/
    ├── directory_bruteforce/
    ├── xss/
    ├── cve/
    └── result/

The generated files contain information collected during the different stages of the assessment.


Project Structure
APTF-Automated-Penetration-Testing-Framework/
|
├── outputs/
|   └── Target scan results
|
├── screenshots/
|   └── Project screenshots
|
├── plugins/
|   └── Security tool integrations
|
├── recon.py
├── install.sh
├── recom.sh
├── requirements.txt
├── README.md
└── LICENSE
Project Objectives

The main objectives of APTF are:

Automate repetitive penetration-testing reconnaissance tasks.
Combine multiple security tools into a single workflow.
Reduce the need to execute individual commands manually.
Organize reconnaissance and vulnerability-assessment results.
Provide a practical learning platform for cybersecurity and security automation.
Demonstrate the use of Python for security automation.
Learning Outcomes

Through the development of APTF, the project provides practical experience with:

Python programming
Linux administration
Network reconnaissance
Web security
Vulnerability assessment
Security-tool automation
Command-line interfaces
Bash scripting
Networking concepts
Git and GitHub
Cybersecurity workflows
Future Improvements

Possible future improvements include:

Web-based reporting dashboard
Improved HTML/PDF report generation
Centralized configuration management
Scan history and result tracking
Additional security-tool integrations
Improved error handling and logging
Parallel execution of independent scanning tasks
Disclaimer

APTF has been developed for educational purposes and authorized security testing.

Do not use this framework against systems, networks, applications, or domains without explicit permission from the owner.

The author does not take responsibility for any misuse of this software.

Author

Gaurav Thakur

Bachelor of Computer Applications (BCA)
Chandigarh University

Email: gauravthakurhp06@gmail.com

GitHub: https://github.com/gauravthakur06

