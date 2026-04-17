# Secure-explainable-ai-mathematics
**Explainable AI for Enhancing Conceptual Understanding in GCSE-Level Mathematics Education**

This is a secure educational web application built with Flask, SQLite, MongoDB, machine learning, and rule-based mathematical logic. It is designed to support students in developing a deeper conceptual understanding of GCSE-level mathematics by guiding them through appropriate solving methods, clear reasoning, and structured explanations.

This application was developed as part of a Data science and artificial intelligence project. It demonstrates secure coding, responsible AI use and data-driven system design

**Table of Contents**
	1.	Overview
	2.	Features
	3.	System Architecture
	4.	Installation Guide
	5.	How to Run the Application
	6.	Using the Application
	7.	Teacher Guide
	8.	Student Guide
	9.	Security Features
	10.	Databases Used
	11.	Explainable AI Logic
	12.	Testing
	13.	Repository / GitHub Activity
	14.	Author

**1. Overview**

The Secure Explainable AI Mathematics application is a Flask-based web system that integrates machine learning with rule-based mathematical logic to recommend suitable solving methods. The system processes user input, applies a trained classification model, and combines this with structured logic to provide clear method recommendations and explanations. It also includes an interactive dashboard with topic-based sections, allowing users to explore different areas and receive guided support in a structured and accessible way.

The application currently supports five key maths topics including:
	•	Quadratic Equations
	•	Simultaneous Equations
	•	Ratio
	•	Sequences (Geometric Progression)
	•	Sequences (Arithmetic Progression)

The system supports two user roles:
	•	Teacher/Admin – can access the dashboard, manage questions, create and delete users, delete questions, and change password.
	•	Student – can log in securely, access learning topics, view recommended methods, and use the system for guided maths support, and change password.

This application combines:
	•	SQLite → user accounts and question storage
	•	MongoDB → analytics logging and usage tracking
	•	Machine Learning + Rule-Based Logic → method recommendation and explainable reasoning


**2️. Key Features**

✔Secure Login and Role-Based Access
	•	Users must log in before accessing the dashboard.
	•	Teachers and students have different permissions.
	•	Teacher-only actions are protected through role-based access control.
	•	Passwords are stored securely using hashing.

✔Explainable Maths Support

The system does not only recommend a method. It also explains:
	•	why the chosen method works
	•	why another method may not be best
	•	The structure of the topic

✔ Topic-Based Dashboard

Students and teachers can use a structured dashboard with a topic selector. This avoids long scrolling and makes the interface cleaner and more focused.

✔ Hybrid AI Decision Layer

The application uses a combination of:
	•	trained machine learning model
	•	TF-IDF vectoriser
	•	rule-based mathematical logic

The rule-based logic acts as the authority layer so recommendations remain mathematically reliable.

✔ Teacher/Admin Management Tools

Teachers can:
	•	add questions
	•	delete questions
	•	create users
	•	delete users
	•	change password

✔ Multi-database system (MDBS)
The system uses two data bases:
	•	SQLite
	•	MongoDB

✔ Custom Error Pages

The application uses customised 403 and 404 pages instead of default Flask error responses.


✔Testing Approach
	•	Unit testing: Tested individual component to ensure they work correctly on their own.
	•	Integration testing: Checked that different parts of the system work together properly.
	•	End-to-end testing: Tested the full system workflow from user input to final output.
The testing approaches confirm that the application behaves correctly, securely, and reliably.


**3. System Architecture**

secure-explainable-ai-mathematics/
│
├── app.py                                      # Main Flask application (routes, security, AI logic, dashboards)
├── fix_db.py                                   # Database recovery / helper script for restoring users
├── load_data.py                                # Loads maths question data into the database
├── Mathematics-questions-dataset.csv           # Main maths questions dataset
├── Mathematics-questions-training-dataset-ML…  # Training dataset used for the ML model
├── README.md                                   # Project overview, setup, user guide, and documentation
├── test_app.py                                 # Unit tests for core rule-based logic
├── test_end2end.py                             # End-to-end tests for full user flows
├── test_routes.py                              # Integration tests for routes and access control
├── tfidf_vectorizer.pkl                        # Saved TF-IDF vectoriser
├── train_model.py                              # Trains the machine learning model
├── trained_method_model.pkl                    # Saved trained method classification model
│
├── instance/
│   └── maths.db                                # SQLite database file
│
├── static/
│   └── background.jpg                          # Background image (UI)
│
├── templates/
│   ├── 403.html                                # Customised forbidden error page
│   ├── 404.html                                # Customised page not found error page
│   ├── dashboard.html                          # Main role-based dashboard
│   └── login.html                              # Secure login page
│
├── .venv/                                      # Virtual environment
├── .pytest_cache/                              # Pytest cache files
├── __pycache__/                                # Compiled Python cache files
└── app/                                        # App-related folder/module


**System Flow**
╔════════════════════════════════════════════════════════════════════════════╗
║                               USERS / ROLES                                ║
║                                                                            ║
║   ┌──────────────┐              ┌──────────────────────┐                   ║
║   │   Student    │              │   Teacher / Admin    │                   ║
║   └───────🟢─────┘             └───────────🟡─────────┘                   ║
╚════════════════════════════════════════════════════════════════════════════╝
                                    ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         WEB BROWSER INTERFACE                                                             │
