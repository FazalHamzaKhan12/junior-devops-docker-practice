# DEVOPS-103: Flask + MySQL Multi-Container Deployment

A hands-on Docker practice project for beginner and Junior DevOps Engineers.

The goal is to deploy a Flask application and MySQL database in **separate Docker containers** on an Ubuntu AWS EC2 instance.

> This project is for learning and practice only. It is not a production deployment.

---

## Scenario

You are working as a Junior DevOps Engineer.

The development team has provided an **Employee Feedback Application**.

Users can:

1. Open the website
2. Enter their name and feedback
3. Submit the form
4. Flask processes the request
5. MySQL stores the feedback

Your job is to containerize and deploy the application.

---

## Architecture

```text
Browser
   |
   | Port 5000
   v
AWS EC2
   |
   v
Flask Container
   |
   | employee-network
   v
MySQL Container
   |
   v
mysql-data
Docker Volume
```

You will run **two containers**:

```text
employee-app  --->  mysql-db
     |                 |
     +--- employee-network
                       |
                       v
                  mysql-data
```

---

## Project Structure

```text
DEVOPS-103/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── README.md
```

The Dockerfile is intentionally not provided.

**Your task is to create it yourself.**

---

# Your Task

## 1. Prepare the EC2 Server

Launch an Ubuntu EC2 instance and connect using SSH.

Verify Docker:

```bash
docker --version
```

---

## 2. Create a Docker Network

Create a user-defined Docker network named:

```text
employee-network
```

Both Flask and MySQL must use this network.

---

## 3. Create a Docker Volume

Create a named volume:

```text
mysql-data
```

MySQL must store its database files at:

```text
/var/lib/mysql
```

The purpose of the volume is to keep database data separate from the MySQL container.

---

## 4. Deploy MySQL

Use:

```text
Image:              mysql:8.4
Container:          mysql-db
Network:            employee-network
Volume:             mysql-data
Volume destination: /var/lib/mysql
```

Configure MySQL with:

```text
MYSQL_ROOT_PASSWORD=root123
MYSQL_DATABASE=company
MYSQL_USER=appuser
MYSQL_PASSWORD=app123
```

> These credentials are intentionally simple because this is a practice project. Do not use credentials like these in production.

Do **not** publish MySQL port `3306` to the internet.

Flask will communicate with MySQL through the private Docker network.

---

## 5. Create the Flask Dockerfile

Write a Dockerfile that:

- Uses `python:3.12-slim`
- Uses `/app` as the working directory
- Installs dependencies from `requirements.txt`
- Copies the application files
- Exposes port `5000`
- Starts `app.py` automatically

Try writing it yourself before looking for a solution.

---

## 6. Build the Flask Image

Build your Flask Docker image.

Choose a clear image name, for example:

```text
employee-feedback-app
```

Verify it:

```bash
docker images
```

---

## 7. Run the Flask Container

Run the Flask container with:

```text
Container: employee-app
Network:   employee-network
Host Port: 5000
App Port:  5000
```

Pass these environment variables:

```text
DB_HOST=mysql-db
DB_USER=appuser
DB_PASSWORD=app123
DB_NAME=company
```

---

## Important Networking Concept

Do not use:

```text
DB_HOST=localhost
```

Inside the Flask container, `localhost` refers to the **Flask container itself**.

The MySQL server is running in another container.

Because both containers use `employee-network`, Flask can connect using:

```text
DB_HOST=mysql-db
```

Docker provides container-name resolution on the user-defined network.

---

## 8. Verify the Containers

Check:

```bash
docker ps
```

You should have two running containers:

```text
employee-app
mysql-db
```

Check logs:

```bash
docker logs employee-app
docker logs mysql-db
```

---

## 9. Test the Database Connection

From EC2:

```bash
curl http://localhost:5000/health
```

A successful result should indicate:

```json
{
  "application": "healthy",
  "database": "connected"
}
```

---

## 10. Configure the EC2 Security Group

Allow inbound TCP traffic to:

```text
Port: 5000
```

Only expose the application port required for this exercise.

Do not expose MySQL port `3306` publicly.

---

## 11. Open the Application

Visit:

```text
http://<EC2-PUBLIC-IP>:5000
```

You should see the Employee Feedback application.

Submit a few feedback records.

---

# Verify Records in MySQL

Enter the MySQL container:

