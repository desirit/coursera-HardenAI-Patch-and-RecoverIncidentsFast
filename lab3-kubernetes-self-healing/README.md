# Lab 3: Kubernetes Self-Healing Systems

## Overview

In this lab, you'll build infrastructure that **automatically recovers from failures**. Using Kubernetes health probes, your system will detect problems and take corrective action without human intervention.

### What You'll Learn

- How Kubernetes liveness and readiness probes work
- How to design health check endpoints for ML services
- How automatic pod restarts protect your system
- How Prometheus monitors service health
- How to perform manual and automatic rollbacks

### Why This Matters

In production ML systems, failures are inevitable:
- Models can return garbage predictions after deployment
- Memory leaks cause containers to crash
- External dependencies become unavailable

Self-healing infrastructure minimizes downtime by detecting these problems and automatically recovering, often before users notice.

## Prerequisites

### Required Tools

Install these before starting the lab:

**macOS:**
```bash
# Install Docker Desktop
brew install --cask docker

# Install Minikube (local Kubernetes)
brew install minikube

# Install kubectl (K8s CLI)
brew install kubectl

# Install Helm (package manager for K8s)
brew install helm
```

**Windows (using WSL2):**
```bash
# Install Docker Desktop from docker.com (enable WSL2 integration)

# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Verify Installation

```bash
docker --version        # Docker version 24.x or higher
minikube version        # minikube version v1.32.x or higher
kubectl version --client # Client Version: v1.29.x or higher
helm version            # version.BuildInfo{Version:"v3.x.x"...}
```

## Architecture

```
                    ┌────────────────────────────────────────────────┐
                    │              Kubernetes Cluster                 │
                    │                                                │
    Traffic ───────►│  ┌─────────────────────────────────────────┐   │
                    │  │            Service (Load Balancer)       │   │
                    │  │  Routes traffic to READY pods only       │   │
                    │  └───────────────┬─────────────────────────┘   │
                    │                  │                             │
                    │    ┌─────────────┼─────────────┐               │
                    │    ▼             ▼             ▼               │
                    │  ┌───┐        ┌───┐        ┌───┐              │
                    │  │Pod│        │Pod│        │Pod│              │
                    │  │ 1 │        │ 2 │        │ 3 │              │
                    │  └─┬─┘        └─┬─┘        └─┬─┘              │
                    │    │            │            │                 │
                    │    ▼            ▼            ▼                 │
                    │  /health     /health     /health    (Liveness) │
                    │  /ready      /ready      /ready    (Readiness) │
                    │  /metrics    /metrics    /metrics  (Prometheus)│
                    └────────────────────────────────────────────────┘

    Liveness Probe:  Is the container alive? → If NO → RESTART container
    Readiness Probe: Is it ready for traffic? → If NO → REMOVE from load balancer
```

## Quick Start

### Step 1: Start Minikube

```bash
# Start minikube with enough resources
minikube start --cpus=2 --memory=4096

# Enable metrics server
minikube addons enable metrics-server

# Point Docker to minikube's daemon (IMPORTANT!)
eval $(minikube docker-env)
```

### Step 2: Build Container Images

```bash
# Build the stable version (v1)
docker build -t model-server:v1 .

# Build the buggy version (v2)
docker build -t model-server:v2 -f Dockerfile.v2 .
```

### Step 3: Deploy to Kubernetes

```bash
# Deploy the application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Watch pods start up
kubectl get pods -w
```

Press Ctrl+C when all pods show `1/1 Running`.

### Step 4: Test the Service

```bash
# Get the service URL
minikube service model-server --url

# Test health endpoint (use the URL from above)
curl $(minikube service model-server --url)/health
```

## Understanding Health Probes

### Liveness Probe

**Purpose:** Detect if the container is alive and functioning.

**Behavior:** If the liveness probe fails 3 consecutive times, Kubernetes **restarts the container**.

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10   # Wait 10s before first check
  periodSeconds: 10         # Check every 10 seconds
  failureThreshold: 3       # Restart after 3 failures
```

**When to use:** Detecting hung processes, infinite loops, deadlocks.

### Readiness Probe

**Purpose:** Detect if the container is ready to receive traffic.

