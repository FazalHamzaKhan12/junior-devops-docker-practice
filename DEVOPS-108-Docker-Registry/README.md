# DEVOPS-108 — Docker Registry Practice

A beginner-friendly, hands-on Docker project demonstrating how to build a Java application image, tag it, publish it to Docker Hub, remove it locally, and pull it again on another machine.

> This is a learning project for practicing the Docker Registry workflow. It is not presented as a production-ready Java application.

Docker Hub repository: [fazalhamzakhan/simple_java_docker](https://hub.docker.com/r/fazalhamzakhan/simple_java_docker)

## Project Overview

This project packages a small Java console application into a Docker image. After testing the image locally, the image is tagged with a Docker Hub repository name and pushed to Docker Hub.

The published image can then be pulled and run on another computer or an EC2 server without copying the Java source code manually.

The version used throughout this project is:

```text
fazalhamzakhan/simple_java_docker:v1
```

## Learning Objectives

By completing this project, I practiced how to:

1. Build a Docker image from a Dockerfile.
2. Run and test an image locally.
3. assign a version tag such as `v1`.
4. Tag an image using a Docker Hub repository name.
5. Authenticate with Docker Hub safely.
6. Push an image to Docker Hub.
7. Remove local image tags.
8. Pull an image from Docker Hub.
9. Run the pulled image on another machine.
10. Understand the difference between a local image and a registry image.

## Application Overview

The Java application prints basic information from its running environment:

- Current time
- Operating system
- Java version
- Available CPU cores
- Maximum, total, and free JVM memory
- Whether a Docker environment was detected

Example output:

```text
========================================
       Simple Java Docker App
========================================
Current time : 2026-08-20 12:30:00
Operating OS : Linux
Java version : 21.0.x
CPU cores    : 2
Max memory   : 494 MB
Total memory : 31 MB
Free memory  : 29 MB
Docker status: Java application is running inside Docker.
========================================
```

Values such as time, Java patch version, CPU cores, and memory depend on the machine and container environment.

## Architecture / Workflow

```text
Java Source Code
      ↓
Dockerfile
      ↓
docker build
      ↓
Local Docker Image
      ↓
docker tag
      ↓
docker push
      ↓
Docker Hub Registry
      ↓
docker pull
      ↓
Another Server / EC2
      ↓
docker run
```

Docker Hub acts as the remote registry between the machine that builds the image and another machine that needs to run it.

## Project Structure

```text
DEVOPS-108-Docker-Registry/
├── src/
│   └── Main.java
├── Dockerfile
├── .dockerignore
└── README.md
```

- `src/Main.java` contains the Java application.
- `Dockerfile` defines how Docker builds and starts the image.
- `.dockerignore` keeps unnecessary local files out of the build context.
- `README.md` documents the Docker Registry workflow.

## Dockerfile Explanation

The Dockerfile is intentionally simple:

```dockerfile
FROM eclipse-temurin:21-jdk-alpine

WORKDIR /app

COPY src/Main.java .

RUN javac Main.java

CMD ["java", "Main"]
```

| Instruction | Purpose |
| --- | --- |
| `FROM` | Selects a Java 21 JDK base image. |
| `WORKDIR` | Sets `/app` as the working directory inside the image. |
| `COPY` | Copies the Java source file into the image. |
| `RUN` | Compiles `Main.java` while the image is being built. |
| `CMD` | Starts the compiled Java application when a container runs. |

## Build Image

Run this command from the project directory:

```bash
docker build -t simple_java_docker:v1 .
```

In simple terms:

```text
docker build = create an image
```

Confirm that the image exists locally:

```bash
docker images
```

## Run Image

Test the local image:

```bash
docker run simple_java_docker:v1
```

To remove the stopped container automatically after the Java program finishes, add `--rm`:

```bash
docker run --rm simple_java_docker:v1
```

The `--rm` option removes the container, not the Docker image.

In simple terms:

```text
docker run = create and run a container from an image
```

## Tag Image

Add the Docker Hub repository name to the local image:

```bash
docker tag simple_java_docker:v1 fazalhamzakhan/simple_java_docker:v1
```

In simple terms:

```text
docker tag = give an image a registry/repository/tag name
```

After tagging, these two names can point to the same Docker image ID:

```text
simple_java_docker:v1
fazalhamzakhan/simple_java_docker:v1
```

Tagging does not build or duplicate the image layers. It creates another reference to the same local image.

Verify this by comparing the image IDs:

```bash
docker images
```

## Docker Login

Authenticate before pushing:

```bash
docker login
```

Follow Docker's prompt or browser-based authentication flow. Do not place passwords, personal access tokens, or credentials in this repository or command examples.

Confirm that the Docker Hub repository belongs to the account used during login.

## Push Image to Docker Hub

Upload the registry-tagged image:

```bash
docker push fazalhamzakhan/simple_java_docker:v1
```

In simple terms:

```text
docker push = upload an image to a registry
```

After the push completes, the `v1` image should be visible in the [Docker Hub repository](https://hub.docker.com/r/fazalhamzakhan/simple_java_docker).

## Remove Local Image

Remove both local tags to properly test pulling the image from Docker Hub:

```bash
docker image rm simple_java_docker:v1
docker image rm fazalhamzakhan/simple_java_docker:v1
```

Why remove both? Both names may reference the same local image ID. Removing only one tag can leave the image available through the other tag.

Check the remaining local images:

```bash
docker images
```

If a container still references the image, remove that stopped container before removing the final image tag.

## Pull Image from Docker Hub

Download version `v1` from Docker Hub:

```bash
docker pull fazalhamzakhan/simple_java_docker:v1
```

In simple terms:

```text
docker pull = download an image from a registry
```

The image is now stored in the local Docker image cache again.

## Run Pulled Image

Run the image that was pulled from Docker Hub:

```bash
docker run --rm fazalhamzakhan/simple_java_docker:v1
```

This same command can be used on another Docker-enabled server or EC2 instance after pulling the image.

The shorter command without automatic container cleanup is also valid:

```bash
docker run fazalhamzakhan/simple_java_docker:v1
```

## Docker Image Versioning

A Docker image reference commonly has three important parts:

```text
username/repository:tag
```

For this project:

```text
fazalhamzakhan/simple_java_docker:v1
│                 │                  │
Docker Hub user   Repository         Version tag
```

Tags identify different image versions. Examples could include:

```text
fazalhamzakhan/simple_java_docker:v1
fazalhamzakhan/simple_java_docker:v2
fazalhamzakhan/simple_java_docker:latest
```

Using an explicit tag such as `v1` makes it clear which version is being pulled and run. The `latest` tag is only a tag name; Docker does not automatically determine which image is newest.

## Useful Docker Commands

| Command | Purpose |
| --- | --- |
| `docker build -t simple_java_docker:v1 .` | Build the local versioned image. |
| `docker run --rm simple_java_docker:v1` | Test the local image. |
| `docker images` | List locally stored images. |
| `docker tag SOURCE TARGET` | Add another name and tag to an image. |
| `docker login` | Authenticate with Docker Hub. |
| `docker push IMAGE` | Upload an image to Docker Hub. |
| `docker pull IMAGE` | Download an image from Docker Hub. |
| `docker image inspect IMAGE` | Display detailed image metadata. |
| `docker image rm IMAGE` | Remove a local image reference. |
| `docker ps` | List running containers. |
| `docker ps -a` | List running and stopped containers. |

## What I Learned

This project demonstrated that a Docker image can move through a repeatable registry workflow:

1. Source code and a Dockerfile create a local image.
2. A local image is tested before publishing.
3. A registry-compatible tag identifies the Docker Hub account, repository, and version.
4. Pushing uploads the image layers and tag to Docker Hub.
5. Pulling downloads the published image to another Docker host.
6. Running the pulled image produces the same packaged Java application without rebuilding it from source.

The key difference is:

- A **local Docker image** exists in the Docker image store of one machine.
- A **Docker Registry image** is published remotely so authorized users or servers can pull it.

Docker Hub makes the image portable between a developer machine, another computer, and an EC2 server.

