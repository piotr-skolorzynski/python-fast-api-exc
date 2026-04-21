from routers import todos, auth, admin, users
from fastapi import FastAPI
import models
from database import engine

# główny plik gdzie będzie się działa zarządzanie całym fastApi projektu

app = FastAPI()

# routing umożliwiający połącznie wszystkich endpointów z różnych plików tak żeby mogła zarządzać nimi jedna instanacj fastApi


models.Base.metadata.create_all(
    bind=engine
)  # utworzy bazke przy odpaleniu uvicorn na tym pliku uvicorn main:app --reload, jeśli bazka jeszcze nie istnieje

# nakazujemy włączenie w naszej aplikacji endpointów z poszczególnych plików
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
