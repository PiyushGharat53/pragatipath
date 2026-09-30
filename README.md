# प्रगतीPath — Longitudinal Livelihood Outcome Intelligence (Prototype)

Smart India Hackathon 2026 · Government of Maharashtra, Dept. of Skills, Employment, Entrepreneurship & Innovation · Team Silicon Horizons

**Live demo:** https://piyushgharat53.github.io/pragatipath/

प्रगतीPath is an outcome-intelligence layer that complements Mahaswayam, MSSDS and SIDH. It follows trainees **after** certification and turns fragmented post-training signals into longitudinal, privacy-conscious livelihood insight, moving from "how many completed training?" to "what happened to them afterwards?".

> All data in this prototype is **synthetic**. No real trainee, employer or government data is used, and there is no live integration with EPFO / Udyam / NCS / NAPS. These are roadmap items.

## What the prototype demonstrates

| Screen | Shows |
| --- | --- |
| Government | KPIs, status by 3/6/12/18/24-month checkpoint, non-placement and attrition reasons, course and district outcomes, attrition-risk watchlist |
| Training provider | Same lens per provider, course breakdown, provider comparison (outcome index) |
| Trainee | Journey timeline, low-burden follow-up form, automatic reason classification from free text |
| Employer | One-tap employment confirmation and optional skill feedback (raises outcome confidence) |
| Identity linkage | Different programme IDs and name spellings resolved into one unified profile |

Outcome types: employed, self-employed, apprentice, unemployed, no response.
Confidence tiers: self-reported → employer-confirmed → registry-matched (simulated).

## Run locally (with API)

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
python seed.py                   # regenerates frontend/data.json
uvicorn main:app --reload
```

Open http://localhost:8000. API docs are at http://localhost:8000/docs.

## Static demo mode (GitHub Pages)

The repo root contains an `index.html` that redirects to `frontend/`. With no backend running, the dashboard loads `frontend/data.json` and runs entirely in the browser. The header badge shows **Live API** or **Static demo mode**.

To publish: **Settings → Pages → Deploy from a branch → `main` → `/ (root)`**.

## Project structure

```
pragatipath/
├── index.html          redirect to frontend/ (for GitHub Pages)
├── README.md
├── backend/
│   ├── main.py         FastAPI app + REST API
│   ├── seed.py         synthetic data generator
│   └── requirements.txt
└── frontend/
    ├── index.html      dashboard (single file, Chart.js)
    └── data.json       generated demo data
```

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Health check |
| GET | `/api/trainees` | All trainee records with checkpoints |
| GET | `/api/trainees/{id}` | Single trainee profile |
| POST | `/api/trainees/{id}/checkpoint` | Submit a follow-up update (consent-gated) |
| POST | `/api/trainees/{id}/verify` | Employer confirmation and skill feedback |
| POST | `/api/classify` | Classify free-text reasons into categories |

## Prototype vs. production

| Prototype | Production plan |
| --- | --- |
| In-memory store | PostgreSQL with audit logs, RBAC and encryption |
| Keyword reason classifier | Trained NLP classifier (scikit-learn) |
| Rule-based attrition risk | ML model with explainable drivers |
| Deterministic ID matching | Fuzzy matching, consent ledger and human review |
| Simulated verification tiers | EPFO/UAN, Udyam/GST, NCS and NAPS integrations |
| Web forms | Multi-channel follow-up (SMS / WhatsApp / IVR) |

Production deployment would be designed in accordance with applicable Indian data-protection, security and government data-governance requirements, including the DPDP Act 2023.

## Tech stack

FastAPI · Python · Chart.js · vanilla JavaScript (production plan: React, PostgreSQL, scikit-learn, Power BI)