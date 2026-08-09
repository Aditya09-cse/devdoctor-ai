# 🩺 DevDoctor-AI

### Track. Investigate. Resolve.

**AI-Powered DevOps Incident Management & Troubleshooting Platform**

DevDoctor-AI is a self-hosted DevOps incident management and troubleshooting platform built with **Flask, PostgreSQL, Ollama, Docker, Kubernetes, GitHub Actions, and DevSecOps tooling**.

It helps engineers **track incidents, investigate infrastructure failures, use AI-assisted troubleshooting, preserve incident knowledge, and automate secure deployments**.

The platform uses a **local LLM through Ollama**, so AI troubleshooting can run without an external AI API.

---

## 🚀 Overview

DevDoctor-AI combines incident management, AI troubleshooting, Kubernetes operations, and DevSecOps automation into a single engineering platform.

```text
                         ┌──────────────────────┐
                         │       ENGINEER       │
                         │      / DEVOPS        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    DevDoctor-AI      │
                         │   Flask Application  │
                         └──────────┬───────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
            ┌────────────┐   ┌────────────┐   ┌────────────┐
            │ PostgreSQL │   │   Ollama   │   │ Kubernetes │
            │  Database  │   │  Local LLM │   │  Runtime   │
            └────────────┘   └────────────┘   └────────────┘
                   │                │                │
                   ▼                ▼                ▼
             Incident Data     AI Analysis      Infrastructure
             Chat History      Troubleshooting   Operations
```

### Core Workflow

```text
Detect
  ↓
Investigate
  ↓
Understand
  ↓
Resolve
  ↓
Learn
  ↓
Prevent
```

---

# ✨ Features

## 🚨 Incident Management

Create and manage operational incidents with:

- Title
- Description
- Category
- Severity
- Status
- Created timestamp
- Updated timestamp
- Resolved timestamp

### Incident Lifecycle

```text
┌─────────┐
│  OPEN   │
└────┬────┘
     │
     ▼
┌────────────────┐
│ INVESTIGATING  │
└───────┬────────┘
        │
        ▼
┌────────────┐
│  RESOLVED  │
└────────────┘
```

---

# 🤖 DevOps AI Assistant

DevDoctor-AI includes a conversational DevOps assistant powered by a **local Ollama LLM**.

Example questions:

```text
Why is my Kubernetes pod restarting?

How do I debug PostgreSQL connection issues?

Why is my Docker container failing?

How do I troubleshoot CrashLoopBackOff?

Why is my application returning HTTP 502?

How do I investigate a failed Kubernetes deployment?
```

### AI Assistant Flow

```text
Engineer Question
       │
       ▼
DevDoctor-AI
       │
       ▼
Ollama Local LLM
       │
       ▼
AI Troubleshooting Response
       │
       ▼
PostgreSQL Chat History
```

---

# 🧠 AI Incident Analysis

DevDoctor-AI can send incident context to Ollama and generate structured troubleshooting guidance.

```text
SUMMARY

LIKELY ROOT CAUSES

TROUBLESHOOTING STEPS

COMMANDS / INVESTIGATION

RECOMMENDED FIX

PREVENTION
```

Supported areas include:

- Kubernetes
- Docker
- Linux
- PostgreSQL
- Networking
- CI/CD
- Cloud infrastructure
- Application failures
- Container failures
- Deployment problems

---

# 📊 Operations Dashboard

The Operations Dashboard provides a centralized operational view.

It is designed to surface:

- Current incidents
- Incident severity
- Incident status
- Open incidents
- Resolved incidents
- Recent operational activity
- AI investigation activity
- Incident health

---

# 📚 Incident Knowledge

DevDoctor-AI stores incidents and investigations to build reusable operational knowledge.

```text
                    Incident
                       │
             ┌─────────┼─────────┐
             │         │         │
             ▼         ▼         ▼
        Investigation  AI      Resolution
                      Analysis
             │         │         │
             └─────────┼─────────┘
                       ▼
                Incident Knowledge
```

Future capabilities can include:

- Historical incident search
- Similar incident detection
- RAG-based troubleshooting
- Incident knowledge retrieval
- Automated root-cause suggestions
- Recurring failure analysis

---

# 🏗 Architecture

