# DEVOPS-104: Three-Tier Application Deployment

An intermediate Junior DevOps practice project for manually deploying Nginx, Flask, and MySQL as three separate Docker containers on one Ubuntu AWS EC2 instance.

## Company Scenario

The company Employee Feedback Application currently exposes Flask directly. Your senior engineer wants a more realistic three-tier deployment where Nginx is the only public entry point.

## Target Architecture

```text
Internet
   │
   │ HTTP :80
   ▼
Nginx container: nginx-proxy
   │
   │ company-network
   ▼
Flask container: employee-app
   │
   │ company-network
   ▼
MySQL container: mysql-db
   │
   ▼
Docker volume: mysql-data
```

Only Nginx should be publicly reachable. Do not publish Flask port `5000` or MySQL port `3306` on the EC2 host.

## Starter Project

```text
DEVOPS-104/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── README.md
```

The `Dockerfile` and `nginx.conf` are intentionally missing. You must create both yourself. Docker Compose is not allowed for this exercise.

## Application Configuration

The Flask application listens internally on port `5000` and reads these environment variables:

| Variable | Practice value |
| --- | --- |
| `DB_HOST` | `mysql-db` |
| `DB_PORT` | `3306` |
| `DB_USER` | `appuser` |
| `DB_PASSWORD` | `app123` |
| `DB_NAME` | `company` |
| `SECRET_KEY` | Choose a practice value |

The supplied credentials are intentionally simple for this local practice exercise. Never use credentials like these in a real deployment or commit real secrets to Git.

## Tier Requirements

### Tier 1: Nginx web tier

| Setting | Required value |
| --- | --- |
| Container name | `nginx-proxy` |
| Public EC2 port | `80` |
| Container port | `80` |
| Internal upstream | `employee-app:5000` |

Nginx must receive browser requests and forward them to Flask through the private Docker network.

### Tier 2: Flask application tier

| Setting | Required value |
| --- | --- |
| Container name | `employee-app` |
| Internal port | `5000` |
| Public port | None |
| Database host | `mysql-db` |

The Flask container must not use `-p 5000:5000` in this task.

### Tier 3: MySQL database tier

| Setting | Required value |
| --- | --- |
| Container name | `mysql-db` |
| Image | `mysql:8.4` |
| Database | `company` |
| Application user | `appuser` |
| Application password | `app123` |
| Root password | `root123` |
| Internal port | `3306` |
| Public port | None |
| Named volume | `mysql-data` |
| Volume path | `/var/lib/mysql` |

The official MySQL image expects the following initialization variables:

```text
MYSQL_DATABASE=company
MYSQL_USER=appuser
MYSQL_PASSWORD=app123
MYSQL_ROOT_PASSWORD=root123
```

## Docker Network

Create one user-defined network named:

```text
company-network
```

All three containers must join this network. Container-name DNS should provide this private communication path:

```text
nginx-proxy → employee-app:5000 → mysql-db:3306
```

Do not use `localhost` for either internal connection. Inside a container, `localhost` refers only to that same container.

## Your Assignment

Complete these tasks manually without Docker Compose:

1. Prepare an Ubuntu EC2 instance and install Docker.
2. Create `company-network`.
3. Create the `mysql-data` named volume.
4. Run the MySQL container with the required configuration.
5. Write the Flask Dockerfile.
6. Build the Flask image.
7. Run `employee-app` privately on `company-network`.
8. Verify that Flask can connect to MySQL.
9. Write an Nginx reverse-proxy configuration.
10. Run `nginx-proxy` on `company-network`.
11. Publish only Nginx port `80`.
12. Configure the EC2 Security Group for HTTP.
13. Open the site using the EC2 public IP.
14. Submit feedback and verify the stored row in MySQL.

## New Concept: Reverse Proxy

Nginx acts as the public receptionist for the private Flask service:

```text
Browser requests http://<EC2-PUBLIC-IP>
              ↓
Nginx receives the request on port 80
              ↓
Nginx forwards it to employee-app:5000
              ↓
Flask returns the response through Nginx
```

Research these Nginx directives before writing your configuration:

- `server`
- `listen`
- `location`
- `proxy_pass`
- Common reverse-proxy headers

Try writing the configuration yourself before looking for a completed example.

## Application Endpoints

- `/` — Employee feedback form
- `/health` — Flask and MySQL health status

The Flask application automatically creates its `feedback` table after reaching the configured MySQL database.

## Expected Result

Users should open:

```text
http://<EC2-PUBLIC-IP>
```

They should not need `:5000`. The full traffic path should be:

```text
Browser → Nginx :80 → Flask :5000 → MySQL :3306 → mysql-data
```

## Acceptance Criteria

- Nginx, Flask, and MySQL run as three separate containers.
- All containers belong to `company-network`.
- Only Nginx publishes a host port.
- Nginx forwards requests to `employee-app:5000`.
- Flask connects to `mysql-db:3306`.
- MySQL uses the `mysql-data` volume at `/var/lib/mysql`.
- Feedback persists if the MySQL container is replaced.
- The website works at the EC2 public IP without `:5000`.
- Docker Compose is not used.
- No real credentials or private keys are committed.

## Required Proof

Provide the output of:

```bash
docker images
docker ps
docker network inspect company-network
docker volume inspect mysql-data
docker logs nginx-proxy
docker logs employee-app
docker logs mysql-db
```

Verify the public entry point:

```bash
curl -I http://localhost
```

Verify the application through Nginx:

```bash
curl http://localhost/health
```

Finally, provide a browser screenshot showing `http://<EC2-PUBLIC-IP>` and confirm that a submitted feedback row exists in MySQL.

## Knowledge Checks

Be prepared to explain:

1. What does a reverse proxy do?
2. Why does Nginx use `employee-app:5000` instead of `localhost:5000`?
3. Why are Flask and MySQL not published to the EC2 host?
4. What is the difference between a container port and a published host port?
5. How does `company-network` resolve container names?
6. Why does MySQL need `mysql-data`?
7. What happens if Nginx starts while Flask is unavailable?

## Ticket

**Ticket:** DEVOPS-104  
**Role:** Junior DevOps Engineer  
**Difficulty:** Intermediate  
**Environment:** Ubuntu AWS EC2  
**Practice style:** Manual Docker only
