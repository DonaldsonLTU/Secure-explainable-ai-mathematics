# =====================================================
# I’m importing my Flask app and database
# =====================================================
from app import app, db

# I’m importing the User model so I can recreate users
from app import User

# I’m importing password hashing for security
from werkzeug.security import generate_password_hash


# =====================================================
# I’m running everything inside the app context
# so Flask knows which database to use
# =====================================================
with app.app_context():

    # I’m creating all tables again (including User table)
    db.create_all()

    # =====================================================
    # I’m recreating the teacher account
    # (SAFE — this is only restoring what was lost)
    # =====================================================
    teacher = User(
        username="teacher",
        password_hash=generate_password_hash("Teacher321!"),
        role="teacher"
    )

    # =====================================================
    # I’m recreating a student account
    # =====================================================
    student = User(
        username="student1",
        password_hash=generate_password_hash("Student123!"),
        role="student"
    )

    # I’m adding both users to the database
    db.session.add(teacher)
    db.session.add(student)

    # I’m committing changes so they are saved permanently
    db.session.commit()

    # Confirmation message in terminal
    print("Database fixed and users recreated successfully ✅")