│                                                                                                           │
│   Dashboard  •  Login  •  System Practice Questions  •  Question Input  •  Explanations • Settings pannel │
└───────────────────────────────────────🟦──────────────────────────────────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                   FLASK WEB APPLICATION  (app.py)                          │
│         Routing • Sessions • Requests • Responses • Templates              │
└───────────────────────┬───────────────────────────────┬────────────────────┘
                        │                               │
             ┌──────────┴──────────┐         ┌──────────┴──────────┐
             ▼                     ▼         ▼                     ▼
┌────────────────────────────┐  ┌───────────────────────────────────────────┐
│  AUTHENTICATION & ACCESS   │  │             USER-FACING FEATURES          │
│         CONTROL            │  │                                           │
│  🟣 Security Layer         │  │  🟢 Practice questions                    │
│  • Secure login            │  │  🟢 User input questions                  │
│  • Session management      │  │  🟢 Topic explanations                    │
│  • Role-based access       │  │  🟢 Worked examples (multiple methods)    │
│  • Admin privileges        │  │  🟢 Method recommendations + reasoning    │
└────────────────────────────┘  │  🟢 Application user guide                │
                                └───────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                   PREDICTION & REASONING ENGINE                            │
├────────────────────────────┬────────────────────────────┬───────────────────────┤
│  TF-IDF Vectoriser (.pkl)  │     ML Model (.pkl)        │  Rule-Based Logic     │
│         🟠 Feature Input    │       🟣 Prediction      │    🟤 Validation      │
└────────────────────────────┴────────────────────────────┴───────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                     EXPLAINABLE OUTPUT LAYER                               │
│                                                                            │
│   🟩 Recommended method                                                    │
│   🟩 Why the method is suitable                                            │
│   ⚪ Why other methods are less suitable                                   │
│   📝 Step-by-step worked examples                                          │
└───────────────────────────────────────🟩────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION / RENDERING                              │
│                                                                            │
│   HTML Templates • CSS • JavaScript • MathJax Rendering                    │
└───────────────────────────────────────🟦────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE LAYER                                     │
│                                                                            │
│   SQLite → core system data                                                │
│   • users (login, passwords, roles)                                        │
│   • stored questions                                                       │
│                                                                            │
│   MongoDB → behaviour tracking                                             │
│   • student interactions (clicks, topics, methods)                         │
│   • usage analytics (timestamps, activity patterns)                        │
└────────────────────────────────────────────────────────────────────────────┘


**4. installation guide**
Requirements
	•	Python 3.10+
	•	pip (Python package manager)
	•	MongoDB Community Server
	•	Visual Studio Code (recommended)

Step 1: Clone or Download the Project
git clone <https://github.com/DonaldsonLTU/Secure-explainable-ai-mathematics>
cd secure-explainable-ai-mathematics

Step 2: Create and Activate Virtual Environment (Recommended)
Activate python -m venv .venv

Step 3: Install Dependencies
-pip install flask flask-wtf flask-sqlalchemy werkzeug pymongo joblib scikit-learn flask-limiter

Step 4: Ensure Required Files Are Present
	•	trained_method_model.pkl
	•	tfidf_vectorizer.pkl
	•	Question dataset files
	•	templates/ and static/ folders

Step 5: Set Environment Variables
-set SECRET_KEY=your-secret-key

Step 6: Ensure MongoDB is Running
	•	Open MongoDB Compass OR start MongoDB service
	•	Default connection: mongodb://localhost:27017/

Step 7: Load Initial Question Data
-python load_data.py

Step 8: Run the Application
python app.py

You should see: Running on http://127.0.0.1:5000

Step 9: Access the Application

Open your browser and go to: http://127.0.0.1:5000

**5. Using the Application**
-Login:
Users begin at the login page and enter their username and password.

-Dashboard
After successful login:
	•	students are taken to a guided learning dashboard
	•	teachers are taken to a dashboard with both learning tools and management features

-Topic Selection
Users select a topic from the dropdown menu:
	•	Quadratic Equations
	•	Simultaneous Equations
	•	Ratio
	•	Geometric Progression
	•	Arithmetic Progression

Once a topic is selected, the relevant topic card appears.

-Question Interaction

Students can:
	•	select a question
	•	see the recommended method
	•	view why that method is suitable
	•	open additional explanation content
    •	view solving methods and worked examples
    •	insert their own question

-Logout:
Users can log out securely at any time.

**6. Teacher/Admin Guide**

Teachers have extended permissions and can manage the learning system.

Teacher tools include:
	•	Add Question
Teachers can insert a new maths question into the SQLite database.
	•	Delete Question
Teachers can remove questions using the question ID.
	•	Create User
Teachers can create new student accounts.
	•	Delete User
Teachers can remove user accounts from the system.
	•	Change Password
Teachers can securely update their own password.
	•	View Question Table
Teachers can view the full question management table on the dashboard.

Teacher journey
Login
  |
  v
