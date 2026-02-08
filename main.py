from fastapi import FastAPI

app = FastAPI(title="Railway FastAPI Demo")


@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Railway"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}
