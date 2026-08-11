# Kubernetes — Introduction to Kubernetes
---

## What is Kubernetes?

Kubernetes (K8s) is an open-source platform for **automating deployment, scaling, and management of containerized applications**.

**Analogy:** Kubernetes is like a ship captain who manages many containers (Docker containers) across multiple ships (servers).

| Feature | What it does |
|---------|--------------|
| **Automated deployment** | Deploy containers without manual steps |
| **Scaling** | Increase or decrease replicas automatically |
| **Self-healing** | Restart failed containers |
| **Load balancing** | Distribute traffic across containers |
| **Rolling updates** | Update without downtime |

---

## Why Kubernetes?

| Problem | Kubernetes Solution |
|---------|----------------------|
| Container runs on one machine → it crashes | Automatically restarts it |
| Traffic increases → need more copies | Scales up/down automatically |
| New version of app → need zero downtime | Rolling updates |
| Container needs to talk to another | Built-in service discovery and networking |

---

## Master Node (Control Plane)

The master node is the **brain** of the cluster. It manages scheduling, scaling, and state.

| Component | What it does |
|-----------|--------------|
| **API Server** | Entry point for all commands |
| **Scheduler** | Decides where to place containers |
| **Controller Manager** | Keeps cluster in desired state |
| **etcd** | Cluster database (stores all data) |

## Worker Node

Worker nodes are the **machines** where actual workloads (containers) run.

| Component | What it does |
|-----------|--------------|
| **Kubelet** | Manages containers on node |
| **Kube-proxy** | Handles networking |
| **Container Runtime** | Runs containers (Docker, containerd) |

---

## Kubernetes Architecture Overview

A Kubernetes cluster has two types of nodes:

```
┌─────────────────────────────────────────────────────────┐
│               MASTER NODE (Control Plane)               │
│  ┌─────────┐ ┌──────────┐ ┌───────────┐ ┌───────────┐   │
│  │ API     │ │ Scheduler│ │ Controller│ │   etcd    │   │
│  │ Server  │ │          │ │ Manager   │ │           │   │
│  └─────────┘ └──────────┘ └───────────┘ └───────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    WORKER NODE 1                        │
│  ┌─────────┐ ┌──────────┐ ┌───────────┐                 │
│  │ kubelet │ │kube-proxy│ │ Container │                 │
│  │         │ │          │ │  Runtime  │                 │
│  └─────────┘ └──────────┘ └───────────┘                 │
│  ┌─────────────────────────────────────────────────┐    │
│  │                     Pods                        │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## Key Kubernetes Objects

| Object | Purpose | Example |
|--------|---------|---------|
| **Pod** | Smallest unit — runs one or more containers | nginx pod |
| **Deployment** | Manages replicas and rolling updates | nginx deployment |
| **Service** | Exposes pods to the network | expose nginx |
| **ConfigMap** | Non-sensitive configuration | app config |
| **Secret** | Store sensitive data | passwords, tokens |
| **Ingress** | External HTTP/HTTPS routing | domain → service |
| **Namespace** | Virtual cluster inside a cluster | dev, staging, prod |
| **PersistentVolume** | Storage for pods | database storage |

---

## Kubernetes vs Docker Commands

| Docker | Kubernetes |
|--------|------------|
| `docker run nginx` | `kubectl run nginx --image=nginx` |
| `docker ps` | `kubectl get pods` |
| `docker stop id` | `kubectl delete pod name` |
| `docker logs id` | `kubectl logs pod-name` |
| `docker exec -it id bash` | `kubectl exec -it pod-name -- bash` |
| `docker build -t myapp .` | `kubectl apply -f deployment.yaml` |

---

## Kubernetes vs Docker Compose vs Docker Swarm

| Feature | Docker Compose | Docker Swarm | Kubernetes |
|---------|----------------|--------------|------------|
| Multi-host | No | Yes | Yes |
| Auto-scaling | No | Yes | Yes |
| Self-healing | No | Yes | Yes |
| Rolling updates | Yes | Yes | Yes |
| Industry adoption | Low | Low | High |
---
## Installation Options (Local Development)

| Option | Purpose |
|--------|---------|
| **Minikube** | Single-node cluster (local learning) |
| **Kind** | Kubernetes in Docker |
| **k3s** | Lightweight Kubernetes |
| **Docker Desktop** | Built-in Kubernetes (easiest) |
| **Cloud (EKS, GKE, AKS)** | Production clusters |

---

## Install Minikube (Recommended)

### Windows

```bash
# Install Minikube
choco install minikube

# Install kubectl
choco install kubernetes-cli

# Start Minikube
minikube start

# Check status
minikube status

# Stop Minikube
minikube stop
```

### Verify

```bash
kubectl version --client
kubectl cluster-info
```

---

## Your First Kubernetes Deployment

### Step 1: Create a deployment

```bash
kubectl create deployment nginx-deploy --image=nginx
```

### Step 2: Check status

```bash
kubectl get pods
kubectl get deployments
```

### Step 3: Expose the deployment as a service

```bash
kubectl expose deployment nginx-deploy --type=LoadBalancer --port=8080 --target-port=80
```

### Step 4: Get service URL

```bash
minikube service nginx-deploy
```

### Step 5: Scale the deployment

```bash
kubectl scale deployment nginx-deploy --replicas=3
kubectl get pods
```

### Step 6: Delete resources

```bash
kubectl delete deployment nginx-deploy
kubectl delete service nginx-deploy
```

---

## YAML Manifest Example

Kubernetes resources are defined in YAML files.

### nginx-deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```

### Apply the manifest

```bash
kubectl apply -f nginx-deployment.yaml
```

---

## kubectl Commands Summary

```bash
# Cluster info
kubectl cluster-info
kubectl version

# Resources
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get all

# Create/Update
kubectl apply -f file.yaml

# Delete
kubectl delete -f file.yaml
kubectl delete pod pod-name

# Debug
kubectl logs pod-name
kubectl describe pod pod-name
kubectl exec -it pod-name -- bash

# Scale
kubectl scale deployment name --replicas=5
```

