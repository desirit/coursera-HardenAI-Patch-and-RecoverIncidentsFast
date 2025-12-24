# Module 2: Building an Incident Knowledge Base

## Overview

This module demonstrates how to build a searchable repository of incident post-mortems that serves as **institutional memory** for your team. When incidents happen (and they will), having documented lessons learned helps you:

1. Avoid repeating the same mistakes
2. Onboard new team members quickly
3. Identify patterns across multiple incidents
4. Track remediation action items to completion

### What You'll Learn

- How to write effective post-mortem documents
- How to organize incident documentation for searchability
- How to track action items from incidents
- How to identify patterns across multiple incidents

### Why This Matters

Most teams learn from incidents... and then forget. The engineer who debugged the issue leaves the company, the Slack thread gets buried, and the same incident happens six months later.

A structured post-mortem knowledge base prevents this knowledge loss and turns every incident into a learning opportunity for the entire organization.

## Prerequisites

- Google account (for Google Docs/Sheets) OR access to similar tools (Notion, Confluence)
- GitHub account (for issue tracking)
- Web browser

## What's Included

This module contains documentation templates and examples:

1. A post-mortem template
2. A sample filled-out post-mortem
3. A tracking spreadsheet
4. GitHub Issues templates for action item tracking

## Part 1: Understanding Post-Mortems

### What is a Post-Mortem?

A post-mortem (also called "incident review" or "retrospective") is a documented analysis of an incident that answers:

- **What happened?** - Timeline of events
- **Why did it happen?** - Root cause analysis
- **What will we do about it?** - Action items to prevent recurrence

### Key Principles

1. **Blameless** - Focus on systems, not individuals
2. **Thorough** - Document everything relevant
3. **Actionable** - Every post-mortem should produce concrete improvements
4. **Accessible** - Anyone in the org should be able to find and learn from it

## Part 2: The Post-Mortem Template

### Review the Template

Open `templates/postmortem_template.md` in this folder. This template includes:

| Section | Purpose |
|---------|---------|
| Tags | Searchable labels for categorization |
| Incident Summary | Quick overview (duration, impact, severity) |
| Timeline | Chronological event log |
| Root Cause | Technical explanation |
| Contributing Factors | What made the problem worse |
| What Went Well | Positive observations (balance!) |
| Action Items | Tracked improvements |
| Lessons Learned | Knowledge to share |

### Using the Template

You can use this template in:

- **Google Docs** - Create a doc, paste the template, save to Templates folder
- **Notion** - Create a template database
- **Confluence** - Create a page template
- **Local Markdown** - Keep in your team's repository

## Part 3: Sample Post-Mortem

Check out `templates/sample_postmortem.md` for a complete example based on this scenario:

**Scenario: Fraud Detection Model Drift**

```
Date: January 15, 2025
System: Fraud Detection Model
Duration: 5.4 hours

What happened:
- Model accuracy degraded from 98% to 66%
- 23,000 transactions were misclassified
- $47,000 in false fraud blocks

Root cause:
- Payment processor changed transaction ID format
- Model's feature extraction treated new format as anomalies
- No automated drift detection was in place

How it was resolved:
- Rolled back to previous model version via MLflow
- Added input schema validation
```

## Part 4: Tracking System

### Option A: Google Sheets Tracker

Create a spreadsheet with these columns:

| Column | Description |
|--------|-------------|
| Date | When the incident occurred |
| System | Which system was affected |
| Category | Type of failure (drift, data quality, etc.) |
| Severity | P0-P3 rating |
| Root Cause | One-line summary |
| Action Items | Count of open items |
| Status | Open / Closed |
| Post-Mortem Link | URL to the document |

Import `tracking_spreadsheet.csv` to see sample data.

### Option B: GitHub Issues

Create GitHub Issues for each action item from your post-mortem:

1. **Create Labels:**
   - `incident-remediation` (red) - Action from post-mortem
   - `model-drift` (blue) - Drift-related issues
   - `data-quality` (purple) - Data issues
   - `p0-critical`, `p1-high`, `p2-medium`, `p3-low` - Priority levels

2. **Create Milestones:**
   - Q1-2025-Incident-Response
   - Q2-2025-Incident-Response

3. **Create Issues:**
   - Use the format in `templates/github_issue_template.md`
   - Link back to the post-mortem document
   - Assign owners and due dates

## Part 5: Organize for Searchability

### Folder Structure

Create a folder structure that makes it easy to find post-mortems:

```
AI-Incidents/
├── 2025/
│   ├── January/
│   │   ├── POST-MORTEM_FraudDetection_ModelDrift_20250115.md
│   │   └── POST-MORTEM_ImageClassifier_FormatError_20250120.md
│   └── February/
│       └── ...
├── Templates/
│   └── POST-MORTEM-TEMPLATE.md
└── Dashboards/
    └── Incident-Tracker.csv (or Google Sheet link)
```

### Naming Convention

Use a consistent naming pattern:
```
POST-MORTEM_[System]_[Category]_[YYYYMMDD]
```

Examples:
- `POST-MORTEM_FraudDetection_ModelDrift_20250115`
- `POST-MORTEM_RecommendationEngine_DataStale_20250203`
- `POST-MORTEM_ChatBot_APIRateLimit_20250217`

### Tags for Search

Always include searchable tags in your post-mortems:
- **System:** `fraud-detection`, `recommendations`, `search`
- **Category:** `model-drift`, `data-quality`, `infrastructure`
- **Severity:** `p0-critical`, `p1-high`, `p2-medium`, `p3-low`
- **Team:** `ml-platform`, `data-engineering`, `product`

## Try It Yourself

See `EXERCISES.md` for hands-on exercises including:

1. Writing your own post-mortem from a scenario
2. Setting up GitHub Issues with proper labels
3. Analyzing patterns in incident data

## Key Takeaways

1. **Document everything** - Future you (and your teammates) will thank you
2. **Blameless culture** - Focus on systems, not people
3. **Track action items** - Post-mortems without follow-through are useless
4. **Make it searchable** - Use consistent naming, tags, and organization
5. **Look for patterns** - Multiple incidents with the same label indicate systemic issues

## Further Reading

- [Google's Post-Mortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [PagerDuty Post-Mortem Guide](https://postmortems.pagerduty.com/)
- [Etsy's Blameless Post-Mortems](https://www.etsy.com/codeascraft/blameless-postmortems)

## Next Steps

After exploring this demo, check out:
- **Module 3**: Kubernetes Self-Healing Systems
