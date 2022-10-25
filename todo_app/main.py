from typing import List
from fastapi import Depends, FastAPI
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


@app.get("/", status_code=200)
async def root():
    return {"message": "Hello World"}


@app.get("/items/", response_model=List[schema.ItemRead], status_code=200)
async def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
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
