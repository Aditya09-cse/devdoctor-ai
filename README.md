# DevDoctor-AI

**AI-Powered DevOps Incident Management & Troubleshooting Platform**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-K8s-326CE5?logo=kubernetes&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?logo=ollama&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?logo=gunicorn&logoColor=white)

---

## Overview

DevDoctor-AI is an incident management console for tracking infrastructure and application incidents — the kind of tool an SRE or platform team uses to log, triage, and resolve production issues — with a locally-hosted LLM wired in to help analyze and troubleshoot them.

Every incident is stored in PostgreSQL with a category (Linux, Docker, Kubernetes, AWS, CI/CD, Database, Networking, Application, Other), a severity, and a status. On demand, the app sends the incident's details to a self-hosted Ollama model and stores the model's structured analysis alongside the incident. A separate AI Assistant page provides free-form conversational troubleshooting help, independent of any specific incident.

Ollama is used instead of a hosted LLM API so the entire stack — app, database, and model — runs without external API keys or network dependencies, which matters for a tool meant to help during infrastructure incidents (including ones where outbound internet access may be degraded). PostgreSQL backs incident records, AI analyses, and assistant chat history with proper relational integrity (analyses cascade-delete with their parent incident).

The project is packaged as a container image, deployed to Kubernetes with resource limits, liveness/readiness probes, persistent storage, and horizontal autoscaling, and shipped through a multi-stage GitHub Actions pipeline that lints, scans, builds, scans again, and deploys to an EC2-hosted Kubernetes cluster — the same shape of workflow used to ship real services.

## Core Features

- **Incident lifecycle** — create, list, filter (status/severity/search), view, and transition incidents through `Open → Investigating → Resolved`, with `resolved_at` tracked automatically.
- **AI incident analysis** — one-click analysis that sends the incident to a local LLM and returns a structured breakdown, stored permanently against the incident.
- **AI DevOps assistant** — a separate conversational page for general troubleshooting questions, backed by chat history persisted in Postgres.
- **Operations dashboard** — live counts of total / open / investigating / resolved / critical-open incidents, plus the 8 most recent incidents.
- **Incident history** — searchable archive of resolved incidents.
- **Health, readiness, and metrics endpoints** — for container orchestration probes and basic scraping.

## Incident Management

Incidents are created with a title, description, category, and severity (`create_incident`), and their status is updated independently via a dedicated route (`update_status`) that also manages `resolved_at`. Listing supports combined filtering by status, severity, and a case-insensitive search across title, description, and category (`ILIKE`).

## DevOps AI Assistant

`/assistant` is a standalone chat interface. Each message is sent to Ollama's `/api/chat` endpoint with a fixed system prompt that scopes the model to Linux, Docker, Kubernetes, AWS, Git, GitHub Actions, CI/CD, Terraform, Ansible, PostgreSQL, networking, and monitoring topics, and instructs it to give direct, concise, non-generic answers (including inferring likely causes for short errors like `CrashLoopBackOff` or `ImagePullBackOff`). Every exchange is persisted to `chat_history` and the last 30 are shown, oldest first.

## AI Incident Analysis

`analyze_incident()` builds a prompt from the incident's ID, title, category, severity, and description, and sends it to Ollama's `/api/generate` endpoint with a system prompt that forces a fixed structure:

```
SUMMARY
LIKELY ROOT CAUSES
TROUBLESHOOTING STEPS
COMMANDS
RECOMMENDED FIX
VERIFICATION
PREVENTION
```

The model is explicitly instructed not to invent logs or claim a confirmed root cause without evidence. The result is stored in `ai_analyses` and rendered on the incident detail page; a failed call returns an HTTP 503 with the error shown inline rather than crashing the request.

## Operations Dashboard

`/` runs a single aggregate query (`COUNT(*) FILTER (...)`) for total, open, investigating, resolved, and critical-open counts, and a second query for the 8 most recently created incidents.

## Incident History

`/history` returns only `status = 'Resolved'` incidents, ordered by `resolved_at` (nulls last) then `created_at`, with the same search behavior as the incidents list.

## Architecture

```
                         ┌────────────┐
                         │    User    │
                         └─────┬──────┘
                               │ HTTP
                               ▼
                  ┌────────────────────────┐
                  │   Flask + Gunicorn      │
                  │   (2 workers, :5001)    │
                  │  /health /ready /metrics│
                  └───────┬────────┬────────┘
                           │        │
                  psycopg  │        │  REST (Ollama HTTP API)
                           ▼        ▼
                ┌──────────────┐  ┌───────────────────┐
                │  PostgreSQL  │  │   Ollama server     │
                │  incidents   │  │  llama3.2 / tinyllama│
                │  ai_analyses │  └───────────────────┘
                │ chat_history │
                └──────────────┘
```

