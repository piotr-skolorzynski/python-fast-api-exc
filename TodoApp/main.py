from fastapi import FastAPI, Request
import os
from .routers import todos, auth, admin, users
from .models import Base
from .database import engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# główny plik gdzie będzie się działa zarządzanie całym fastApi projektu

app = FastAPI()

# routing umożliwiający połącznie wszystkich endpointów z różnych plików tak żeby mogła zarządzać nimi jedna instanacj fastApi


Base.metadata.create_all(bind=engine)
# utworzy bazke przy odpaleniu uvicorn na tym pliku uvicorn main:app --reload
# (jeśli przeszedłeś na relative path to uvicorn TodoApp.main:app --reload), jeśli bazka jeszcze nie istnieje

# wskazanie folderu z templatami jinja
# templates = Jinja2Templates(directory="templates") - to nie zadziałało, musiałem złapać ścieżkę do pliku poniżej
base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
# dodajemy pliki statyczne z css i js
app.mount(
    "/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static"
)


@app.get("/")
async def templates_test(request: Request):
    return templates.TemplateResponse(request, "home.html", {"request": request})


# health check test
@app.get("/healthy")
async def health_check():
    return {"status": "Healthy"}


# nakazujemy włączenie w naszej aplikacji endpointów z poszczególnych plików
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
