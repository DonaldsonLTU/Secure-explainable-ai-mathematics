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

# I'm importing Flask-Limiter to help prevent brute-force attacks and request flooding
# This supports STRIDE mitigation for:
# - Spoofing (reducing automated login attempts)
# - Denial of Service (limiting excessive requests)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ------------------------------
# MONGODB CONNECTION (LOCAL)
# ------------------------------

from pymongo import MongoClient
from datetime import datetime

# I’m connecting to my local MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# I’m creating a separate database for AI Maths analytics
mongo_db = client["ai_maths_analytics"]

# I’m creating collections
interaction_collection = mongo_db["student_interactions"]
usage_collection = mongo_db["usage_history"]

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

# I'm strengthening session security to prevent cookie theft and spoofing
# STRIDE mitigation:
# - Spoofing (reduces session hijacking risk)
# - Elevation of Privilege (protects role-based sessions)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False

# I'm configuring Flask-Limiter to reduce abuse and request flooding
# This helps mitigate:
# - STRIDE: Denial of Service (rate limiting excessive traffic)
# - STRIDE: Spoofing (limiting repeated login attempts)
# Default limit = 100 requests per minute per IP address
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"]
)

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
    
    # -----------------------------------------
# Rule-based simultaneous method decision logic
# -----------------------------------------
def rule_based_simultaneous_method(a1, b1, c1, a2, b2, c2):
    """
    This function decides whether Substitution or Elimination is best
    using GCSE-friendly logic, and it builds a student-friendly explanation.
    """

    # # I'm converting inputs to integers so my comparisons are reliable
    a1, b1, c1 = int(a1), int(b1), int(c1)
    a2, b2, c2 = int(a2), int(b2), int(c2)

    # # I'm building neat equation strings for ML + display
    eq1 = f"{a1}x + {b1}y = {c1}"
    eq2 = f"{a2}x + {b2}y = {c2}"

    # ----------------------------------------------------
    # 1) Elimination check (coefficients match or opposites)
    # ----------------------------------------------------
    # # I'm checking if x coefficients match (e.g., 2x and 2x) or are opposites (e.g., 2x and -2x)
    x_elim_ready = (a1 != 0 and a2 != 0 and (a1 == a2 or a1 == -a2))

    # # I'm checking if y coefficients match (e.g., 3y and 3y) or are opposites (e.g., 3y and -3y)
    y_elim_ready = (b1 != 0 and b2 != 0 and (b1 == b2 or b1 == -b2))

    # # I'm preparing a small detail string so the explanation can point to the exact matching pair
    match_detail = ""
    if x_elim_ready:
        match_detail = f"the x coefficients already match ({a1}x and {a2}x)"
    elif y_elim_ready:
        match_detail = f"the y coefficients already match ({b1}y and {b2}y)"

    if x_elim_ready or y_elim_ready:
        explanation = (
            f"In this pair of equations, {match_detail}, which allows us to add or subtract the equations "
            f"to remove one variable easily.\n\n"
            "This process eliminates one variable and reduces the system to a single linear equation.\n\n"
            "Although substitution would also work, elimination is more direct here because we can cancel a variable "
            "without first rearranging an equation."
        )
        return "Elimination", explanation, eq1, eq2

    # ----------------------------------------------------
    # 2) Substitution check (a coefficient is 1 or -1)
    # ----------------------------------------------------
    # # I'm checking if any coefficient is 1 or -1, because that makes rearranging very straightforward
    substitution_ready = (abs(a1) == 1 or abs(b1) == 1 or abs(a2) == 1 or abs(b2) == 1)

    # # I'm spotting which variable is easiest to make the subject, so the explanation feels specific
    easy_subject = ""
    if abs(a1) == 1:
        easy_subject = "x (in Equation 1)"
    elif abs(b1) == 1:
        easy_subject = "y (in Equation 1)"
    elif abs(a2) == 1:
        easy_subject = "x (in Equation 2)"
    elif abs(b2) == 1:
        easy_subject = "y (in Equation 2)"

    if substitution_ready:
        explanation = (
            "In this pair of equations, one variable can be rearranged easily because its coefficient is 1 or −1.\n\n"
            f"We rearrange that equation to make {easy_subject} the subject.\n\n"
            "We then substitute it into the second equation.\n\n"
            "Although elimination would also work, substitution is more direct here because the rearrangement is "
            "straightforward from the start."
        )
        return "Substitution", explanation, eq1, eq2

    # ----------------------------------------------------
    # 3) Default choice (Elimination)
    # ----------------------------------------------------
    # # If nothing is obviously 1/-1, I default to elimination because it's a standard GCSE approach
    explanation = (
        "In this pair of equations, no variable is immediately easy to rearrange because there is no coefficient of 1 or −1.\n\n"
        "So elimination is usually the better choice, because we can multiply one or both equations to make a coefficient match, "
        "then add or subtract to remove one variable.\n\n"
        "Although substitution would still work, elimination is more structured here."
    )
    return "Elimination", explanation, eq1, eq2

