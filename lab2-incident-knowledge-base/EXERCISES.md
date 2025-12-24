# Lab 2: Exercises

Complete these hands-on exercises to build your incident knowledge base skills.

---

## Exercise 1: Write a Post-Mortem from Scratch

**Objective**: Practice writing a complete post-mortem document.

**Time**: 15 minutes

### Scenario

You are the on-call engineer for an e-commerce recommendation system. Here's what happened:

```
Incident Details:
-----------------
Date: February 3, 2025
System: Product Recommendation Engine
Duration: 4 hours (06:00 - 10:00 UTC)

What happened:
- The recommendation API started returning the same 10 products for all users
- This affected personalization for approximately 50,000 users
- Conversion rate dropped from 3.2% to 1.1% during the outage

Root cause:
- The user embedding cache was configured with a 24-hour TTL
- A deployment at 05:45 cleared the cache
- The embedding generation service was rate-limited and couldn't repopulate
- System fell back to "most popular" products for all users

How it was discovered:
- Automated A/B test monitoring detected significant conversion drop
- Alert fired at 06:30 (30 minutes after incident started)

How it was resolved:
- Increased rate limits on embedding service temporarily
- Pre-warmed cache with priority users first
- Added circuit breaker to prevent cascade failures
```

### Your Task

1. Create a new file called `my_postmortem.md`
2. Use the template from `templates/postmortem_template.md`
3. Fill in ALL sections based on the scenario above
4. Include at least 4 action items with realistic owners and due dates
5. Add appropriate tags for searchability

### Checklist

- [ ] Title follows naming convention
- [ ] Tags are searchable and relevant
- [ ] Timeline has at least 6 entries
- [ ] Root cause is clearly explained
- [ ] Contributing factors identified (at least 3)
- [ ] "What went well" section included
- [ ] Action items have owners and due dates
- [ ] Lessons learned section completed

---

## Exercise 2: Create GitHub Issues from Action Items

**Objective**: Track post-mortem action items using GitHub Issues.

**Time**: 10 minutes

### Steps

1. Go to GitHub and create a new repository called `incident-response-lab`

2. Create the following labels:
   - `incident-remediation` (color: #d73a4a)
   - `model-drift` (color: #0075ca)
   - `data-quality` (color: #7057ff)
   - `caching` (color: #bfd4f2)
   - `p1-high` (color: #d93f0b)
   - `p2-medium` (color: #fbca04)

3. Create a milestone: `Q1-2025-Incident-Response`

4. Create at least 2 GitHub Issues from your post-mortem action items:
   - Use the template from `templates/github_issue_template.md`
   - Apply appropriate labels
   - Assign to the milestone
   - Add success criteria as checkboxes

### Example Issue Title
```
Implement cache pre-warming on deployment (from POST-MORTEM-2025-02-03)
```

### Deliverable

Provide the URLs to your GitHub Issues:
```
Issue 1: https://github.com/YOUR_USERNAME/incident-response-lab/issues/1
Issue 2: https://github.com/YOUR_USERNAME/incident-response-lab/issues/2
```

---

## Exercise 3: Analyze Incident Patterns

**Objective**: Learn to identify patterns across multiple incidents.

**Time**: 10 minutes

### Data Analysis

Open `tracking_spreadsheet.csv` and answer the following questions:

1. **Category Distribution**

   Count the incidents by category:
   - Model Drift: ___
   - Data Quality: ___
   - Bias Emergence: ___
   - Performance: ___

2. **Severity Analysis**

   Count by severity:
   - P1 (Critical): ___
   - P2 (High): ___
   - P3 (Medium): ___

3. **System Patterns**

   Which system has the most incidents? ___________

   How many incidents does it have? ___

4. **Action Item Completion**

   How many incidents have all action items complete? ___

   How many still have open items? ___

### Pattern Recognition Questions

Based on your analysis:

1. If you could only invest in fixing one category of issues, which would have the most impact?
   ```
   Answer: _______________________________________________
   Reasoning: ____________________________________________
   ```

2. What systemic improvements could prevent multiple incident types?
   ```
   Answer: _______________________________________________
   ```

3. Are there any seasonal patterns in when incidents occur?
   ```
   Answer: _______________________________________________
   ```

---

## Exercise 4: Create a Folder Structure

**Objective**: Organize documentation for searchability.

**Time**: 5 minutes

### Task

Create a local folder structure that mirrors what you would use in production:

```bash
mkdir -p AI-Incidents/2025/{January,February,March}
mkdir -p AI-Incidents/2024/{October,November,December}
mkdir -p AI-Incidents/Templates
mkdir -p AI-Incidents/Dashboards
```

### Then:

1. Copy the template to `AI-Incidents/Templates/POST-MORTEM-TEMPLATE.md`
2. Copy the sample to `AI-Incidents/2025/January/POST-MORTEM_FraudDetection_ModelDrift_20250115.md`
3. Move your Exercise 1 post-mortem to the appropriate folder

### Verification

Run this command to see your structure:
```bash
find AI-Incidents -type f -name "*.md" | sort
```

Expected output:
```
AI-Incidents/2025/January/POST-MORTEM_FraudDetection_ModelDrift_20250115.md
AI-Incidents/2025/February/my_postmortem.md (or similar)
AI-Incidents/Templates/POST-MORTEM-TEMPLATE.md
```

---

## Bonus Exercise: Cross-Reference Analysis

**Objective**: Practice linking related incidents for deeper insights.

**Time**: 10 minutes

### Scenario

You notice that Fraud Detection has had 3 incidents in the past 4 months:
- 2024-10-10: Currency conversion rate changes (Model Drift)
- 2024-11-28: Missing feature values (Data Quality)
- 2025-01-15: Vendor format change (Model Drift)

### Questions

1. What's the common theme across these incidents?
   ```
   Answer: ________________________________________________
   ```

2. What systemic fix could prevent all three types of issues?
   ```
   Answer: ________________________________________________
   ```

3. Draft a "Related Incidents" section for the January 2025 post-mortem that references the other two incidents with brief explanations:
   ```markdown
   ## Related Incidents
   - [Your response here]
   ```

4. What label would you create in GitHub to track all Fraud Detection issues across categories?
   ```
   Label name: ___________________
   Color: _______________________
   Description: _________________
   ```

---

## Summary Checklist

After completing all exercises, you should have:

- [ ] Written a complete post-mortem document
- [ ] Created a GitHub repository with labels and milestones
- [ ] Created 2+ GitHub Issues from action items
- [ ] Analyzed incident patterns from spreadsheet data
- [ ] Set up an organized folder structure
- [ ] (Bonus) Identified cross-incident patterns

## Reflection Questions

1. What was the most challenging part of writing a post-mortem?

2. How would you ensure your team actually reads and learns from post-mortems?

3. What automation could help with incident documentation?

4. How often should you review past incidents for patterns?
