# Docker — Volumes & Persistent Data

---

## Why Volumes?

Containers are ephemeral (disposable). When a container is deleted, all data inside it is lost unless you use volumes.

| Scenario | Without Volume | With Volume |
|----------|----------------|-------------|
| Container restarts | Data lost | Data kept |
| Container deleted | Data gone | Data safe |
| Share between containers | Not possible | Yes |
| Backup / restore | Manual only | Easy |

---

## 3 Ways to Store Data in Docker

| Type | Use Case | Example |
|------|----------|---------|
| Bind Mount | Live development (edit files on laptop, container sees changes) | `-v ./app:/usr/share/nginx/html` |
| Named Volume | Persistent app data (databases, uploads) | `-v app_data:/var/lib/mysql` |
| Tmpfs Mount | Temporary, in-memory (caches, secrets) | `--tmpfs /tmp` |

---

## Bind Mount (Live Editing)

Edit files on your laptop and see changes instantly in the container.

```bash
# Create a folder and HTML file
mkdir live-app
cd live-app
echo "<h1>Live Reload!</h1>" > index.html

# Run nginx with bind mount
docker run -d -p 8080:80 -v $(pwd):/usr/share/nginx/html nginx
```

Now edit `index.html` on your laptop and refresh the browser — changes appear instantly.

---

## Named Volume (Database Persistence)

Named volumes are managed by Docker and persist data even after container deletion.

```bash
# Create a named volume
docker volume create mysql-data

# Run MySQL with that volume
docker run -d \
  --name mysql-demo \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -v mysql-data:/var/lib/mysql \
  mysql:8.0

# Stop and remove the container
docker stop mysql-demo
docker rm mysql-demo

# Run a new container with the same volume — data is still there
docker run -d \
  --name mysql-new \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -v mysql-data:/var/lib/mysql \
  mysql:8.0
```

---

## Tmpfs Mount (Temporary Data)

Data is stored in memory only — lost when container stops.

```bash
docker run -d \
  --name cache-demo \
  --tmpfs /tmp \
  nginx
```

---

## Volume Commands

```bash
docker volume ls                     # List volumes
docker volume create myvol           # Create a volume
docker volume inspect myvol          # Show details
docker volume rm myvol               # Delete a volume
docker volume prune                  # Remove unused volumes
```

---

## Docker Compose with Volumes (Production Style)

```yaml
version: '3.8'

services:
  app:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html   # bind mount (dev)
      - app-logs:/var/log/nginx        # named volume

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
    volumes:
      - db-data:/var/lib/mysql          # named volume

volumes:
  db-data:
  app-logs:
```

---

## Bind Mount vs Named Volume

| Feature | Bind Mount | Named Volume |
|---------|------------|--------------|
| Managed by Docker | No | Yes |
| Path specified by user | Yes (absolute path) | No (Docker chooses) |
| Works on all OS | Yes (with path changes) | Yes |
| Backup | Manual | Easy with `docker run --rm -v` |
| Use case | Development | Production |

---

## Backup and Restore Volumes

### Backup a volume
```bash
docker run --rm -v mydata:/source -v $(pwd):/backup alpine tar czf /backup/mydata-backup.tar.gz -C /source .
```

### Restore a volume
```bash
docker run --rm -v mydata:/target -v $(pwd):/backup alpine tar xzf /backup/mydata-backup.tar.gz -C /target
```

---

## When to Use What

| Need | Solution |
|------|----------|
| Edit code live | Bind mount (`-v ./app:/app`) |
| Keep database data | Named volume |
| Keep logs / uploads | Named volume |
| Temporary cache | Tmpfs (`--tmpfs /tmp`) |
| Share data between containers | Named volume |

---

## Commands Summary

```bash
# Create volume
docker volume create myvol

# List volumes
docker volume ls

# Inspect volume
docker volume inspect myvol

# Delete volume
docker volume rm myvol

# Remove unused volumes
docker volume prune

# Run with volume
docker run -d -v myvol:/app/data nginx

# Run with bind mount
docker run -d -v $(pwd):/app nginx

# Copy volume data
docker run --rm -v myvol:/source -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /source .
```

---
