# GitHub Issue Template for Post-Mortem Action Items

Use this template when creating GitHub Issues from post-mortem action items.

---

## Issue Title Format
```
[Action Summary] (from POST-MORTEM-YYYY-MM-DD)
```

---

## Example Issue

### Title
```
Implement automated drift detection (from POST-MORTEM-2025-01-15)
```

### Labels
- `incident-remediation`
- `model-drift`
- `fraud-detection`
- `p1-high`

### Milestone
```
Q1-2025-Incident-Response
```

### Assignee
```
@[team-member-username]
```

### Description
```markdown
## Context
**Incident:** Fraud Detection Model Drift - 2025-01-15
**Post-Mortem:** [Link to Google Doc or markdown file]

## Root Cause
Model accuracy degraded from 98% to 66% due to input data distribution shift.
A payment processor changed their transaction ID format, introducing characters
the model had never seen during training.

## Action Required
Implement automated drift detection for the fraud detection model that:
1. Monitors input feature distributions in real-time
2. Compares against training data baseline
3. Alerts when distribution shift exceeds threshold (KL divergence > 0.1)
4. Triggers automatic model health check

## Success Criteria
- [ ] Drift detection pipeline deployed to production
- [ ] Alerts configured in PagerDuty
- [ ] Runbook created for drift alert response
- [ ] Drift detected within 30 minutes of distribution shift (vs 5+ hours currently)

## Due Date
2025-02-01

## Dependencies
- Prometheus metrics infrastructure (available)
- Access to training data statistics (need to extract)

## Related Issues
- #143 - Add input schema validation
- #145 - Set up accuracy alerting
```

---

## Labels to Create

| Label | Color | Description |
|-------|-------|-------------|
| `incident-remediation` | #d73a4a (red) | Action item from post-mortem |
| `model-drift` | #0075ca (blue) | Related to model drift issues |
| `data-quality` | #7057ff (purple) | Related to data quality issues |
| `bias-detection` | #e99695 (pink) | Related to bias/fairness issues |
| `p0-critical` | #b60205 (dark red) | Critical priority |
| `p1-high` | #d93f0b (orange) | High priority |
| `p2-medium` | #fbca04 (yellow) | Medium priority |
| `p3-low` | #0e8a16 (green) | Low priority |

---

## Milestones to Create

| Milestone | Due Date | Description |
|-----------|----------|-------------|
| Q1-2025-Incident-Response | 2025-03-31 | Q1 2025 incident remediation items |
| Q2-2025-Incident-Response | 2025-06-30 | Q2 2025 incident remediation items |
| Q3-2025-Incident-Response | 2025-09-30 | Q3 2025 incident remediation items |
| Q4-2025-Incident-Response | 2025-12-31 | Q4 2025 incident remediation items |

---

## Sample Issues to Create for Practice

### Issue #1: Implement automated drift detection
- Labels: `incident-remediation`, `model-drift`, `p1-high`
- Milestone: Q1-2025-Incident-Response
- Status: Open (In Progress)

### Issue #2: Add input schema validation
- Labels: `incident-remediation`, `data-quality`, `p1-high`
- Milestone: Q1-2025-Incident-Response
- Status: Open (Not Started)

### Issue #3: Create vendor change notification process
- Labels: `incident-remediation`, `p2-medium`
- Milestone: Q1-2025-Incident-Response
- Status: Closed

### Issue #4: Set up accuracy alerting
- Labels: `incident-remediation`, `model-drift`, `p1-high`
- Milestone: Q1-2025-Incident-Response
- Status: Open (In Progress)

### Issue #5: Document rollback runbook
- Labels: `incident-remediation`, `documentation`, `p2-medium`
- Milestone: Q1-2025-Incident-Response
- Status: Closed
