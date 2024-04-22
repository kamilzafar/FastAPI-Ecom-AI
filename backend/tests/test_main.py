from fastapi.testclient import TestClient
from ecom.main import app
from ecom.utils.db import db_session
from ecom.utils import settings
from sqlmodel import create_engine, Session, SQLModel

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_user():

    connection_string = str(settings.TEST_DATABASE_URL)

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                yield session  

        app.dependency_overrides[db_session] = get_session_override 

        client = TestClient(app=app)

        response = client.post(
            "/api/signup",
            json={
                "username": "testuser1",
                "email": "testuser1@gmail.com",
                "password": "password"
            }
        )
        assert response.status_code == 200
        assert response.json()["username"] == "testuser1"

def test_login_for_access_token():

    connection_string = str(settings.TEST_DATABASE_URL)

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            yield session

        client = TestClient(app=app)

        app.dependency_overrides[db_session] = get_session_override

        response = client.post(
            "/api/login",
            data={
                "username": "testuser1",
                "password": "password"
            }
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert "expires_in" in response.json()
        assert "token_type" in response.json()


def test_get_product():

    connection_string = str(settings.TEST_DATABASE_URL)

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
            yield session  

        app.dependency_overrides[db_session] = get_session_override 

        client = TestClient(app=app)

        response = client.get("/api/products")
        assert response.status_code == 200
        assert response.json()[0]["name"] == "SLOGAN PRINT T-SHIRT"

def test_get_product_by_slug():

    connection_string = str(settings.TEST_DATABASE_URL)

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            yield session

        app.dependency_overrides[db_session] = get_session_override

        client = TestClient(app=app)

        # Assuming a product with slug "test-product" exists in the database
        response = client.get("/api/products/slogan-print-t-shirt")

        assert response.status_code == 200
        assert "name" in response.json()
        assert "description" in response.json()
        assert "price" in response.json()
        assert "slug" in response.json()
        assert "image1" in response.json()
        assert "image2" in response.json()
        assert response.json()["slug"] == "slogan-print-t-shirt"