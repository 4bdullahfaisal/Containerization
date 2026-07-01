# Docker — Container & Custom Image
**Purpose:** Run your first container and build a custom Docker image

---

## What is Docker?

Docker is a platform to **build, run, and share** applications inside containers.

A container is a lightweight, isolated environment that includes everything needed to run an application.

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
| Image | Template for creating containers |
| Container | Running instance of an image |
| Registry | Stores images (e.g., Docker Hub) |

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

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

### 4. Build the Image

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

## Dockerfile Breakdown

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

| Line | Meaning |
|------|---------|
| `FROM nginx:alpine` | Base image (lightweight nginx) |
| `COPY index.html ...` | Copy file from laptop into container |
| `EXPOSE 80` | (Optional) Document which port container listens on |

---

## Common Docker Commands Summary

```bash
# Images
docker images                  # List images
docker rmi [image-id]          # Remove image
docker build -t name:tag .     # Build image

# Containers
docker run -d -p host:container image
docker ps                      # List running
docker ps -a                   # List all
docker stop [id]               # Stop container
docker rm [id]                 # Remove container
docker logs [id]               # View container logs
docker exec -it [id] bash      # Access container shell

# Cleanup
docker container prune         # Remove stopped containers
docker image prune             # Remove unused images
docker system prune            # Remove everything unused
```

---
