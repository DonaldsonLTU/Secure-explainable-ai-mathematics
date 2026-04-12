# Secure-explainable-ai-mathematics
Explainable AI for Enhancing Conceptual Understanding in GCSE-Level Mathematics Education

╔════════════════════════════════════════════════════════════════════════════╗
║                               USERS / ROLES                                ║
║                                                                            ║
║   ┌──────────────┐              ┌──────────────────────┐                   ║
║   │   Student    │              │   Teacher / Admin    │                   ║
║   └───────🟢─────┘             └───────────🟡─────────┘                   ║
╚════════════════════════════════════════════════════════════════════════════╝
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         WEB BROWSER INTERFACE                                        │
│                                                                                      │
│   Dashboard  •  Login  •  System Practice Questions  •  Question Input  •  Results   │
└───────────────────────────────────────🟦─────────────────────────────────────────────┘
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
│  🟣 Security Layer        │  │  🟢 Practice questions                    │
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
│         🟠 Feature Input   │          🟣 Prediction    │       🟤 Validation   |
└────────────────────────────┴────────────────────────────┴────────────────────────┘
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
│                         SQLITE DATABASE  (maths.db)                        │
├────────────────────────────┬────────────────────────────┬───────────────────┤
│   Questions Dataset       │   Users & Roles            │   Admin Content   │
│  • Questions Dataset       │  • Students                │  • Topics         │
│  • Metadata                │  • Teachers / Admins       │  • Worked examples│
│  • Tags / Difficulty       │  • Credentials             │  • Method rules   │
└────────────────────────────┴────────────────────────────┴───────────────────┘



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