# Synchro API
A simple REST API to interact with the Fake API in JSONPlaceholder - Free Fake REST API

## Libraries
`python-decouple` - We use this library to load sensible information from the `.env` file

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
