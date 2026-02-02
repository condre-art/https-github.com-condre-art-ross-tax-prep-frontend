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

## Testing

```bash
pytest
```
