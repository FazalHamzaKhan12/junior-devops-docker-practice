# Junior DevOps Docker Practice

Hands-on Docker projects created while learning DevOps on Linux and AWS EC2.

This repository documents my practical Docker learning journey, starting from basic containerization and progressing toward multi-container applications, Docker Compose, reverse proxies, registries, and more advanced Docker concepts.

## Projects

| Project | Topic | Technologies |
|---|---|---|
| DEVOPS-101 | Flask Docker Deployment | Flask, Docker, EC2 |
| DEVOPS-102 | Static Website Container | Nginx, Docker, EC2 |
| DEVOPS-103 | Two-Tier Application | Flask, MySQL, Docker Network |
| DEVOPS-104 | Three-Tier Application | Nginx, Flask, MySQL |
| DEVOPS-105 | Docker Compose Practice | Flask, MySQL, Docker Compose |
| DEVOPS-106 | FastAPI Two-Tier Application | FastAPI, MySQL, Docker Compose |
| DEVOPS-107 | URL Shortener | Nginx, Flask, Redis, Docker Compose |
| DEVOPS-108 | Docker Registry Practice | Java, Docker Hub, Image Registry |

## Learning Progression

```text
Dockerfile
    ↓
Images & Containers
    ↓
Ports & Networking
    ↓
Volumes
    ↓
Multi-Container Applications
    ↓
Nginx Reverse Proxy
    ↓
Docker Compose
    ↓
Healthchecks & Dependencies
    ↓
Docker Registry / Docker Hub
    ↓
More Advanced Docker Topics
```

## Skills Practiced

- Dockerfiles
- Docker images and containers
- Port publishing
- Docker networking
- Docker volumes
- Environment variables
- Container-to-container communication
- Docker Compose
- Healthchecks
- Service dependencies
- Nginx reverse proxy
- Flask and FastAPI deployments
- MySQL and Redis containers
- Docker image tagging
- Docker Hub push/pull workflow
- AWS EC2 deployment
- Container troubleshooting

## Docker Registry Practice

DEVOPS-108 introduced the Docker Registry workflow:

```text
Source Code
    ↓
Docker Build
    ↓
Local Image
    ↓
Docker Tag
    ↓
Docker Push
    ↓
Docker Hub
    ↓
Docker Pull
    ↓
Run Container
```

Docker Hub image:

`fazalhamzakhan/simple_java_docker:v1`

## How I Use This Repository

Each project has its own folder with the files and documentation needed for that exercise.

The goal is to solve the projects through hands-on practice rather than only following copy-paste tutorials.

## Important

This repository is for learning and practice. Some configurations are intentionally simplified and should not be considered production-ready.

Never commit:

- Credentials
- API/access tokens
- SSH private keys
- `.pem` files
- Production passwords
- `.env` files containing secrets

## Next

More projects will be added as I continue learning:

- Multi-stage Docker builds
- Docker image optimization
- Docker security basics
- CI/CD
- Kubernetes