# -----------------------------------------
# Rule-based ratio method decision logic
# -----------------------------------------
def rule_based_ratio_method(total_amount, part1, part2):
    """
    This function provides neutral recommendation for ratio problems.
    Both unitary and fraction methods are valid for GCSE ratio sharing.
    """

    # # I'm converting inputs to integers for safe calculations
    total_amount = int(total_amount)
    part1 = int(part1)
    part2 = int(part2)

    # # I'm calculating total ratio parts
    total_parts = part1 + part2

    # # I'm building a student-friendly explanation
    explanation = (
        "In ratio sharing problems, both the unitary method and the fraction method can be used to find each share.\n\n"
        "Even when questions are presented in different structures or scenarios — such as money, sweets, or quantities — "
        "the mathematical structure remains the same.\n\n"
        "Both methods follow the same principle and will produce the same answer.\n\n"
        "The choice depends on which approach feels clearer or more comfortable.\n\n"
        "--------------------------------------------------\n\n"
        "Unitary Method\n\n"
        "The unitary method works by first finding the value of one part.\n\n"
        "Step 1: Add the ratio parts together to find the total number of parts.\n"
        "Step 2: Divide the total amount by the total parts to find the value of one part.\n"
        "Step 3: Multiply each ratio part by that value to find each share.\n\n"
        "--------------------------------------------------\n\n"
        "Fraction Method\n\n"
        "The fraction method treats each ratio part as a fraction of the total.\n\n"
        "Step 1: Add the ratio parts to find the total number of parts.\n"
        "Step 2: Write each share as (individual ratio part ÷ total parts) × total amount.\n"
        "Step 3: Multiply to find each share directly."
    )

    return "Unitary Method or Fraction Method", explanation

# -----------------------------------------
# Rule-based geometric progression method decision logic
# -----------------------------------------
def rule_based_gp_method(a_n, a, r, n):
    """
    This function decides whether Iteration or Formula method is appropriate
    based on availability of common ratio and other inputs.
    """

    # # I'm converting inputs carefully, allowing empty values
    a_n = int(a_n) if a_n else None
    a = int(a) if a else None
    r = int(r) if r else None
    n = int(n) if n else None

    # ----------------------------------------
    # CASE 1: r is missing → Formula required
    # ----------------------------------------
    if r is None:

        explanation = (
            "The common ratio is not directly available from the given information.\n\n"
            "Since iteration requires knowing the common ratio in order to multiply repeatedly, "
            "it cannot be applied here.\n\n"
            "In addition, when the term being found is far from the first term, repeatedly multiplying "
            "would be time-consuming and inefficient.\n\n"
            "Therefore, the formula method must be used to work with the variables and determine "
            "the unknown values in a more systematic and time-efficient way.\n\n"
            "---------------------------------------------\n\n"
            "Formula Method\n\n"
            "The formula method uses:\n"
            "aₙ = a × rⁿ⁻¹\n\n"
            "Where:\n"
            "aₙ = the nth term (the term being found)\n"
            "a = the first term\n"
            "r = the common ratio (the number we multiply by each time)\n"
            "n = the term position\n\n"
            "Step 1: Identify the known variables.\n"
            "Step 2: Substitute into the formula.\n"
            "Step 3: Rearrange if necessary to find the unknown.\n"
            "Step 4: Evaluate carefully."
        )

        return "Formula Method", explanation

    # ------------------------------------------------
    # CASE 2: r is known and we are finding a_n
    # ------------------------------------------------
    elif r is not None and a is not None and n is not None and a_n is None:

        explanation = (
            "The common ratio is known, so we can repeatedly multiply by the ratio "
            "to reach the required term.\n\n"
            "This makes the iteration method straightforward and easy to apply.\n\n"
            "Although the formula method could also be used, iteration is more direct in this case.\n\n"
            "---------------------------------------------\n\n"
            "Iteration Method\n\n"
            "The iteration method works by multiplying each term by the common ratio "
            "to generate the next term.\n\n"
            "Step 1: Start with the first term.\n"
            "Step 2: Multiply by the common ratio to get the next term.\n"
            "Step 3: Repeat until the required term is reached.\n\n"
            "This method only works when the common ratio is known."
        )

        return "Iteration Method", explanation

    # ----------------------------------------
    # Default → Formula method
    # ----------------------------------------
    else:

        explanation = (
            "The formula method is the most reliable approach in this situation.\n\n"
            "It allows us to work directly with the known variables and determine the unknown values "
            "in a structured way.\n\n"
            "The formula used is:\n"
            "aₙ = a × rⁿ⁻¹"
        )

        return "Formula Method", explanation
    
