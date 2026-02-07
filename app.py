# I’m importing Flask tools for routing, sessions, and redirects
from flask import Flask, request, redirect, url_for, session, render_template_string, abort

# I’m importing Werkzeug tools for secure password hashing and checking
from werkzeug.security import generate_password_hash, check_password_hash

import os

# I’m creating the Flask application instance
app = Flask(__name__)

# I’m setting a secret key for secure session management
# In production this would come from environment variables
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

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
    # I’m handling the login form submission
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # I’m validating credentials securely
        if username in users and check_password_hash(users[username]["password"], password):
            session["user"] = username
            session["role"] = users[username]["role"]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password", 401

    # I’m rendering a simple login form (HTML inline for now)
    return render_template_string("""
        <h2>Secure Explainable AI Mathematics Login</h2>
        <form method="post">
            <label>Username:</label><br>
            <input type="text" name="username" required><br><br>

            <label>Password:</label><br>
            <input type="password" name="password" required><br><br>

            <button type="submit">Login</button>
        </form>
    """)

# -------------------------------------------------
# DASHBOARD (ROLE-BASED ACCESS)
# -------------------------------------------------
@app.route("/dashboard")
def dashboard():
    # I’m blocking access if the user is not logged in
    if "user" not in session:
        abort(403)

    # I’m displaying different content based on role
    if session["role"] == "teacher":
        return "<h1>Teacher Dashboard</h1><p>Welcome, Teacher.</p>"
    else:
        return "<h1>Student Dashboard</h1><p>Welcome, Student.</p>"

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