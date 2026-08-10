# DEVOPS-101: Flask Docker Deployment on AWS EC2

A beginner-friendly **Junior DevOps practice project** for learning Docker, Linux, and AWS EC2.

> This project is for learning and hands-on practice only.

## Scenario

You are working as a **Junior DevOps Engineer**.

A developer has given you a small Flask application called **Server Info Service**.

Your job is to:

- Create a Dockerfile
- Build a Docker image
- Run the application inside a container
- Deploy it on Ubuntu EC2
- Make the website accessible from a browser

---

## Architecture

```text
Browser
   ↓
EC2 Public IP : 5000
   ↓
Docker Container
   ↓
Flask Application
```

---

## Starter Files

```text
DEVOPS-101-flask-docker-ec2/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── README.md
```

The Dockerfile is intentionally not provided.

**Your first task is to create it yourself.**

---

# Your Tasks

### 1. Prepare EC2

- Launch an Ubuntu EC2 instance
- Connect using SSH
- Install Docker
- Verify Docker is running

### 2. Create the Dockerfile

Your Dockerfile should:

- Use `python:3.12-slim`
- Use `/app` as the working directory
- Copy `requirements.txt`
- Install Python dependencies
- Copy the application files
- Set `APP_ENV=production`
- Expose port `5000`
- Start `app.py` when the container starts

### 3. Build the Image

Create a Docker image named:

```text
company-server-app
```

### 4. Run the Container

Create a container named:

```text
server-app
```

Configure:

```text
EC2 Port:       5000
Container Port: 5000
```

Run the container in the background.

### 5. Configure AWS

Configure the EC2 Security Group to allow the required traffic on port:

```text
5000
```

### 6. Test the Application

Open:

```text
http://<EC2-PUBLIC-IP>:5000
```

You should see the **Server Info Service** website.

---

## Verify Your Work

Use Docker commands to check:

- Is the container running?
- Was the image created?
- Are there any errors in the container logs?
- Is port `5000` correctly published?

Try solving these yourself before searching for the answer.

---

## Troubleshooting

If the website doesn't work, investigate in this order:

```text
Flask Application
       ↓
Docker Container
       ↓
Port Mapping
       ↓
EC2 Instance
       ↓
Security Group
       ↓
Browser
```

Useful commands to remember:

```bash
docker ps
docker ps -a
docker logs server-app
docker images
```

---

## Completion Checklist

- [ ] Connected to Ubuntu EC2
- [ ] Docker installed
- [ ] Dockerfile created
- [ ] Image built successfully
- [ ] Container running
- [ ] Port `5000` published
- [ ] EC2 Security Group configured
- [ ] Website accessible from browser
- [ ] Container logs checked
- [ ] No passwords, SSH keys, or AWS credentials committed

---

## Knowledge Check

After completing the project, try answering:

1. What is a Dockerfile?
2. What is the difference between an image and a container?
3. What does `WORKDIR` do?
4. What is the difference between `RUN` and `CMD`?
5. What does `EXPOSE 5000` mean?
6. What does Docker port mapping do?
7. Why must port `5000` also be allowed in the EC2 Security Group?
8. Which command would you use if the container suddenly stopped?

---

## Skills Practiced

- Dockerfile
- Docker images
- Docker containers
- Port mapping
- Docker logs
- Flask
- Linux
- AWS EC2
- Security Groups
- Basic troubleshooting

---

## Important

This is a **practice project**, not a complete production deployment.

Never commit:

- `.pem` files
- SSH private keys
- AWS credentials
- Passwords
- API keys
- Access tokens

---

## Project Information

**Ticket:** DEVOPS-101  
**Level:** Beginner  
**Role:** Junior DevOps Engineer — Practice Scenario  
**Technologies:** Docker, Flask, Python, Linux, AWS EC2

### Next Challenge

After completing this project, continue to:

**DEVOPS-102 — Nginx Static Website Deployment**