Flask talks to PostgreSQL through `psycopg` (via `db.py`, using a context-managed cursor that commits on success and rolls back on any exception) and to Ollama over plain HTTP using the `requests` library — there is no ORM and no message queue; both integrations are direct, synchronous calls.

## Kubernetes Architecture

Everything runs inside a dedicated `ai-incident-namespace`:

| Resource | Name | Notes |
|---|---|---|
| Deployment | `ai-incident-deployment` | App, 2 replicas, requests `100m`/`128Mi`, limits `500m`/`512Mi` |
| Deployment | `postgres-deployment` | 1 replica |
| Deployment | `ollama` | 1 replica, `initContainer` pulls `tinyllama:latest` before the main container starts |
| Service | `ai-incident-service` | `NodePort`, port `80` → `5001`, nodePort `31697` |
| Service | `postgres` | `ClusterIP`, port `5432` |
| Service | `ollama` | `ClusterIP`, port `11434` |
| ConfigMap | `database-variable` | `DB_NAME`, `DB_USER`, `DB_HOST`, `DB_PORT` |
| ConfigMap | `postgres-init` | Embeds the full schema, mounted at `/docker-entrypoint-initdb.d` |
| Secret | `db-secrets` | `DB_PASSWORD` — created at deploy time by `deploy.sh`, never committed |
| PV / PVC | `ai-incident-pv` / `ai-incident-pvc` | `hostPath` volume, 512Mi / 256Mi, mounted at `/app/data` in the app container |
| PV / PVC | `ollama-incident-pv` / `ollama-incident-pvc` | `hostPath` volume, 1Gi, mounted at `/root/.ollama` for model storage |
| HPA | `my-app-hpa` | Targets `ai-incident-deployment` |

```
Namespace: ai-incident-namespace
┌──────────────────────────────────────────────────────────┐
│                                                            │
│   ai-incident-deployment (2 pods) ──► ai-incident-service │
│         │            │                    (NodePort)      │
│         │            │                                    │
│         ▼            ▼                                    │
│   postgres-deployment    ollama (1 pod, tinyllama)         │
│         │                     │                            │
│         ▼                     ▼                            │
│   ai-incident-pvc      ollama-incident-pvc                 │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

The app deployment mounts a `/app/data` PVC, but nothing in `app.py` reads from or writes to that path — all application state (incidents, analyses, chat history) is stored in PostgreSQL, not on this volume.

## Internal Service Communication

Inside the cluster, the app resolves `postgres` and `ollama` through Kubernetes' internal DNS — no IPs, no external endpoints:

- **Flask → PostgreSQL**: `DB_HOST=postgres` (from the `database-variable` ConfigMap) on port `5432`, authenticated with `DB_PASSWORD` from the `db-secrets` Secret.
- **Flask → Ollama**: `OLLAMA_URL=http://ollama:11434`, set directly as an environment value on the app deployment (not sourced from the ConfigMap).

## AI Troubleshooting Flow

```
Incident created
       │
       ▼
User clicks "Analyze"
       │
       ▼
Flask builds a structured prompt (ID, title, category, severity, description)
       │
       ▼
POST /api/generate  ──►  Ollama (model: OLLAMA_MODEL, temp 0.2, 700 tokens, 180s timeout)
       │
       ▼
Structured 7-section response returned
       │
       ▼
Stored in ai_analyses, rendered on incident detail page
```

The Assistant follows the same request shape but calls `/api/chat` with a conversation-style payload (system + user message) instead of a single prompt string, and nothing is tied to an `incident_id`.

`ollama_health()` calls `GET /api/tags` with a 3-second timeout and returns a boolean, used only by `/ready`.

## Data Model

```
incidents                       ai_analyses
─────────────────               ──────────────────
id            SERIAL PK   ┌───► incident_id  FK → incidents.id (ON DELETE CASCADE)
title         VARCHAR     │     analysis      TEXT
description   TEXT        │     created_at    TIMESTAMP
category      VARCHAR     │
severity      VARCHAR     │
status        VARCHAR     │
created_at    TIMESTAMP   │
updated_at    TIMESTAMP   │
resolved_at   TIMESTAMP   ┘

chat_history
──────────────────
id             SERIAL PK
user_message   TEXT
ai_response    TEXT
created_at     TIMESTAMP
```

