from warnings import deprecated

from fastapi import APIRouter
from starlette import status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext

# żeby endpointy z tego pliku były w instancji fastApi z main.py musimy odziedziczyć routing
router = APIRouter()

# hashowanie
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# teraz w endpointach dekoratory piszemy @router i on przekaże endpoint do instancji fastApi z main.py
@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(
            create_user_request.password
        ),  # wykorzystujem nasz has context z passlib do zaszyfrowania hasła
        is_active=True,
    )

    return create_user_model
