# Scraper "PW Scraper"

## Description

**PW Scraper** is a Scrapy-based project designed to scrape the website of [Warsaw University of Technology (PW)](https://repo.pw.edu.pl). It automatically retrieves details about:

- Scientists and their profiles
- Scientific publications
- Organizational structure of the university


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

- Python 3.8 or higher.
- Installed dependencies listed in [`requirements.txt`](https://github.com/IO-Lab2/PW-Scraper/blob/dev/requirements.txt):
- `scrapy`
- `scrapy-playwright`
- `playwright`
- `gitdb==4.0.11`
- `GitPython==3.1.41`
- `psycopg`
- `setuptools==69.0.3`
- `smmap==5.0.1`

- PostgreSQL as the database for storing results.

---

## Usage

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. **Run the scraper:**

In the main directory of the Scrapy project, where the `scrapy.cfg` file is located, run the following command in the terminal:

```bash
scrapy crawl pw_spider
```

## Files and Modules

### Directory Structure


```
.
├── .devcontainer/                   # Development environment configuration
│   ├── Dockerfile                   # Dockerfile for the container
│   ├── devcontainer.json            # Configuration file for the dev container
│   └── docker-compose.yml           # Docker Compose configuration
├── .github/                         # GitHub Actions configuration
│   └── dependabot.yml               # Dependabot configuration for dependency updates
├── .vscode/                         # Visual Studio Code configuration
│   └── launch.json                  # Debugger configuration
├── pw_scraper/                      # Main project folder
│   ├── __pycache__/                 # Auto-generated Python cache files
│   │   ├── __init__.cpython-313.pyc
│   │   ├── items.cpython-313.pyc
│   │   ├── middlewares.cpython-313.pyc
│   │   ├── pipelines.cpython-313.pyc
│   │   └── settings.cpython-313.pyc
│   ├── spiders/                     # Spiders folder
│   │   ├── __pycache__/             # Cache files for spiders
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── publications.cpython-313.pyc
│   │   │   └── pw_spider.cpython-313.pyc
│   │   ├── __init__.py              # Initialization file for spiders
│   │   ├── pw_spider.py             # Main spider for scraping scientists
│   │   └── publications.py          # Spider for scraping publication data
│   ├── items.py                     # Data model definitions
│   ├── middlewares.py               # Middleware configurations
│   ├── pipelines.py                 # Data processing and saving pipelines
│   ├── settings.py                  # Scrapy and Playwright settings
├── .gitignore                       # Git ignore file
├── app.py                           # Main application for running Scrapy
├── links.json                       # Empty data file for links
├── organisation.json                # Results about organizational structure
├── personalData.json                # Data about scientists
├── pub.json                         # Data about publications
├── requirements.txt                 # List of dependencies
├── scrapy.cfg                       # Scrapy configuration file
├── scrapy_errors.log                # Log file for scraping errors (currently empty)
└── README.MD                        # Project documentation
```

### Main Files

- **[`settings.py`](https://github.com/IO-Lab2/PW-Scraper/blob/dev/pw_scraper/settings.py)**:
  The Scrapy settings configure how the scraper operates. It uses Playwright to handle JavaScript-heavy pages, 
  supports retries for failed requests, and logs activities to scrapy_errors.log. Custom pipelines and middlewares 
  process and save data, with database integration for storing scraped results. 
  The configuration also enables AutoThrottle for managing request rates dynamically.

- **[`items.py`](https://github.com/IO-Lab2/PW-Scraper/blob/dev/pw_scraper/items.py)**:
  Defines data models for the project, such as:
  - `ScientistItem`: Stores information about scientists (name, email, academic title, etc.).
  - `PublicationItem`: Stores details about publications (title, journal, publisher, etc.).

- **[`pipelines.py`](https://github.com/IO-Lab2/PW-Scraper/blob/dev/pw_scraper/pipelines.py)**:
This code cleans, saves, and organizes scraped data. The CleanItemsPipeline removes extra spaces and normalizes text fields. 
The pw_scraperPipeline saves data into JSON files, organizing it by type (e.g., scientists or organizations). 
Finally, the DatabasePipeline connects to a PostgreSQL database and updates or adds records for scientists, publications, 
and organizations, maintaining relationships between them.

- **[`pw_spider.py`](https://github.com/IO-Lab2/PW-Scraper/blob/dev/pw_scraper/spiders/pw_spider.py)**:
  Main spider scrapes the Warsaw University of Technology repository to collect data on scientists 
  and organizational structures. It retrieves and processes hierarchical organization data, scientist profiles 
  (name, email, titles, research areas), 
  and bibliometric metrics (h-index, publication count).

- **[`publications.py`](https://github.com/IO-Lab2/PW-Scraper/blob/dev/pw_scraper/spiders/publications.py)**:
  The PublicationsSpider scrapes publication data from the Warsaw University of Technology repository. 
  It uses Playwright to navigate JavaScript-heavy pages, extracts details like title, authors, journal, 
  and scores, and handles paginated results efficiently.

---

## Sample Output

Example data extracted by the scraper is stored in `organisation.json`:

```json
[
  {
    "university": "Warsaw University of Technology",
    "institute": "Faculty of Electronics and Information Technology",
    "cathedras": []
  },
  {
    "university": "Warsaw University of Technology",
    "institute": "Faculty of Mechanical and Industrial Engineering",
    "cathedras": []
  }
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
