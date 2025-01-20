# Stack

## Description
The `stack` repository contains configurations and files for running the application using Docker Compose and `.gitignore` rules to manage file exclusions in the version control system.

---

## Folder Structure
```
stack/
├── .gitignore
└── compose.yml
```
---
## Running the Services
1. Start the services:
   ```bash
   docker-compose up -d
   ```
---

## Files

### `.gitignore`
This file excludes temporary files, logs, directories such as `letsencrypt`, and files containing sensitive information like `.env`

### `compose.yml`
Defines Docker Compose services:

- **`reverse-proxy` (Traefik):** A reverse proxy handling HTTP/HTTPS and automatic SSL certificates.
- **`api`:** The application handling request to the database running on port `8000`, using the `.env` file for configuration.
- **`watchtower`:** Automatically checks for new versions of docker images used by other services and updates them if a new one is found.
- **`front-end`:** Website's front end with which the user interacts.
- **`whoami`:** A simple test service for verifying the configuration.
