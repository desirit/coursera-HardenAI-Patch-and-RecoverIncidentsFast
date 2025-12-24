# POST-MORTEM: Fraud Detection - Model Drift - 2025-01-15

---

## Tags
`model-drift` `tensorflow` `production` `p1-severity` `fraud-detection-team`

---

## Incident Summary
**Duration:** 2025-01-15 09:23 UTC to 2025-01-15 14:47 UTC (5.4 hours)
**Impact:** 23,000 transactions misclassified; $47,000 in false fraud blocks
**Severity:** P1
**Detection:** Customer complaints about blocked legitimate purchases

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 09:23 | Model accuracy begins degrading (detected in retrospect) |
| 10:15 | First customer complaint about blocked transaction |
| 11:30 | Support escalates to engineering after 12 similar complaints |
| 11:45 | On-call engineer begins investigation |
| 12:30 | Identifies model drift as root cause |
| 13:15 | Decision made to rollback to previous model version |
| 14:00 | Rollback initiated via MLflow |
| 14:47 | Service restored, accuracy returns to baseline |

---

## Root Cause
Distribution shift in input data caused model drift. A payment processor changed their transaction ID format on January 14th, introducing characters the model had never seen during training. The model's feature extraction treated these as anomalies, increasing false positive rate from 2% to 34%.

---

## Contributing Factors
- **No drift monitoring:** We lacked automated detection for input distribution changes
- **No vendor change notifications:** Payment processor didn't notify us of format change
- **Slow detection:** Relied on customer complaints instead of automated alerts
- **Missing validation:** No input schema validation before model inference

---

## What Went Well
- Rollback process worked smoothly (15 minutes once decision made)
- Team collaboration was excellent during incident
- MLflow versioning made previous model immediately available
- Customer support flagged pattern quickly

---

## Action Items

| ID | Action | Owner | Due Date | Status | GitHub Issue |
|----|--------|-------|----------|--------|--------------|
| 1 | Implement automated drift detection | @ml-engineer-1 | 2025-02-01 | In Progress | #142 |
| 2 | Add input schema validation | @ml-engineer-2 | 2025-02-15 | Not Started | #143 |
| 3 | Create vendor change notification process | @ops-lead | 2025-01-30 | Complete | #144 |
| 4 | Set up accuracy alerting (< 95% threshold) | @ml-engineer-1 | 2025-02-01 | In Progress | #145 |
| 5 | Document rollback runbook | @ml-engineer-2 | 2025-01-25 | Complete | #146 |

---

## Lessons Learned
1. **Input validation is as important as model accuracy** - External data format changes can silently break models
2. **Customer complaints are a lagging indicator** - Need proactive monitoring before users notice
3. **Vendor relationships need engineering involvement** - Technical changes should be communicated to ML teams
4. **Drift can happen suddenly** - Not just gradual; external changes cause step-function shifts

---

## Related Incidents
- 2024-09-22: Recommendations model drift (similar root cause - data format change)
- 2024-11-03: Search ranking degradation (different cause - training data staleness)

---

**Post-Mortem Author:** [ML Team Lead]
**Review Date:** 2025-01-17
**Attendees:** ML Team Lead, Senior ML Engineer, Data Engineer, Engineering Manager
