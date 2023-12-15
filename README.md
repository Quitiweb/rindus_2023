# Synchro API
A simple REST API to interact with the Fake API in JSONPlaceholder - Free Fake REST API

## Libraries used
 - `psycopg2-binary`:  Python-PostgreSQL Database Adapter (`binary` to avoid building it from source)
 - `python-decouple`: To load sensible information from the `.env` file
 - `requests`: To get data from JsonPlaceholder Free Fake Rest API


## Building and Running the Project
Build the Docker Image
```bash
make build
```

### Database Migrations
Create and Apply Migrations
```bash
make migrate
```

### Creating a Superuser
Create a Django Superuser
```bash
make createsuperuser
```

### Run the Project
```bash
make up
```
