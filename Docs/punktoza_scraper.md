# Scraper "Punktoza"

## Description

**Punktoza** is a Scrapy-based project that scrapes [punktoza.pl](https://punktoza.pl), automatically retrieving details about scientific journals, including:

- Journal name
- Impact Factor points
- Publisher
- Journal type

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
- Instaled Scrapy and Playwright
- PostgreSQL as the database for storing results.

---

## Usage

1. **Install dependencies:**

   ```bash
   pip install scrapy scrapy-playwright python-dotenv psycopg
   playwright install

   ```

2. **Run the scraper:**

In the main directory of the Scrapy project,
which is where the [`scrapy.cfg`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/scrapy.cfg) file is located run the following command by terminal:

```bash
scrapy crawl punktoza_spider
```

---

## Files and Modules

### Directory Structure

```
punktoza/
├── punktoza/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── punktoza_spider.py
├── scrapy.cfg
├── .env.example
├── example_output.json
└── .gitignore
```

### Main Files

- [`settings.py`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/punktoza/settings.py): Scrapy configuration, including Playwright integration, connection limits, and logging.
- [`items.py`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/punktoza/items.py): Defines the data model used by the scraper.
- [`middlewares.py`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/punktoza/middlewares.py): Middleware configuration and customizations for the scraper.
- [`pipelines.py`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/punktoza/pipelines.py): Processing and storing the collected data in a PostgreSQL database.
- [`punktoza_spider.py`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/punktoza/spiders/punktoza_spider.py): Main scraper file handling data extraction and pagination.

---

## Sample Output

Data extracted by the scraper might look like this
[`example_output.json`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/example_output.json):

```json
[
  { "Publication_name": "Academy of Management Annals", "IF_points": "14.3" },
  { "Publication_name": "Academy of Management Journal", "IF_points": "9.5" },
  { "Publication_name": "Academy of Management Review", "IF_points": "19.3" },
  { "Publication_name": "Accounting Review", "IF_points": "4.4" }
]
```

---

## Notes and Limitations

1. **JavaScript Handling:**
   The service requires JavaScript support, necessitating the use of Playwright.
2. **Performance:**
   For large tables, execution time may be lengthy. Adjust the number of concurrent connections in [`settings.py`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/punktoza/settings.py) if needed.
3. **Missing Data:**
   Some fields might be empty (e.g., `publisher`). The scraper handles such cases through validation in [`pipelines.py`](https://github.com/IO-Lab2/Scraper/blob/punktoza_scraper/punktoza/pipelines.py).

---
