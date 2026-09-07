# WordPress on Kubernetes Mini-Project

A complete WordPress + MySQL deployment on Kubernetes designed for DevOps beginners to learn core concepts like ConfigMaps, Secrets, PersistentVolumes, and rolling updates.

![Kubernetes](https://img.shields.io/badge/kubernetes-%23326CE5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![WordPress](https://img.shields.io/badge/WordPress-%23117AC9.svg?style=for-the-badge&logo=WordPress&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)


##Project Overview

This project deploys a production-like WordPress installation with:
- **MySQL 5.7** database with persistent storage
- **WordPress** application with 2 replicas for high availability
- **Secrets** for secure password management
- **ConfigMaps** for configuration separation
- **PersistentVolumeClaims** for data persistence
- **NodePort** service for external access

## Prerequisites

- Docker Desktop (with Kubernetes enabled) OR Minikube
- kubectl command-line tool
- Basic understanding of YAML and terminal commands

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Deploy MySQL

```bash
kubectl apply -f mysql-deployment.yaml
```

### 3. Wait for MySQL to Start

```bash
kubectl get pods -w
```
Wait until MySQL pod shows `Running` status (approximately 30 seconds).

### 4. Deploy WordPress

```bash
kubectl apply -f wordpress-deployment.yaml
```

### 5. Verify All Pods Are Running

```bash
kubectl get pods
```

Expected output:
```
mysql-xxxxxxxxx-xxxxx     1/1     Running
wordpress-xxxxxxxxx-xxxxx 1/1     Running
wordpress-xxxxxxxxx-xxxxx 1/1     Running
```

## Access WordPress

- **Docker Desktop**: Open `http://localhost:30080`
- **Minikube**: Run `minikube service wordpress-service`

Complete the WordPress installation wizard and start creating content!

## Testing DevOps Concepts

### Test 1: Data Persistence
```bash
# Create a blog post
# Delete the WordPress pod
kubectl delete pod <wordpress-pod-name>

# Wait for new pod to start
kubectl get pods -w

# Refresh browser - your post is still there!
```

### Test 2: Scaling
```bash
# Scale WordPress to 3 replicas
kubectl scale deployment wordpress --replicas=3

# Verify new pods
kubectl get pods
```

### Test 3: Rolling Update
```bash
# Update to specific WordPress version
kubectl set image deployment/wordpress wordpress=wordpress:5.8

# Watch the rollout
kubectl rollout status deployment wordpress
```

### Test 4: Rollback
```bash
# Rollback to previous version
kubectl rollout undo deployment wordpress
```

## Debugging Commands

```bash
# View MySQL logs
kubectl logs -f <mysql-pod-name>

# View WordPress logs
kubectl logs -f <wordpress-pod-name>

# Get detailed pod information
kubectl describe pod <pod-name>

# Check environment variables inside a pod
kubectl exec -it <pod-name> -- env

# Connect to MySQL from inside the cluster
kubectl run -it --rm mysql-client --image=mysql:5.7 -- mysql -h mysql-service -u wordpress -pwordpress
```

## Clean Up

```bash
# Delete all resources
kubectl delete -f mysql-deployment.yaml
kubectl delete -f wordpress-deployment.yaml

# Verify cleanup
kubectl get all
```

## File Structure

```
.
├── mysql-deployment.yaml      # MySQL deployment, secret, configmap, PVC, and service
└── wordpress-deployment.yaml  # WordPress deployment, configmap, PVC, and service
```

## Learning Outcomes

By completing this project, you'll understand:

-  Deploying stateful applications with PersistentVolumes
-  Managing sensitive data with Kubernetes Secrets
-  Separating configuration with ConfigMaps
-  Connecting services using internal DNS
-  Scaling applications horizontally
-  Performing zero-downtime rolling updates
-  Rolling back failed deployments
-  Debugging pods using logs and describe commands

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ImagePullBackOff` | Check internet connection or verify image name |
| `CrashLoopBackOff` | Check logs with `kubectl logs <pod-name>` |
| `Pending` | Reduce replicas to 1 if insufficient resources |
| Connection refused | Ensure MySQL is fully running before deploying WordPress |

## Useful Commands

```bash
# Get all resources in default namespace
kubectl get all

# Get detailed YAML of a resource
kubectl get deployment wordpress -o yaml

# Port forward for local testing
kubectl port-forward service/wordpress-service 8080:80

# Scale down to 1 replica
kubectl scale deployment wordpress --replicas=1

# Delete a specific resource
kubectl delete deployment wordpress
```

## Next Steps

After mastering this project, try:

1. Adding a custom domain using Ingress
2. Deploying the Kubernetes Dashboard
3. Setting up monitoring with Prometheus and Grafana
4. Implementing a CI/CD pipeline with GitHub Actions
5. Adding SSL/TLS certificates with cert-manager

## Acknowledgments

- WordPress for the awesome CMS
- MySQL for the reliable database
- Kubernetes for making container orchestration accessible
