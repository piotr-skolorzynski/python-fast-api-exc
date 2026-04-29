from datetime import datetime, timedelta, timezone
from ..database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from pydantic import BaseModel
from ..models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
)  # OAuth2PasswordRequestForm zapewnia w swagerze możliwość użycia bardziej bezpiecznego formularza wymagającego podania hasła,

# OAuth2PasswordBearer - służy do bezpiecznego przesłania tokena w swagerze, ten formularz będzie ukryty pod ikoną kłódki
from jose import jwt, JWTError

# dodanie strony dla auth
from fastapi.templating import Jinja2Templates

# żeby endpointy z tego pliku były w instancji fastApi z main.py musimy odziedziczyć routing
router = APIRouter(
    prefix="/auth", tags=["auth"]
)  # prefix - wsztystkie endpointy w tym pliku zaczną się od 'auth' # tags podzieli swagger na tag 'auth' dla lepszej czytelności, pozostałe jeśli nie mają tagów będa pod tagiem default

# konfigurowanie JWT
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# hashowanie
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# dekodowanie JWT
oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="auth/token"
)  # ścieżka do entpointu, uwzględnia również prefix


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


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


### templates###
# zapięcie template
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))


@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})


### endpoints###
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
def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# jeśli korzystamy z JWT to za każdym razem chcemy sprawdzić usera i zweryfikować token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None or user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


# teraz w endpointach dekoratory piszemy @router i on przekaże endpoint do instancji fastApi z main.py
@router.post("/", status_code=status.HTTP_201_CREATED)
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
        phone_number=create_user_request.phone_number,
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}