Indexes: `idx_incidents_status`, `idx_incidents_created` (`created_at DESC`), `idx_ai_incident` (`ai_analyses.incident_id`).

`category` is a free-form label validated against `{Linux, Docker, Kubernetes, AWS, CI/CD, Terraform, Database, Networking, Application, Other}` — this is an incident classification tag, not an indication that Terraform is used anywhere in this project's own infrastructure.

## Health / Readiness / Metrics

| Endpoint | Behavior |
|---|---|
| `/health` | Static liveness check — always returns `{"status": "healthy", "service": "incident-manager"}`. Used by the Kubernetes liveness and readiness probes. |
| `/ready` | Runs `SELECT 1` against Postgres and calls Ollama's `/api/tags`; returns `200` only if both succeed, otherwise `503` with per-dependency booleans. Not wired to any Kubernetes probe. |
| `/metrics` | Hand-written Prometheus text-exposition format (`# HELP` / `# TYPE`, content-type `version=0.0.4`) exposing `incidents_total`, `incidents_open`, `incidents_investigating`, `incidents_resolved` as gauges. No metrics client library, and no Prometheus server is deployed in this repository to scrape it. |

## Containerization

`Dockerfile` builds from `python:3.12-slim`, installs `app/requirements.txt`, copies the `app/` directory, creates and switches to a non-root `appuser`, exposes port `5001`, and runs:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--timeout", "180", "app:app"]
```

`docker-compose.yml` runs three services on a shared bridge network (`app-network`):

- **app** — built from the published image `aditya0910/ai-powered-incident-manager-app`, port `5001:5001`, waits on Postgres's healthcheck and Ollama's start.
- **postgres** — `postgres:16-alpine`, schema loaded from `database/init.sql` via the standard init-scripts mount, with a `pg_isready` healthcheck.
- **ollama** — `ollama/ollama:latest`, with a named volume for model storage.

Both the app and Postgres use named volumes (`postgres-data`, `ollama-data`) for persistence across container restarts.

## Kubernetes Autoscaling

`app-hpa.yml` targets `ai-incident-deployment` with:

| Setting | Value |
|---|---|
| Min replicas | 2 |
| Max replicas | 3 |
| CPU target | 60% average utilization |
| Memory target | 500Mi average value |
| Scale-down stabilization | 60s |

Only the app deployment autoscales — Postgres and Ollama run as fixed single-replica deployments.

## DevSecOps Pipeline

`devsecops-pipeline.yml` is the entry point, triggered on push to `main` or manually via `workflow_dispatch`. It composes seven reusable workflows:

```
push to main / workflow_dispatch
        │
        ▼
┌───────────────┬────────────────┬──────────────────┬───────────────┐
│ Code-Quality   │ Secrets-Scan   │ Dependency-Scan   │ Docker-Scan   │
│ flake8 + bandit│ gitleaks       │ pip-audit         │ hadolint      │
└───────┬────────┴────────┬───────┴─────────┬─────────┴──────┬────────┘
        └─────────────────┴─────────────────┴─────────────────┘
                                  │
                                  ▼
                        Build (docker build & push)
                                  │
                                  ▼
                     trivy (image vulnerability scan)
                                  │
                                  ▼
                deploy (SCP manifests + SSH into EC2 → deploy.sh → verify.sh)
