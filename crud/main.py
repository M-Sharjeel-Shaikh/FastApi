from typing import Union
from fastapi import FastAPI, Depends
import database, models
import schemas
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

#This will create our database if it doesent already exists
Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()


@app.get("/")
def getItems(session: Session = Depends(get_session)):
    return session.query(models.Todos).all()


@app.post("/")
def addItem(item:schemas.Item, session = Depends(get_session)):
    item = models.Todos(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    return session.query(models.Todos).get(id)


@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session = Depends(get_session)):
    itemObject = session.query(models.Todos).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


@app.delete("/{id}")
def deletetodos(id:int, session = Depends(get_session)):
    todosObject = session.query(models.Todos).get(id)
    session.delete(todosObject)
    session.commit()
    session.close()
    return 'todos was deleted'