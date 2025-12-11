# SGBO Notebook API

## Development setup

### Requirements

- Docker (colima)
- Docker Compose

### Run the development API server

With docker compose:
```console
docker compose up -d
```

Create a superuser for admin access:
```console
docker/bin/exec make superuser
```

Run the development server
```console
docker/bin/exec make dev
```

Browse to http://localhost:8000 for the API and http://localhost:8000/admin for the Django admin.

## JSON schema

The JSON data stored in the `entities` field is defined with the following JSON schema:

https://github.com/maerteijn/sgbo-notebook-api/blob/90b59463a69dc8858e0e17b9101a912097e5aa99/src/sgbo_notebook_api/schemas.py#L1-L19