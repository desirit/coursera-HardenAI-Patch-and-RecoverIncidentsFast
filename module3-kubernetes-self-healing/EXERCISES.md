# Module 3: Exercises

Complete these hands-on exercises to master Kubernetes self-healing systems.

---

## Exercise 1: Explore the Healthy System

**Objective**: Understand how a healthy Kubernetes deployment looks and behaves.

**Time**: 10 minutes

### Prerequisites

Make sure you have completed the setup from the README:
```bash
minikube start
eval $(minikube docker-env)
docker build -t model-server:v1 .
docker build -t model-server:v2 -f Dockerfile.v2 .
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Steps

1. **View running pods:**
   ```bash
   kubectl get pods
   ```

   Record the output:
   ```
   NAME                            READY   STATUS    RESTARTS   AGE
   _________________________________________________________________
   _________________________________________________________________
   _________________________________________________________________
   ```

2. **Check pod details:**
   ```bash
   kubectl describe pod <pod-name-from-above>
   ```

   Find and record:
   - Liveness probe configuration: ________________________________
   - Readiness probe configuration: ________________________________
   - Last probe results in Events section: ________________________________

3. **View service endpoints:**
   ```bash
   kubectl get endpoints model-server
   ```

   How many pod IPs are listed? ___

4. **Test health endpoints:**
   ```bash
   URL=$(minikube service model-server --url)
   echo "Service URL: $URL"

   curl $URL/health
   curl $URL/ready
   curl $URL/metrics
   ```

   Record the health response:
   ```json

   ```

### Questions

1. What does "READY 1/1" mean in the pod listing?
   ```
   Answer: _______________________________________________
   ```

2. Why are there 3 pod IPs in the endpoints?
   ```
   Answer: _______________________________________________
   ```

3. What would happen if a pod's readiness probe failed?
   ```
   Answer: _______________________________________________
   ```

---

## Exercise 2: Deploy Buggy Version and Observe Failures

**Objective**: See Kubernetes self-healing in action when deployments fail.

**Time**: 15 minutes

### Steps

1. **Deploy the buggy version:**
   ```bash
   kubectl apply -f k8s/deployment-v2.yaml
   ```

2. **Watch pods (keep this running):**
   ```bash
   kubectl get pods -w
   ```

   Watch for 2-3 minutes and record what you see:
   ```
   Time    Pod Name    Ready    Status    Restarts
   ------------------------------------------------





   ```

3. **In another terminal, check events:**
   ```bash
   kubectl get events --sort-by='.lastTimestamp' | head -20
   ```

   What types of events do you see?
   ```


   ```

4. **Check endpoints:**
   ```bash
   kubectl get endpoints model-server
   ```

   How many pod IPs are listed now? ___

5. **Try to access the service:**
   ```bash
   curl $(minikube service model-server --url)/health
   ```

   Does it work? ___  Why or why not?

### Questions

1. What causes the RESTARTS count to increase?
   ```
   Answer: _______________________________________________
   ```

2. Why do pods show "0/1" in the READY column?
   ```
   Answer: _______________________________________________
   ```

3. What is the difference between a liveness failure and a readiness failure?
   ```
   Liveness failure: _______________________________________
   Readiness failure: ______________________________________
   ```

---

## Exercise 3: Perform Rollback

**Objective**: Learn how to recover from a bad deployment.

**Time**: 10 minutes

### Steps

1. **Check deployment history:**
   ```bash
   kubectl rollout history deployment/model-server
   ```

   How many revisions are there? ___

2. **Rollback to previous version:**
   ```bash
   kubectl rollout undo deployment/model-server
   ```

3. **Watch the rollback:**
   ```bash
   kubectl get pods -w
   ```

   Describe what happens:
   ```



   ```

4. **Verify recovery:**
   ```bash
   kubectl get pods
   kubectl get endpoints model-server
   curl $(minikube service model-server --url)/health
   ```

5. **Check the rollback in history:**
   ```bash
   kubectl rollout history deployment/model-server
   ```

### Questions

1. How long did the rollback take?
   ```
   Answer: ___ seconds
   ```

2. What version is running now after the rollback?
   ```bash
   kubectl get pods -o jsonpath='{.items[0].spec.containers[0].env}'
   ```
   ```
   Answer: _______________________________________________
   ```

3. In a production environment, how could this rollback be automated?
   ```
   Answer: _______________________________________________
   ```

---

## Exercise 4: Set Up Prometheus Monitoring

**Objective**: Configure Prometheus to monitor model health metrics.

**Time**: 20 minutes

### Steps

1. **Install Prometheus:**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update

   helm install prometheus prometheus-community/prometheus \
     -f k8s/prometheus-values.yaml \
     --namespace monitoring --create-namespace
   ```

