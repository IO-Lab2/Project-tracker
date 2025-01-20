# Front-End 

## Description 
The front-end of the project is the Next.js app for searching, filtering and comparing researcher, organisation and publication data. Application pages, such as the comparison view, researcher profile and search, are defined in the app folder with a global layout to ensure a consistent appearance. Components in the components folder are responsible for the interactive user interface, enabling dynamic filtering and results management.The app allows users to search the knowledge base, add scientists for comparison and obtain detailed bibliometric information. 

### Example:

![Layout Image](https://github.com/IO-Lab2/Docs/blob/dev/Layout1.png?raw=true)
![Layout Image](https://github.com/IO-Lab2/Docs/blob/dev/Layout2.png?raw=true)



---

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
- [Directory Structure](#directory-structure)
- [Deployment](#deployment)

---

## Features
- **Dynamic Search:** Search and filter results based on academic institutions, publications, and researchers.
- **Comparison Tool:** Compare bibliometric data of scientists.
- **Responsive Design:** Optimized for desktop and mobile devices.
- **Interactive UI:** Built with reusable components.

---

## Technologies Used
- **React**
- **Next.js**
- **TypeScript**
- **Tailwind CSS**
- **PostCSS**

---

## Installation and Setup

### Prerequisites
- Node.js 
- Package manager (npm, yarn, pnpm, or bun)

### Steps

1. Start the development server:
 ```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

2. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

### Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!
---

## Directory Structure

```
.
├── .devcontainer/                   # Configuration for the development container
│   └── devcontainer.json            # JSON configuration file for the development container
├── .github/                         # GitHub configuration
│   ├── dependabot.yml               # Dependabot configuration for managing dependencies
│   └── workflows/                   # Workflows for CI/CD automation
│       └── docker-image.yml         # Workflow for building Docker images
├── app/                             # Application source files
│   ├── compare/                     # Module handling the comparison of scientists
│   │   └── page.tsx                 # Page for displaying comparison results
│   ├── scientist/                   # Module dedicated to scientist-related details
│   │   └── page.tsx                 # Page showing detailed scientist profiles
│   ├── view/                        # Module for general views and search results
│   │   └── page.tsx                 # Page displaying the main search results
│   ├── favicon.ico                  # Icon displayed in the browser tab
│   ├── globals.css                  # Global CSS styles using Tailwind CSS
│   ├── layout.tsx                   # Defines the global layout and structure of the app
│   └── page.tsx                     # Entry point and home page of the application
├── components/                      # Reusable UI components
│   ├── FilterHeaderTable.tsx        # Filter header table component
│   ├── FilterViewOption.tsx         # Filter view options component
│   ├── ScientistCompareCard.tsx     # Scientist comparison card component
│   ├── SearchOptions.tsx            # Search options UI component
│   └── SkipFilterButton.tsx         # Button to skip filters
├── lib/                             # Utility libraries
│   ├── API.ts                       # API interaction utilities
│   ├── CompareState.ts              # State management for comparison
│   └── FilterState.ts               # State management for filters
├── public/                          # Static assets
│   ├── globe.svg                    # Globe SVG icon
│   ├── next.svg                     # Next.js logo in SVG format
│   ├── vercel.svg                   # Vercel logo in SVG format
│   └── window.svg                   # Window icon in SVG format
├── .eslint.json                     # ESLint configuration
├── .gitignore                       # Git ignore file for excluding files from version control
├── Dockerfile                       # Docker configuration for the project
├── next.config.ts                   # Next.js configuration
├── package.json                     # Project metadata and dependencies
├── postcss.config.mjs               # PostCSS configuration
├── README.md                        # Project documentation
├── tailwind.config.ts               # Tailwind CSS configuration
└── tsconfig.json                    # TypeScript configuration
```

---

### Main Files  
- **[``app``](https://github.com/IO-Lab2/Front-end/tree/dev/app)**:  

   The app catalogue manages the logic and structure of the app, defining pages such as the home page, comparison view and researcher profile. With a global layout from layout.tsx, it provides a consistent look and style integration. The pages interact with the API, filter logic and routing, allowing the user to seamlessly view data and interact with the application.

- **[``components``](https://github.com/IO-Lab2/Front-end/tree/dev/components)**:  
The folder contains reusable user interface components that are key to building a dynamic and interactive application. These components include elements that support data filtering (FilterHeaderTable, FilterViewOption), management of search options (SearchOptions), and visualisation of scientists and organisations as cards or cells (ScientistCell, ScientistCompareCard, OrganisationCell).


- **[``lib/API.ts``](https://github.com/IO-Lab2/Front-end/blob/dev/lib/API.ts)**:  
   The code defines TypeScript interfaces for data modelling (e.g. Organisation, Scientist, Bibliometrics) and functions to interact with the project API. Functions such as fetchScientistInfo or fetchSearch allow information about scientists, organisations and publications to be retrieved using filters. They support HTTP requests and return data in JSON format, ensuring stability through error handling. 

- **[``Dockerfile``](https://github.com/IO-Lab2/Front-end/blob/dev/Dockerfile)**:  
  Defines the steps to build a Docker image for the application, including installing dependencies, configuring the environment, and running the production build of the Next.js application.

- **[``next.config.ts``](https://github.com/IO-Lab2/Front-end/blob/dev/next.config.ts)**:  
   The configuration file for Next.js, allowing management of global application settings such as domains.

---

## Deployment

### Docker Deployment
1. Build the Docker image:
   ```bash
   docker build -t front-end-image .
   ```
2. Run the container:
   ```bash
   docker run -p 3000:3000 front-end-image
   ```

### Vercel Deployment
The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

---

