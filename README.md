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
