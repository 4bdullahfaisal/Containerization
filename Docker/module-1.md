# Docker — Container & Custom Image

**Purpose:** Run your first container and build a custom Docker image

---

## What is Docker?

`Docker` is a platform to **build, run, and share** applications inside containers.

**or**

`Docker` is a platform that lets you package applications and their dependencies into standardized units called containers.

- Containers are running instances of Docker images.

A `Container` is a lightweight, isolated environment that includes everything needed to run an application.

**Analogy:** Docker is like a shipping container — it packages your app and its dependencies so it runs the same anywhere.

---

## Docker vs Virtual Machine

| Feature | Docker Container | Virtual Machine |
|---------|------------------|-----------------|
| Size | MBs | GBs |
| Startup time | Seconds | Minutes |
| OS | Shares host kernel | Full OS |
| Resource usage | Lightweight | Heavy |

---

## Docker Architecture

| Component | What it does |
|-----------|--------------|
| Docker Client | Command line tool (`docker`) |
| Docker Daemon | Runs on host, manages containers |
| Dockerfile | Script for building images |
| Image | Template for creating containers |
| Container | Running instance of an image |
| Volumes | Persistent data storage |
| Networks | Container communication |
| Registry | Stores images (e.g., Docker Hub) |
| Docker Compose | Multi-container orchestration |

---

## First Docker Commands

```bash
# Check Docker version
docker --version

# Run a test container
docker run hello-world

# Run nginx web server in the background (-d)
docker run -d -p 80:80 nginx

# Run nginx on a custom port
docker run -d -p 8080:80 nginx
```

### Explanation of `docker run -d -p 8080:80 nginx`

| Part | Meaning |
|------|---------|
| `docker run` | Start a new container |
| `-d` | Detached mode (runs in background) |
| `-p 8080:80` | Map port 8080 on host → port 80 inside container |
| `nginx` | Image to use |

---

## Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a running container
docker stop [container-id]

# Remove a stopped container
docker rm [container-id]

# Remove all stopped containers
docker container prune
```

---

## Building a Custom Image

### 1. Create Project Folder

```bash
mkdir my-web-app
cd my-web-app
```

### 2. Create `index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>My First Docker App</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
    </style>
</head>
<body>
    <h1>🚀 My First Docker App</h1>
    <p>This container is running a custom web page.</p>
</body>
</html>
```

### 3. Create `Dockerfile`

A Dockerfile is a **text document** containing instructions to build a Docker image. It's the blueprint for creating containers.

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

| Line | Meaning |
|------|---------|
| `FROM nginx:alpine` | Base image (lightweight nginx) |
| `COPY index.html ...` | Copy file from laptop into container |

### 4. Build the Image

Docker images are **read-only templates** containing instructions for creating containers. They're built from Dockerfiles and stored in registries.

```bash
docker build -t my-web-app .
```

| Part | Meaning |
|------|---------|
| `docker build` | Build an image from a Dockerfile |
| `-t my-web-app` | Tag (name) the image |
| `.` | Use current directory as build context |

### 5. Run the Custom Image

```bash
docker run -d -p 8080:8080 my-web-app
```

Open `http://localhost:8080` in your browser.

---

## Dockerfile Common Instructions Reference

| Instruction | Purpose | Example |
|-------------|---------|---------|
| **FROM** | Sets base image | `FROM nginx:alpine` |
| **RUN** | Executes commands during build | `RUN apt-get update` |
| **COPY** | Copies files from host to image | `COPY index.html /usr/share/...` |
| **ADD** | Like COPY, but can unpack archives | `ADD app.tar.gz /app/` |
| **WORKDIR** | Sets working directory | `WORKDIR /app` |
| **ENV** | Sets environment variables | `ENV PORT=8080` |
| **EXPOSE** | Documents port exposure | `EXPOSE 80` |
| **CMD** | Default command to run | `CMD ["python", "app.py"]` |
| **ENTRYPOINT** | Main command (can't be overridden) | `ENTRYPOINT ["java", "-jar"]` |
| **USER** | Sets user for running container | `USER appuser` |
| **ARG** | Build-time variables | `ARG VERSION=latest` |

---

## Docker Daemon

The Docker daemon (`dockerd`) is the background service managing Docker objects on the host system.

```bash
# Start daemon
sudo systemctl start docker

# Stop daemon
sudo systemctl stop docker

# Restart daemon
sudo systemctl restart docker

# Check daemon status
sudo systemctl status docker

# View daemon logs
journalctl -u docker.service -f

# Debug mode
docker -D info
```

---

## Common Docker Commands Summary

```bash
# Containers
docker run -d -p host:container image
docker ps                      # List running
docker ps -a                   # List all
docker stop [id]               # Stop container
docker rm [id]                 # Remove container
docker logs [id]               # View container logs
docker exec -it [id] bash      # Access container shell

# Images
docker images                  # List images
docker rmi [image-id]          # Remove image
docker build -t name:tag .     # Build image

# Cleanup
docker container prune         # Remove stopped containers
docker image prune             # Remove unused images
docker system prune            # Remove everything unused
```

---
