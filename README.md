# Harden AI: Patch and Recover Incidents Fast - Demo Code

Welcome to the demo code repository for the Coursera course **"Harden AI: Patch and Recover Incidents Fast"**. This repository contains the code used to demonstrate key concepts during the course videos.

## Overview

This repository contains three demo modules, each demonstrating a critical aspect of AI/ML incident response and recovery:

| Module | Topic | Description |
|--------|-------|-------------|
| [Module 1](./module1-canary-deployments/) | Canary Deployments for ML Models | Traffic splitting and automatic rollback |
| [Module 2](./module2-incident-knowledge-base/) | Incident Knowledge Base | Post-mortem templates and tracking |
| [Module 3](./module3-kubernetes-self-healing/) | Kubernetes Self-Healing | Health probes and automatic recovery |

## Purpose

This code accompanies the video demonstrations in the course. You can use it to:

- **Follow along** with the course videos
- **Experiment** with the concepts on your own machine
- **Extend** the examples for your own projects

## Prerequisites

### General Requirements
- Basic understanding of Python programming
- Familiarity with command-line interfaces
- Git installed on your machine

### Module-Specific Requirements

**Module 1: Canary Deployments**
- Python 3.10 or higher
- pip (Python package manager)

**Module 2: Incident Knowledge Base**
- Google account (for Google Docs/Sheets) or similar tools
- GitHub account
- Web browser

**Module 3: Kubernetes Self-Healing**
- Docker Desktop
- Minikube
- kubectl
- Helm 3.x

## Quick Start

```bash
# Clone this repository
git clone https://github.com/desirit/coursera-HardenAI-Patch-and-RecoverIncidentsFast.git
cd coursera-HardenAI-Patch-and-RecoverIncidentsFast

# Navigate to a module
cd module1-canary-deployments

# Follow the README in each module folder
```

## Module Summaries

### Module 1: Canary Deployments for ML Models

Demonstrates how to safely deploy new ML model versions using canary releases:
- Set up MLflow for model versioning
- Implement traffic splitting between production and canary models
- Monitor real-time accuracy metrics
- Trigger automatic rollback when performance degrades

**Technologies:** MLflow, Flask, scikit-learn

### Module 2: Building an Incident Knowledge Base

Demonstrates how to create a searchable repository of incident post-mortems:
- Write structured post-mortem documents
- Organize knowledge in Google Drive
- Track patterns with Google Sheets
- Manage action items with GitHub Issues

**Technologies:** Google Workspace, GitHub Issues, Markdown

### Module 3: Kubernetes Self-Healing Systems

Demonstrates infrastructure that automatically recovers from failures:
- Deploy applications to Kubernetes with health probes
- Configure liveness and readiness checks
- Set up Prometheus monitoring
- Observe automatic pod restarts and rollbacks

**Technologies:** Kubernetes, Docker, Prometheus, Helm

## Learning Objectives

After exploring these demos, you will understand how to:

1. **Implement safe deployment strategies** that minimize the blast radius of ML model failures
2. **Build institutional memory** through structured incident documentation
3. **Design self-healing systems** that automatically detect and recover from failures
4. **Apply monitoring best practices** for AI/ML production systems

## Folder Structure

```
├── README.md                              # This file
├── module1-canary-deployments/
│   ├── README.md                          # Setup and usage guide
│   ├── EXERCISES.md                       # Try-it-yourself exercises
│   ├── app.py                             # Flask canary router
│   ├── setup_models.py                    # MLflow model setup
│   ├── send_requests.py                   # Traffic generator
│   └── requirements.txt
│
├── module2-incident-knowledge-base/
│   ├── README.md                          # Setup and usage guide
│   ├── EXERCISES.md                       # Try-it-yourself exercises
│   ├── templates/
│   │   ├── postmortem_template.md         # Blank template
│   │   ├── sample_postmortem.md           # Example (filled)
│   │   └── github_issue_template.md       # Issue template
│   └── tracking_spreadsheet.csv           # Sample data
│
└── module3-kubernetes-self-healing/
    ├── README.md                          # Setup and usage guide
    ├── EXERCISES.md                       # Try-it-yourself exercises
    ├── model_server.py                    # Flask health probe demo
    ├── Dockerfile                         # Stable version
    ├── Dockerfile.v2                      # Degraded version
    ├── requirements.txt
    └── k8s/
        ├── deployment.yaml                # Stable deployment
        ├── deployment-v2.yaml             # Degraded deployment
        ├── service.yaml
        └── prometheus-values.yaml
```

## Troubleshooting

### Common Issues

**Module 1: MLflow server won't start**
```bash
# Check if port 5001 is in use
lsof -i :5001
# Kill the process if needed
kill -9 <PID>
```

**Module 3: Minikube won't start**
```bash
# Reset minikube
minikube delete
minikube start --driver=docker
```

### Getting Help

- Review the course videos for conceptual understanding
- Check the module-specific README for detailed instructions
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

If you find this demo code helpful, please star this repository and share with your colleagues.
