import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

app = FastAPI(title="Railway FastAPI Demo")


class Base(DeclarativeBase):
    pass


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))


class Item(BaseModel):
    name: str


class ItemOut(BaseModel):
    id: int
    name: str


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


def _database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        return "sqlite:///./dev.db"
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


engine = create_engine(_database_url())


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/items")
def list_items():
    with Session(engine) as session:
        results = session.execute(select(ItemModel)).scalars().all()
        return {"items": [ItemOut(id=r.id, name=r.name) for r in results]}


@app.post("/items", status_code=201)
def create_item(item: Item):
    with Session(engine) as session:
        row = ItemModel(name=item.name)
        session.add(row)
        session.commit()
        session.refresh(row)
        return ItemOut(id=row.id, name=row.name)


@app.get("/items/{item_id}")
def get_item(item_id: int):
    with Session(engine) as session:
        row = session.get(ItemModel, item_id)
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemOut(id=row.id, name=row.name)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    with Session(engine) as session:
        row = session.get(ItemModel, item_id)
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        row.name = item.name
        session.commit()
        return ItemOut(id=row.id, name=row.name)


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        row = session.get(ItemModel, item_id)
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(row)
        session.commit()
        return ItemOut(id=row.id, name=row.name)
