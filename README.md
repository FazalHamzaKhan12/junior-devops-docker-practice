# Junior DevOps Docker Practice

A collection of hands-on, company-style Docker assignments designed for Junior DevOps Engineers and beginners learning Docker on Linux and AWS EC2.

The projects are structured as practical tasks instead of step-by-step copy-paste tutorials.

> This repository is created for learning and hands-on DevOps practice.

## Goal

Practice Docker and basic deployment workflows including:

- Writing Dockerfiles
- Building Docker images
- Running and managing containers
- Port publishing
- Docker networking
- Docker volumes
- Environment variables
- Container-to-container communication
- Nginx reverse proxy
- Multi-tier application architecture
- Container troubleshooting
- Linux server administration
- AWS EC2 deployment
- Docker Compose

## Projects

### DEVOPS-101 — Flask Docker Deployment

Containerize a Flask application and deploy it to an Ubuntu EC2 instance.

**Skills:**

- Dockerfile
- Python Docker image
- Container management
- Port 5000 publishing
- EC2 Security Groups
- Docker logs

---

### DEVOPS-102 — Nginx Static Website

Containerize a static HTML/CSS website using Nginx and deploy it on EC2.

**Skills:**

- Nginx
- Dockerfile
- Port 80
- Static website hosting
- EC2 deployment
- Basic troubleshooting

---

### DEVOPS-103 — Two-Tier Application

Deploy a Flask application and MySQL database as separate Docker containers.

**Architecture:**

```text
Flask
  ↓
MySQL
```

**Skills:**

- Multiple containers
- Custom Docker networks
- Environment variables
- MySQL
- Named volumes
- Persistent database storage
- Container-to-container communication

---

### DEVOPS-104 — Three-Tier Application with Nginx Reverse Proxy

Deploy a three-tier Employee Feedback application using Nginx, Flask, and MySQL in separate Docker containers.

**Architecture:**

```text
Internet
   ↓
Nginx :80
   ↓
Flask :5000
   ↓
MySQL :3306
```

Nginx acts as the public-facing reverse proxy. Flask handles the application logic, and MySQL stores employee feedback.

Only Nginx is exposed publicly. Flask and MySQL communicate privately through the Docker network.

**Skills:**

- Three-tier architecture
- Nginx reverse proxy
- Flask application container
- MySQL database container
- Docker networking
- Container DNS / hostname communication
- Environment variables
- MySQL persistent volume
- Public vs private container ports
- AWS EC2 Security Groups
- HTTP 500 vs 502 troubleshooting
- Multi-container debugging

---

## How to Use This Repository

1. Open a project folder.
2. Read the project ticket.
3. Try completing the assignment yourself.
4. Build and deploy it on Linux or AWS EC2.
5. Use Docker logs and inspection commands when something fails.
6. Complete the knowledge-check questions.
7. Move to the next project.

## Learning Progression

```text
DEVOPS-101
Flask + Docker
      ↓
DEVOPS-102
Nginx + Docker
      ↓
DEVOPS-103
Flask + MySQL
Two-Tier Application
      ↓
DEVOPS-104
Nginx + Flask + MySQL
Three-Tier Application
      ↓
DEVOPS-105
Docker Compose
```

## Important

These projects are created for **educational and hands-on DevOps practice**.

They intentionally simplify some production concepts so beginners can understand Docker fundamentals before moving to Docker Compose, Kubernetes, CI/CD, monitoring, and production deployment practices.

Never commit:

- AWS credentials
- SSH private keys
- `.pem` files
- Passwords
- API tokens
- Production secrets
- `.env` files containing secrets