2. **Wait for Prometheus to start:**
   ```bash
   kubectl get pods -n monitoring -w
   ```

3. **Access Prometheus UI:**
   ```bash
   minikube service prometheus-server -n monitoring
   ```

4. **Try these PromQL queries in the Prometheus UI:**

   | Query | What it shows | Your Result |
   |-------|---------------|-------------|
   | `model_accuracy` | Current accuracy | |
   | `model_degraded` | Is model degraded? | |
   | `model_latency_ms` | Average latency | |
   | `model_requests_total` | Total requests | |

5. **Check the Alerts tab:**
   - What alerts are defined?
   - Are any alerts currently firing?

6. **Deploy v2 and watch alerts:**
   ```bash
   kubectl apply -f k8s/deployment-v2.yaml
   ```

   Wait 1-2 minutes, then check the Alerts tab again.

   Which alerts fired?
   ```


   ```

7. **Rollback and verify alerts resolve:**
   ```bash
   kubectl rollout undo deployment/model-server
   ```

### Questions

1. What is the accuracy threshold that triggers an alert?
   ```
   Answer: _______________________________________________
   ```

2. How could you configure Prometheus to automatically trigger a rollback?
   ```
   Answer: _______________________________________________
   ```

---

## Exercise 5: Design Your Own Health Checks

**Objective**: Think critically about what makes a good health check.

**Time**: 15 minutes

### Scenario

You're deploying a recommendation model that:
- Loads embeddings from Redis on startup (takes 30 seconds)
- Makes predictions using a TensorFlow model
- Caches results in memory (limited to 1GB)
- Calls an external user profile API

### Design Task

Design liveness and readiness probes for this service:

**Liveness Probe:**
```yaml
livenessProbe:
  httpGet:
    path: /_________
    port: ____
  initialDelaySeconds: ____  # Why this value?
  periodSeconds: ____
  failureThreshold: ____

# What should /health check?
# 1.
# 2.
# 3.
```

**Readiness Probe:**
```yaml
readinessProbe:
  httpGet:
    path: /_________
    port: ____
  initialDelaySeconds: ____  # Why this value?
  periodSeconds: ____
  failureThreshold: ____

# What should /ready check?
# 1.
# 2.
# 3.
```

### Questions

1. Why might liveness and readiness check different things?
   ```
   Answer: _______________________________________________
   ```

2. What happens if the external user profile API is down?
   - Should the pod fail liveness? ___
   - Should the pod fail readiness? ___
   - Why?
   ```
   Answer: _______________________________________________
   ```

3. What happens if the 1GB memory cache fills up?
   - Should the pod fail liveness? ___
   - Should the pod fail readiness? ___
   - Why?
   ```
   Answer: _______________________________________________
   ```

---

## Bonus Exercise: Simulate Cascading Failure

**Objective**: Understand how readiness probes prevent cascading failures.

**Time**: 15 minutes

### Scenario

Imagine you have 3 pods, each handling 33% of traffic. If one pod becomes unhealthy:

- **Without readiness probes**: Traffic still goes to unhealthy pod -> Errors -> Unhappy users
- **With readiness probes**: Unhealthy pod removed -> 2 pods handle 50% each -> No errors

### Experiment

1. Deploy v1 with only 2 replicas:
   ```bash
   kubectl scale deployment/model-server --replicas=2
   ```

2. Note the current pods:
   ```bash
   kubectl get pods
   ```

3. Manually make one pod unready by exec-ing into it:
   ```bash
   kubectl exec -it <pod-name> -- /bin/sh
   # Inside the pod, create a file that would fail health
   # (This is simulated - our app doesn't check for files)
   ```

4. Instead, observe what happens when you deploy v2 while watching endpoints:
   ```bash
   # Terminal 1
   watch kubectl get endpoints model-server

   # Terminal 2
   kubectl apply -f k8s/deployment-v2.yaml
   ```

5. Notice how endpoints shrink as pods become unready, protecting users.

### Key Insight

The readiness probe is your first line of defense. It:
- Protects users from bad pods
- Gives you time to rollback
- Prevents cascading failures

---

## Summary Checklist

After completing all exercises, you should be able to:

- [ ] Explain the difference between liveness and readiness probes
- [ ] Interpret pod status (READY, RESTARTS columns)
- [ ] Perform a rollback using kubectl
- [ ] Query Prometheus for model metrics
- [ ] Design appropriate health checks for a service
- [ ] Understand how readiness probes prevent cascading failures

## Reflection

1. What was the most surprising thing you learned?

2. How would you improve the health check design in this module?

3. What other automated recovery mechanisms could complement health probes?