```text
                           USER / ENGINEER
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │      DevDoctor-AI       │
                    │     Flask Application   │
                    │       Gunicorn          │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
       ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
       │   PostgreSQL   │ │    Ollama    │ │  Kubernetes   │
       │    Database    │ │  Local LLM   │ │  Environment  │
       └───────┬────────┘ └──────┬───────┘ └───────────────┘
               │                 │
               ▼                 ▼
       Incident Data       AI Troubleshooting
       Chat History        Incident Analysis
       AI Analyses         DevOps Assistant
```

---

# 🧩 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Flask | Backend framework |
| Gunicorn | Production WSGI server |
| PostgreSQL | Persistent database |
| Ollama | Local LLM inference |
| Llama / TinyLlama | AI troubleshooting |
| Docker | Containerization |
| Docker Compose | Local development |
| Kubernetes | Container orchestration |
| PersistentVolume | Persistent storage |
| PersistentVolumeClaim | Storage allocation |
| ConfigMap | Application configuration |
| Kubernetes Secrets | Sensitive configuration |
| Git | Version control |
| GitHub | Source control |
| GitHub Actions | CI/CD automation |
| Bandit | Python security scanning |
| Gitleaks | Secret detection |
| Trivy | Container vulnerability scanning |

---

# 🔐 Security

DevDoctor-AI follows a DevSecOps-oriented development workflow.

Sensitive configuration should never be committed to Git.

```text
.env
k8s/secrets.yml
```

Use:

```text
.env.example
```

as the configuration template.

### Security Controls

```text
Developer
    │
    ▼
GitHub
    │
    ├── Code Quality
    ├── Dependency Scan
    ├── Bandit SAST
    ├── Gitleaks Secret Scan
    ├── Docker Validation
    └── Trivy Image Scan
            │
            ▼
       Secure Image
            │
            ▼
      Kubernetes
```

---

# 🔄 DevSecOps Pipeline

```text
                    Git Push
                       │
                       ▼
                 GitHub Actions
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Code Quality   Dependency Scan   Secret Scan
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                 Docker Lint
                       │
                       ▼
                Docker Build
                       │
                       ▼
                 Trivy Scan
                       │
                       ▼
               Container Image
                       │
                       ▼
             Kubernetes Deployment
```

---

# 📁 GitHub Actions Workflows

```text
.github/workflows/

├── code-quality.yml
├── dependency-scan.yml
├── deploy-to-server.yml
├── devsecops-pipeline.yml
├── docker-build-push.yml
├── docker-lint.yml
├── image-scan.yml
└── secret-scan.yml
```

---

# 🚢 Deployment Path

```text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Code Quality
    ├── Dependency Scan
    ├── Secret Detection
    ├── Docker Lint
    ├── Docker Build
    └── Trivy Scan
            │
            ▼
       Container Image
            │
            ▼
      Deployment Workflow
            │
            ▼
     Kubernetes Cluster
            │
       ┌────┼────┐
       ▼    ▼    ▼
     Flask  DB  Ollama
```

---

# ☸ Kubernetes Architecture

```text
                    Kubernetes Cluster
                           │
                           ▼
                 ai-incident-namespace
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌────────────┐   ┌────────────┐   ┌────────────┐
    │ Flask App  │   │ PostgreSQL │   │   Ollama   │
    │ Deployment │   │ Deployment │   │ Deployment │
    └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
          │                │                │
          ▼                ▼                ▼
    Flask Service     Postgres Service   Ollama Service
          │                │                │
          │                ▼                ▼
          │             PVC / PV          PVC / PV
          │
          ▼
       Application
       Persistent Data
```

---

# 📦 Kubernetes Resources

```text
k8s/

├── ConfigMap.yml
├── app-deployment.yml
├── flask-service.yml
├── namespace.yml
├── postgres-deployment.yml
├── postgres-init.yml
├── postgres-service.yml
├── ollama-deployment.yml
├── ollama-pv.yml
├── ollama-pvc.yml
├── ollama-service.yml
├── pv.yml
└── pvc.yml
```

| Resource | Purpose |
|---|---|
| Namespace | Isolates project resources |
| Flask Deployment | Runs Flask application |
| Flask Service | Exposes Flask application |
| PostgreSQL Deployment | Runs database |
| PostgreSQL Service | Database communication |
| PostgreSQL Init | Database initialization |
| Ollama Deployment | Runs local LLM |
| Ollama Service | AI service communication |
| PV | Persistent storage |
| PVC | Storage request |
| Ollama PV | Persistent model storage |
| Ollama PVC | Ollama storage claim |
| ConfigMap | Non-sensitive configuration |

