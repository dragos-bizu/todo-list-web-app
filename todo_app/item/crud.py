from this import d
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import model, schema


def get_item(db: Session, item_id: int):
    return db.query(model.Item).filter(model.Item.id == item_id).first()


def get_pending_items(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(model.Item)
        .filter(model.Item.is_done == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_done_items(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(model.Item)
        .filter(model.Item.is_done == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_item(db: Session, item: schema.ItemCreate):
    db_item = model.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def edit_item(db: Session, item: schema.ItemEdit, item_id: int):
    db_item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.dict(exclude_unset=True)
    for field in item_data:
        setattr(db_item, field, item_data[field])
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item
