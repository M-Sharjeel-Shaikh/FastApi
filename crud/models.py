from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(String(256))