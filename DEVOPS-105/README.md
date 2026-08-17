# DEVOPS-105: Flask + MySQL with Docker Compose

A beginner-friendly hands-on DevOps project for learning how to manage a multi-container application using **Docker Compose**.

> This project is created for learning and practice purposes. It is not intended to represent a complete production deployment.

## Project Scenario

Imagine you have joined a company as a **Junior DevOps Engineer**.

The development team has provided a small Employee Feedback application built with:

- Flask
- Python
- MySQL

The application was previously deployed using individual Docker commands.

Your task is to use **Docker Compose** to manage the complete application from a single Compose file.

---

## Architecture

```text
User Browser
     |
     | Port 5000
     v
┌─────────────────┐
│ Flask Container │
│   Port 5000     │
└────────┬────────┘
         |
         | Docker Network
         | mysql:3306
         v
┌─────────────────┐
│ MySQL Container │
│   Port 3306     │
└────────┬────────┘
         |
         v
   mysql_data
   Docker Volume
```

Only the Flask application is exposed to the host.

MySQL communicates with Flask through the internal Docker Compose network.

---

## Project Structure

```text
DEVOPS-105/
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yml
├── static/
│   └── style.css
└── templates/
    └── index.html
```

---

# Your Task

Create a Docker Compose configuration that runs the Flask application and MySQL database together.

The goal is to replace multiple manual Docker commands with:

```bash
docker compose up -d
```

---

## MySQL Service Requirements

Create a service named:

```text
mysql
```

Use:

```text
Image: mysql:8.4
Database: companydb
Root Password: root
Internal Port: 3306
Volume: mysql_data
Volume Path: /var/lib/mysql
Network: company-net
```

MySQL does **not** need port `3306` published to the host because Flask communicates with it through the Docker network.

### Health Check

Configure a MySQL health check so Docker Compose can determine when the database is ready to accept connections.

This is important because:

```text
Container Running
       ≠
Database Ready
```

---

## Flask Service Requirements

Create a service named:

```text
flask
```

Build the Flask image using the provided `Dockerfile`.

Configure:

```text
Host Port:      5000
Container Port: 5000
Network:        company-net
```

The application expects these environment variables:

```text
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=companydb
```

The hostname is `mysql` because Docker Compose provides service-name DNS resolution between containers on the same network.

---

## Service Dependency

Configure Flask so it waits for the MySQL service to become healthy before starting.

The expected startup flow is:

```text
docker compose up
       |
       v
MySQL Container Starts
       |
       v
MySQL Health Check
       |
       v
MySQL Becomes Healthy
       |
       v
Flask Container Starts
       |
       v
Flask Connects to MySQL
```

---

# Docker Compose Concepts Practiced

This project introduces:

- `services`
- `image`
- `build`
- `container_name`
- `environment`
- `ports`
- `volumes`
- `networks`
- `depends_on`
- `healthcheck`
- `restart`

---

# Running the Project

Validate the Compose file before starting:

```bash
docker compose config
```

Build and start the application:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Expected services:

```text
mysql
flask
```

MySQL should eventually report:

```text
healthy
```

---

# View Logs

View all service logs:

```bash
docker compose logs
```

Flask only:

```bash
docker compose logs flask
```

MySQL only:

```bash
docker compose logs mysql
```

Follow logs continuously:

```bash
docker compose logs -f
```

---

# Access the Application

Open:

```text
http://<EC2-PUBLIC-IP>:5000
```

If using AWS EC2, make sure the Security Group permits the required inbound traffic to port `5000` for your practice environment.

---

# Verify the Database

You can check whether the database exists:

```bash
docker exec -it mysql mysql -uroot -proot -e "SHOW DATABASES;"
```

You should see:

```text
companydb
```

The Flask application automatically creates its required `feedback` table after successfully connecting to MySQL.

---

# Stopping the Application

Stop and remove the Compose containers and network:

