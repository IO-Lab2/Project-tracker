# Project Tracker

This repository serves as the central hub for all components of the academic knowledge base project. The project integrates data from three universities: Warsaw University of Life Sciences (SGGW), Warsaw University of Technology (PW), and Bialystok University of Technology (PB). The purpose is to filter and compare researchers, their achievements, and publications across these universities.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Main Repositories and Components](#main-repositories-and-components)
   - [API](#api)
   - [Database](#database)
   - [Demo Repository](#demo-repository)
   - [Docs](#docs)
   - [Front-End](#front-end)
   - [GitCrashCourse](#gitcrashcourse)
   - [Https-Requests-For-Scraper](#https-requests-for-scraper)
   - [Manual-Testing-Of-Frontend](#manual-testing-of-frontend)
   - [PB-Scraper](#pb-scraper)
   - [PW-Scraper](#pw-scraper)
   - [Scraper](#scraper)
   - [Stack](#stack)
3. [Presentation](#presentation)
4. [Website and User Guide](#website-and-user-guide)
5. [UML Diagram](#uml-diagram)

## Project Overview
The project is an academic knowledge base that allows users to filter researchers from three different universities (SGGW, PW, PB) and compare them across various criteria such as publications, impact factor (IF), ministerial points, and more. The system integrates data scraping, API services, and a user-friendly front-end.

### Key Features:
- **Filtering:** Filter researchers by university, department, position, number of publications, IF factor, ministerial points, and more.
- **Comparison:** Compare up to 10 researchers side by side using pie charts.
- **Data Updates:** Automatic updates of data every 3-10 days through web scraping.
- **Researcher Profiles:** Access to detailed profiles and publications from each university's database.

---

## Main Repositories and Components

### [API](https://github.com/IO-Lab2/API)
The backend API that handles data retrieval, filtering, and updates.

#### Key Features:
- **Development with DevContainer:** 
  - Prerequisites: Docker, Visual Studio Code, Remote Containers extension.
  - Clone the repo, run `Dev Container: Reopen in Container` from the command palette.
- **API Documentation:** [API Documentation](https://api.epickaporownywarkabazwiedzyuczelni.rocks/docs#/)
- **Workflow:** Upon successful tests, the API image is created and deployed to the server.

### [Database](https://github.com/IO-Lab2/Database)
Repository for the SQL queries managing the PostgreSQL database.

#### Key Features:
- **Database Access:** 
  - Use `psql` or connection string to access the PostgreSQL database.
  - Visual Studio Code Database Client extension for browsing the database structure.
  
### [Demo Repository](https://github.com/IO-Lab2/demo-repository)
A demo repository showcasing basic GitHub workflows and practices.

### [Docs](https://github.com/IO-Lab2/Docs)
Documentation for the entire project, including installation guides, architecture, and detailed descriptions of each component.

### [Front-End](https://github.com/IO-Lab2/front-end)
A Next.js application for the front-end of the project, enabling filtering, searching, and comparing researchers.

#### Key Features:
- **Technologies Used:** React, Next.js, Tailwind CSS, TypeScript.
- **Getting Started:**
  ```bash
  npm run dev
