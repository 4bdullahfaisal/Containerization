# Kubernetes — Architecture & Components

**Date:** [Today's Date]  
**Purpose:** Understand Kubernetes architecture, control plane, and worker node components

---

## What is Kubernetes?

Kubernetes (K8s) is an open-source system for automating deployment, scaling, and management of containerized applications.

**Analogy:**  
If Docker is a single shipping container, Kubernetes is the **cargo ship + crane operator + dock manager** that runs thousands of containers at scale.

---

## Why Kubernetes?

| Problem | Kubernetes Solution |
|---------|----------------------|
| Container runs on one machine → it crashes | Automatically restarts it |
| Traffic increases → need more copies | Scales up/down automatically |
| New version of app → need zero downtime | Rolling updates |
| Container needs to talk to another | Built-in service discovery and networking |

---

## Kubernetes Architecture Overview

```
                    ┌─────────────────────────────────────┐
                    │        CONTROL PLANE (Master)       │
                    │  ┌──────────────┐                   │
                    │  │ API Server   │ ← kubectl         │
                    │  ├──────────────┤                   │
                    │  │ Scheduler    │ ← schedules pods  │
                    │  ├──────────────┤                   │
                    │  │ Controller   │ ← watches state   │
                    │  │ Manager      │                   │
                    │  ├──────────────┤                   │
                    │  │ etcd         │ ← cluster state   │
                    │  └──────────────┘                   │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────┴──────────────────────┐
                    │           WORKER NODES               │
                    │                                      │
                    │  ┌────────────────────────────┐     │
                    │  │         Node 1             │     │
                    │  │  ┌──────┐  ┌──────┐       │     │
                    │  │  │Pod A │  │Pod B │       │     │
                    │  │  └──────┘  └──────┘       │     │
                    │  │  Kubelet   Container       │     │
                    │  │            Runtime         │     │
                    │  └────────────────────────────┘     │
                    │                                      │
                    │  ┌────────────────────────────┐     │
                    │  │         Node 2             │     │
                    │  │  ┌──────┐  ┌──────┐       │     │
                    │  │  │Pod C │  │Pod D │       │     │
                    │  │  └──────┘  └──────┘       │     │
                    │  │  Kubelet   Container       │     │
                    │  │            Runtime         │     │
                    │  └────────────────────────────┘     │
                    └─────────────────────────────────────┘
```

---

## Master Node (Control Plane)

The master node is the **brain** of the cluster. It manages scheduling, scaling, and state.

### Master Node Components

| Component | What it does |
|-----------|--------------|
| **API Server** | Frontend of control plane. Handles `kubectl` commands and REST API calls. |
| **Scheduler** | Decides which worker node should run each new pod. |
| **Controller Manager** | Watches cluster state and fixes drift (e.g., restarts failed pods). |
| **etcd** | Key-value store that holds the entire cluster state and configuration. |

### Master Node — Quick Summary

| Component | Role |
|-----------|------|
| API Server | Frontend |
| Scheduler | Placement |
| Controller Manager | Watch & Fix |
| etcd | Cluster State |

---

## Worker Node

Worker nodes are the **machines** where actual workloads (containers) run.

### Worker Node Components

| Component | What it does |
|-----------|--------------|
| **Kubelet** | Agent that runs on each node. Communicates with control plane and ensures containers are running. |
| **Container Runtime** | Runs the actual containers (e.g., Docker, containerd). |
| **kube-proxy** | Handles networking, load balancing, and routing traffic to pods. |

### Worker Node — Quick Summary

| Component | Role |
|-----------|------|
| Kubelet | Node agent |
| Container Runtime | Runs containers |
| kube-proxy | Networking |

---

## Core Kubernetes Objects

| Object | Purpose |
|--------|---------|
| **Pod** | Smallest unit — runs one or more containers |
| **Deployment** | Manages replicas and rolling updates |
| **Service** | Exposes pods to the network |
| **ConfigMap** | Non-sensitive configuration |
| **Secret** | Sensitive data (passwords, keys) |
| **Ingress** | HTTP/HTTPS routing |
| **Namespace** | Virtual cluster inside a cluster |
| **PersistentVolume** | Storage for pods |

---

## kubectl Commands Summary

```bash
# Cluster Info
kubectl cluster-info

# Nodes
kubectl get nodes

# Pods
kubectl get pods
kubectl get pods -o wide
kubectl describe pod pod-name

# Deployments
kubectl get deployments
kubectl describe deployment deploy-name

# Services
kubectl get svc
kubectl describe svc service-name

# ConfigMaps / Secrets
kubectl get configmap
kubectl get secret

# Apply YAML
kubectl apply -f file.yaml

# Delete YAML
kubectl delete -f file.yaml

# Logs
kubectl logs pod-name

# Exec into pod
kubectl exec -it pod-name -- /bin/sh
```

---

## Quick Interview Answers

**Q: What is Kubernetes?**
> "Kubernetes is an open-source platform for automating deployment, scaling, and management of containerized applications."

**Q: What is a Pod?**
> "A Pod is the smallest unit in Kubernetes. It runs one or more containers that share storage and network."

**Q: What is the difference between a Node and a Pod?**
> "A Node is a physical or virtual machine that runs pods. A Pod is a group of containers running inside a node."

**Q: What is the role of the API Server?**
> "The API Server is the frontend of the control plane. It handles all REST API requests and `kubectl` commands."

**Q: What does the Scheduler do?**
> "The Scheduler decides which worker node should run a newly created pod based on resource availability."

**Q: What is etcd?**
> "etcd is a key-value store that holds the entire cluster state and configuration data."

**Q: What is a Deployment?**
> "A Deployment manages a set of pods, handles rolling updates, and ensures the desired number of replicas are running."

---

## Minikube — Local Kubernetes

Minikube runs a single-node cluster on your laptop.

```bash
# Start Minikube
minikube start

# Check status
minikube status

# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

---

## Hands-On Example

```bash
# Start cluster
minikube start

# Create deployment
kubectl create deployment nginx-deploy --image=nginx

# Expose as service
kubectl expose deployment nginx-deploy --type=NodePort --port=80

# Scale up to 3 replicas
kubectl scale deployment nginx-deploy --replicas=3

# Check pods
kubectl get pods

# Delete everything
kubectl delete service nginx-deploy
kubectl delete deployment nginx-deploy

# Stop minikube
minikube stop
```

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

**End of Kubernetes Architecture & Components**
