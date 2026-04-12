# =====================================================
# END-TO-END TESTING (FULL USER FLOW)
# I am testing login -> dashboard -> logout
# =====================================================

import pytest
from app import app

# =====================================================
# TEST CLIENT SETUP
# I disable CSRF ONLY for testing (safe)
# =====================================================
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    from app import db, User
    from werkzeug.security import generate_password_hash

    with app.test_client() as client:
        with app.app_context():
            # I create tables
            db.create_all()

            # I create test users (SAFE — temporary only)
            teacher = User(
                username="teacher",
                password_hash=generate_password_hash("Teacher321!"),
                role="teacher"
            )

            student = User(
                username="student1",
                password_hash=generate_password_hash("Student123!"),
                role="student"
            )

            db.session.add(teacher)
            db.session.add(student)
            db.session.commit()

        yield client

        # cleanup
        with app.app_context():
            db.drop_all()


# =====================================================
# TEST 1: FULL TEACHER FLOW
# login -> dashboard -> logout
# =====================================================
def test_teacher_full_flow(client):

    # I simulate login
    response = client.post("/", data={
        "username": "teacher",
        "password": "Teacher321!"
    }, follow_redirects=True)

    # I check dashboard loaded
    assert b"Dashboard" in response.data

    # I check teacher table is visible
    assert b"Teacher Question Management" in response.data

    # I simulate logout
    response = client.get("/logout", follow_redirects=True)

    # I confirm back to login page
    assert b"Login" in response.data


# =====================================================
# TEST 2: FULL STUDENT FLOW
# login -> dashboard (restricted view)
# =====================================================
def test_student_full_flow(client):

    # I simulate student login
    response = client.post("/", data={
        "username": "student1",
        "password": "Student123!"
    }, follow_redirects=True)

    # Dashboard should load
    assert b"Dashboard" in response.data

    # Student should NOT see teacher table
    assert b"Teacher Question Management" not in response.data


# =====================================================
# TEST 3: TOPIC INTERACTION FLOW
# dashboard -> select topic (basic check)
# =====================================================
def test_topic_page_load(client):

    # login first
    client.post("/", data={
        "username": "teacher",
        "password": "Teacher321!"
    }, follow_redirects=True)

    # access dashboard
    response = client.get("/dashboard")

    # check topics UI exists
    assert b"Topics" in response.data
    assert b"Quadratic Equations" in response.data