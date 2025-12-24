# Lab 2: Building an Incident Knowledge Base

## Overview

In this lab, you'll learn how to build a searchable repository of incident post-mortems that serves as **institutional memory** for your team. When incidents happen (and they will), having documented lessons learned helps you:

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

## Lab Structure

This lab is primarily documentation-based. You'll be creating:

1. A post-mortem template
2. A sample filled-out post-mortem
3. A tracking spreadsheet
4. GitHub Issues for action item tracking

**Estimated Time:** 20-30 minutes

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

## Part 2: Create Your Post-Mortem Template

### Step 1: Review the Template

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

### Step 2: Create Your Own Template

You can use this template in:

- **Google Docs** - Create a doc, paste the template, save to Templates folder
- **Notion** - Create a template database
- **Confluence** - Create a page template
- **Local Markdown** - Keep in your team's repository

## Part 3: Write a Sample Post-Mortem

### Exercise: Document a Hypothetical Incident

Use the scenario below to practice writing a post-mortem.

**Scenario: Image Classification API Failure**

```
Date: January 20, 2025
System: Product Image Classifier
Duration: 3 hours (10:00 - 13:00 UTC)

What happened:
- The image classification API started returning "Unknown" for all images
- 15,000 products were incorrectly categorized during the outage
- Customer-facing catalog showed wrong categories

Root cause:
- A new version of the model was deployed that expected PNG images
- The production pipeline was sending JPEG images
- The model failed silently, defaulting to "Unknown" category

How it was resolved:
- Rolled back to the previous model version
- Added input format validation to the API
```

### Your Task

1. Open `templates/sample_postmortem.md` for reference
2. Create a new file `my_postmortem.md`
3. Fill in all sections based on the scenario above
4. Add realistic action items

## Part 4: Create a Tracking System

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

## Lab Exercises

### Exercise 1: Write Your Own Post-Mortem (15 min)

Using the scenario from Part 3:
1. Create a new post-mortem document
2. Fill in all sections
3. Create 3-5 realistic action items
4. Add appropriate tags

### Exercise 2: Set Up Tracking (10 min)

1. Create a GitHub repository called `incident-response`
2. Add the labels listed in Part 4
3. Create 2-3 issues from your post-mortem action items
4. Assign a milestone

### Exercise 3: Pattern Recognition (5 min)

Review the sample data in `tracking_spreadsheet.csv`:
1. Which category has the most incidents?
2. What's the average time to resolution?
3. Are there any patterns in when incidents occur?

## Self-Assessment Checklist

After completing this lab, you should be able to:

- [ ] Explain the purpose of a blameless post-mortem
- [ ] Create a post-mortem from an incident description
- [ ] Set up a searchable folder structure for documentation
- [ ] Track action items in GitHub Issues with proper labeling
- [ ] Identify patterns across multiple incidents

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

After completing this lab, proceed to:
- **Lab 3**: Kubernetes Self-Healing Systems