**Behavior:** If the readiness probe fails, Kubernetes **removes the pod from the load balancer** (but doesn't restart it).

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5    # Wait 5s before first check
  periodSeconds: 5          # Check every 5 seconds
  failureThreshold: 2       # Remove from LB after 2 failures
```

**When to use:** Warm-up periods, temporary overload, dependency failures.

## Lab Exercises

### Exercise 1: Observe Healthy System (10 min)

1. View running pods:
   ```bash
   kubectl get pods
   ```

2. Check pod details:
   ```bash
   kubectl describe pod <pod-name>
   ```
   Look for the "Events" section - you should see successful liveness and readiness probes.

3. View service endpoints:
   ```bash
   kubectl get endpoints model-server
   ```
   All pod IPs should be listed.

4. Test the health endpoints:
   ```bash
   URL=$(minikube service model-server --url)
   curl $URL/health
   curl $URL/ready
   curl $URL/metrics
   ```

### Exercise 2: Deploy Buggy Version (15 min)

1. Deploy the buggy version:
   ```bash
   kubectl apply -f k8s/deployment-v2.yaml
   ```

2. Watch the chaos unfold:
   ```bash
   kubectl get pods -w
   ```

3. Observe:
   - `RESTARTS` column increasing (liveness failures)
   - `READY` showing `0/1` (readiness failures)

4. Check events:
   ```bash
   kubectl get events --sort-by='.lastTimestamp'
   ```

5. Check endpoints (pods removed from load balancer):
   ```bash
   kubectl get endpoints model-server
   ```

### Exercise 3: Perform Rollback (10 min)

1. Check deployment history:
   ```bash
   kubectl rollout history deployment/model-server
   ```

2. Rollback to previous version:
   ```bash
   kubectl rollout undo deployment/model-server
   ```

3. Watch recovery:
   ```bash
   kubectl get pods -w
   ```

4. Verify health is restored:
   ```bash
   curl $(minikube service model-server --url)/health
   ```

### Exercise 4: Set Up Prometheus Monitoring (20 min)

1. Install Prometheus:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update

   helm install prometheus prometheus-community/prometheus \
     -f k8s/prometheus-values.yaml \
     --namespace monitoring --create-namespace
   ```

2. Wait for Prometheus to start:
   ```bash
   kubectl get pods -n monitoring -w
   ```

3. Access Prometheus UI:
   ```bash
   minikube service prometheus-server -n monitoring
   ```

4. In the Prometheus UI, try these queries:
   - `model_accuracy` - Current model accuracy
   - `model_degraded` - Is model degraded? (0 or 1)
   - `model_latency_ms` - Average latency

5. Check the "Alerts" tab for predefined alerts.

## Key Concepts

### Why Two Probes?

| Probe | What it detects | Action taken |
|-------|-----------------|--------------|
| Liveness | Container is dead/stuck | Restart container |
| Readiness | Container is overwhelmed/warming up | Stop sending traffic |

### Self-Healing Flow

```
1. Pod deployed with v2 (buggy)
           │
           ▼
2. Health check fails (/health returns 503)
           │
           ▼
3. After 3 failures, Kubernetes restarts pod
           │
           ▼
4. Pod restarts but keeps failing
           │
           ▼
5. Meanwhile, /ready also fails
           │
           ▼
6. Pod removed from Service endpoints
           │
           ▼
7. No traffic routed to unhealthy pod
           │
           ▼
8. Human or automation triggers rollback
           │
           ▼
9. v1 pods deploy, pass probes, receive traffic
```

## Troubleshooting

### Minikube Won't Start

```bash
# Delete and recreate
minikube delete
minikube start --driver=docker
```

### Images Not Found

```bash
# Make sure you're using minikube's docker
eval $(minikube docker-env)

# Rebuild images
docker build -t model-server:v1 .
```

### Can't Access Service

```bash
# Try tunnel mode
minikube tunnel

# Or use port-forward
kubectl port-forward svc/model-server 8080:80
```

### Prometheus Not Scraping

```bash
# Check pod annotations
kubectl get pod <pod-name> -o yaml | grep -A5 annotations
```

## Cleanup

```bash
# Delete deployments
kubectl delete -f k8s/

# Uninstall Prometheus
helm uninstall prometheus -n monitoring

# Stop minikube (preserves state)
minikube stop

# Or delete completely
minikube delete
```

## Key Takeaways

1. **Liveness probes restart stuck containers** - Use for detecting crashes and deadlocks
2. **Readiness probes protect your users** - Remove unhealthy pods from load balancer before users notice
3. **Design meaningful health checks** - Check what matters (model loaded, dependencies available)
4. **Monitor and alert** - Prometheus provides visibility into system health
5. **Practice rollbacks** - Know how to quickly recover from bad deployments

## Further Reading

- [Kubernetes Probes Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Designing Health Check Endpoints](https://blog.colinbreck.com/kubernetes-liveness-and-readiness-probes-how-to-avoid-shooting-yourself-in-the-foot/)
- [Prometheus Monitoring](https://prometheus.io/docs/introduction/overview/)

## Previous Labs

- **Lab 1**: Canary Deployments for ML Models
- **Lab 2**: Building an Incident Knowledge Base
