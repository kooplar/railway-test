from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Railway FastAPI Demo")

class Item(BaseModel):
    name: str


items: list[dict] = []
next_id = 1


@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Railway"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/echo")
def echo(q: str = ""):
    return {"echo": q}


@app.get("/items")
def list_items():
    return {"items": items}


@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    new_item = {"id": next_id, "name": item.name}
    next_id += 1
    items.append(new_item)
    return new_item


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    for existing in items:
        if existing["id"] == item_id:
            existing["name"] = item.name
            return existing
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for idx, existing in enumerate(items):
        if existing["id"] == item_id:
            return items.pop(idx)
    raise HTTPException(status_code=404, detail="Item not found")
