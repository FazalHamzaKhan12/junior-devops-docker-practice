# DEVOPS-101: Flask Docker Deployment on AWS EC2

A simple hands-on project created **for DevOps practice and learning purposes**.

The goal of this project is to practice containerizing a Flask application with Docker and deploying it on an Ubuntu AWS EC2 instance.

## Project Overview

A small Flask application called **Server Info Service** displays:

- Application status
- Environment information
- Company DevOps Portal

The application runs inside a Docker container on port `5000`.

## Architecture

```text
Browser
   ↓
EC2 Public IP:5000
   ↓
Docker Container
   ↓
Flask Application
```

## Project Structure

```text
server-info-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── static/
│   └── style.css
└── templates/
    └── index.html
```

## Dockerfile

The Dockerfile uses:

- `python:3.12-slim`
- `/app` working directory
- `requirements.txt` for Python dependencies
- `APP_ENV=production`
- Port `5000`
- Flask application as the container startup command

## Build the Image

```bash
docker build -t company-server-app .
```

## Run the Container

```bash
docker run -d \
  --name server-app \
  -p 5000:5000 \
  company-server-app
```

## Verify the Deployment

Check the running container:

```bash
docker ps
```

Check application logs:

```bash
docker logs server-app
```

Open the application:

```text
http://<EC2-PUBLIC-IP>:5000
```

Port `5000` must also be allowed in the EC2 Security Group.

## What I Practiced

- Writing a Dockerfile
- Building Docker images
- Running and managing containers
- Docker port mapping
- Docker logs and basic troubleshooting
- Deploying a containerized Flask application
- Linux/Ubuntu server usage
- AWS EC2 Security Groups

## Important Note

This project is created **only for learning and hands-on DevOps practice**.

It is not intended to represent a complete production deployment. For example, a real production Flask application would typically use additional components and security practices such as a production WSGI server, restricted network access, HTTPS, secrets management, monitoring, and other deployment controls.

## Project Information

**Ticket:** DEVOPS-101  
**Role:** Junior DevOps Engineer (Practice Scenario)  
**Platform:** AWS EC2  
**Technologies:** Docker, Flask, Python, Linux, AWS EC2
