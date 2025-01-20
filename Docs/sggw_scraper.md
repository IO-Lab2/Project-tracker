# Scraper "SGGW"

## Description

**SGGW Scraper** is a Scrapy-based project designed to scrape the website of [Warsaw University of Life Sciences (SGGW)](https://bw.sggw.edu.pl). It automatically retrieves details about:

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
- Installed dependencies listed in [`requirements.txt`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/requirements.txt):
  - `scrapy`
  - `scrapy-playwright`
  - `playwright`
  - `psycopg2-binary`
  - `python-dotenv`
  - `beautifulsoup4`
- PostgreSQL as the database for storing results.

---

## Usage

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   playwright install

2. **Run the scraper:**

In the main directory of the Scrapy project,
which is where the [`scrapy.cfg`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/scrapy.cfg) file is located run the following command by terminal:
``` bash
python run_spiders.py
```
## Files and Modules

### Directory Structure

```
sggw_scraper/
├── sggwScraper/
│   ├── __pycache__/
│   │   ├── __init__.cpython-312.pyc       # Compiled initialization file
│   │   ├── items.cpython-312.pyc          # Compiled items module
│   │   ├── middlewares.cpython-312.pyc    # Compiled middlewares module
│   │   ├── pipelines.cpython-312.pyc      # Compiled pipelines module
│   │   └── settings.cpython-312.pyc       # Compiled settings module
│   ├── spiders/
│   │   ├── __pycache__/
│   │   │   ├── __init__.cpython-312.pyc   # Compiled __init__.py for spiders
│   │   │   └── sggw.cpython-312.pyc       # Compiled sggw spider
│   │   ├── __init__.py                    # Initialization file for spiders
│   │   ├── publications.py                # Spider for scraping publications
│   │   └── sggw.py                        # Spider for scientists and organizations
│   ├── __init__.py                        # Initialization file for sggwScraper
│   ├── items.py                           # Data model definitions
│   ├── middlewares.py                     # Custom middleware configurations
│   ├── pipelines.py                       # Data processing and database storage
│   ├── settings.py                        # Scrapy and Playwright configurations
├── .gitignore                             # File specifying files to ignore in version control
├── overview.json                          # Sample data for organizational structures
├── run_spiders.py                         # Script for running all spiders
├── scrapy.cfg                             # Scrapy project configuration file
├── scrapy_errors.log                      # Log file for errors encountered during scraping
├── requirements.txt                       # List of required Python libraries
└── README.md                              # Documentation for the project


```

### Main Files

- **[`settings.py`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/sggwScraper/settings.py)**:  
  Configures the Scrapy framework, including Playwright integration for handling dynamic content. This file also manages logging settings for tracking errors and events, retry mechanisms for failed requests, and throttling settings to control the rate of requests to prevent overloading the target server.pipeline customisation for PostgreSQL database validation and writing.

- **[`items.py`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/sggwScraper/items.py)**:  
  Defines data models (items) for the scraper. Key models include:
  - `ScientistItem` for storing information about scientists, such as name, title, email, and bibliometric indicators.
  - `publicationItem` for capturing details of scientific publications, such as title, journal, publisher, and publication date.
  - `organizationItem` for representing organizational structures, including universities, institutes, and departments.

- **[`pipelines.py`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/sggwScraper/pipelines.py)**:  
  Handles the processing of scraped data, including cleaning, validation, and transformation. This file also manages the integration with a PostgreSQL database, ensuring data is correctly stored and maintaining relationships between entities like scientists, publications, and organizations.

- **[`sggw.py`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/sggwScraper/spiders/sggw.py)**:  
  A spider that focuses on scraping profiles of scientists, organizational structures, and research areas from the SGGW website. It uses Playwright to handle dynamic elements and includes mechanisms for navigating multiple pages, extracting nested organizational data, and capturing bibliometric indicators.

- **[`publications.py`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/sggwScraper/spiders/publications.py)**:  
  A spider designed for collecting detailed information about scientific publications. This includes metadata such as authors, journal name, impact factor, ministerial scores, and publication dates. It processes paginated data and ensures author-publication relationships are maintained.

- **[`run_spiders.py`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/sggwScraper/run_spiders.py)**:  
  A script that sequentially executes the `sggw.py` and `publications.py` spiders. It simplifies running the entire scraping workflow by automating the execution of both spiders with a single command.

## Sample Output

Data extracted by the scraper might look like this
[`overview.json`](https://github.com/IO-Lab2/Scraper/blob/sggw_scraper/sggwScraper/overview.json):

```json
[
  {"university": "Warsaw University of Life Sciences - SGGW", "institute": "Main Library", "cathedras": []},
{"university": "Warsaw University of Life Sciences - SGGW", "institute": "Section of Science Service", "cathedras": []},
{"university": "Warsaw University of Life Sciences - SGGW", "institute": "Section of National Projects", "cathedras": []},
{"university": "Warsaw University of Life Sciences - SGGW", "institute": "Section of International Research Projects", "cathedras": []},
{"university": "Warsaw University of Life Sciences - SGGW", "institute": "Information and Technology Transfer Center", "cathedras": []},
{"university": "Warsaw University of Life Sciences - SGGW", "institute": "Doctoral School Office", "cathedras": []},
{"university": "Warsaw University of Life Sciences - SGGW", "institute": "Cellular Immunotherapy Center", "cathedras": []}
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
