from typing import List
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .item import crud, model, schema

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["http://localhost", "http://localhost:3000", "http://127.0.0.1"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=200)
async def root():
    return {"message": "Hello World"}


@app.get("/items/", response_model=List[schema.ItemRead], status_code=200)
async def get_pending_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_pending_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/done", response_model=List[schema.ItemRead], status_code=200)
async def get_done_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_done_items(db, skip=skip, limit=limit)
    return items


@app.get("/item/{item_id}", response_model=schema.ItemRead, status_code=200)
async def get_one_item(db: Session = Depends(get_db), item_id: int = 1):
    item = crud.get_item(db, item_id)
    return item


@app.post("/items/", response_model=schema.ItemCreate, status_code=201)
async def create_new_item(item: schema.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.patch("/items/{item_id}", response_model=schema.ItemRead, status_code=200)
async def edit_item(item_id: int, item: schema.ItemEdit, db: Session = Depends(get_db)):
    return crud.edit_item(db=db, item_id=item_id, item=item)


@app.delete("/items/{item_id}", response_model=schema.ItemRead, status_code=200)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db=db, item_id=item_id)
