from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Todos
import models
from database import SessionLocal, engine
from starlette import status

# główny plik gdzie będzie się działa zarządzanie całym fastApi projektu

app = FastAPI()

models.Base.metadata.create_all(
    bind=engine
)  # utworzy bazke przy odpaleniu uvicorn na tym pliku uvicorn main:app --reload, jeśli bazka jeszcze nie istnieje


# odpowiada za połączenie z bazą danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Depends to jest dependecy injection z biblioteki FastApi, czyli wstrzykujemy tutaj naszą fukcję get_fb żeby nawiązać połączenie do bazki
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found.")
