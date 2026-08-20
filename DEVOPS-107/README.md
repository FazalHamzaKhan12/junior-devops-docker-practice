# DEVOPS-107: Flask, Redis, and Nginx with Docker Compose

A three-service Docker Compose practice project built around a ready-made Flask URL Shortener.

## Scenario

Users submit a long URL and receive a short code. Flask handles the shortening logic, while Redis stores the mapping and click count. Nginx is the only public entry point.

```text
https://example.com/very/long/path
                 ↓
               Flask
                 ↓
          short code: abc123
                 ↓
Redis stores abc123 → original URL
```

## Target Architecture

```text
Internet
   │
   │ :80
   ▼
Nginx service
   │
   │ app-net
   ▼
Flask service
   │
   │ app-net
   ▼
Redis service
   │
   ▼
redis_data volume
```

Only Nginx should publish a host port. Flask port `5000` and Redis port `6379` remain private.

## Project Structure

```text
DEVOPS-107/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── Dockerfile
├── nginx.conf
├── compose.yml
└── README.md
```

The Flask application and Nginx configuration are complete. The `Dockerfile` and `compose.yml` are intentionally unsolved.

## Application Features

- Validates HTTP and HTTPS URLs
- Generates unique short codes
- Stores mappings in Redis
- Redirects short codes to their destinations
- Tracks redirect counts
- Displays the three newest links
- Exposes `/health` for Flask and Redis status
- Uses reverse-proxy headers when generating public links

## First Task: Redis Service Only

Start `compose.yml` by defining only the Redis service with:

- `image`
- `volume`
- `network`
- `healthcheck`
- `restart`

Send that section for review before adding Flask or Nginx.

## Redis Requirements

| Setting | Required value |
| --- | --- |
| Service name | `redis` |
| Image | `redis:7-alpine` |
| Internal port | `6379` |
| Published port | None |
| Named volume | `redis_data` |
| Volume path | `/data` |
| Network | `app-net` |

Use `redis-cli ping` for the healthcheck. A healthy Redis service returns `PONG`.

## Second Task: Flask Dockerfile

Write the Dockerfile yourself using:

- `python:3.12-slim`
- `/app` as the working directory
- Dependencies from `requirements.txt`
- The application source copied into the image
- Port `5000` exposed
- `python app.py` as the startup command

## Flask Service Requirements

| Setting | Required value |
| --- | --- |
| Service name | `flask` |
| Container name | `url-app` |
| Internal port | `5000` |
| Published port | None |
| Network | `app-net` |

Pass these environment variables:

```text
REDIS_HOST=redis
REDIS_PORT=6379
```

Flask must wait for Redis to become healthy. `REDIS_HOST` is `redis` because Compose provides internal DNS using service names.

## Nginx Service Requirements

| Setting | Required value |
| --- | --- |
| Service name | `nginx` |
| Image | `nginx:alpine` |
| Container name | `nginx-proxy` |
| Host port | `80` |
| Container port | `80` |
| Network | `app-net` |
| Configuration mount | `nginx.conf:/etc/nginx/nginx.conf:ro` |

The supplied Nginx configuration forwards requests to:

```text
flask:5000
```

Do not use `localhost:5000`. Inside the Nginx container, `localhost` means Nginx itself.

## Compose Structure to Build

```text
services:
  redis:
  flask:
  nginx:

volumes:
  redis_data:

networks:
  app-net:
```

Practice these Compose features:

- `image`
- `build`
- `environment`
- `volumes`
- `networks`
- `healthcheck`
- `depends_on`
- `ports`
- `restart`

## Expected Startup

```text
docker compose up
        ↓
Redis starts
        ↓
Redis healthcheck returns PONG
        ↓
Flask starts
        ↓
Nginx starts
        ↓
User accesses port 80
```

## Commands to Practice

Validate, build, and start:

```bash
docker compose config
docker compose up -d --build
```

Inspect services and logs:

```bash
docker compose ps
docker compose logs redis
docker compose logs flask
docker compose logs nginx
```

Stop while preserving mappings:

```bash
docker compose down
```

Stop and delete stored mappings:

```bash
docker compose down -v
```

> The `-v` option deletes `redis_data` and all shortened URL mappings stored in it.

## Verification

Open the public website:

```text
http://<EC2-PUBLIC-IP>
```

Check health through Nginx:

```bash
curl http://localhost/health
```

Create several short links, run `docker compose down`, then start the project again. The mappings should still work. After `docker compose down -v`, previously created mappings should be gone.

## Acceptance Criteria

- [ ] Flask image builds successfully
- [ ] Redis becomes healthy
- [ ] Flask waits for Redis health
- [ ] Flask uses `REDIS_HOST=redis`
- [ ] Nginx proxies to `flask:5000`
- [ ] All services use `app-net`
- [ ] Only Nginx publishes a host port
- [ ] Redis uses the `redis_data` volume
- [ ] Website works on EC2 port `80`
- [ ] URL shortening and redirects work
- [ ] Mappings survive a normal `docker compose down`
- [ ] `docker compose down -v` removes mappings
- [ ] `docker compose config` validates successfully

## Check Questions

1. What hostname should Flask use for Redis?
2. Which service should be the only one with a host `ports` mapping?

## Ticket

**Ticket:** DEVOPS-107  
**Role:** Junior DevOps Engineer  
**Primary focus:** Three-service Docker Compose  
**New technology:** Redis
