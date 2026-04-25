from fastapi import FastAPI
from .routers import todos, auth, admin, users
from .models import Base
from .database import engine

# główny plik gdzie będzie się działa zarządzanie całym fastApi projektu

app = FastAPI()

# routing umożliwiający połącznie wszystkich endpointów z różnych plików tak żeby mogła zarządzać nimi jedna instanacj fastApi


Base.metadata.create_all(bind=engine)
# utworzy bazke przy odpaleniu uvicorn na tym pliku uvicorn main:app --reload
# (jeśli przeszedłeś na relative path to uvicorn TodoApp.main:app --reload), jeśli bazka jeszcze nie istnieje


# health check test
@app.get("/healthy")
async def health_check():
    return {"status": "Healthy"}


# nakazujemy włączenie w naszej aplikacji endpointów z poszczególnych plików
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
