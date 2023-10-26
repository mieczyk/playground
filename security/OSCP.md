# Advanced Penetration Testing for Highly-Secured Environments
## 1. Penetration Testing Essentials
- The essential element of penetration testing is planning.
- Example of a *penetration testing framework*:
	1. Pre-site Inspection Checklist:
		1. **Introduction** - the essential part of this step is to get the **written authorization** for further testing. Ethical hackers always have got a proper authorization.
		2. **Accreditation status** - type of the test (e.g. full tests).
		3. **Scope** - very important part as it determines our penetration testing methodology.
			1. **Compliance** - is the target compliant with given standards and regulations.
			2. **Vulnerability assesment** - finding potential vulnerabilities that can be exploited in the penetration testing phase.
			3. **Penetration testing** - black/gray/white box testing. At this point we should have all required data gathered and make sure that we understand the scope of the work.
	2. **Network footprinting** - active (will probably detected by IDS/IPS) and passive. 
		1. https://centralops.net/co/ - online tools for passive reconnaissance. For example: *Domain Dossier* and *Email Dossier*.
	3. **Input validation** - have a list of possible input entries with information what output can be expected from each. ![[input_validation_checks.png]]
	4. Setting up a **bind/reverse shell**.
	5. Selecting a proper tool for attacked application/server (e.g. wpscan for WordPress). The tools' selection is based on your findings. It's obligatory to have a full checklist, what we're going to check exactly.
- [Penetration Testing Execution Standard (PTES)](http://www.pentest-standard.org/index.php/Main_Page) - provides technical procedures that can be used during penetration testing.
	- **Pre-engagement interactions** - determining a testing scope is crucial.
	- **Intelligence gathering** - ...
	- [Technical Guide](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines) - when we combine this supplement's info with the standard, we've got a comprehensive plan for penetration testing.

---
TODO:
- Next page: 12
- Read and take notes:  [What Is a Pentest Framework? Top 7 Frameworks Explained](https://www.esecurityplanet.com/networks/pentest-framework/).
- Review the tools available on the centralops.net. Learn how to use them!