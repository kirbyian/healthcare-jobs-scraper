A Python-based pipeline that automates scraping of healthcare job listings from multiple Irish job-boards and hospital portals.
Extracts key metadata, stores to a database or Excel/CSV, and generates reports for recruiter pipelines.

What It Does

Scrapes targeted websites (job-boards, hospital careers portals) for healthcare roles in Ireland.

Extracts fields such as job title, location, posting date, closing date, link, hospital/trust, role type.

Persists data in a relational database (config via db_connector.py) and optionally writes to Excel/CSV (job_data.xlsx).

Sends email summary reports (email_report.py) for new or closed positions.

Requirements
pip install python-dotenv
pip install beautifulsoup4 openpyxl


(See readme.txt for full list.) 
GitHub

Setup & Usage

Clone the repo.

Create a .env file with database credentials, email SMTP config, target URLs.

Run the appropriate parser script:

python public_jobs_parser.py
python hospital_parser_util.py
# etc


Review output in job_data.xlsx or query the database for ingestion into downstream systems.

Structure

candidate_manager_parser.py: parses internal candidate-management site postings.

hospital_parser_util.py, saolta_parser.py, mater_parser.py: specialized parsers for different hospitals/trusts.

email_report.py: builds and sends email summary reports.

db_connector.py: database connectivity and insertion logic.

