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

## Deploy on Railway
Start command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
