# Project documentation: IO-lab2

## Description

This project is a comprehensive scientific information management system designed to improve the organization and accessibility of data about researchers, their achievements, and publications. The application integrates with the [punktoza.pl](https://punktoza.pl) website and university knowledge databases, such as:

- **[Warsaw University of Life Sciences (SGGW)](https://bw.sggw.edu.pl)**
- **[Warsaw University of Technology (PW)](https://repo.pw.edu.pl)**
- **[Bialystok University of Technology (PB)](https://bazawiedzy.pb.edu.pl)**

Thanks to filtering and comparison features, the application enables effective searching and analysis of the academic achievements of university staff.

---
## Table of Contents

1. [Description](#introduction)
2. [Functionality](#functionality)
3. [Technologies](#technologies)
   - [Front-End](#front-end)
   - [Back-End](#back-end)
   - [Web Scraper](#web-scraper)
   - [Infrastructure](#infrastructure)
4. [Installation and Usage](#installation-and-usage)
   - [Requirements](#requirements)
   - [Installation](#installation)
5. [Main Files with Links to Detailed Documentation](#main-files-with-links-to-detailed-documentation)
   - [Scrapers](#scrapers)
   - [Front-end](#front-end-1)
   - [API](#api)
   - [Stack](#stack)

---

## Functionality

1 **Filtering**:

   - By university, institute, department, position, number of publications, IF factor, ministerial points, publishers and publication dates.
   - Option to exclude researchers without publications.

2 **Compare**:

   - Simultaneous comparison of up to 10 researchers.
   - Presentation of output in the form of pie charts (ministerial points, IF, number of publications).

3. **Integration with databases**:

   - Automatic web scraping from university knowledge databases.
   - Data update every 3-10 days.

---

## Technologies

### Front-End

- **React**: Framework for building web applications.
- **Next.js**: Enhances server-side rendering and route management.
- **Tailwind CSS**: Application styling.
- **TypeScript**: Static typing in code.

### Back-End

- **Go**: Main programming language for the API.
- **PostgreSQL**: Database for storing information about researchers, publications and organisational structures.

### Web Scraper

- **Python**: Language used to scrape data.
- **Scrapy, Playwright, BeautifulSoup**: Tools for scraping dynamic web pages.

### Infrastructure

- **Docker**: Application containerisation.
- **Docker Compose**: Managing multi-container services.

---

## Installation and Usage

### Requirements

- Node.js and a package manager (npm, yarn or pnpm).
- Python 3.8+ along with the required libraries.
- Docker and Docker Compose.

### Installation

 dokonczyć pisać 

l
---

## Main Files with Links to Detailed Documentation

###  Srapers

[`sggw_scraper`](https://github.com/IO-Lab2/Docs/blob/dev/sggw_scraper.md), [`pb_scraper`](https://github.com/IO-Lab2/Docs/blob/dev/pb_scraper.md?plain=1), [`pw_scraper`](https://github.com/IO-Lab2/Docs/blob/dev/pw_scraper.md), [`punktoza_sraper`](https://github.com/IO-Lab2/Docs/blob/dev/punktoza_scraper.md)  automatically retrieves details about:

- Scientists and their profiles
- Scientific publications
- Organizational structure of the university

### [`Front-end`](https://github.com/IO-Lab2/Docs/blob/dev/front-end.md)
The project is a Next.js app designed for searching, filtering, and comparing data on researchers, organizations, and publications. It provides a user-friendly interface with dynamic filtering and detailed information access.

### [`Api`](https://github.com/IO-Lab2/Docs/blob/dev/api.md)
The API acts as the project's backend, enabling efficient management of data related to researchers, publications, and organizations. It supports core operations such as data retrieval, filtering, and updates, ensuring seamless integration with the front-end. 

### [`stack`](https://github.com/IO-Lab2/Docs/blob/dev/stack.md)
The stack folder contains configurations and files for running the application using Docker Compose and .gitignore rules to manage file exclusions in the version control system.




