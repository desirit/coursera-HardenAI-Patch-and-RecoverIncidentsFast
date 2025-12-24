# Harden AI: Patch and Recover Incidents Fast - Hands-On Labs

Welcome to the hands-on labs for the Coursera course **"Harden AI: Patch and Recover Incidents Fast"**. These labs provide practical experience with the key concepts covered in the course.

## Overview

This repository contains three self-contained lab modules, each focusing on a critical aspect of AI/ML incident response and recovery:

| Lab | Topic | Time Required | Difficulty |
|-----|-------|---------------|------------|
| [Lab 1](./lab1-canary-deployments/) | Canary Deployments for ML Models | 30-45 min | Beginner |
| [Lab 2](./lab2-incident-knowledge-base/) | Building an Incident Knowledge Base | 20-30 min | Beginner |
| [Lab 3](./lab3-kubernetes-self-healing/) | Kubernetes Self-Healing Systems | 45-60 min | Intermediate |

## Prerequisites

### General Requirements
- Basic understanding of Python programming
- Familiarity with command-line interfaces
- Git installed on your machine

### Lab-Specific Requirements

**Lab 1: Canary Deployments**
- Python 3.10 or higher
- pip (Python package manager)

**Lab 2: Incident Knowledge Base**
- Google account (for Google Docs/Sheets)
- GitHub account
- Web browser

**Lab 3: Kubernetes Self-Healing**
- Docker Desktop
- Minikube
- kubectl
- Helm 3.x

## Quick Start

```bash
# Clone this repository
git clone https://github.com/desirit/coursera-HardenAI-Patch-and-RecoverIncidentsFast.git
cd coursera-HardenAI-Patch-and-RecoverIncidentsFast

# Navigate to a lab
cd lab1-canary-deployments

# Follow the README in each lab folder
```

## Lab Summaries

### Lab 1: Canary Deployments for ML Models

Learn how to safely deploy new ML model versions using canary releases:
- Set up MLflow for model versioning
- Implement traffic splitting between production and canary models
- Monitor real-time accuracy metrics
- Trigger automatic rollback when performance degrades

**Key Skills:** MLflow, Flask, A/B testing, gradual rollouts

### Lab 2: Building an Incident Knowledge Base

Create a searchable repository of incident post-mortems:
- Write structured post-mortem documents
- Organize knowledge in Google Drive
- Track patterns with Google Sheets
- Manage action items with GitHub Issues

**Key Skills:** Documentation, incident management, knowledge sharing

### Lab 3: Kubernetes Self-Healing Systems

Build infrastructure that automatically recovers from failures:
- Deploy applications to Kubernetes with health probes
- Configure liveness and readiness checks
- Set up Prometheus monitoring
- Observe automatic pod restarts and rollbacks

**Key Skills:** Kubernetes, Docker, Prometheus, infrastructure resilience

## Learning Objectives

After completing these labs, you will be able to:

1. **Implement safe deployment strategies** that minimize the blast radius of ML model failures
2. **Build institutional memory** through structured incident documentation
3. **Design self-healing systems** that automatically detect and recover from failures
4. **Apply monitoring best practices** for AI/ML production systems

## Folder Structure

```
student-labs/
├── README.md                           # This file
├── lab1-canary-deployments/
│   ├── README.md                       # Lab guide
│   ├── EXERCISES.md                    # Hands-on exercises
│   ├── app.py                          # Flask canary router
│   ├── setup_models.py                 # MLflow model setup
│   ├── send_requests.py                # Traffic generator
│   ├── quick_setup.sh                  # Automated setup
│   └── requirements.txt
│
├── lab2-incident-knowledge-base/
│   ├── README.md                       # Lab guide
│   ├── EXERCISES.md                    # Hands-on exercises
│   ├── templates/
│   │   ├── postmortem_template.md      # Blank template
│   │   ├── sample_postmortem.md        # Example (filled)
│   │   └── github_issue_template.md    # Issue template
│   ├── tracking_spreadsheet.csv        # Sample data
│   └── github_setup/                   # GitHub repo templates
│
└── lab3-kubernetes-self-healing/
    ├── README.md                       # Lab guide
    ├── EXERCISES.md                    # Hands-on exercises
    ├── model_server.py                 # Flask health probe demo
    ├── Dockerfile                      # Stable version
    ├── Dockerfile.v2                   # Degraded version
    ├── deploy.sh                       # Deployment script
    ├── requirements.txt
    └── k8s/
        ├── deployment.yaml             # Stable deployment
        ├── deployment-v2.yaml          # Degraded deployment
        ├── service.yaml
        └── prometheus-values.yaml
```

## Troubleshooting

### Common Issues

**Lab 1: MLflow server won't start**
```bash
# Check if port 5001 is in use
lsof -i :5001
# Kill the process if needed
kill -9 <PID>
```

**Lab 3: Minikube won't start**
```bash
# Reset minikube
minikube delete
minikube start --driver=docker
```

### Getting Help

- Review the course videos for conceptual understanding
- Check the lab-specific README for detailed instructions
- Open an issue in this repository for technical problems

## Contributing

Found a bug or have a suggestion? We welcome contributions!

1. Fork this repository
2. Create a feature branch (`git checkout -b fix/issue-description`)
3. Make your changes
4. Submit a pull request

## Author

**Ritesh Vajariya**
Email: ritesh@goaiguru.com
GitHub: [@desirit](https://github.com/desirit)

## License

This educational material is provided under the MIT License as part of the Coursera course "Harden AI: Patch and Recover Incidents Fast".

---

**Happy Learning!**

If you find these labs helpful, please star this repository and share with your colleagues.
