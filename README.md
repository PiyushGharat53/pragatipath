# प्रगतीPath — Longitudinal Livelihood Outcome Intelligence (Prototype)

Smart India Hackathon · Government of Maharashtra, Dept. of Skills, Employment, Entrepreneurship & Innovation · Team Silicon Horizons

A working prototype of an outcome-intelligence layer that complements Mahaswayam, MSSDS and SIDH. It follows trainees **after** certification and turns fragmented signals into longitudinal outcome insight.

> All data is **synthetic**. No real trainee, employer or government data is used, and no live integration with EPFO / Udyam / NCS / NAPS exists — these are roadmap items.

## What the prototype demonstrates

| Screen | Shows |
| --- | --- |
| Government | KPIs, status by 3/6/12/18/24-month checkpoint, attrition/non-placement reasons, course & district outcomes, attrition-risk watchlist |
| Training provider | Same lens per provider, course breakdown, provider comparison (outcome index) |
| Trainee | Journey timeline, low-burden follow-up form, automatic reason classification from free text |
| Employer | One-tap employment confirmation + optional skill feedback (raises outcome confidence) |
| Identity linkage | Different programme IDs/name spellings resolved into one unified profile |

Outcome types: employed, self-employed, apprentice, unemployed, no response. Confidence tiers: self-reported → employer-confirmed → registry-matched (simulated).

## Run locally (with API)

```bash
cd backend
pip install -r requirements.txt
python seed.py                 # writes frontend/data.json (needed for static mode)
uvicorn main:app --reload
# open http://localhost:8000   (API docs: /docs)
```

## Run as static demo (no backend)

Open `frontend/index.html` through any static server (`python -m http.server` inside `frontend/`), or deploy to GitHub Pages: **Settings → Pages → Deploy from branch → `main` → folder `/frontend`**. Commit `frontend/data.json` so Pages can load it. The header badge shows *Live API* or *Static demo mode*.

## Structure

```
backend/   main.py (FastAPI) · seed.py (synthetic data) · requirements.txt
frontend/  index.html (dashboard, Chart.js) · data.json (generated)
```

## Prototype vs. production

| Prototype | Production plan |
| --- | --- |
| In-memory store | PostgreSQL, audit logs, RBAC, encryption |
| Keyword reason classifier | Trained NLP classifier (scikit-learn) |
| Rule-based attrition risk | ML model with explainable drivers |
| Deterministic ID matching | Fuzzy matching + consent ledger + human review |
| Simulated verification tiers | EPFO/UAN, Udyam/GST, NCS, NAPS integrations |
| Web forms | Multi-channel follow-up (SMS/WhatsApp/IVR) |

Production deployment would be designed in accordance with applicable Indian data-protection, security and government data-governance requirements (incl. DPDP Act 2023).