# Lab 1: Canary Deployments for ML Models

## Overview

In this lab, you'll implement a **canary deployment** strategy for machine learning models. Canary deployments allow you to safely roll out new model versions by gradually shifting traffic from your stable production model to the new version while monitoring performance metrics.

### What You'll Learn

- How to set up MLflow for model versioning and registry
- How to implement traffic splitting between model versions
- How to monitor real-time accuracy and latency metrics
- How to trigger automatic rollback when performance degrades

### Why This Matters

In production ML systems, deploying a new model is risky. The model may:
- Have lower accuracy on real-world data
- Cause unexpected errors for edge cases
- Have performance regressions (higher latency)

Canary deployments minimize these risks by exposing only a small percentage of traffic to the new model initially, allowing you to catch problems before they affect all users.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Basic understanding of Flask web applications
- Familiarity with ML model concepts

## Architecture

```
                    ┌─────────────────────────────────────────────────┐
                    │              Flask Canary Router                │
                    │                                                 │
   Requests ───────►│   if random() < CANARY_PERCENTAGE:              │
                    │       route_to(canary_model)     ────► 🟡 Canary│
                    │   else:                                         │
                    │       route_to(production_model) ────► 🔵 Prod  │
                    │                                                 │
                    │   Track: accuracy, latency per model            │
                    └─────────────────────────────────────────────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   Rollback Check    │
                              │                     │
                              │ if canary_accuracy  │
                              │    < threshold:     │
                              │   CANARY = 0%       │
                              └─────────────────────┘
```

## Quick Start

### Step 1: Set Up Your Environment

```bash
# Navigate to this lab directory
cd lab1-canary-deployments

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start MLflow Server

Open a **new terminal** and run:

```bash
cd lab1-canary-deployments
source venv/bin/activate
mlflow server --host 127.0.0.1 --port 5001
```

You should see MLflow start on http://127.0.0.1:5001

### Step 3: Register Models

In your **original terminal**:

```bash
python setup_models.py
```

This creates two model versions:
- **Version 1 (Production)**: The stable, tested model
- **Version 2 (Staging/Canary)**: The new model being tested

### Step 4: Start the Canary Router

```bash
python app.py
```

The server starts on http://127.0.0.1:8080

### Step 5: Send Test Traffic

Open a **third terminal**:

```bash
cd lab1-canary-deployments
source venv/bin/activate

# Send 20 test requests
python send_requests.py send 20

# View metrics
python send_requests.py metrics
```

## Understanding the Code

### Key File: `app.py`

The core routing logic is in the `/predict` endpoint:

```python
# CANARY ROUTING DECISION
if random.random() * 100 < CANARY_PERCENTAGE:
    # Route to CANARY model (new version)
    model_version = "canary"
    model = canary_model
else:
    # Route to PRODUCTION model (stable version)
    model_version = "production"
    model = production_model
```

### Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CANARY_PERCENTAGE` | 20 | Percentage of traffic to canary |
| `ACCURACY_THRESHOLD` | 85 | Minimum accuracy before rollback |
| `LATENCY_THRESHOLD` | 100 | Maximum P95 latency (ms) |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Make a prediction (automatically routed) |
| `/metrics` | GET | View accuracy and latency per model |
| `/check_rollback` | POST | Trigger rollback check |
| `/set_canary/<n>` | POST | Set canary percentage to n% |
| `/simulate_failure/1` | POST | Enable failure simulation |
| `/reset` | POST | Reset all metrics |

## Lab Exercises

Complete these exercises to deepen your understanding. See `EXERCISES.md` for detailed instructions.

### Exercise 1: Observe Traffic Splitting (10 min)

1. Start the system (MLflow + app.py)
2. Send 50 requests: `python send_requests.py send 50`
3. View metrics: `python send_requests.py metrics`
4. **Question**: What percentage of requests went to canary? Is it close to 20%?

### Exercise 2: Gradual Rollout (15 min)

1. Reset the system: `python send_requests.py reset`
2. Set canary to 5%: `python send_requests.py canary 5`
3. Send 30 requests and check metrics
4. Increase to 10%, 20%, then 50%
5. **Question**: At what percentage would you feel confident promoting the canary to production?

### Exercise 3: Automatic Rollback (15 min)

1. Reset the system
2. Enable failure simulation: `python send_requests.py fail`
3. Send 20 requests
4. Trigger rollback check: `python send_requests.py rollback`
5. **Observe**: What happened to the canary percentage?
6. **Question**: Why is automatic rollback important for ML systems?

### Exercise 4: Modify the Threshold (10 min)

1. Open `app.py` and find `ACCURACY_THRESHOLD`
2. Change it from 85 to 90
3. Restart the server and repeat Exercise 3
4. **Question**: How does a stricter threshold affect the rollback behavior?

## Common Issues

### MLflow Connection Error

```
Error: Could not connect to MLflow server
```

**Solution**: Make sure MLflow is running on port 5001:
```bash
mlflow server --host 127.0.0.1 --port 5001
```

### Port Already in Use

```
Error: Address already in use
```

**Solution**: Kill the existing process:
```bash
lsof -i :8080  # or :5001
kill -9 <PID>
```

### Models Not Loading

```
Error: Model version not found
```

**Solution**: Re-run the setup script:
```bash
python setup_models.py
```

## Key Takeaways

1. **Gradual Rollout**: Start with a small canary percentage (5-10%) and increase gradually
2. **Metrics-Driven Decisions**: Always compare accuracy and latency between versions
3. **Automatic Protection**: Set thresholds that trigger rollback without human intervention
4. **Blast Radius**: If canary fails at 10%, only 10% of users were affected

## Further Reading

- [MLflow Model Registry Documentation](https://mlflow.org/docs/latest/model-registry.html)
- [Canary Deployments Explained](https://martinfowler.com/bliki/CanaryRelease.html)
- [Progressive Delivery](https://www.split.io/glossary/progressive-delivery/)

## Next Steps

After completing this lab, proceed to:
- **Lab 2**: Building an Incident Knowledge Base
- **Lab 3**: Kubernetes Self-Healing Systems
