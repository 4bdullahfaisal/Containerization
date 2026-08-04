# Docker — Docker Registry

---

## What is a Docker Registry?

A **Docker Registry** is a storage system for Docker images, used to share and distribute container images

**Analogy:** Docker Registry is like GitHub for Docker images.

| Component | Purpose |
|-----------|---------|
| **Registry** | Stores and distributes images |
| **Repository** | Collection of related images (e.g., `nginx`) |
| **Tag** | Version of an image (e.g., `nginx:alpine`) |
| **Image** | The actual packaged application |

---

## Types of Registries

| Type | Use Case | Example |
|------|----------|---------|
| **Public Registry** | Sharing open-source images | Docker Hub |
| **Private Registry** | Storing proprietary images | AWS ECR, Azure ACR, GCR |
| **Self-Hosted Registry** | Full control, offline environments | Your own server |

---

## Registry Use Cases

| Use Case | Why |
|----------|-----|
| **Team sharing** | Share images within team without making them public |
| **CI/CD** | Push built images from pipelines |
| **Air-gapped** | Private networks with no internet access |
| **Version control** | Store different versions of your app |
| **Security** | Keep proprietary images private |

---

## Docker Hub (Public Registry)

Docker Hub is the default public registry.

---

### Login to Docker Hub

```bash
docker login
```

---

### Search and Pull Images

```bash
# Search for an image
docker search nginx

# Pull an image
docker pull nginx:alpine

# Pull from your own repository
docker pull username/my-app:latest
```

---

### Build Local Image

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
```

```bash
# Build from your Dockerfile
docker build -t my-app .

# Check your images
docker images
```

---

### Step 5: Tag Image for Docker Hub

```bash
#docker tag local-image username/repository:tag
docker tag my-app:latest username/my-app:latest

# Check tagged image
docker images | grep username
```

---

### Step 6: Push to Docker Hub

```bash
docker push username/my-app:latest
```

---

### Step 7: Verify on Docker Hub

1. Go to: **https://hub.docker.com**
2. Click **"Repositories"**
3. You'll see your image

---

### Step 8: Pull and Run from Docker Hub

```bash
# Pull from Docker Hub
docker pull username/my-app:latest

# Run it
docker run -d -p 8080:80 username/my-app:latest
```

---

## Tagging Format

```
[registry/][username/]image-name[:tag]
```

| Part | Example |
|------|---------|
| Registry | `docker.io` (default) |
| Username | `abdullah` |
| Image name | `nginx-site` |
| Tag | `latest`, `v1.0`, `1.0.0` |

```text
docker tag nginx-site:latest abdullah/first-repo:latest
               │           │        │           │
               │           │        │           └── Tag (version)
               │           │        └── Repository name (on Docker Hub)
               │           └── Tag (local version)
               └── Local image name
```

### Multiple Tags (Versions)

```bash
# Tag with different versions
docker tag my-app:latest username/my-app:latest
docker tag my-app:latest username/my-app:v1.0
docker tag my-app:latest username/my-app:stable

# Push all versions
docker push username/my-app:latest
docker push username/my-app:v1.0
docker push username/my-app:stable

# Or push all at once
docker push username/my-app --all-tags
```

---

## Part 2: Private Self-Hosted Registry

Private registries are self-hosted for internal use.

### Step 1: Run Local Registry

```bash
docker run -d -p 5000:5000 --name registry registry:2

# Check it's running
docker ps | grep registry
```

---

### Step 2: Build an Image

```bash
docker build -t my-app .
```

---

### Step 3: Tag for Local Registry

```bash
docker tag my-app localhost:5000/my-app:latest
```

---

### Step 4: Push to Local Registry

```bash
docker push localhost:5000/my-app:latest
```

---

### Step 5: Pull from Local Registry

```bash
docker pull localhost:5000/my-app:latest
```

---

### Step 6: Check Registry Contents

```bash
curl http://localhost:5000/v2/_catalog
```

---

### Step 7: Stop Registry

```bash
docker stop registry
docker rm registry
docker rm -v registry   # Remove with data
```

---

## Private Registry with Docker Compose

### docker-compose.yml

```yaml
version: '3.8'

services:
  registry:
    image: registry:2
    container_name: private-registry
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - registry_data:/var/lib/registry

volumes:
  registry_data:
```

### Start Registry

```bash
docker compose up -d
```

### Push to Compose Registry

```bash
docker tag my-app localhost:5000/my-app:latest
docker push localhost:5000/my-app:latest
```

---

## Remove Images from Registry

```bash
# List repositories
curl -X GET http://localhost:5000/v2/_catalog

# List tags
curl -X GET http://localhost:5000/v2/my-app/tags/list

# Delete image (need digest)
curl -X DELETE http://localhost:5000/v2/my-app/manifests/{digest}
```

---

## CI/CD Pipeline Integration

### GitLab CI Example

```yaml
# .gitlab-ci.yml

stages:
  - build
  - push
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .

push:
  stage: push
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $DOCKER_IMAGE

deploy:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker pull $DOCKER_IMAGE
    - docker run -d -p 8080:80 $DOCKER_IMAGE
  only:
    - main
```

---

## Commands Summary

```bash
# Login/Logout
docker login                                             # Login to Docker Hub
docker logout                                            # Logout

# Tagging
docker tag source registry/repo:tag                      # Tag image for registry
docker tag my-app username/my-app:latest                 # Tag for Docker Hub
docker tag my-app localhost:5000/my-app:latest          # Tag for local registry

# Push
docker push registry/repo:tag                            # Push to registry
docker push username/my-app:latest                       # Push to Docker Hub
docker push localhost:5000/my-app:latest                # Push to local registry

# Pull
docker pull registry/repo:tag                            # Pull from registry
docker pull username/my-app:latest                       # Pull from Docker Hub
docker pull localhost:5000/my-app:latest                # Pull from local registry

# Search
docker search image-name                                 # Search Docker Hub

# Local Registry
docker run -d -p 5000:5000 --name registry registry:2    # Run local registry
docker stop registry                                     # Stop registry
docker rm registry                                       # Remove registry
curl http://localhost:5000/v2/_catalog                   # List repositories

# Manage Images
docker images                                            # List local images
docker rmi username/my-app:latest                        # Remove local image
docker rmi $(docker images -q)                           # Remove all images
```

---

## Summary of Complete Workflow Table

| Command | Purpose |
|---------|---------|
| `docker login` | Login to Docker Hub |
| `docker build -t name .` | Build image locally |
| `docker tag old new` | Tag for registry |
| `docker push name` | Upload to registry |
| `docker pull name` | Download from registry |
| `docker search name` | Search Docker Hub |

---

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `denied: requested access to the resource is denied` | Run `docker login` first |
| `repository name must be lowercase` | Use lowercase only |
| `no basic auth credentials` | `docker logout` then `docker login` |
| `unauthorized: authentication required` | Check username in tag is correct |
| `image not found locally` | Build image first with `docker build` |

---
