# DEVOPS-102: Nginx Static Website Deployment on AWS EC2

A beginner-friendly **Junior DevOps practice project** for learning Docker, Nginx, Linux, and AWS EC2.

> This project is for learning and hands-on practice only.

## Scenario

You are working as a **Junior DevOps Engineer**.

The frontend team has given you a completed static company website containing HTML, CSS, and images.

Your job is to:

- Create a Dockerfile
- Containerize the website using Nginx
- Build a Docker image
- Run the website inside a container
- Deploy it on Ubuntu EC2
- Make it accessible through the internet

---

## Architecture

```text
Browser
   ↓
EC2 Public IP : 80
   ↓
Docker Container
   ↓
Nginx
   ↓
HTML / CSS / Images
```

---

## Starter Files

```text
DEVOPS-102-nginx-static-site/
├── index.html
├── css/
│   └── style.css
├── images/
└── README.md
```

The Dockerfile is intentionally not provided.

**Your first task is to create it yourself.**

---

# Your Tasks

## 1. Prepare EC2

- Launch or use an Ubuntu EC2 instance
- Connect using SSH
- Install Docker if needed
- Verify Docker is running

Check:

```bash
docker --version
```

---

## 2. Create the Dockerfile

Your Dockerfile should:

- Use an official lightweight Nginx image
- Copy the website files into the Nginx web directory
- Expose port `80`
- Allow the official Nginx image to handle container startup

### Hint

Nginx serves its default static website from:

```text
/usr/share/nginx/html/
```

Try creating the Dockerfile yourself.

---

## 3. Build the Image

Create a Docker image named:

```text
company-nginx-site
```

Verify that the image was created successfully.

---

## 4. Run the Container

Create a container named:

```text
company-website
```

Configure:

```text
EC2 Port:       80
Container Port: 80
```

Run the container in the background.

---

## 5. Test from EC2

First check that the container is running.

Then test Nginx directly from the EC2 instance:

```bash
curl http://localhost
```

If you receive your HTML, the container and Nginx are working.

---

## 6. Configure AWS

Configure the EC2 Security Group to allow required HTTP traffic on:

```text
Port: 80
Protocol: TCP
```

Do not expose unnecessary ports.

---

## 7. Test from Browser

Open:

```text
http://<EC2-PUBLIC-IP>
```

You should see the company website.

---

# Expected Result

```text
Internet
   ↓
EC2 :80
   ↓
Docker :80
   ↓
Nginx
   ↓
index.html
```

---

# Troubleshooting

If the website doesn't work, don't immediately delete the container.

Investigate the problem.

Useful commands:

```bash
docker ps
docker ps -a
docker logs company-website
docker images
curl http://localhost
```

Troubleshoot in this order:

```text
Website Files
     ↓
Nginx
     ↓
Container
     ↓
Port Mapping
     ↓
EC2
     ↓
Security Group
     ↓
Browser
```

---

# Completion Checklist

- [ ] Connected to Ubuntu EC2
- [ ] Docker installed
- [ ] Dockerfile created independently
- [ ] Official Nginx image used
- [ ] Docker image built successfully
- [ ] Container running
- [ ] Port `80` published
- [ ] `curl http://localhost` works
- [ ] EC2 Security Group configured
- [ ] Website accessible through EC2 public IP
- [ ] Container logs checked
- [ ] No credentials or SSH keys committed

---

# Knowledge Check

After completing the project, try answering:

1. What is Nginx?
2. Why don't we need Python or Flask for this website?
3. Where does Nginx serve static files from?
4. What does `EXPOSE 80` mean?
5. Does `EXPOSE 80` publish the port automatically?
6. What does port mapping do?
7. Why must port `80` also be allowed in the EC2 Security Group?
8. What happens if the main Nginx process stops?
9. What is the difference between a Docker image and container?
10. Which command would you check first if the container stopped?

---

# Skills Practiced

- Dockerfile
- Docker images
- Docker containers
- Nginx basics
- Static website hosting
- Port mapping
- Docker logs
- Linux
- AWS EC2
- Security Groups
- Basic troubleshooting

---

# Important

This is a **practice project**, not a complete production deployment.

Never commit:

- `.pem` files
- SSH private keys
- AWS credentials
- Passwords
- API keys
- Access tokens
- Secrets

---

## Project Information

**Ticket:** DEVOPS-102  
**Level:** Beginner  
**Role:** Junior DevOps Engineer — Practice Scenario  
**Technologies:** Docker, Nginx, Linux, AWS EC2, HTML/CSS

### Previous Challenge

**DEVOPS-101 — Flask Docker Deployment**

### Next Challenge

**DEVOPS-103 — Two-Container Application with Docker Networking**
