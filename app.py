# I’m importing Flask tools for routing, sessions, and redirects
from flask import Flask, request, redirect, url_for, session, render_template, abort, render_template_string

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
# DASHBOARD (ROLE-BASED ACCESS)
# -------------------------------------------------
# I’m displaying the dashboard using a proper HTML template (MVC separation)
@app.route("/dashboard")
def dashboard():
    # I’m blocking access if the user is not logged in
    if "user" not in session:
        abort(403)

    # I’m passing session data safely into the template
    return render_template(
        "dashboard.html",
        user=session["user"],
        role=session["role"]
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
# RUN APPLICATION
# -------------------------------------------------
# I’m running the Flask development server
if __name__ == "__main__":
    app.run(debug=True)