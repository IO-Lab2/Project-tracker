# Scraper "PB Scraper"

## Description

**PB Scraper** is a Scrapy-based project designed to scrape the website of [Bialystok University of Technology](https://bazawiedzy.pb.edu.pl). It automatically retrieves details about:

- Scientists and their profiles, including bibliometric indicators and associated organizations.
- Scientific publications, including titles, journals, and authorship.
- Organizational structure of the university, including faculties, institutes, and departments in a hierarchical format.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Usage](#usage)
3. [Files and Modules](#files-and-modules)
   - [Directory Structure](#directory-structure)
   - [Main Files](#main-files)
4. [Sample Output](#sample-output)
5. [Notes and Limitations](#notes-and-limitations)

---
## Requirements

- **Python 3.8 or higher.**
- Installed dependencies listed in [`requirements.txt`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/requirements.txt):
  - `attrs==24.2.0`
  - `Automat==24.8.1`
  - `certifi==2024.8.30`
  - `cffi==1.17.1`
  - `charset-normalizer==3.4.0`
  - `constantly==23.10.4`
  - `cryptography==43.0.3`
  - `cssselect==1.2.0`
  - `defusedxml==0.7.1`
  - `filelock==3.16.1`
  - `greenlet==3.1.1`
  - `hyperlink==21.0.0`
  - `idna==3.10`
  - `incremental==24.7.2`
  - `itemadapter==0.9.0`
  - `itemloaders==1.3.2`
  - `jmespath==1.0.1`
  - `lxml==5.3.0`
  - `packaging==24.2`
  - `parsel==1.9.1`
  - `playwright==1.49.0`
  - `Protego==0.3.1`
  - `psycopg2==2.9.10`
  - `pyasn1==0.6.1`
  - `pyasn1_modules==0.4.1`
  - `pycparser==2.22`
  - `PyDispatcher==2.0.7`
  - `pyee==12.0.0`
  - `pyOpenSSL==24.2.1`
  - `python-dotenv==1.0.1`
  - `queuelib==1.7.0`
  - `requests==2.32.3`
  - `requests-file==2.1.0`
  - `Scrapy==2.12.0`
  - `scrapy-playwright==0.0.42`
  - `service-identity==24.2.0`
  - `setuptools==75.6.0`
  - `tldextract==5.1.3`
  - `Twisted==24.10.0`
  - `typing_extensions==4.12.2`
  - `urllib3==2.2.3`
  - `w3lib==2.2.1`
  - `zope.interface==7.1.1`

- **PostgreSQL** as the database for storing results.

---


## Usage

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   playwright install

2. **Run the scraper:**

In the main directory of the Scrapy project, where the `scrapy.cfg` file is located, run the following command in the terminal:

```bash
scrapy crawl pb_spider
```

## Files and Modules

### Directory Structure
```
.
├── docs/                         # Documentation and examples
│   ├── example_log.log           # Example log file capturing scraper activities
│   ├── example_output.json       # Sample output of scraped data in JSON format
│   └── jak.txt                   # Additional notes for the scraper
├── scraper/                      # Source code directory containing the main project files
│   ├── knowledge_scraper/        # Scrapy project files
│   │   ├── spiders/              # Spiders folder
│   │   │   ├── __init__.py       # Initialization file for spiders module
│   │   │   ├── pb_spider.py      # Main spider for scraping organizations, scientists, and publications
│   │   ├── __init__.py           # Initialization file for the `knowledge_scraper` package
│   │   ├── items.py              # Data models for Scrapy items
│   │   ├── middlewares.py        # Middleware configurations for custom processing of requests and responses
│   │   ├── pipelines.py          # Handles data validation, cleaning, and storage into the database
│   │   └── settings.py           # Scrapy settings and configurations for the project
│   ├── other/                    # Miscellaneous helper files
│   │   ├── __init__.py           # Initialization file for the `other` package
│   │   ├── expand_organizations.js  # JavaScript utility for expanding hierarchical organizational structures
│   │   └── read_js.py            # Python script to interact with JavaScript files or outputs
│   ├── scripts/                  # Specialized helper modules for database and scraping logic
│   │   ├── database/             # Database-related scripts
│   │   │   ├── __init__.py       # Initialization file for the `database` package
│   │   │   ├── data_manipulation.py  # Utilities for inserting or updating rows in the database
│   │   │   ├── data_query.py     # Functions for querying database records
│   │   │   └── database.py       # Database connection setup and environment variable loading
│   │   ├── pb/                   # PB-specific utility scripts
│   │   │   ├── __init__.py       # Initialization file for the `pb` package
│   │   │   ├── misc.py           # Miscellaneous helper functions for PB-specific tasks
│   │   │   ├── urls.py           # Functions for handling and modifying URLs
│   │   └── playwright.py         # Helper script for managing Playwright interactions
│   ├── utils/                    # General-purpose utility modules
│   │   ├── __init__.py           # Initialization file for the `utils` package
│   │   ├── basic_conversion.py   # Functions for data type conversion and transformations
│   │   ├── basic_validation.py   # Functions for validating data during processing
│   │   ├── log_messages.py       # Logging utilities for consistent log formatting
│   │   └── misc.py               # General helper functions used across the project
│   ├── constants.py              # Repository-wide constants and settings
│   └── scrapy.cfg                # Scrapy configuration file defining the project settings
├── README.md                     # Project documentation
└── requirements.txt              # List of Python dependencies for the project
```


### Main Files

- **[`settings.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/knowledge_scraper/settings.py)**:  
  Configures Scrapy's behavior, including settings for Playwright, request handling, logging, and middleware. It enables retries, handles JavaScript-heavy pages, and integrates with custom pipelines and middlewares for data processing and storage.

- **[`items.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/knowledge_scraper/items.py)**:  
  Defines data models for the scraper, including:
  - `ScientistItem`: Captures data about scientists (name, email, academic title, etc.).
  - `PublicationItem`: Stores publication details (title, journal, publisher, etc.).
  - `OrganizationItem`: Represents the hierarchical structure of organizations.
  - `BibliometricsItem`: Tracks metrics such as h-index and publication count.

- **[`pipelines.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/knowledge_scraper/pipelines.py)**:  
  Processes, validates, and stores scraped data. It uses custom validation rules for scientists, publications, and organizations.

- **[`pb_spider.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/knowledge_scraper/spiders/pb_spider.py)**:  
  The main spider that scrapes organizational data, scientist profiles, and publications. It handles hierarchical data extraction, navigates between related pages.

- **[`expand_organizations.js`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/other/expand_organizations.js)**:  
  A JavaScript utility for expanding hierarchical structures on organization pages, allowing the scraper to navigate through nested organizational data.

- **[`database.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/scripts/database/database.py)**:  
  Manages database connections using environment variables. It provides helper functions to establish and validate connections for data storage.

- **[`data_manipulation.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/scripts/database/data_manipulation.py)**:  
  Contains utilities for inserting or updating rows in the database. It ensures data consistency by checking for existing entries before performing updates.

- **[`playwright.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/scripts/playwright.py)**:  
  Handles interactions with Playwright for managing JavaScript-heavy pages. It optimizes the scraping process by aborting unnecessary requests, such as images or media.

- **[`constants.py`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/scraper/constants.py)**:  
  Defines constants and global variables used across the project, ensuring consistency and central management of settings like URLs and database keys.


---

## Sample Output

Example data extracted by the scraper is stored in [`example_output.json`](https://github.com/IO-Lab2/PB-Scraper/blob/dev/docs/exaple_output.json). Below is a sample of organizational data:

```json
[
{"parent_id": null, "name": "Bialystok University of Technology", "organization_type": "university", "identifier": "66fa4ac3-2912-59b2-a12c-899d930f5ea1"},
{"parent_id": "66fa4ac3-2912-59b2-a12c-899d930f5ea1", "name": "Faculty of Architecture", "organization_type": "institute", "identifier": "d1bcc91a-7af2-5701-af19-261817da1f93"},
{"parent_id": "d1bcc91a-7af2-5701-af19-261817da1f93", "name": "Institute of Architecture and Town Planning", "organization_type": "institute", "identifier": "74d112dd-0136-5dd2-8647-f58c891cbcd3"}
]
```

---

## Notes and Limitations

1. **JavaScript Handling:**
   The service requires JavaScript support, necessitating the use of Playwright.

2. **Performance**:  
   For large datasets or websites with complex structures, the scraping process may take longer.

3. **Database Dependency**:  
   The project relies on a PostgreSQL database for storing scraped data. Ensure the database is correctly configured and accessible before running the scraper.

4. **Data Validation**:  
   Some scraped fields may be incomplete or empty (e.g.journal details). The pipeline handles basic cleaning, but manual verification of critical data might be required.
---