```bash
docker exec -it mysql-db mysql -u appuser -p
```

Then use:

```sql
SHOW DATABASES;

USE company;

SHOW TABLES;

SELECT * FROM feedback;
```

You should see the feedback submitted through the website.

---

# Persistence Challenge

Now prove that your Docker volume works.

### Step 1

Submit several feedback records.

### Step 2

Verify them:

```sql
SELECT * FROM feedback;
```

### Step 3

Remove the MySQL container.

**Do not remove `mysql-data`.**

### Step 4

Create the MySQL container again using:

```text
mysql-data:/var/lib/mysql
```

### Step 5

Check the database again.

Your previous feedback should still exist.

This demonstrates:

```text
Container deleted
       |
       v
Database volume remains
       |
       v
New MySQL container
       |
       v
Same database data
```

---

# Troubleshooting

If something fails, investigate before deleting everything.

### Check all containers

```bash
docker ps -a
```

### Check Flask

```bash
docker logs employee-app
```

### Check MySQL

```bash
docker logs mysql-db
```

### Check the network

```bash
docker network inspect employee-network
```

### Check the volume

```bash
docker volume inspect mysql-data
```

### Check the health endpoint

```bash
curl http://localhost:5000/health
```

A useful troubleshooting path is:

```text
Flask
  |
  v
Environment Variables
  |
  v
Docker Network
  |
  v
MySQL
  |
  v
Docker Volume
```

---

# Acceptance Criteria

The project is complete when:

- [ ] Flask Dockerfile is created
- [ ] Flask image builds successfully
- [ ] `employee-network` exists
- [ ] `mysql-data` exists
- [ ] Flask and MySQL run in separate containers
- [ ] Both containers use `employee-network`
- [ ] Flask container is named `employee-app`
- [ ] MySQL container is named `mysql-db`
- [ ] MySQL uses `mysql:8.4`
- [ ] Flask connects using `DB_HOST=mysql-db`
- [ ] EC2 port `5000` maps to Flask port `5000`
- [ ] MySQL port `3306` is not publicly published
- [ ] Feedback is stored successfully
- [ ] Feedback survives MySQL container recreation
- [ ] Application works through the EC2 public IP
- [ ] No private keys or real credentials are committed

---

# Required Proof

Capture the output of:

```bash
docker images
docker ps
docker network inspect employee-network
docker volume inspect mysql-data
docker logs employee-app
docker logs mysql-db
```

Test:

```bash
curl http://localhost:5000/health
```

Also capture a browser screenshot showing the application running from the EC2 public IP.

---

# Knowledge Check

After completing the project, try answering these without looking at your notes:

1. Why does `DB_HOST=localhost` not work here?
2. Why can Flask use `mysql-db` as a hostname?
3. What is a user-defined Docker network?
4. Why don't we publish MySQL port `3306`?
5. Why does MySQL need a Docker volume?
6. What does `/var/lib/mysql` contain?
7. What is the difference between an image and a container?
8. What does `-p 5000:5000` do?
9. What happens if the MySQL container is deleted but the volume remains?
10. Which commands would you use first if Flask could not connect to MySQL?

---

# Skills Practiced

- Dockerfile creation
- Docker images
- Docker containers
- Multi-container applications
- Docker networking
- Container DNS/name resolution
- Environment variables
- MySQL containers
- Docker named volumes
- Persistent database storage
- Docker troubleshooting
- Linux server administration
- AWS EC2
- EC2 Security Groups

---

# Learning Progression

```text
DEVOPS-101
Flask + Docker + EC2
        |
        v
DEVOPS-102
Nginx + Docker + EC2
        |
        v
DEVOPS-103
Flask + MySQL + Docker Network + Volume
        |
        v
DEVOPS-104
Docker Compose
```

---

## Project Information

**Ticket:** DEVOPS-103  
**Role:** Junior DevOps Engineer (Practice Scenario)  
**Difficulty:** Beginner / Intermediate  
**Environment:** Ubuntu AWS EC2  
**Technologies:** Docker, Flask, MySQL, Linux, AWS EC2  
**Main Focus:** Docker Networking + Persistent Storage

---

## Disclaimer

This project is designed for educational and hands-on DevOps practice.

The architecture is intentionally simple. A real production deployment would require additional considerations such as secrets management, HTTPS, restricted network access, database backups, monitoring, health checks, production WSGI servers, and other security and reliability controls.
