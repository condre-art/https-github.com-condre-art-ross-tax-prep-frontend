# Tax Software Backend

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Development

Run the FastAPI app locally:

```bash
uvicorn app.main:app --reload
```

## Database migrations (Cloudflare D1)

Apply database migrations locally:

```bash
wrangler d1 migrations apply d1 --local
```

Apply database migrations to the remote D1 database:

```bash
wrangler d1 migrations apply d1
```

## Testing

```bash
pytest
```
