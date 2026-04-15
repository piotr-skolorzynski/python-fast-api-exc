from fastapi import FastAPI
import models
from database import engine

# główny plik gdzie będzie się działa zarządzanie całym fastApi projektu

app = FastAPI()

models.Base.metadata.create_all(
    bind=engine
)  # utworzy bazke przy odpaleniu uvicorn na tym pliku uvicorn main:app --reload
