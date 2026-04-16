from fastapi import APIRouter

# żeby endpointy z tego pliku były w instancji fastApi z main.py musimy odziedziczyć routing
router = APIRouter()

# teraz w endpointach dekoratory piszemy @router i on przekaże endpoint do instancji fastApi z main.py


@router.get("/auth/")
async def get_user():
    return {"user": "authenticated"}