# -----------------------------------------
# Rule-based arithmetic progression method decision logic
# -----------------------------------------
def rule_based_ap_method(a_n, a, d, n):
    """
    This function decides whether Iteration or Formula method is appropriate
    based on availability of common difference and other inputs.
    """

    # # I'm converting inputs carefully, allowing empty values
    a_n = int(a_n) if a_n else None
    a = int(a) if a else None
    d = int(d) if d else None
    n = int(n) if n else None

    # ----------------------------------------
    # CASE 1: d is missing → Formula required
    # ----------------------------------------
    if d is None:

        explanation = (
            "Arithmetic Progressions (AP) and Geometric Progressions (GP) are both types of sequences.\n\n"
            "They are similar because both follow a consistent pattern from one term to the next.\n\n"
            "However, the key difference is:\n"
            "• In an Arithmetic Progression, we add a fixed number each time. This fixed number is called the common difference (d).\n"
            "• In a Geometric Progression, we multiply by a fixed number each time. This fixed number is called the common ratio (r).\n\n"
            "Since the common difference is not directly available from the given information, "
            "iteration cannot be applied.\n\n"
            "In addition, when the required term is far from the first term, repeatedly adding would be inefficient.\n\n"
            "Therefore, the formula method must be used.\n\n"
            "---------------------------------------------\n\n"
            "Formula Method\n\n"
            "The formula used is:\n"
            "aₙ = a + (n − 1)d\n\n"
            "Where:\n"
            "aₙ = the nth term\n"
            "a = the first term\n"
            "d = the common difference (the number added each time)\n"
            "n = the term position\n\n"
            "Step 1: Identify the known variables.\n"
            "Step 2: Substitute into the formula.\n"
            "Step 3: Rearrange if necessary to find the unknown.\n"
            "Step 4: Evaluate carefully."
        )

        return "Formula Method", explanation

    # ------------------------------------------------
    # CASE 2: d is known and we are finding a_n
    # ------------------------------------------------
    elif d is not None and a is not None and n is not None and a_n is None:

        explanation = (
            "Arithmetic Progressions (AP) and Geometric Progressions (GP) are both types of sequences.\n\n"
            "The difference is that AP increases or decreases by adding a fixed number (the common difference), "
            "while GP changes by multiplying by a fixed number.\n\n"
            "Since the common difference is known, we can repeatedly add it to reach the required term.\n\n"
            "This makes the iteration method straightforward and easy to apply.\n\n"
            "Although the formula method could also be used, iteration is more direct in this case.\n\n"
            "---------------------------------------------\n\n"
            "Iteration Method\n\n"
            "The iteration method works by adding the common difference to each term "
            "to generate the next term.\n\n"
            "Step 1: Start with the first term.\n"
            "Step 2: Add the common difference to get the next term.\n"
            "Step 3: Repeat until the required term is reached.\n\n"
            "This method only works when the common difference is known."
        )

        return "Iteration Method", explanation

    # ----------------------------------------
    # Default → Formula method
    # ----------------------------------------
    else:

        explanation = (
            "The formula method is the most reliable approach in this situation.\n\n"
            "The formula used is:\n"
            "aₙ = a + (n − 1)d"
        )

        return "Formula Method", explanation

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
# I'm limiting login attempts to prevent brute-force attacks
# STRIDE mitigation:
# - Spoofing (reducing credential guessing)
# - Denial of Service (preventing login flooding)
@limiter.limit("5 per minute")
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
    # AI prediction placeholders
    # -------------------------------
    predicted_method = None
    selected_topic = None

    # # I'm keeping separate explanations for each topic input feature
    quadratic_explanation = None
    simultaneous_explanation = None
    ratio_explanation = None
    gp_explanation = None
    ap_explanation = None

    # -------------------------------
    # Handle form submission (AI)
    # -------------------------------
    if request.method == "POST":

        selected_topic = request.form.get("topic")
        # ------------------------------
        # Logging student interaction
        # ------------------------------
        interaction_collection.insert_one({
            "username": session.get("user"),
            "role": session.get("role"),
            "topic_selected": selected_topic,
            "timestamp": datetime.utcnow()
        })

        # =========================
        # QUADRATIC BLOCK
        # =========================
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

        # =========================
        # SIMULTANEOUS BLOCK
        # =========================
        elif selected_topic == "simultaneous":

            # # I'm collecting the 2-equation coefficients from the student inputs
            a1 = request.form.get("a1")
            b1 = request.form.get("b1")
            c1 = request.form.get("c1")

            a2 = request.form.get("a2")
            b2 = request.form.get("b2")
            c2 = request.form.get("c2")

            # # I'm building a question string for the ML model (assistive layer)
            question_text = f"Solve the simultaneous equations: {a1}x + {b1}y = {c1}, and {a2}x + {b2}y = {c2}"

            # # I'm generating ML suggestion (assistive layer)
            ml_method = predict_method(question_text)

            # # I'm applying rule-based authority logic (this is the truth layer)
            rule_method, explanation_text, eq1, eq2 = rule_based_simultaneous_method(a1, b1, c1, a2, b2, c2)

            # # Hybrid decision layer (rule overrides ML if mismatch)
            if ml_method == rule_method:
                predicted_method = ml_method
            else:
                predicted_method = rule_method

            # # I'm passing the student-friendly explanation to the template
            simultaneous_explanation = explanation_text

        # =============================
        # RATIO BLOCK
        # =============================
        elif selected_topic == "ratio":

            # # I'm collecting the ratio inputs from the student
            total_amount = request.form.get("total_amount")
            part1 = request.form.get("part1")
            part2 = request.form.get("part2")

            # # I'm building a natural question string for the ML model (assistive layer)
            question_text = f"Share {total_amount} in the ratio {part1}:{part2}"

            # # I'm generating ML suggestion (assistive layer)
            ml_method = predict_method(question_text)

            # # I'm applying rule-based neutral logic (authoritative layer)
            rule_method, explanation_text = rule_based_ratio_method(total_amount, part1, part2)

            # # Hybrid decision layer (rule overrides ML if mismatch)
            if ml_method == rule_method:
                predicted_method = ml_method
            else:
                predicted_method = rule_method

            # # I'm storing explanation for display
            ratio_explanation = explanation_text

