# Copilot Instructions for Tax Prep Platform

## Project Architecture
- **Backend:** FastAPI (Python) in `tax-software/backend/app/`
  - Routers are domain-based (e.g., `admin_router.py`, `irs_router.py`, `workflow_router.py`)
  - Shared logic in `lib/` (e.g., `cade2.py`, `ews.py`)
  - DB schema in `schema.sql`, seed data in `seed_data.py`
  - Tests in `tax-software/backend/tests/` (Pytest)
- **Frontend:** React (Vite + TypeScript) in `tax-software/frontend/src/`
  - Dashboard widgets/layouts grouped by user role: `dashboard/admin/`, `dashboard/client/`, `dashboard/staff/`, `dashboard/shared/`
  - Shared UI: `dashboard/shared/` (e.g., `Card.tsx`, `Sidebar.tsx`, `Table.tsx`)
  - Styling: `ios-theme.css` and per-component CSS
  - Tests colocated with components (Jest)
- **Database:** Cloudflare D1 (migrations/scripts in backend `app/`)
- **Infrastructure:**
  - Cloudflare Workers/Pages (see `wrangler.toml`)
  - Vercel for frontend (`vercel.json`)
  - AWS Lambda pattern in `tax-software/` is legacy/example only

## Developer Workflows
### Backend (FastAPI)
- Activate venv: `.venv\Scripts\activate` (Windows)
- Start dev server: `uvicorn app.main:app --reload` (from `tax-software/backend`)
- Run tests: `pytest` (from `tax-software/backend`)
- Apply DB migrations: `wrangler d1 migrations apply d1 --local`

### Frontend (React)
- Install deps: `npm install` (from `tax-software/frontend`)
- Start dev server: `npm run dev`
- Run tests: `npm test`

## Project-Specific Patterns
- **Backend routers**: Each domain (admin, irs, workflow, etc.) has its own router file. Register routers in `main.py`.
- **Frontend dashboard**: Role-based folders under `dashboard/` for widgets and layouts. Shared components in `dashboard/shared/`.
- **Testing**: Backend uses Pytest in `tests/`; frontend uses Jest with tests next to components.
- **DB migrations**: Managed via Wrangler CLI; see `wrangler.toml` for config.
- **Legacy AWS Lambda**: Files in `tax-software/` (e.g., `template.yaml`) are for reference only, not used in main workflow.

## Integration & Deployment
- **Cloudflare**: Use Wrangler for D1 DB, secrets, and deployment. See `wrangler.toml`.
- **Vercel**: Frontend deploy config in `vercel.json`.

## Tips for AI Agents
- Always check `README.md` in root, backend, and frontend for up-to-date commands and structure.
- Prefer FastAPI + React stack for new features; ignore AWS Lambda code unless explicitly requested.
- Reference `tax-software/backend/app/` for API and DB patterns.
- Reference `tax-software/frontend/src/dashboard/` for UI/role-based patterns.
- Use project-specific scripts/configs (not generic ones).

## Examples
- To add a new API route: create a new router in `backend/app/`, register in `main.py`.
- To add a new dashboard widget: add to the appropriate role folder in `frontend/src/dashboard/`.
- To seed DB: run `seed_data.py` in backend/app/.
