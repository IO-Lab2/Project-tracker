# API

## Description

The API serves as the backend component of the project, providing a robust, scalable, and modular infrastructure to handle various operations. It is built in **Go**, utilizing a layered architecture that separates core logic, request handling, and database interaction for maintainability and efficiency.

### Key functionalities include:
- Managing scientists, publications, organizations, and bibliometric data.
- Providing search capabilities with filters for academic titles, positions, publication counts, and more.
- Supporting CRUD operations across entities like scientists, organizations, and bibliometrics.

## Table of Contents
- [Requirements](#requirements)
- [How to work with devcontainer](#how-to-work-with-devcontainer)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Awesome docs](#awesome-docs)
- [Files and Modules](#files-and-modules)
    - [Directory Structure](#directory-structure)
    - [Main Files](#main-files)
- [Workflow](#workflow)
  - [Testing Workflow](#testing-workflow-go.yml)
  - [Docker Workflow](#docker-workflow-dockerimage.yml)
  - [Manual Deployment](#manual-deployment)
  - [Server Deployment](#server-deployment)
---
## Requirements

- **Docker**: Used for containerization of the development environment and production builds.
- **Visual Studio Code**: Integrated development environment (IDE) for working with the codebase.
- **Remote - Containers Extension**: For working within the devcontainer setup.
- **Git**: For version control and collaboration.
- **Go**: Primary programming language for the project, version specified in `go.mod`.




---
## How to work with devcontainer

### Prerequisites
- Docker installed on your machine
- Visual Studio Code
- Visual Studio Code Remote - Containers extension installed

### Steps
1. Clone the repository to your local machine and open it in Visual Studio Code.
2. Open the command palette (Ctrl+Shift+P or Cmd+Shift+P on macOS) and select `Dev Container: Reopen in Container`.
3. Wait for the container to build and the project to open inside the container environment.
---


## Awesome docs:
Access the full API documentation here:  
[API Documentation](https://api.epickaporownywarkabazwiedzyuczelni.rocks/docs#/)

---

## Files and Modules

### Directory Structure

```
.
├── .devcontainer/                   # Configuration for the development container
│   └── devcontainer.json            # JSON configuration file for the development container
├── .github/                         # GitHub configuration
│   ├── dependabot.yml               # Dependabot configuration for managing dependencies
│   └── workflows/                   # Workflows for CI/CD automation
│       ├── dockerImage.yml          # Workflow for building Docker images
│       └── go.yml                   # Workflow for running tests and builds for Go
├── internal/                        # Internal application logic
│   ├── database/                    # Database connection and initialization
│   │   └── database.go              # Code to configure and manage the database connection
│   ├── handlers/                    # HTTP handlers for request processing
│   │   ├── bibliometrics_handlers.go # Handlers for bibliometrics-related operations
│   │   ├── scientists_handlers.go    # Handlers for scientist-related operations
│   │   ├── ...                      # Other handler files
│   ├── logger/                      # Logging setup
│   │   └── logging.go               # Logger configuration for the application
│   ├── models/                      # Data models used throughout the application
│   │   ├── bibliometrics.go         # Model representing bibliometrics data
│   │   ├── search_models.go         # Models for search operations
│   │   ├── ...                      # Other model files
│   ├── repositories/                # Database repositories for querying data
│   │   ├── scientists_repository.go # Repository for accessing scientist data
│   │   ├── publishers_repository.go # Repository for accessing publisher data
│   │   ├── ...                      # Other repository files
│   ├── requests/                    # Request definitions for incoming API calls
│   │   ├── bibliometrics_requests.go # Requests for bibliometrics endpoints
│   │   ├── scientists_requests.go    # Requests for scientist endpoints
│   │   ├── ...                      # Other request files
│   ├── responses/                   # Response definitions for outgoing API responses
│   │   ├── bibliometrics_responses.go # Responses for bibliometrics endpoints
│   │   ├── scientists_responses.go    # Responses for scientist endpoints
│   │   ├── ...                      # Other response files
│   └── services/                    # Business logic and application services
│       ├── bibliometrics_services.go # Business logic for bibliometrics
│       ├── search_services.go       # Business logic for search operations
│       ├── ...                      # Other service files
├── routes/                          # API route definitions and setup
│   ├── bibliometrics/               # Routes for bibliometrics module
│   │   └── bibliometrics_routes.go  # Route definitions for bibliometrics API
│   ├── filters/                     # Routes for filter module
│   │   └── filters_routes.go        # Route definitions for filters API
│   ├── organizations/               # Routes for organizations module
│   │   └── organizations_routes.go  # Route definitions for organizations API
│   ├── publications/                # Routes for publications module
│   │   └── publications_routes.go   # Route definitions for publications API
│   ├── scientists/                  # Routes for scientists module
│   │   └── scientists_routes.go     # Route definitions for scientists API
│   ├── search/                      # Routes for search functionality
│   │   └── search_routes.go         # Route definitions for search API
│   └── tests/                       # API route tests
│       ├── bibliometrics_test.go    # Tests for bibliometrics routes
│       ├── search_test.go           # Tests for search routes
│       ├── ...                      # Other test files
├── .env.example                     # Example environment variables file
├── .gitignore                       # Git ignore file for excluding files from version control
├── Dockerfile                       # Dockerfile for building the application container
├── go.mod                           # Go module dependencies and metadata
├── go.sum                           # Checksum for Go module dependencies
├── main.go                          # Main application entry point
└── README.md                        # Documentation for the project

```
### Main Files
- **[`main.go`](https://github.com/IO-Lab2/API/blob/dev/main.go)**:  
    This code serves as the main entry point for the API server application written in Go. It initializes the database connection, configures the logger, and sets up a router with middleware for logging events, error recovery, and handling CORS. Finally, it registers all API routes using huma and starts the server, making it ready to handle incoming requests.
- **[`Dockerfile`](https://github.com/IO-Lab2/API/blob/dev/Dockerfile)**:  
    This Dockerfile creates a multi-stage build for a Go application. In the first stage (builder), it sets up the environment, downloads dependencies, and builds the application into a binary named api. In the second stage, it creates a lightweight container with the built binary, exposes port 8000, and sets the command to run the api executable when the container starts.
- **[`internal/database.go`](https://github.com/IO-Lab2/API/blob/dev/internal/database/database.go)**:  
    This code manages the database connection for a Go application. It initializes the database connection (InitDB) , sets connection limits, and ensures proper cleanup with CloseDB. It also provides a global method (GetDB) to access the database instance, ensuring it is properly initialized before use.
- **[`internal/handlers`](https://github.com/IO-Lab2/API/tree/dev/internal/handlers)**:  
    The folder contains the HTTP request handling logic for the API. It serves as a bridge between incoming client requests and the service layer, processing inputs. Each file in the folder corresponds to a specific API feature, such as managing scientists, publications, organizations, or performing search operations.  
- **[`internal/services`](https://github.com/IO-Lab2/API/tree/dev/internal/services)**:  
    The folder contains the business logic of the application, acting as a bridge between the database repositories and HTTP handlers. Each file in the folder is responsible for a specific feature, such as managing academic titles, publications, organizations, scientists, or performing searches. It processes data, enforces business rules, and ensures proper error handling before returning results to the handlers.  
- **[`routes`](https://github.com/IO-Lab2/API/tree/dev/routes)**:  
    The  folder defines the API's routing structure, organizing endpoint registrations for various features like bibliometrics, filters, organizations, publications, scientists, and search. Each file links specific routes to their handlers and services, ensuring modular and clear route management. The [`tests`](https://github.com/IO-Lab2/API/tree/dev/routes/tests) subfolder includes tests to validate the correctness of these routes.         
---

## Workflow

The GitHub Actions workflows automatically handle testing and deploying the API. Here’s how it works:

1. **Testing Workflow (`go.yml`)**:  
   - Runs unit tests and validates the Go code after every commit.  
   - If all tests pass, the `dockerImage.yml` workflow is triggered.

2. **Docker Workflow (`dockerImage.yml`)**:  
   - Builds a Docker image of the API.  
   - Pushes the Docker image to the server for deployment.

### Manual Deployment
If you want to deploy a new API version to the server despite failing tests:
1. Navigate to the **'Actions'** tab in the GitHub repository.
2. Select the **'dockerImage'** workflow from the sidebar.
3. Click the **'Run workflow'** button, leave the settings unchanged, and confirm by clicking the button again.

### Server Deployment
A Watchtower service on the server checks for new Docker images every 10 minutes. Once the `dockerImage.yml` 
workflow completes, the new version of the API will be deployed to the server automatically within 10 minutes.
