from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import models
import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_menu():
    return models.Menu(title="Test Menu", description="Test Description")


@pytest.fixture
def test_submenu(test_menu):
    return models.Submenu(title="Test Submenu", description="Test Description", menu_id=test_menu.id)


@pytest.fixture
def test_dish(test_submenu):
    return models.Dish(title="Test Dish", description="Test Description", price=10.00, submenu_id=test_submenu.id)


@pytest.fixture
def setup_dish(db_session, test_menu, test_submenu, test_dish):
    # Add and commit test_menu, test_submenu, and test_dish in sequence
    db_session.add(test_menu)
    db_session.commit()

    test_submenu.menu_id = test_menu.id
    db_session.add(test_submenu)
    db_session.commit()

    test_dish.submenu_id = test_submenu.id
    db_session.add(test_dish)
    db_session.commit()

    return test_menu, test_submenu, test_dish
