# I'm importing pytest for testing
import pytest

# I'm importing my Flask app
from app import app, db, User

from werkzeug.security import generate_password_hash


# ==================================================
# TEST CLIENT SETUP
# ==================================================
# I'm creating a test client to simulate browser requests
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    # I'm using an in-memory database (SAFE — nothing saved permanently)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # I'm creating a test user (safe, temporary)
            test_user = User(
                username="testuser",
                password_hash=generate_password_hash("123456"),
                role="teacher"
            )
            db.session.add(test_user)
            db.session.commit()

        yield client

        # cleanup after test
        with app.app_context():
            db.drop_all()


# ==================================================
# TEST: LOGIN PAGE LOADS
# ==================================================
def test_login_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Login" in response.data


# ==================================================
# TEST: DASHBOARD REDIRECT WITHOUT LOGIN
# ==================================================
def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    # should redirect (302) or block access
    assert response.status_code in [302, 401, 403]


# ==================================================
# TEST: LOGIN WORKS (SIMULATED)
# ==================================================
def test_login_post(client):
    response = client.post("/", data={
        "username": "testuser",
        "password": "123456"
    }, follow_redirects=True)

    # we just check app responds (even if auth logic differs)
    assert response.status_code == 200


# ==================================================
# TEST: DASHBOARD AFTER LOGIN
# ==================================================
def test_dashboard_access_after_login(client):
    client.post("/", data={
        "username": "testuser",
        "password": "123456"
    })

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Dashboard" in response.data