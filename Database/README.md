# Database
Repository containing sql queries written for PostgreSQL

## How to access the database

1. Copy the .env.example file to .env file

jeśli chcesz się połączyć do bazy to masz dwie możliwości:
z command line: https://www.postgresql.org/download/,
musisz zainstalować sobie psql shella, a potem wpisać komendę:
```
psql -h ioprojectdatabase.postgres.database.azure.com -p 5432 -U postgres postgres
```
i wpisać hasło, które podałem w .env.example
Należy zaznaczyć opcję "SSL"

lub po prostu connection stringiem:
```
 psql 'postgresql://postgres:dd?3zfeH)z,G.4y@ioprojectdatabase.postgres.database.azure.com:5432/postgres'
```

2. Visual studio code ma dodatek:

Name: Database Client
Id: cweijan.vscode-database-client2
Description: Database manager for MySQL/MariaDB, PostgreSQL, SQLite, Redis and ElasticSearch.
Version: 7.6.3
Publisher: Weijan Chen
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-database-client2

oraz

Name: Database Client JDBC
Id: cweijan.dbclient-jdbc
Description: JDBC Adapter For Database Client
Version: 1.3.6
Publisher: Weijan Chen
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=cweijan.dbclient-jdbc

i wtedy będziesz mógł w vs code przeglądać sobie strukturę bazy