---

# 🔌 Internal Service Communication

```text
Flask Application
       │
       ├──────────────► PostgreSQL
       │                    │
       │                    └── postgres:5432
       │
       └──────────────► Ollama
                            │
                            └── ollama:11434
```

Kubernetes Services provide stable internal endpoints and DNS-based service discovery.

---

# 🤖 AI Troubleshooting Architecture

```text
                    Incident
                       │
                       ▼
                Incident Details
                       │
                       ▼
                Flask Application
                       │
                       ▼
               Ollama API Request
                       │
                       ▼
                 Local LLM Model
                       │
                       ▼
              Troubleshooting Output
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        Display Result      PostgreSQL
                                │
                                ▼
                         Stored AI Analysis
```

---

# 💾 Data Model

```text
                  ┌──────────────┐
                  │   incidents  │
                  └───────┬──────┘
                          │
                          │ incident_id
                          ▼
                  ┌──────────────┐
                  │  ai_analyses │
                  └──────────────┘


                  ┌──────────────┐
                  │ chat_history │
                  └──────────────┘
```

## `incidents`

```text
id
title
description
category
severity
status
created_at
updated_at
resolved_at
```

## `ai_analyses`

```text
id
incident_id
analysis
created_at
```

## `chat_history`

```text
id
user_message
ai_response
created_at
```

---

# 🩺 Health Checks

## Liveness

```http
GET /health
```

Checks whether the application process is running.

## Readiness

```http
GET /ready
```

Checks whether required dependencies are available.

```text
              /ready
                 │
        ┌────────┴────────┐
        ▼                 ▼
   PostgreSQL          Ollama
        │                 │
        └────────┬────────┘
                 ▼
          Application Ready
```

---

# 🐳 Docker Development

## Start

```bash
docker compose up -d
```

## Check Containers

```bash
docker compose ps
```

## View Logs

```bash
docker compose logs -f
```

## Rebuild

```bash
docker compose up -d --build
```

## Stop

```bash
docker compose down
```

---

# 💻 Run Locally

## Prerequisites

- Python 3.x
- Docker
- Docker Compose
- Git
- Ollama
- Kubernetes and kubectl for Kubernetes deployment

## Clone Repository

```bash
git clone https://github.com/Aditya09-cse/DevDoctor-Ai.git
cd DevDoctor-Ai
```

## Configure Environment

```bash
cp .env.example .env
```

Configure required environment variables.

Never commit `.env`.

## Start with Docker Compose

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
```

---

# ☸ Kubernetes Deployment

## 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yml
```

## 2. Apply ConfigMap

```bash
kubectl apply -f k8s/ConfigMap.yml
```

## 3. Create Persistent Storage

```bash
kubectl apply -f k8s/pv.yml
kubectl apply -f k8s/pvc.yml
kubectl apply -f k8s/ollama-pv.yml
kubectl apply -f k8s/ollama-pvc.yml
```

## 4. Deploy PostgreSQL

```bash
kubectl apply -f k8s/postgres-init.yml
kubectl apply -f k8s/postgres-deployment.yml
kubectl apply -f k8s/postgres-service.yml
```

## 5. Deploy Ollama

```bash
kubectl apply -f k8s/ollama-deployment.yml
kubectl apply -f k8s/ollama-service.yml
```

## 6. Deploy Flask Application

```bash
kubectl apply -f k8s/app-deployment.yml
kubectl apply -f k8s/flask-service.yml
```

## 7. Verify

```bash
kubectl get all -n ai-incident-namespace
```

```bash
kubectl get pods -n ai-incident-namespace
```

```bash
kubectl get svc -n ai-incident-namespace
```

---

# 🌐 Access Application

For local Kubernetes:

```bash
kubectl port-forward \
svc/flask-service \
5001:80 \
-n ai-incident-namespace
```

Then open:

```text
http://localhost:5001
```

Use the actual service name and port defined in `k8s/flask-service.yml` if different.

---

# 🛠 Useful Kubernetes Commands

### Pods

```bash
kubectl get pods -n ai-incident-namespace
```

