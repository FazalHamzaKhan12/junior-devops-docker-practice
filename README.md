# Junior DevOps Docker Practice

A collection of hands-on, company-style Docker assignments designed for Junior DevOps Engineers and beginners learning Docker on Linux and AWS EC2.

The projects are intentionally structured as practical tickets rather than step-by-step copy-paste tutorials.

## Goal

Practice real Docker workflows including:

* Writing Dockerfiles
* Building Docker images
* Running containers
* Port publishing
* Docker networking
* Docker volumes
* Container troubleshooting
* Linux server administration
* AWS EC2 deployment
* Docker Compose

## Projects

### DEVOPS-101 — Flask Docker Deployment

Containerize a Flask application and deploy it to an Ubuntu EC2 instance.

Skills:

* Dockerfile
* Python image
* Port 5000
* EC2 Security Groups
* Container logs

---

### DEVOPS-102 — Nginx Static Website

Containerize a static HTML/CSS website using Nginx and deploy it on EC2.

Skills:

* Nginx
* Dockerfile
* Port 80
* Static web hosting
* EC2 deployment

---

### DEVOPS-103 — Two-Tier Application

Deploy an application and database as separate Docker containers.

Skills:

* Multiple containers
* Custom Docker networks
* Environment variables
* MySQL
* Persistent volumes
* Container-to-container communication

---

## How to Use This Repository

1. Open a project folder.
2. Read the project ticket.
3. Try completing the assignment without checking a solution.
4. Build and deploy the project on your Linux or EC2 environment.
5. Use Docker logs and inspection commands when something fails.
6. Complete the knowledge-check questions.
7. Move to the next ticket.

## Important

These projects are created for educational and hands-on DevOps practice.

They intentionally simplify some production concepts so beginners can understand Docker fundamentals before learning Kubernetes, CI/CD, monitoring, and production architecture.

Never commit:

* AWS credentials
* SSH private keys
* `.pem` files
* passwords
* API tokens
* production secrets

