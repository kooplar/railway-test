# FastAPI on Railway (Simple)

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/ping

## Database migrations
Run locally (uses SQLite by default):
```bash
alembic upgrade head
```

If you have `DATABASE_URL` set (e.g., Railway Postgres), Alembic will use it.

## Deploy on Railway
Start command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