```bash
kubectl get pods -n ai-incident-namespace -w
```

### Services

```bash
kubectl get svc -n ai-incident-namespace
```

### Deployments

```bash
kubectl get deployments -n ai-incident-namespace
```

### Persistent Volumes

```bash
kubectl get pv
```

### Persistent Volume Claims

```bash
kubectl get pvc -n ai-incident-namespace
```

### Logs

```bash
kubectl logs <pod-name> -n ai-incident-namespace
```

```bash
kubectl logs -f <pod-name> -n ai-incident-namespace
```

### Describe Pod

```bash
kubectl describe pod <pod-name> \
-n ai-incident-namespace
```

### Execute Shell

```bash
kubectl exec -it <pod-name> \
-n ai-incident-namespace -- bash
```

### Deployment Details

```bash
kubectl describe deployment <deployment-name> \
-n ai-incident-namespace
```

### Events

```bash
kubectl get events \
-n ai-incident-namespace \
--sort-by=.lastTimestamp
```

### Restart Deployment

```bash
kubectl rollout restart deployment <deployment-name> \
-n ai-incident-namespace
```

### Check Rollout

```bash
kubectl rollout status deployment <deployment-name> \
-n ai-incident-namespace
```

### Rollout History

```bash
kubectl rollout history deployment <deployment-name> \
-n ai-incident-namespace
```

### Rollback

```bash
kubectl rollout undo deployment <deployment-name> \
-n ai-incident-namespace
```

---

# 🔍 Incident Troubleshooting Workflow

```text
                 INCIDENT DETECTED
                        │
                        ▼
                 CREATE INCIDENT
                        │
                        ▼
                    INVESTIGATE
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
       Manual Debugging       AI Assistance
             │                     │
             │                  Ollama
             │                     │
             └──────────┬──────────┘
                        ▼
                   ROOT CAUSE
                        │
                        ▼
                    APPLY FIX
                        │
                        ▼
                      VERIFY
                        │
                        ▼
                     RESOLVE
                        │
                        ▼
                STORE KNOWLEDGE
```

---

# 🧪 DevOps Troubleshooting Examples

## Kubernetes

```text
CrashLoopBackOff
ImagePullBackOff
Pending Pods
Failed Probes
Service Connectivity
Deployment Failures
Configuration Errors
```

## Docker

```text
Port Already Allocated
Container Crash
Image Build Failure
Environment Variable Problems
Container Networking
Volume Problems
```

## PostgreSQL

```text
Connection Refused
Authentication Errors
Database Unavailable
Connection Pool Problems
Initialization Failures
```

## Linux

```text
High CPU
High Memory
Disk Problems
Process Failures
Permission Problems
Network Connectivity
```

## CI/CD

```text
Pipeline Failure
Docker Build Failure
Secret Detection
Security Scan Failure
Deployment Failure
```

---

# 📂 Project Structure

```text
DevDoctor-Ai/
│
├── .github/
│   └── workflows/
│       ├── code-quality.yml
│       ├── dependency-scan.yml
│       ├── deploy-to-server.yml
│       ├── devsecops-pipeline.yml
│       ├── docker-build-push.yml
│       ├── docker-lint.yml
│       ├── image-scan.yml
│       └── secret-scan.yml
│
├── app/
│   ├── app.py
│   ├── db.py
│   ├── ollama_client.py
│   ├── requirements.txt
│   ├── static/
│   └── templates/
│
├── database/
│   └── init.sql
│
├── k8s/
│   ├── ConfigMap.yml
│   ├── app-deployment.yml
│   ├── flask-service.yml
│   ├── namespace.yml
│   ├── postgres-deployment.yml
│   ├── postgres-init.yml
│   ├── postgres-service.yml
│   ├── ollama-deployment.yml
│   ├── ollama-pv.yml
│   ├── ollama-pvc.yml
│   ├── ollama-service.yml
│   ├── pv.yml
│   └── pvc.yml
│
├── .env.example
├── .gitignore
├── .trivyignore
├── Dockerfile
├── docker-compose.yml
├── kind-config.yml
└── README.md
```

---

# 🔄 End-to-End Platform Flow