# =============================
        # GEOMETRIC PROGRESSION BLOCK
        # =============================
        elif selected_topic == "gp":

            # # I'm collecting GP inputs (allowing empty values)
            a_n = request.form.get("a_n")
            a = request.form.get("a")
            r = request.form.get("r")
            n = request.form.get("n")

            # # I'm building a question string for ML (assistive layer)
            question_text = f"Geometric progression with a={a}, r={r}, n={n}, a_n={a_n}"

            # # I'm generating ML suggestion (assistive layer)
            ml_method = predict_method(question_text)

            # # I'm applying rule-based authority logic
            rule_method, explanation_text = rule_based_gp_method(a_n, a, r, n)

            # # Hybrid decision layer (rule overrides ML if mismatch)
            if ml_method == rule_method:
                predicted_method = ml_method
            else:
                predicted_method = rule_method

            # # I'm storing explanation for display
            gp_explanation = explanation_text

# =========================
        # ARITHMETIC PROGRESSION BLOCK
        # =========================
        elif selected_topic == "ap":

            # # I'm collecting AP inputs from the student
            a_n = request.form.get("a_n")
            a = request.form.get("a")
            d = request.form.get("d")
            n = request.form.get("n")

            # # I'm building a natural question string for ML (assistive layer)
            question_text = f"Find term in arithmetic progression with a={a}, d={d}, n={n}"

            # # I'm generating ML suggestion (assistive layer)
            ml_method = predict_method(question_text)

            # # I'm applying rule-based authority logic
            rule_method, explanation_text = rule_based_ap_method(a_n, a, d, n)

            # # Hybrid decision layer (rule overrides ML if mismatch)
            if ml_method == rule_method:
                predicted_method = ml_method
            else:
                predicted_method = rule_method

            # # I'm storing explanation for display
            ap_explanation = explanation_text

            # ------------------------------
        # Logging method recommendation
        # ------------------------------
        usage_collection.insert_one({
            "username": session.get("user"),
            "topic": selected_topic,
            "recommended_method": predicted_method,
            "timestamp": datetime.utcnow()
        })

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
        quadratic_explanation=quadratic_explanation,
        simultaneous_explanation=simultaneous_explanation,
        ratio_explanation=ratio_explanation,
        gp_explanation=gp_explanation,
        ap_explanation=ap_explanation
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


# ==========================================
# SECURITY HEADERS (STRIDE – Info Disclosure Protection)
# ==========================================
# I'm strengthening protection against Information Disclosure and XSS
# This applies HTTP security headers to every response

@app.after_request
def apply_security_headers(response):
    """
    Adding HTTP security headers to reduce:
    - Clickjacking
    - MIME sniffing
    - XSS exposure
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline'; "
    "font-src 'self' https://cdn.jsdelivr.net;"
)
    return response

# -------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------
# I’m running the Flask development server
# I'm disabling debug mode to prevent sensitive information leakage (STRIDE – Information Disclosure)
if __name__ == "__main__":
    app.run(debug=False)
