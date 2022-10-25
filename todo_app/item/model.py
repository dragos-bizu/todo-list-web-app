from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from todo_app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
