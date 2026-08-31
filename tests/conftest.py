import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.models import Base, User as UserModel, Student as StudentModel

from app.main import app
from app.database import get_db



TEST_DATABASE_URL = (
    "postgresql://postgres:123123@localhost:5432/student_management_test"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_database():
    yield

    db = TestingSessionLocal()

    db.query(UserModel).delete()
    db.query(StudentModel).delete()

    db.commit()
    db.close()