```text
                         ENGINEER
                            │
                            ▼
                    DevDoctor-AI UI
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        Incidents       AI Assistant    Dashboard
             │              │              │
             ▼              ▼              │
        PostgreSQL        Ollama            │
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                    Incident Knowledge
                            │
                            ▼
                     DevOps Operations
                            │
                            ▼
                       Kubernetes
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
           Flask        PostgreSQL       Ollama
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                     CI/CD + DevSecOps
                            │
                  ┌─────────┼─────────┐
                  │         │         │
                  ▼         ▼         ▼
                Bandit   Gitleaks   Trivy
                  │         │         │
                  └─────────┼─────────┘
                            ▼
                     Secure Deployment
```

---

# 🏭 Engineering Focus

DevDoctor-AI is designed as a practical DevOps/SRE engineering project.

```text
                    DevDoctor-AI
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
 Application         Infrastructure     Security
 Engineering         Engineering        Engineering
       │                 │                 │
       ▼                 ▼                 ▼
     Flask            Docker           Bandit
  PostgreSQL        Kubernetes        Gitleaks
       │                 │              Trivy
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
                    Automation
                         │
                         ▼
                   GitHub Actions
                         │
                         ▼
                         AI
                         │
                         ▼
                       Ollama
```

### Engineering Areas

- Linux operations
- Python development
- Flask
- PostgreSQL
- Docker
- Docker Compose
- Kubernetes
- Kubernetes networking
- Persistent storage
- ConfigMaps
- Secrets
- Health probes
- CI/CD
- GitHub Actions
- DevSecOps
- SAST
- Secret scanning
- Container security
- Vulnerability scanning
- Incident management
- Local LLM inference
- AI-assisted troubleshooting

---

# 📈 Engineering Roadmap

## ✅ Implemented

- [x] Incident management
- [x] Incident lifecycle
- [x] PostgreSQL persistence
- [x] AI incident analysis
- [x] DevOps AI Assistant
- [x] Chat history
- [x] Operations dashboard
- [x] Incident knowledge foundation
- [x] Docker containerization
- [x] Docker Compose
- [x] Kubernetes deployment
- [x] PostgreSQL on Kubernetes
- [x] Ollama on Kubernetes
- [x] Persistent storage
- [x] ConfigMap integration
- [x] Kubernetes Secrets support
- [x] Health endpoints
- [x] Kubernetes health probes
- [x] GitHub Actions
- [x] DevSecOps pipeline
- [x] Code quality checks
- [x] Dependency scanning
- [x] Secret scanning
- [x] Docker linting
- [x] Trivy image scanning
- [x] Automated deployment workflow

## 🚧 Future Improvements

### Observability

- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Centralized logging
- [ ] Alerting
- [ ] Distributed tracing
- [ ] Application performance monitoring

### AI

- [ ] RAG-based incident knowledge
- [ ] Historical incident similarity
- [ ] Automated root-cause analysis
- [ ] Larger local models
- [ ] Multi-model support
- [ ] AI-generated remediation plans
- [ ] Automated incident summarization

### Kubernetes

- [ ] Helm chart
- [ ] Horizontal Pod Autoscaling
- [ ] Resource requests and limits
- [ ] NetworkPolicies
- [ ] Ingress
- [ ] TLS
- [ ] Production storage classes
- [ ] High availability

### DevSecOps

- [ ] SBOM generation
- [ ] Image signing
- [ ] Supply-chain security
- [ ] Policy enforcement
- [ ] Automated rollback
- [ ] Deployment gates

---

# 🎯 Project Goal

DevDoctor-AI combines:

```text
Software Development
        +
Containerization
        +
Kubernetes
        +
CI/CD
        +
DevSecOps
        +
Infrastructure Operations
        +
Local Artificial Intelligence
        =
DevDoctor-AI
```

The long-term goal is to evolve DevDoctor-AI into an intelligent **DevOps/SRE incident investigation platform** that helps engineers move from:

```text
Detect
  ↓
Investigate
  ↓
Understand
  ↓
Resolve
  ↓
Learn
  ↓
Prevent
```

---

# ⚡ DevDoctor-AI

### Track. Investigate. Resolve.

**AI-Powered DevOps Incident Management & Troubleshooting Platform**

Built with:

```text
Python • Flask • PostgreSQL • Ollama
Docker • Kubernetes • GitHub Actions
DevSecOps • Local AI
```

**Built by Aditya Singh Tomar**
