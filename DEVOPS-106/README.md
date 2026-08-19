# DEVOPS-106: FastAPI and MySQL with Docker Compose

A beginner Docker Compose practice project using a ready-made FastAPI task API and MySQL database.

## Main Learning Goal

Focus on Docker Compose rather than FastAPI development. The application is already implemented; your work is to containerize it and define the two-service Compose deployment.

## Architecture

```text
Browser / API Client
        │
        │ :8000
        ▼
FastAPI service: api
        │
        │ task-net
        ▼
MySQL service: mysql
        │
        ▼
Named volume: mysql_data
```

## Project Structure

```text
DEVOPS-106/
├── app/
│   └── main.py
├── requirements.txt
├── Dockerfile
├── compose.yml
└── README.md
```

The FastAPI application is complete. The `Dockerfile` and `compose.yml` are intentionally left unsolved.

## Available API Operations

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service information |
| `GET` | `/health` | API and MySQL health |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List all tasks |
| `PATCH` | `/tasks/{id}/complete` | Mark a task complete |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `GET` | `/docs` | Interactive Swagger documentation |

The application creates its `tasks` table automatically after connecting to MySQL.

## First Task: Write Only the Dockerfile

Create a working FastAPI image using:

- Base image: `python:3.12-slim`
- Working directory: `/app`
- Dependencies from `requirements.txt`
- Application source copied into the image
- Container port: `8000`
- Uvicorn listening on `0.0.0.0:8000`
- Import target: `app.main:app`

Do not complete `compose.yml` until your Dockerfile has been reviewed.

## MySQL Service Requirements

| Setting | Required value |
| --- | --- |
| Service name | `mysql` |
| Image | `mysql:8.4` |
| Database | `taskdb` |
| User | `taskuser` |
| Password | `task123` |
| Root password | `root123` |
| Named volume | `mysql_data` |
| Volume mount | `/var/lib/mysql` |
| Network | `task-net` |

Use these MySQL initialization variables:

```text
MYSQL_DATABASE=taskdb
MYSQL_USER=taskuser
MYSQL_PASSWORD=task123
MYSQL_ROOT_PASSWORD=root123
```

Add a MySQL healthcheck. Do not publish MySQL port `3306` to the EC2 host.

## FastAPI Service Requirements

| Setting | Required value |
| --- | --- |
| Service name | `api` |
| Container name | `task-api` |
| Build context | Current directory |
| Host port | `8000` |
| Container port | `8000` |
| Network | `task-net` |

Pass these variables to FastAPI:

```text
DB_HOST=mysql
DB_PORT=3306
DB_USER=taskuser
DB_PASSWORD=task123
DB_NAME=taskdb
```

`DB_HOST` must be `mysql` because Compose makes service names resolvable through internal DNS. Inside the API container, `localhost` means the API container itself, not MySQL.

Configure the API service to wait for the MySQL healthcheck to pass.

## Compose Concepts to Practice

- `services`
- `image`
- `build`
- `environment`
- `ports`
- `volumes`
- `networks`
- `healthcheck`
- `depends_on`
- `restart`

## Commands to Practice

Validate your Compose file:

```bash
docker compose config
```

Build and start:

```bash
docker compose up -d --build
```

Inspect services and logs:

```bash
docker compose ps
docker compose logs mysql
docker compose logs api
```

Stop while preserving database data:

```bash
docker compose down
```

Stop and delete the database volume:

```bash
docker compose down -v
```

> The `-v` option deletes the named volume and its stored task data.

## Verification

Check application health:

```bash
curl http://localhost:8000/health
```

Open Swagger documentation:

```text
http://<EC2-PUBLIC-IP>:8000/docs
```

Example task payload:

```json
{
  "title": "Review Docker Compose logs"
}
```

## Persistence Test

1. Create multiple tasks through `/docs`.
2. Run `docker compose down`.
3. Start the project again.
4. Confirm that the tasks still exist.
5. Run `docker compose down -v`.
6. Recreate the project and confirm that the previous tasks are gone.

## Acceptance Criteria

- [ ] FastAPI image builds successfully
- [ ] MySQL becomes healthy
- [ ] FastAPI waits for MySQL health
- [ ] FastAPI uses `DB_HOST=mysql`
- [ ] Both services use `task-net`
- [ ] MySQL uses the `mysql_data` volume
- [ ] MySQL port `3306` remains private
- [ ] FastAPI is published on port `8000`
- [ ] `/health` reports a connected database
- [ ] `/docs` opens successfully
- [ ] Task creation, listing, completion, and deletion work
- [ ] Task data survives a normal `docker compose down`

## Quick Questions

1. Why should `DB_HOST` be `mysql` instead of `localhost`?
2. Why is `taskuser` safer than connecting the application as MySQL `root`?

## Ticket

**Ticket:** DEVOPS-106  
**Role:** Junior DevOps Engineer  
**Primary focus:** Docker Compose  
**Environment:** Ubuntu EC2
