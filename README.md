# ParliamentLens — AI-Powered Debate Transparency Platform

## Vision
> To make political discourse transparent, factual, and accessible using AI.

## What this repo contains (Stage 0)
- Monorepo layout with three apps:
  - `apps/web` — React + Vite + Tailwind + ShadCN-ready UI
  - `apps/api` — Node.js + Express + TypeScript
  - `apps/ai` — Python FastAPI microservice
- Dockerized services with a single `docker-compose.yml`
- Environment variable templates (`.env.example` files)
- Basic health endpoints and a landing page so you can run everything immediately

## Quick start (dev, without Docker)
### Prereqs
- Node 20+ and pnpm (or npm/yarn)
- Python 3.10+
- (Optional) MongoDB + Redis running locally (Docker compose already provides these)

### 1) Install deps
```bash
# from repo root
cd apps/web && pnpm install && cd ../..
cd apps/api && pnpm install && cd ../..
cd apps/ai && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && deactivate
```

### 2) Start services in three terminals
```bash
# Terminal A (API)
cd apps/api && pnpm dev

# Terminal B (AI)
cd apps/ai && . .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Terminal C (Web)
cd apps/web && pnpm dev
```

Open http://localhost:5173

## Quick start (with Docker)
```bash
# from repo root
docker compose up --build
```
Open:
- Web: http://localhost:5173
- API: http://localhost:8000/health
- AI:  http://localhost:8001/health

## Social impact (talk track)
- Enables citizens, students, and journalists to access structured, transparent debate insights.
- Reduces misinformation via summaries, emotion maps, and fact-check stubs (later stages).
- Multilingual, accessible UI with voice/video input lowers barriers to civic participation.