Dashboard
  |
  +-- Select a maths topic
  +-- View method recommendation
  +-- Add question
  +-- Delete question
  +-- Create user
  +-- Delete user
  +-- Change password
  |
  v
Logout

**7. Student Guide**

Students use the system as a guided learning tool.

Student features:
	•	secure login
	•	access to the topic selector
	•	recommended maths methods
	•	explanation of why a method works
	•	structured topic-based learning support
	•	password change option

Student restrictions:
	•	no teacher-only admin controls
	•	no question management table
	•	no ability to create or delete users
	•	no ability to delete questions

Student journey
Login
  |
  v
Dashboard
  |
  +-- Read welcome message and learning guide
  +-- Select topic
  +-- Choose question
  +-- View recommended method
  +-- Read explanation
  +-- Continue practice
  |
  v
Logout

**8. Security Features**

The system includes multiple security protections:

✔ Authentication and Login Protection
Users must log in before accessing protected routes. This prevents unauthorised dashboard access.

✔ Password Hashing
Passwords are stored securely using Werkzeug hashing rather than plain text.

✔ Role-Based Access Control (RBAC)
Teacher-only routes and functions are protected using login_required and teacher_only decorators. 

✔ Secure Session Handling
The application uses session cookies with secure configuration, including HTTPOnly session protection.  

✔ CSRF Protection
All forms are protected using Flask-WTF and CSRF tokens.  

✔ Input Validation and Sanitisation
User input is validated through Flask-WTF and controlled processing logic.

✔ Rate Limiting
Login attempts are limited to reduce brute-force attacks and abuse.

✔ Environment-Based Configuration
Sensitive configuration such as the Flask secret key is environment-aware, with environment variable support.

✔ Security Headers
The application applies headers such as:
	•	X-Content-Type-Options
	•	X-Frame-Options
	•	Content-Security-Policy

to reduce information disclosure and browser-based attacks.

STRIDE Mapping

The implemented security measures align with STRIDE:
	•	Spoofing → authentication, password hashing, session security
	•	Tampering → input validation, CSRF protection
	•	Repudiation → session-controlled user actions
	•	Information Disclosure → hashing, security headers, safe error pages
	•	Denial of Service → rate limiting
	•	Elevation of Privilege → role-based access control

**9. Databases Used**

-SQLite

SQLite stores:
	•	user accounts
	•	hashed passwords
	•	user roles
	•	maths questions
	•	recommended method labels
	•	method reasoning text

-MongoDB

MongoDB stores:
	•	student interaction logs
	•	usage history
	•	topic selection events
	•	recommended method events
	•	timestamps
MongoDB is used because it supports flexible analytics logging and future interaction analysis.

1️**10. Explainable AI Logic**

This system does not rely only on Machine learning predictions; it uses a hybrid approach consisting of:
1.	Machine Learning Layer
A trained Random Forest classification model predicts a method recommendation from question text using:
	•	TF-IDF vectorisation
	•	saved classification model

2.	Rule-Based Logic Layer
The system then applies topic-specific mathematical rules to verify the machine learning suggestion.
This hybrid design improves reliability and makes the system more suitable for educational use.


**11. Testing**

Testing was implemented to ensure the system is reliable, secure, and works correctly.

-Unit Testing

Unit tests were used to verify core method-selection logic independently.

The tests confirmed correct behaviour for:
	•	quadratic method logic
	•	simultaneous equations logic
	•	ratio logic
	•	geometric progression logic
	•	arithmetic progression logic

-Integration Testing

Integration tests were used to verify that system components work together correctly.

These tests confirmed:
	•	login route handling
	•	form submission behaviour
	•	dashboard access after login
	•	protected route behaviour

-End-to-End Testing

End-to-end tests were used to simulate real user journeys in the system.

These tests confirmed:
	•	teacher login, dashboard access, and logout
	•	student login and restricted access behaviour
	•	topic page loading and full interaction flow

Overall, the inclusion of unit, integration, and end-to-end testing strengthens confidence in the system’s reliability and security.

**12. Repository / GitHub Activity**

The project was developed using Git and GitHub with clear version control practice.

This includes:
	•	meaningful commits
	•	development progress
	•	testing commits
	•	UI refinement commits
	•	project documentation updates

This demonstrates structured development workflow and good software engineering practice.

**13. Future Improvements**
	•	Use a larger and more diverse dataset
To improve model accuracy and handle a wider range of mathematical problem types.
	•	Expand rule-based mathematical logic
To improve reliability and ensure correct method recommendations across more complex scenarios.
	•	Increase the range of worked examples
To cover more question structures and help students find examples closer to their own problems.
	•	Support more complex mathematical structures
Such as powers, roots, and advanced fractions to improve system coverage.
	•	Add layered explanations
Allowing students to move from simple explanations to deeper conceptual understanding.
	•	Introduce an answer-checking feature
So students can input their own solutions and receive feedback on errors.
•	more maths topics beyond the current five

**14. Author**

Donaldson Mordi
Explainable AI for Enhancing Conceptual Understanding in GCSE-Level Mathematics Education 
Leeds Trinity University