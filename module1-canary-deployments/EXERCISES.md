# Module 1: Exercises

Complete these hands-on exercises to reinforce your understanding of canary deployments.

---

## Exercise 1: Observe Traffic Splitting

**Objective**: Understand how traffic is distributed between production and canary models.

**Time**: 10 minutes

### Steps

1. Make sure MLflow and the app server are running (see README.md)

2. Reset the system to a clean state:
   ```bash
   python send_requests.py reset
   ```

3. Send 50 test requests:
   ```bash
   python send_requests.py send 50
   ```

4. View the metrics:
   ```bash
   python send_requests.py metrics
   ```

### Expected Output

You should see output similar to:
```
  ┌─────────────┬──────────┬──────────┬─────────────┐
  │   Model     │ Requests │ Accuracy │ Avg Latency │
  ├─────────────┼──────────┼──────────┼─────────────┤
  │ 🔵 production │       40 │   100.0% │       2.1ms │
  │ 🟡 canary     │       10 │   100.0% │       2.3ms │
  └─────────────┴──────────┴──────────┴─────────────┘
```

### Questions to Answer

1. What percentage of requests went to the canary model?
2. Is this percentage close to the configured 20%?
3. Why might the actual percentage differ slightly from the configured value?

### Your Answers

```
1. _______________________________________________________

2. _______________________________________________________

3. _______________________________________________________
```

---

## Exercise 2: Gradual Rollout Simulation

**Objective**: Practice the gradual rollout strategy used in production deployments.

**Time**: 15 minutes

### Background

In real-world deployments, you typically:
1. Start with a very small percentage (1-5%)
2. Monitor for issues
3. Gradually increase if metrics look good
4. Roll back immediately if problems appear

### Steps

1. Reset the system:
   ```bash
   python send_requests.py reset
   ```

2. Set canary to 5%:
   ```bash
   python send_requests.py canary 5
   ```

3. Send 30 requests and record the canary request count:
   ```bash
   python send_requests.py send 30
   python send_requests.py metrics
   ```

4. Increase to 10% and repeat:
   ```bash
   python send_requests.py canary 10
   python send_requests.py send 30
   python send_requests.py metrics
   ```

5. Continue with 20%, 50%, then 100%

### Data Collection Table

| Canary % | Requests Sent | Canary Requests | Canary Accuracy |
|----------|---------------|-----------------|-----------------|
| 5%       | 30            |                 |                 |
| 10%      | 30            |                 |                 |
| 20%      | 30            |                 |                 |
| 50%      | 30            |                 |                 |
| 100%     | 30            |                 |                 |

### Questions to Answer

1. At what canary percentage would you feel confident promoting the canary to production?

2. What metrics would you want to see before increasing the percentage?

3. How long would you wait at each stage in a real production environment?

### Your Answers

```
1. _______________________________________________________

2. _______________________________________________________

3. _______________________________________________________
```

---

## Exercise 3: Automatic Rollback

**Objective**: Experience how automatic rollback protects your system from bad deployments.

**Time**: 15 minutes

### Steps

1. Reset the system:
   ```bash
   python send_requests.py reset
   ```

2. Verify canary is at 20%:
   ```bash
   python send_requests.py metrics
   ```

3. Enable failure simulation (this makes the canary model produce wrong predictions 40% of the time):
   ```bash
   python send_requests.py fail
   ```

4. Send requests to accumulate metrics:
   ```bash
   python send_requests.py send 20
   ```

5. Check the metrics - notice the canary accuracy has dropped:
   ```bash
   python send_requests.py metrics
   ```

6. Trigger the rollback check:
   ```bash
   python send_requests.py rollback
   ```

7. Check metrics again:
   ```bash
   python send_requests.py metrics
   ```

### Expected Behavior

When canary accuracy drops below 85% (the threshold), the system should:
- Set canary percentage to 0%
- Route all traffic to production
- Display a rollback alert

### Questions to Answer

1. What was the canary accuracy before rollback was triggered?

2. What is the canary percentage after rollback?

3. Why is automatic rollback critical for ML systems in production?

4. What could happen if you didn't have automatic rollback?

### Your Answers

```
1. _______________________________________________________

2. _______________________________________________________

3. _______________________________________________________

4. _______________________________________________________
```

---

## Exercise 4: Customize the Rollback Threshold

**Objective**: Understand the trade-offs in setting accuracy thresholds.

**Time**: 10 minutes

### Steps

1. Open `app.py` in a text editor

2. Find the line:
   ```python
   ACCURACY_THRESHOLD = 85  # Rollback if below 85%
   ```

3. Change it to:
   ```python
   ACCURACY_THRESHOLD = 90  # Rollback if below 90%
   ```

4. Save the file and restart the app server (Ctrl+C, then `python app.py`)

5. Repeat Exercise 3 with the new threshold

### Questions to Answer

1. Did the rollback trigger faster with a 90% threshold?

2. What are the pros of a higher threshold (e.g., 95%)?

3. What are the cons of a higher threshold?

4. How would you determine the right threshold for your production system?

### Your Answers

```
1. _______________________________________________________

2. _______________________________________________________

3. _______________________________________________________

4. _______________________________________________________
```

---

## Bonus Exercise: Add Latency-Based Rollback

**Objective**: Extend the rollback logic to include latency checks.

**Time**: 20 minutes

### Challenge

Currently, the `/check_rollback` endpoint only checks accuracy. Modify it to also check latency.

### Requirements

1. Calculate the P95 latency for the canary model
2. If P95 latency exceeds `LATENCY_THRESHOLD` (100ms), trigger rollback
3. Log a clear message indicating whether rollback was due to accuracy or latency

### Hints

```python
# Calculate P95 latency
import numpy as np
latencies = metrics["canary"]["latencies"]
p95_latency = np.percentile(latencies, 95) if latencies else 0
```

### Verification

1. Test by adding artificial delay to the canary model
2. Verify that high latency triggers rollback even when accuracy is good

---

## Reflection Questions

After completing all exercises, consider these broader questions:

1. **Real-World Scale**: How would this system need to change if you had millions of requests per second instead of dozens?

2. **Multiple Metrics**: Besides accuracy and latency, what other metrics might you want to monitor?

3. **A/B Testing**: How is canary deployment different from A/B testing?

4. **Feature Flags**: How could you combine canary deployments with feature flags?

5. **Shadow Mode**: What if you wanted to test the canary model without affecting users at all?

---

## Summary

By completing these exercises, you have:

- [ ] Observed traffic splitting between model versions
- [ ] Practiced gradual rollout strategies
- [ ] Experienced automatic rollback protection
- [ ] Modified threshold configurations
- [ ] (Bonus) Extended rollback logic with latency checks

**Congratulations!** You now understand the fundamentals of canary deployments for ML models.
