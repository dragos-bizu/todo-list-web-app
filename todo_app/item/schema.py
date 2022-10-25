from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: bool = False
    created_at: datetime = datetime.now()
    modified_at: datetime = datetime.now()

    class Config:
        orm_mode = True


class ItemCreate(Item):
    pass


class ItemRead(Item):
    id: int


class ItemEdit(Item):
    name: Optional[str] = None
    description: Optional[str] = None
