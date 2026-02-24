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

# ------------------------------
# I am loading trained ML components
# ------------------------------

import joblib

# I am loading the trained classification model
model = joblib.load("trained_method_model.pkl")

# I am loading the TF-IDF vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# I’m creating the Flask application instance
app = Flask(__name__)

# I’m enabling global CSRF protection for all forms in the application
csrf = CSRFProtect(app)

# ------------------------------
# AI method prediction function
# ------------------------------

def predict_method(question_text):
    """
    This function takes a maths question as input,
    transforms it using the saved TF-IDF vectorizer,
    and returns the predicted solving method.
    """
    
    # I convert the question into numerical features
    transformed_input = vectorizer.transform([question_text])
    
    # I ask the trained model to predict the method
    prediction = model.predict(transformed_input)
    
    return prediction[0]

# -----------------------------------------
# Rule-based quadratic method decision logic
# -----------------------------------------

def rule_based_quadratic_method(a, b, c):
    """
    This function uses actual mathematical logic
    (discriminant analysis) to determine the best solving method.
    It also builds a student-friendly explanation dynamically.
    """

    # # I'm converting inputs to integers so maths works correctly
    a = int(a)
    b = int(b)
    c = int(c)

    # # I'm calculating the discriminant
    D = (b ** 2) - (4 * a * c)

    import math

    # # I'm checking if the discriminant is a perfect square
    is_perfect_square = D >= 0 and math.isqrt(D) ** 2 == D

    # ----------------------------------
    # If factorisation is suitable
    # ----------------------------------
    if is_perfect_square:

        explanation = (
            f"In this question, we can find two numbers that multiply to give {c} (the constant term) "
            f"and add together to give {b} (linear term).\n\n"
            "Because such numbers exist, the quadratic can be factorised directly "
            "into two brackets and solved efficiently.\n\n"
            "Although other methods such as completing the square or the quadratic formula "
            "would also work, factorisation is the quickest method in this case."
        )

        return "Factorisation", explanation

    # ----------------------------------
    # Otherwise use general methods
    # ----------------------------------
    else:

        explanation = (
            f"For factorisation to work efficiently, we must find two numbers that multiply "
            f"to give {c} and add together to give {b}.\n\n"
            "In this case, no such pair of numbers exists.\n\n"
            "Therefore, factorisation is not suitable here. "
            "We use completing the square or the quadratic formula instead, "
            "because these methods work for all quadratic equations."
        )

        return "Completing the Square or Quadratic Formula", explanation

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

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    # I'm getting the logged-in user's role from the session
    user_role = session.get("role")

    # I'm loading all questions from the database
    questions = Question.query.all()

    # I'm grouping questions by topic so they can appear inside topic boxes
    topics = {}

  # -------------------------------
# -------------------------------
    # AI prediction placeholders
    # -------------------------------
    predicted_method = None
    selected_topic = None
    quadratic_explanation = None  # I'm storing explanation text for quadratics

    # -------------------------------
    # Handle form submission (AI)
    # -------------------------------
    if request.method == "POST":

        selected_topic = request.form.get("topic")

        if selected_topic == "quadratic":
            a = request.form.get("a")
            b = request.form.get("b")
            c = request.form.get("c")

            # I'm building the equation string exactly like training data style
            question_text = f"Solve {a}x^2 + {b}x + {c} = 0"

            # I'm still generating ML suggestion (assistive layer)
            ml_method = predict_method(question_text)

            # I'm applying rule-based authority logic
            rule_method, explanation_text = rule_based_quadratic_method(a, b, c)

            # Hybrid decision layer (rule overrides ML if mismatch)
            if ml_method == rule_method:
                predicted_method = ml_method
            else:
                predicted_method = rule_method

            # I'm storing explanation so we can show students WHY
            quadratic_explanation = explanation_text

    # ---------------------------------
    # I'm grouping questions by topic
    # (this must stay OUTSIDE POST)
    # ---------------------------------
    for q in questions:
        if q.topic not in topics:
            topics[q.topic] = []
        topics[q.topic].append(q)

    # I'm sending grouped topics + role + AI result to the template
    return render_template(
        "dashboard.html",
        role=user_role,
        topics=topics,
        questions=questions,
        predicted_method=predicted_method,
        selected_topic=selected_topic,
        quadratic_explanation=quadratic_explanation
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