```bash
docker compose down
```

The named database volume remains.

To also remove the volume:

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` deletes the project's named volume and therefore removes the stored MySQL data.

---

# Troubleshooting

If the application does not work, check each layer instead of immediately rebuilding everything.

```text
Browser
   ↓
Flask Container
   ↓
Docker Network
   ↓
MySQL Container
   ↓
MySQL Database
   ↓
Docker Volume
```

Useful commands:

```bash
docker compose ps
docker compose logs flask
docker compose logs mysql
docker compose config
docker network ls
docker volume ls
```

---

# Common Problems

### Unknown Database

Example:

```text
Unknown database 'companydb'
```

Check that the MySQL configuration uses the correct environment variable:

```text
MYSQL_DATABASE
```

Environment variable names must be spelled exactly.

Also remember that MySQL initialization variables are applied when MySQL initializes a new data directory.

---

### Flask Cannot Reach MySQL

Flask should use:

```text
MYSQL_HOST=mysql
```

Not:

```text
MYSQL_HOST=localhost
```

Inside the Flask container, `localhost` refers to the Flask container itself.

---

### Container Running but Application Not Ready

A running container does not always mean the application inside it is ready.

This is why the MySQL service uses a health check.

---

# Acceptance Criteria

The project is complete when:

- [ ] `docker compose config` validates successfully
- [ ] Flask image builds successfully
- [ ] Flask and MySQL start with one Compose command
- [ ] MySQL becomes healthy
- [ ] Flask waits for MySQL health
- [ ] Flask connects to MySQL using `mysql` as the hostname
- [ ] `companydb` is created
- [ ] Feedback can be stored in MySQL
- [ ] Flask is accessible on port `5000`
- [ ] MySQL port `3306` is not publicly published
- [ ] MySQL data uses a named volume
- [ ] Both services communicate through the Compose network
- [ ] `docker compose down` removes the application containers
- [ ] Database data survives a normal `docker compose down`
- [ ] No real credentials, keys, or secrets are committed

---

# Knowledge Check

After completing the project, try answering these without looking at your notes:

1. What problem does Docker Compose solve?
2. What is the difference between a Dockerfile and a Compose file?
3. Why does Flask use `MYSQL_HOST=mysql`?
4. Why doesn't Flask use `localhost` for MySQL?
5. Why don't we need to publish MySQL port `3306`?
6. What does a named volume do?
7. Why do we use a MySQL health check?
8. What is the difference between a container being `running` and `healthy`?
9. What does `depends_on` with `service_healthy` do?
10. What does `docker compose up -d` do?
11. What does `docker compose down` do?
12. What is the difference between `docker compose down` and `docker compose down -v`?
13. Why does Compose create names such as `devops-105_company-net`?
14. What does `docker compose config` help you check?

---

# What I Practiced

Through this project:

```text
Dockerfile
    ↓
Build Flask Image
    ↓
Docker Compose
    ↓
Flask + MySQL Services
    ↓
Compose Network
    ↓
Service Name DNS
    ↓
Persistent Volume
    ↓
Health Checks
    ↓
Service Dependencies
```

The main lesson is that Docker Compose does not replace Docker itself.

It provides a convenient way to **define and manage multiple Docker containers, networks, volumes, ports, and configuration in one YAML file**.

---

## Project Information

**Ticket:** DEVOPS-105  
**Role:** Junior DevOps Engineer (Practice Scenario)  
**Difficulty:** Beginner  
**Environment:** Ubuntu / AWS EC2  
**Technologies:** Docker, Docker Compose, Flask, Python, MySQL, Linux

---

## Disclaimer

This project is designed for **educational and hands-on DevOps practice**.

Simple credentials such as `root` are intentionally used to keep the exercise focused on Docker Compose fundamentals. They should not be treated as production security practices.

Real applications should use proper secret management, restricted database users, production application servers, HTTPS, monitoring, backups, and other security and reliability controls.