```

| Stage | Tool | What it does |
|---|---|---|
| Code-Quality | flake8, bandit | Lints and SAST-scans `app/app.py` |
| Secrets-Scan | Gitleaks | Scans the full git history for committed secrets |
| Dependency-Scan | pip-audit | Checks `app/requirements.txt` for known CVEs |
| Docker-Scan | Hadolint | Lints the `Dockerfile` |
| Build | Docker Buildx | Builds and pushes to Docker Hub, tagged with the branch ref, `latest`, and the commit SHA |
| trivy | Trivy | Scans the pushed image for HIGH/CRITICAL CVEs, fails the build on any (`exit-code: 1`), respecting `.trivyignore` |
| deploy | appleboy scp-action / ssh-action | Copies `k8s/`, `deploy.sh`, `verify.sh` to the EC2 host, then runs them over SSH |

## CI/CD Deployment Flow

`deploy-to-server.yml` copies `k8s/`, `scripts/deploy.sh`, and `scripts/verify.sh` to the target EC2 host's home directory over SCP, then SSHes in and runs `deploy.sh` with `DB_PASSWORD`, `DOCKER_IMAGE`, and `IMAGE_TAG` (the commit SHA) exported as environment variables, followed by `verify.sh`.

## Security

- **Non-root container**: the Dockerfile creates `appuser` and switches to it before running Gunicorn.
- **Secret handling**: `DB_PASSWORD` is never committed — `.env` and `k8s/secrets.yml` are both git-ignored, and the Kubernetes Secret is created imperatively by `deploy.sh` from a CI-provided environment variable.
- **CI secrets**: Docker Hub credentials, the EC2 SSH host/user/key, and `DB_PASSWORD` are all consumed as GitHub Actions secrets, passed to reusable workflows via `secrets: inherit`.
- **Static analysis**: Bandit (Python SAST) and Hadolint (Dockerfile lint) run on every pipeline execution.
- **Dependency scanning**: pip-audit checks the Python dependency tree; Trivy scans the built image and fails the pipeline on unfixed HIGH/CRITICAL CVEs (`.trivyignore` currently lists two placeholder CVE IDs).
- **Secret scanning**: Gitleaks runs against full git history (`fetch-depth: 0`) on every pipeline execution.

None of this is presented as enterprise-grade coverage — it's a standard open-source scanning toolchain wired into CI rather than a bolt-on afterthought.

## Automation Scripts

| Script | Purpose |
|---|---|
| `scripts/setup.sh` | Provisions a fresh Ubuntu host: updates packages, installs Docker, `kubectl`, and `kind`, creates a local Kind cluster (`aditya-cluster`) from `kind-config.yml`, installs the Kubernetes Metrics Server, and patches it with `--kubelet-insecure-tls` for local use. |
| `scripts/deploy.sh` | Applies the namespace, creates/updates the `db-secrets` Secret from `$DB_PASSWORD`, applies ConfigMaps and storage, deploys Postgres, Ollama, and the app, applies the HPA, updates the app image to `$DOCKER_IMAGE:$IMAGE_TAG`, and waits on the rollout. |
| `scripts/verify.sh` | Prints versions (Docker, kubectl, Kind), cluster nodes, all pods, Metrics Server status, polls `kubectl top nodes` until metrics are available, then prints app pods, pod metrics, HPA status, and running containers. |

`deploy.sh` and `verify.sh` both assume they're running on the target host with `k8s/` and `scripts/` copied into the home directory — this is how `deploy-to-server.yml` stages them via SCP before running.

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask 3.1, Gunicorn |
| Database | PostgreSQL 16 (Alpine), `psycopg[binary]` |
| AI | Ollama (`llama3.2` / `tinyllama`, configurable via `OLLAMA_MODEL`) |
| Frontend | Server-rendered Jinja2 templates, vanilla JS, hand-written CSS |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes (Kind for local, EC2-hosted cluster for CI/CD) |
| Autoscaling | Kubernetes HPA (`autoscaling/v2`) |
| CI/CD | GitHub Actions (reusable workflows) |
| Security tooling | Flake8, Bandit, pip-audit, Hadolint, Gitleaks, Trivy |

## Project Structure

```
DevDoctor-Ai/
├── .github/workflows/
│   ├── devsecops-pipeline.yml      # Orchestrator
│   ├── code-quality.yml            # flake8 + bandit
│   ├── secret-scan.yml             # gitleaks
│   ├── dependency-scan.yml         # pip-audit
│   ├── docker-lint.yml             # hadolint
│   ├── docker-build-push.yml       # build & push to Docker Hub
│   ├── image-scan.yml              # trivy
│   └── deploy-to-server.yml        # SCP + SSH deploy to EC2
├── app/
│   ├── app.py                      # Flask routes
│   ├── db.py                       # psycopg connection/cursor
│   ├── ollama_client.py            # Ollama /api/generate & /api/chat
│   ├── requirements.txt
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── incidents.html
│       ├── incident.html
│       ├── history.html
│       └── assistant.html
├── database/
│   └── init.sql                    # Schema for local/Docker Compose use
├── k8s/
│   ├── namespace.yml
│   ├── ConfigMap.yml
│   ├── postgres-init.yml
│   ├── postgres-deployment.yml
│   ├── postgres-service.yml
│   ├── ollama-deployment.yml
│   ├── ollama-service.yml
│   ├── ollama-pv.yml
│   ├── ollama-pvc.yml
│   ├── app-deployment.yml
│   ├── flask-service.yml
│   ├── app-hpa.yml
│   ├── pv.yml
│   └── pvc.yml
├── scripts/
│   ├── setup.sh                    # Host provisioning + Kind cluster
│   ├── deploy.sh                   # Kubernetes deployment
│   └── verify.sh                   # Post-deploy verification
├── Dockerfile
├── docker-compose.yml
├── kind-config.yml
├── .env.example
├── .trivyignore
└── .gitignore
```

## Local Development

```bash
git clone https://github.com/Aditya09-cse/DevDoctor-Ai.git
cd DevDoctor-Ai

