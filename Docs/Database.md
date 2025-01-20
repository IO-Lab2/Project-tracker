# Database

## Description
The database stores information about scientists, publications, and organizations.


---
## Table of Contents

1. [Usage](#usage)
2. [Database Schema](#database-schema)
   - [Tables](#tables)
   - [Queries](#queries)
   



## usage
Tu get access to the database u need to:  
**1. Copy the .env.example file to .env file**

If you want to connect to the database, you have two options:   
**first option:**
- Download the psql shell  
   You can download the psql shell from the [official PostgreSQL website](https://www.postgresql.org/download/).
   After that, enter the password from the `.env.example` file and select the `'SSL'` option.

**Second option:**
- Run the following command to connect to the database:
   ```bash
   psql -h ioprojectdatabase.postgres.database.azure.com -p 5432 -U postgres postgres

**2. how to browse the database structure using Visual Studio Code:**

- Name: Database Client
Id: cweijan.vscode-database-client2
Description: Database manager for MySQL/MariaDB, PostgreSQL, SQLite, Redis and ElasticSearch.
Version: 7.6.3
Publisher: Weijan Chen
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-database-client2

and

- Name: Database Client JDBC
Id: cweijan.dbclient-jdbc
Description: JDBC Adapter For Database Client
Version: 1.3.6
Publisher: Weijan Chen
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=cweijan.dbclient-jdbc


## Database Schema
### Tables
This [`tables.sql`](https://github.com/IO-Lab2/Database/blob/dev/tables.sql) make tables available for storing :
- information about scientists
- information about organizations
- the relationship between scientists and organizations
- information about publications
- the relationships between scientists and publications
- bibliometric indicators of scientists


### Queries
The database includes the following tables:

1. **Scientists**
   - Stores information about researchers, including their names and affiliations.
   - **SQL File**: [`scientists.sql`](https://github.com/IO-Lab2/Database/blob/dev/SQL%20QUERIES/scientists.sql)

2. **Publications**
   - Contains detailed information about scientific publications, including titles, journal names, publication dates, citation counts, and the journal's impact factor.
   - **SQL File**: [`publications.sql`](https://github.com/IO-Lab2/Database/blob/dev/SQL%20QUERIES/publications.sql)

3. **Organizations**
   - Stores information about organizations, including their names and types (e.g., "university", "company"). 
   - **SQL File**: [`organizations.sql`](https://github.com/IO-Lab2/Database/blob/dev/SQL%20QUERIES/organizations.sql)

4. **Bibliometrics**
   - Tracks publication metrics, including index, citation counts, publication counts, and ministerial scores .
   - **SQL File**: [`bibliometrics.sql`](https://github.com/IO-Lab2/Database/blob/dev/SQL%20QUERIES/bibliometrics.sql)

5. **Scientists_Publications**
   - A join table linking scientists to their publications.
   - **SQL File**: [`scientists_publications.sql`](https://github.com/IO-Lab2/Database/blob/dev/SQL%20QUERIES/scientists_publications.sql)

6. **Scientists_Organizations**
   - A join table linking scientists to their organizations.
   - **SQL File**: [`scientist-organization.sql`](https://github.com/IO-Lab2/Database/blob/dev/SQL%20QUERIES/scientist-organization.sql)

7. **Scientists_Joins**
   - Manages complex relationships between scientists and multiple entities.
   - **SQL File**: [`scientists_joins.sql`](https://github.com/IO-Lab2/Database/blob/dev/scientists_joins.sql)




