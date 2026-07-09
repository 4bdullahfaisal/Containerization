# Docker — Docker Compose (Multi-Container Apps)

---

## What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications.

**Analogy:** Docker Compose is like a **playlist** for containers — you define all the songs (services) once, then press play.

### Without Compose:
- Run each container manually
- Remember all `docker run` flags
- Hard to restart after reboot

### With Compose:
- Define everything in one file
- Declare once, run with one command
- Start all services together

---

## Install Docker Compose

Docker Desktop includes Compose by default.

```bash
docker compose version
```

---

## docker-compose.yml Structure

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: appdb
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

### Breakdown:

| Section | Purpose |
|---------|---------|
| `version` | Compose file format version |
| `services` | List of containers to run |
| `web` / `db` | Service names |
| `image` | Docker image to use |
| `ports` | Port mapping (host:container) |
| `volumes` | Persistent data or file mounts |
| `environment` | Environment variables |
| `volumes:` (top-level) | Named volumes for data persistence |

---

## Docker Compose Commands

```bash
docker compose up -d          # Start all services (detached)
docker compose down           # Stop and remove containers
docker compose ps             # List services
docker compose logs           # View all logs
docker compose logs web       # View logs for web service
docker compose restart web    # Restart specific service
docker compose exec web sh    # Shell into web container
docker compose stop           # Stop services (keeps containers)
docker compose start          # Start stopped services
docker compose build          # Build images (if using build:)
docker compose down -v        # Down + remove volumes
```

---

## Example: Web + Database

### 1. Create Project Folder

```bash
mkdir docker-compose-demo
cd docker-compose-demo
```

### 2. Create HTML Folder

```bash
mkdir html
```

### 3. Create `html/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Docker Compose Demo</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
    </style>
</head>
<body>
    <h1>🚀 Docker Compose is running!</h1>
    <p>This page is mounted from your laptop.</p>
    <p>Database is also running in another container.</p>
</body>
</html>
```

### 4. Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: appdb
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

### 5. Start Services

```bash
docker compose up -d
```

### 6. Check Status

```bash
docker compose ps
```

### 7. View in Browser

Open `http://localhost:8080`

### 8. Connect to Database

```bash
# From host machine (if MySQL client installed)
mysql -h 127.0.0.1 -P 3306 -u root -proot123

# Or from inside container
docker compose exec db mysql -u root -proot123
```

---

## docker-compose.yml vs docker run

| `docker run` | `docker-compose.yml` |
|--------------|----------------------|
| `-d` | `detach: true` |
| `-p 8080:80` | `ports: - "8080:80"` |
| `-v ./html:/usr/share/nginx/html` | `volumes: - ./html:/usr/share/nginx/html` |
| `--name my-web` | `container_name: my-web` |
| `-e ENV=prod` | `environment: - ENV=prod` |

---

## Adding a Third Service (Redis)

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: appdb
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  cache:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  db_data:
```

Restart:

```bash
docker compose down
docker compose up -d
docker compose ps
```

---

## Common Docker Compose Scenarios

| Scenario | Services |
|----------|----------|
| Web App | nginx + php-fpm + mysql |
| Wordpress | wordpress + mysql |
| Monitoring | prometheus + grafana + node-exporter |
| ELK Stack | elasticsearch + logstash + kibana |
| App + Cache | app + redis |
| App + DB | app + postgres |

---

## Docker Compose File Tips

| Tip | Example |
|-----|---------|
| Use environment variables | `environment: - DB_PASSWORD=${DB_PASS}` |
| Use .env file | Create `.env` file with variables |
| Use build instead of image | `build: ./app` |
| Use depends_on for order | `depends_on: - db` |
| Use restart policy | `restart: always` |

---

## Commands Summary

```bash
docker compose up -d          # Start all services
docker compose down           # Stop and remove
docker compose ps             # List services
docker compose logs           # View logs
docker compose exec web sh    # Shell into web container
docker compose restart web    # Restart web service
docker compose stop           # Stop without removing
docker compose start          # Start stopped services
docker compose down -v        # Down + remove volumes
```

---
