# Copilot Instructions for Tax Prep Platform

## Project Overview
- This is a full-stack tax preparation platform with:
  - **Backend:** FastAPI (Python) in `tax-software/backend/app/`
  - **Frontend:** React (Vite + TypeScript) in `tax-software/frontend/src/`
  - **Database:** Cloudflare D1 (migrations/scripts in `tax-software/backend/app/`)
  - **Infrastructure:** Cloudflare Workers/Pages, Vercel, and legacy AWS Lambda pattern (see `tax-software/`)

## Key Structure
- `tax-software/backend/app/`: FastAPI routers, business logic, migrations, and seed data
- `tax-software/backend/tests/`: Pytest-based backend tests
- `tax-software/frontend/src/`: React dashboard, widgets, and shared UI components
- `tax-software/frontend/`: Vite config, npm scripts, and static assets
- `tax-software/`: Example AWS Lambda pattern (not primary stack)

## Developer Workflows
- **Backend (FastAPI):**
  - Activate venv: `.venv\Scripts\activate` (Windows)
  - Run dev server: `uvicorn app.main:app --reload` (from `tax-software/backend`)
  - Run tests: `pytest` (from `tax-software/backend`)
  - Apply DB migrations: `wrangler d1 migrations apply d1 --local`
- **Frontend (React):**
  - Install deps: `npm install` (from `tax-software/frontend`)
  - Start dev server: `npm run dev`
  - Run tests: `npm test`

## Patterns & Conventions
- **Backend:**
  - Routers are split by domain (e.g., `admin_router.py`, `irs_router.py`, etc.)
  - Shared logic in `lib/` subfolder
  - Use `schema.sql` for DB schema, `seed_data.py` for initial data
- **Frontend:**
  - Dashboard widgets and layouts are grouped by user role (`admin/`, `client/`, `staff/`, `shared/`)
  - Use TypeScript and functional React components
  - Styling via `ios-theme.css` and component-level CSS
- **Testing:**
  - Backend: Pytest, tests in `tax-software/backend/tests/`
  - Frontend: Jest, tests colocated with components

## Integration & Deployment
- **Cloudflare:**
  - Use Wrangler for D1 DB and secrets (`wrangler secret put ...`)
  - See `wrangler.toml` for config
- **Vercel:**
  - See `vercel.json` for frontend deployment
- **AWS Lambda pattern:**
  - Example only, not used in main workflow

## Tips for AI Agents
- Always check `README.md` in root, backend, and frontend for up-to-date commands and structure
- Prefer FastAPI + React stack for new features; AWS Lambda code is legacy/example
- Reference `tax-software/backend/app/` for API patterns and DB access
- Reference `tax-software/frontend/src/dashboard/` for UI/role-based patterns
- Use project-specific scripts and configs (not generic ones)
