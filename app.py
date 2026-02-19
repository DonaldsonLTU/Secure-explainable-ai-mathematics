# I’m importing Flask tools for routing, sessions, and redirects
from flask import Flask, request, redirect, url_for, session, render_template, abort, render_template_string

# I’m importing SQLAlchemy to manage the relational database
from flask_sqlalchemy import SQLAlchemy

# I’m importing Werkzeug tools for secure password hashing and checking
from werkzeug.security import generate_password_hash, check_password_hash

# I’m importing FlaskForm so I can create secure and structured web forms
# I’m importing form field types to handle username input, password input, and form submission
# I’m importing validators to ensure required fields are not left empty
# I’m importing CSRF protection to defend against cross-site request forgery attacks

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

import os

# I’m creating the Flask application instance
app = Flask(__name__)

# I’m enabling global CSRF protection for all forms in the application
csrf = CSRFProtect(app)

# I’m setting a secret key for secure session management
# In production this would come from environment variables
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# -------------------------------------------------
# SQLITE DATABASE CONFIGURATION (RELATIONAL DB)
# -------------------------------------------------
# I’m configuring a local SQLite database file for structured question storage
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maths.db"

# I’m disabling modification tracking to improve performance
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# I’m creating the database object that connects Flask to SQLite
db = SQLAlchemy(app)

# -------------------------------------------------
# QUESTION MODEL (DATABASE TABLE STRUCTURE)
# -------------------------------------------------
# I’m defining the Question table structure for storing maths questions
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(200), nullable=False)
    method_reason = db.Column(db.Text, nullable=False)

    # Simple test route to confirm database connection works
@app.route("/test-db")
def test_db():
    questions = Question.query.all()
    return f"Database connected. {len(questions)} questions found."

# -------------------------------------------------
# LOGIN FORM (FLASK-WTF + CSRF PROTECTION)
# -------------------------------------------------
# I’m defining a secure login form using Flask-WTF
# This replaces manual form handling and enables CSRF protection automatically
class LoginForm(FlaskForm):
    # I’m defining a username input field that must not be empty
    username = StringField("Username", validators=[DataRequired()])

    # I’m defining a password input field that must not be empty
    password = PasswordField("Password", validators=[DataRequired()])

    # I’m defining the submit button for the login form
    submit = SubmitField("Login")

# -------------------------------------------------
# TEMPORARY IN-MEMORY USERS (SECURE BUT SIMPLE)
# -------------------------------------------------
# I’m defining fixed users to avoid database complexity for now
# Passwords are hashed immediately (good security practice)
users = {
    "teacher": {
        "role": "teacher",
        "password": generate_password_hash("Teacher321!")
    },
    "student1": {
        "role": "student",
        "password": generate_password_hash("Student123!")
    },
    "student2": {
        "role": "student",
        "password": generate_password_hash("Student123!")
    },
    "student3": {
        "role": "student",
        "password": generate_password_hash("Student123!")
    }
}

# -------------------------------------------------
# ROUTE PROTECTION DECORATORS (SECURITY + RBAC)
# -------------------------------------------------
# I’m importing wraps so my decorators don’t break Flask routing
from functools import wraps

# I’m creating a decorator to ensure the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# I’m creating a decorator to restrict access to teachers only
def teacher_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "teacher":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------
# TEACHER-ONLY ROUTE (RBAC ENFORCEMENT)
# -------------------------------------------------
# I’m creating a route that only teachers are allowed to access
@app.route("/teacher")
@login_required
@teacher_only
def teacher_dashboard():
    return "<h1>Teacher Area</h1><p>Only teachers can access this page.</p>"

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    # I’m creating an instance of the secure Flask-WTF login form
    form = LoginForm()

    # I’m handling the login form submission securely
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # I’m validating credentials securely
        if username in users and check_password_hash(users[username]["password"], password):
            session["user"] = username
            session["role"] = users[username]["role"]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password", 401

    # I’m rendering the login page and passing the form to the template
    return render_template("login.html", form=form)

# -------------------------------------------------
# DASHBOARD ROUTE (ROLE-BASED QUESTION DISPLAY)
# -------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    # I'm getting the logged-in user's role from the session
    user_role = session.get("role")

    # I'm loading all questions from the database
    questions = Question.query.all()

    # I'm grouping questions by topic so they can appear inside topic boxes
    topics = {}

    for q in questions:
        if q.topic not in topics:
            topics[q.topic] = []
        topics[q.topic].append(q)

    # I'm sending grouped topics + role to the template
    return render_template(
        "dashboard.html",
        role=user_role,
        topics=topics,
        questions=questions  # full dataset (teacher only)
    )
# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
@app.route("/logout")
def logout():
    # I’m clearing the session securely
    session.clear()
    return redirect(url_for("login"))

# -------------------------------------------------
# CUSTOM ERROR HANDLERS (SECURITY + UX)
# -------------------------------------------------
# I’m handling 403 errors to avoid leaking sensitive information
@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

# I’m handling 404 errors to provide a safe, user-friendly message
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

# -------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------
# I’m running the Flask development server
if __name__ == "__main__":
    app.run(debug=True)