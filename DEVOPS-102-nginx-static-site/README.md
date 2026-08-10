# DEVOPS-102: Nginx Static Website Deployment with Docker & AWS EC2

A beginner-friendly, hands-on DevOps practice project for learning how to containerize a static website with **Docker + Nginx** and deploy it on an **Ubuntu AWS EC2 instance**.

> This repository is created for learning and practice purposes. It is not intended to represent a complete production deployment.

## Project Scenario

Imagine you have joined a company as a **Junior DevOps Engineer**.

The frontend team has completed a static company website containing HTML, CSS, and images.

Your task is to:

- Containerize the website using Nginx
- Build a Docker image
- Run the website inside a container
- Publish it on port `80`
- Deploy it to an Ubuntu EC2 instance
- Make it accessible through the EC2 public IP

The goal is to complete the deployment yourself rather than simply copy Docker commands.

---

## Architecture

```text
User Browser
     |
     | HTTP :80
     v
AWS EC2 Instance
     |
     | Port 80
     v
Docker Container
     |
     v
Nginx Web Server
     |
     v
Static HTML / CSS / Images
```

---

## Starter Project Structure

```text
company-website/
├── index.html
├── css/
│   └── style.css
├── images/
├── Dockerfile
└── README.md
```

If you're using this repository as a practice challenge, try writing the `Dockerfile` yourself before looking at any completed solution.

---

# Your Task

## 1. Prepare an EC2 Instance

Launch an Ubuntu EC2 instance and connect using SSH.

Make sure Docker is installed and running.

Verify:

```bash
docker --version
```

---

## 2. Write the Dockerfile

Create a Dockerfile that:

- Uses an official lightweight Nginx image
- Copies the website files into the Nginx document root
- Exposes HTTP port `80`
- Uses the default Nginx container startup behavior

### Hint

The official Nginx image serves static files from:

```text
/usr/share/nginx/html/
```

Try writing the Dockerfile yourself before continuing.

---

## 3. Build the Docker Image

Build an image named:

```text
company-nginx-site
```

You should be able to verify it with:

```bash
docker images
```

---

## 4. Run the Container

Create a container named:

```text
company-website
```

Requirements:

```text
EC2 Host Port:     80
Container Port:    80
```

Run the container in detached mode.

---

## 5. Verify the Container

Check that the container is running:

```bash
docker ps
```

Check Nginx logs:

```bash
docker logs company-website
```

Test directly from the EC2 instance:

```bash
curl http://localhost
```

If HTML is returned, your container and Nginx server are working.

---

## 6. Configure AWS Security Group

Allow inbound HTTP traffic on:

```text
Protocol: TCP
Port:     80
```

For practice, configure the source according to your access requirements.

Do not expose unnecessary ports.

---

## 7. Open the Website

Find your EC2 public IPv4 address and visit:

```text
http://<EC2-PUBLIC-IP>
```

You should now see the static website being served from the Nginx Docker container.

---

# Expected Result

```text
Browser
   ↓
EC2 Public IP
   ↓
Port 80
   ↓
Docker Container
   ↓
Nginx
   ↓
index.html
```

---

# Troubleshooting Challenge

If the website doesn't work, don't immediately delete everything and start again.

Investigate the problem.

### Is the container running?

```bash
docker ps -a
```

### What does Nginx say?

```bash
docker logs company-website
```

### Does it work from inside EC2?

```bash
curl http://localhost
```

### Is port 80 published?

```bash
docker ps
```

Then check your AWS EC2 Security Group.

A useful troubleshooting order is:

```text
Application Files
      ↓
Nginx
      ↓
Docker Container
      ↓
Docker Port Mapping
      ↓
EC2
      ↓
Security Group
      ↓
Internet
```

---

# Acceptance Criteria

Your challenge is complete when:

- [ ] Dockerfile is written
- [ ] Official Nginx image is used
- [ ] Docker image builds successfully
- [ ] Image is named `company-nginx-site`
- [ ] Container is named `company-website`
- [ ] Container remains running
- [ ] Host port `80` maps to container port `80`
- [ ] `curl http://localhost` returns the website
- [ ] EC2 Security Group permits required HTTP traffic
- [ ] Website works through the EC2 public IP
- [ ] No credentials, SSH keys, or secrets are committed

---

# Knowledge Check

After completing the project, try answering these without looking at your notes:

1. What is Nginx?
2. Why doesn't this application need Python or Node.js?
3. Where does Nginx store its default website files?
4. What does `EXPOSE 80` mean?
5. Does `EXPOSE 80` automatically publish port 80?
6. What does `-p 80:80` do?
7. Why does AWS Security Group need to allow port 80?
8. What happens if the main Nginx process stops?
9. What is the difference between a Docker image and container?
10. Which commands would you use first if the website stopped working?

---

# Skills Practiced

This project helps beginners practice:

- Dockerfile creation
- Docker images
- Docker containers
- Nginx basics
- Static website hosting
- Docker port publishing
- Container logs
- Basic Docker troubleshooting
- Linux/Ubuntu server administration
- AWS EC2
- AWS Security Groups
- HTTP port 80

---

# Security Note

Never commit:

```text
.pem files
SSH private keys
AWS credentials
Passwords
Access tokens
.env files containing secrets
```

Use a `.gitignore` where appropriate.

---

# Practice Progression

If you completed this project successfully, a good learning path is:

```text
DEVOPS-101
Flask + Docker + EC2
        ↓
DEVOPS-102
Nginx + Docker + EC2
        ↓
DEVOPS-103
Multi-Container Application
        ↓
DEVOPS-104
Docker Compose
```

---

## Project Information

**Ticket:** DEVOPS-102  
**Role:** Junior DevOps Engineer (Practice Scenario)  
**Difficulty:** Beginner  
**Environment:** Ubuntu AWS EC2  
**Technologies:** Docker, Nginx, Linux, AWS EC2, HTML/CSS

---

## Disclaimer

This project is designed for **educational and hands-on DevOps practice**.

The architecture is intentionally kept simple so beginners can understand Docker, Nginx, networking, and EC2 deployment fundamentals before moving to more production-oriented architectures.
