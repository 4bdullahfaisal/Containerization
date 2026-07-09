# Docker — Docker Networking

---

## Why Docker Networking?

Containers need to communicate with each other and with the outside world.

| Scenario | Why you need it |
|----------|----------------|
| Web app talks to database | Containers need to communicate |
| Multiple containers on same host | Isolate or connect them |
| Access container from browser | Port mapping (`-p`) |
| Microservices | Service discovery and communication |

---

## Docker Network Types

| Network Type | Use Case |
|--------------|----------|
| **bridge** (default) | Containers on same host talk to each other |
| **host** | Container uses host's network directly (fast, less isolation) |
| **none** | No network (isolated) |
| **overlay** | Multi-host (Swarm / Kubernetes) |

---

## Network Commands

```bash
docker network ls               # List networks
docker network create mynet     # Create network
docker network inspect mynet    # Show details
docker network rm mynet         # Delete network
docker network prune            # Remove unused networks
docker network connect mynet container   # Attach container to network
docker network disconnect mynet container   # Detach container
```

---

## Bridge Network (Default)

When you run a container without `--network`, it connects to the default `bridge` network.

Containers on bridge network:

- Can talk to each other using their IP addresses

- Cannot use container names (unless custom network)

```bash
# Run two containers on default bridge
docker run -d --name app1 nginx
docker run -d --name app2 nginx

# Test connectivity (by IP, not name)
docker inspect app1 | grep IPAddress
docker exec app2 ping [IP-of-app1]
```

> ⚠️ Containers on default bridge cannot reach each other by container name — only by IP.

---

## Custom Bridge Network (Recommended)

Custom networks provide automatic DNS resolution — containers can talk using names.

```bash
# Create a custom network
docker network create my-network

# Run containers on custom network
docker run -d --name web --network my-network nginx
docker run -d --name db --network my-network mysql

# Now 'web' can reach 'db' by name
docker exec web ping db
```
---

## Host Network

Container uses the host's network directly — no isolation, but fastest performance.

```bash
docker run -d --name web --network host nginx
# Access at http://localhost (no port mapping needed)
```

> ⚠️ Use only when performance is critical and security is less of a concern.

---

## None Network

Container has no network access — completely isolated.

```bash
docker run -d --network none nginx
```

**Use case:** Security-sensitive or offline processing.

---

## Port Mapping (Publish Ports)

Expose container ports to the host.

```bash
# Map port 8080 on host → port 80 inside container
docker run -d -p 8080:80 nginx

# Map multiple ports
docker run -d -p 8080:80 -p 8443:443 nginx

# Bind to specific IP
docker run -d -p 127.0.0.1:8080:80 nginx
```

---

## Docker Compose Networking

Compose automatically creates a network for you — containers can reach each other by service name.

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      
# Compose creates default network
```

Inside `web`, you can reach `db` by its service name `db`.

---

## Custom Networks in Compose

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    networks:
      - frontend

  api:
    image: my-api
    networks:
      - frontend
      - backend

  db:
    image: mysql:8.0
    networks:
      - backend

networks:
  frontend:
  backend:
```

---

## Practice: Container Communication

```bash
# 1. Create network
docker network create app-net

# 2. Run containers on same network
docker run -d --name web1 --network app-net alpine tail -f /dev/null
docker run -d --name web2 --network app-net alpine tail -f /dev/null

# 3. Test connectivity (inside web1, ping web2)
docker exec web1 ping web2

# 4. See results
docker logs web1
```

---

## Port Mapping vs Network

| Feature | Port Mapping (-p) | Custom Network |
|---------|-------------------|----------------|
| Purpose | Expose container to outside world | Container-to-container communication |
| Example | `-p 8080:80` | `--network mynet` |
| Use for | Browser access, API calls | Web app talking to database |

---

## Networking Best Practices

| Practice | Why |
|----------|-----|
| Use custom bridge networks | Better isolation and service discovery |
| Use Compose for multi-container apps | Automatic network management |
| Don't use host network unless needed | Security risk |
| Use service names in Compose | No hardcoded IPs |
| Limit exposed ports | Only expose what's needed |

---

## Commands Summary

| Command | Description |
|---------|-------------|
| `docker network ls` | List all networks |
| `docker network create mynet` | Create a network named "mynet" |
| `docker network inspect mynet` | Display detailed information about "mynet" |
| `docker network rm mynet` | Remove the network "mynet" |
| `docker network prune` | Remove all unused networks |
| `docker run -d --network mynet nginx` | Run a container on the specific network "mynet" |
| `docker network connect mynet container-name` | Connect a container to "mynet" |
| `docker network disconnect mynet container-name` | Disconnect a container from "mynet" |
| `docker run -d -p 8080:80 nginx` | Map host port 8080 to container port 80 |
| `docker run -d -p 3000:3000 node-app` | Map host port 3000 to container port 3000 |

---