cp .env.example .env
# edit .env with your own DB_PASSWORD, etc.

docker compose up -d --build
```

This starts the Flask app, PostgreSQL (schema auto-applied from `database/init.sql`), and Ollama on a shared Docker network. The app is available at `http://localhost:5001`.

Pull a model into the running Ollama container if it isn't already present:

```bash
docker exec -it devops-ai-ollama ollama pull llama3.2:1b
```

## Docker Compose

| Service | Image | Ports | Notes |
|---|---|---|---|
| `app` | `aditya0910/ai-powered-incident-manager-app:latest` | `5001:5001` | Waits for Postgres healthcheck |
| `postgres` | `postgres:16-alpine` | internal only | `pg_isready` healthcheck, schema mounted read-only |
| `ollama` | `ollama/ollama:latest` | internal only | Model data on named volume `ollama-data` |

## Kubernetes Deployment

**Local (Kind):**

```bash
./scripts/setup.sh      # installs Docker, kubectl, kind; creates the cluster + Metrics Server
```

`setup.sh` provisions the cluster only — it does not deploy the application. Once the cluster is up, apply the manifests (or run `deploy.sh` with `~/k8s` and `~/scripts` present, and `DB_PASSWORD` / `DOCKER_IMAGE` / `IMAGE_TAG` exported, matching how CI runs it):

```bash
export DB_PASSWORD=yourpassword
export DOCKER_IMAGE=aditya0910/ai-powered-incident-manager-app
export IMAGE_TAG=latest

./scripts/deploy.sh
./scripts/verify.sh
```

**AWS EC2 (automated via CI/CD):** on every push to `main`, `deploy-to-server.yml` copies `k8s/`, `deploy.sh`, and `verify.sh` to the EC2 host and runs the same two scripts over SSH — this is the production deployment path and requires no manual steps beyond configuring the repository secrets (`EC2_SSH_HOST`, `EC2_SSH_USER`, `EC2_SSH_PRIVATE_KEY`, `DB_PASSWORD`, `DOCKERHUB_USER`, `DOCKERHUB_PASSWORD`).

## Application Access

- **Kind (local)**: `flask-service.yml` exposes the app as a `NodePort` on `31697`, and `kind-config.yml` maps that same port from the control-plane container to the host — so once deployed, the app is reachable at `http://localhost:31697`.
- **Docker Compose (local)**: the app is bound directly to the host at `http://localhost:5001`.
- **EC2**: the app is reachable on the same NodePort (`31697`) on the host's public IP/DNS, as configured by whoever provisions the EC2 instance and its security group — no specific IP or DNS is defined in this repository.

## Useful Kubernetes Commands

```bash
kubectl get pods -n ai-incident-namespace
kubectl get svc -n ai-incident-namespace
kubectl get hpa -n ai-incident-namespace
kubectl top pods -n ai-incident-namespace

kubectl logs -n ai-incident-namespace deployment/ai-incident-deployment
kubectl describe pod -n ai-incident-namespace <pod-name>

kubectl rollout status deployment/ai-incident-deployment -n ai-incident-namespace
kubectl rollout undo deployment/ai-incident-deployment -n ai-incident-namespace
```

## Engineering Focus

This project's surface area is the incident manager; its substance is everything around it — a Flask backend with parameterized SQL and a clean separation between routing, data access, and AI integration; a container image built as a non-root user; a Kubernetes deployment with real resource limits, liveness/readiness probes, persistent storage for stateful components, and CPU/memory-based autoscaling; and a CI/CD pipeline that gates every build behind linting, SAST, dependency auditing, Dockerfile linting, secret scanning, and image vulnerability scanning before it ever reaches EC2.

---

### Track. Investigate. Resolve.

**DevDoctor-AI** — built by Aditya Singh Tomar

[github.com/Aditya09-cse/DevDoctor-Ai](https://github.com/Aditya09-cse/DevDoctor-Ai)