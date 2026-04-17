from datetime import datetime, timedelta, timezone
from database import SessionLocal
from fastapi import APIRouter, Depends
from starlette import status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from fastapi.security import (
    OAuth2PasswordRequestForm,
)  # zapewnia w swagerze możliwość użycia bardziej bezpiecznego formularza wymagającego podania hasła
from jose import jwt

# żeby endpointy z tego pliku były w instancji fastApi z main.py musimy odziedziczyć routing
router = APIRouter()

# konfigurowanie JWT
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# hashowanie
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# model określający odpowiedź z tokenem oraz dodatkowymi informacjami
class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# funkcja odpowiedzialna za uwierzytlenienie użytkownika
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(
        password, user.hashed_password
    ):  # sprawdamy czy hasło zgadza się z hashowanym hasłem
        return False
    return user


# generate access tokens
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# teraz w endpointach dekoratory piszemy @router i on przekaże endpoint do instancji fastApi z main.py
@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
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
    # zapisz w bazce
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):  # teraz swagger będzie podawał formularz
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return "Failed Authentication"

    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}
