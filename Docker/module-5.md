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
|------|---------|----------|
| **Public Registry** | Sharing open-source images | Docker Hub
| **Private Registry** | Storing proprietary images | AWS ECR, Azure ACR, GCR
| **Self-Hosted Registry** | Full control, offline environments | Your own server


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

```bash
# Search for an image
docker search nginx

# Pull an image
docker pull nginx:alpine

## Push to Docker Hub (requires login)

# 1. Login
docker login

# 2. Build image
docker build -t my-web-app .

# 3. Tag image with your Docker Hub username
docker tag my-web-app username/my-web-app:latest

# 4. Push to Docker Hub
docker push username/my-web-app:latest

# 5. Verify
docker search username/my-web-app
```
---

### Tagging Format

```
[registry/][username/]image-name[:tag]
```

| Part | Example |
|------|---------|
| Registry | `docker.io` (default) |
| Username | `abdullah` |
| Image name | `my-app` |
| Tag | `latest`, `v1.0`, `1.0.0` |

---

## Private Registry (Self-Hosted)

Private registries are self-hosted for internal use

Run your own registry locally.

### Run a Local Registry

```bash
docker run -d -p 5000:5000 --name registry registry:2
```

**or**

```bash
docker run -d \
  --name registry \
  -p 5000:5000 \
  registry:2
```

### Tag and Push to Local Registry

```bash

# Login to registry
docker login
docker login localhost:5000

# Start local registry
docker run -d -p 5000:5000 --name registry registry:2

# Build an image
docker build -t my-app .

# Tag it for local registry
# docker tag source-image registry-url/repo:tag 
docker tag my-app localhost:5000/my-app:latest
   
# Push to local registry
# docker push registry-url/repo:tag
docker push localhost:5000/my-app:latest
                

# Pull from local registry
# docker pull registry-url/repo:tag 
docker pull localhost:5000/my-app:latest        

# 6. Check registry contents
curl http://localhost:5000/v2/_catalog

# Logout
docker logout

```

---


## Private Registry with Docker Compose

```yaml
version: '3.8'

services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    volumes:
      - registry_data:/var/lib/registry

volumes:
  registry_data:
```

Start:

```bash
docker compose up -d
```
---

## Remove Images from Registry

```bash
# List repositories
curl -X GET http://localhost:5000/v2/_catalog

# Delete image (registry v2)
curl -X DELETE http://localhost:5000/v2/my-app/manifests/{digest}
```
---

### CI/CD Workflow:

```yaml
# GitLab CI example
# .gitlab-ci.yml
build:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
deploy:
  script:
    - docker pull $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    - docker run -d -p 8080:80 $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
```

---

## Commands Summary

```bash
docker login                                             # Login to Docker Hub
docker logout                                            # Logout
docker tag source registry/repo:tag                      # Tag image for registry
docker push registry/repo:tag                            # Push to registry
docker pull registry/repo:tag                            # Pull from registry
docker search image-name                                 # search image

# Local registry
docker run -d -p 5000:5000 --name registry registry:2    # Run local registry
docker push localhost:5000/image                         # Push to local registry
docker pull localhost:5000/image                         # Pull from local registry
curl http://localhost:5000/v2/_catalog                   # List repositories
```

---

---
