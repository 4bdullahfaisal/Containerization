# ProgreeApp

<p align="center">
  <img src="https://img.shields.io/badge/ProgreeApp-Flask%20Container-0d9488?style=flat&logo=flask&logoColor=white" alt="ProgreeApp Flask container">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Docker-Multi--stage-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker multi-stage build">
  <img src="https://img.shields.io/badge/Port-6767%3A6767-f59e0b?style=flat&logo=docker&logoColor=white" alt="Container port 6767 mapped to host port 6767">
</p>

> A compact, production-minded Flask service packaged as a small, secure Docker image. ProgreeApp demonstrates environment-based configuration, health checks, a non-root runtime user, and a clean multi-stage build.

## Task 2: Application Containerization & Asset Optimization

This project fulfills **Task 2** by packaging a modular Flask web application in a reliable, production-oriented container environment. The implementation focuses on keeping the final image small, moving build-only dependencies out of the runtime layer, mapping configuration through environment variables, and exposing a functional HTTP port.

| Requirement | Implementation |
| --- | --- |
| Multi-stage configuration Dockerfile | `Dockerfile` uses a `python:3.12-slim-bullseye` builder stage and a separate `python:3.12-slim` runtime stage. |
| Multi-dependency web app runtime | `requirements.txt` pins Flask for the web framework and Gunicorn for production serving. |
| Minimized final image footprint | GCC and other build tools remain in the builder stage; dependencies are installed with `--no-cache-dir` and only `/install` is copied into the runtime image. |
| Secure environment variable mapping | `APP_NAME`, `APP_ENV`, `PORT`, and `SECRET_KEY` are read from the environment, allowing deployment-specific values without hardcoding secrets. |
| Functional container port routing | Gunicorn binds to `0.0.0.0:6767`, the image documents `EXPOSE 6767`, and Docker maps it with `-p 6767:6767`. |
| Reliable runtime execution | The final container runs as the unprivileged `appuser` and uses Gunicorn instead of Flask's development server. |
| Asset and cache optimization | `.dockerignore` excludes Python bytecode, virtual environments, test caches, secrets, documentation, and screenshots from the Docker build context. |

### Containerization flow

```text
requirements.txt
  |
  v
Builder stage: install dependencies into /install
  |
  v
Runtime stage: copy dependencies + app.py only
  |
  v
appuser -> Gunicorn -> 0.0.0.0:6767 -> host:6767
```

## Overview

ProgreeApp is intentionally small so the containerization workflow stays easy to inspect and reuse. The service exposes a friendly root response and a machine-readable health endpoint:

- **Application:** Flask 3.0.3
- **Production server:** Gunicorn 22.0.0
- **Runtime:** Python 3.12 slim image
- **Container build:** Two stages, with build dependencies kept out of the runtime image
- **Runtime user:** Non-root `appuser`
- **Default port:** `6767`
- **Configuration:** Environment variables, with safe local defaults

## Architecture

```text
Client
  |
  | HTTP :6767
  v
Gunicorn (1 application module)
  |
  v
Flask app.py
  |-- GET /        -> greeting with application name and environment
  `-- GET /health  -> {"status": "ok"}
```

The Dockerfile separates dependency installation from runtime execution. The builder stage installs Python dependencies into `/install`; the runtime stage copies only those installed dependencies and the application code into a fresh Python slim image.

The final image does not include the compiler toolchain, package cache, README files, screenshots, virtual environments, or local Python caches. This keeps the runtime layer focused on the files needed to serve the application.

## Quick Start

### Run locally

Create a virtual environment and install the pinned dependencies:

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python app.py
```

The development server will listen on `http://localhost:6767`.

### Run with Docker

Build the image from the project directory:

```bash
docker build -t progreeapp:latest .
```

Start the container and publish its port:

```bash
docker run --rm --name progreeapp \
  -p 6767:6767 \
  -e APP_NAME=ProgreeApp \
  -e APP_ENV=production \
  progreeapp:latest
```

On Windows PowerShell, use a backtick instead of a trailing backslash, or keep the command on one line.

Open `http://localhost:6767` in a browser, or verify the health endpoint:

```bash
curl http://localhost:6767/health
```

Expected response:

```json
{"status":"ok"}
```

## API Reference

### `GET /`

Returns a plain-text greeting using `APP_NAME` and `APP_ENV`.

Example response:

```text
Hello from ProgreeApp running in production mode!
```

### `GET /health`

Returns a JSON readiness signal. This endpoint is suitable for a basic container or reverse-proxy health check.

**Response:** `200 OK`

```json
{"status":"ok"}
```

## Configuration

All settings are read at process startup from environment variables.

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | `ProgreeApp` | Name included in the root response |
| `APP_ENV` | `development` in local mode, `production` in Docker | Environment label included in the root response |
| `PORT` | `6767` | Port used by the Flask development server; the Docker image binds Gunicorn to `6767` |
| `SECRET_KEY` | `dev-secret` | Application secret placeholder; provide a strong value outside local development |

Example custom configuration:

```bash
APP_NAME="Progree API" APP_ENV=staging PORT=6767 python app.py
```

## Project Structure

```text
.
├── app.py             # Flask application and HTTP routes
├── Dockerfile         # Multi-stage production container build
├── requirements.txt   # Pinned runtime dependencies
├── screenshots/       # Project screenshots
└── README.md          # Project documentation
```

## Security Notes

- The production container runs as the unprivileged `appuser`, not as `root`.
- Build tools are installed only in the temporary builder stage and are not copied into the final image.
- Dependencies are installed with `--no-cache-dir` to avoid retaining package caches in the image.
- Secrets should be injected at runtime. Do not commit real values for `SECRET_KEY` or other credentials.
- The default `dev-secret` is suitable only as a development fallback and must be replaced in deployed environments.
- For internet-facing deployments, place the service behind TLS termination, authentication, rate limiting, and an appropriate reverse proxy.

## Troubleshooting

**Port `6767` is already in use**

Run the container on another host port while keeping the container port unchanged:

```bash
docker run --rm -p 8080:6767 progreeapp:latest
```

Then visit `http://localhost:8080`.

**The container exits immediately**

Inspect its logs:

```bash
docker logs progreeapp
```

Confirm that the image was built from the directory containing both `Dockerfile` and `requirements.txt`.

**The health check cannot connect**

Confirm the port mapping and that the service is listening on all interfaces. The image uses Gunicorn at `0.0.0.0:6767`, which is required for access through Docker port publishing.

## Screenshots

Project screenshots are available in the [`screenshots/`](screenshots/) directory:

- [view 1](screenshots/Screenshot%202026-09-15%20114514.png)
- [view 2](screenshots/Screenshot%202026-09-15%20114653.png)
- [view 3](screenshots/Screenshot%202026-09-15%20114725.png)
- [view 4](screenshots/Screenshot%202026-09-15%20114807.png)
- [view 5](screenshots/Screenshot%202026-09-15%20114812.png)
- [view 6](screenshots/Screenshot%202026-09-15%20115040.png)
