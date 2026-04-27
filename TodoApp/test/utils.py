import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from ..routers.auth import bcrypt_context
from ..database import Base
from ..models import Todos, Users

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# na początek trzeba stworzyć sobie bazę danych do testowania
SQLALCHEMY_TEST_DATABASE_URL = os.getenv("SQLALCHEMY_TEST_DATABASE_URL")

# silnik bazy danych
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create db session
@pytest.fixture
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:  # delete inserted todo during the test
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="prezio",
        email="prezio@email.com",
        first_name="Krzysztof",
        last_name="Jarzyna",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
