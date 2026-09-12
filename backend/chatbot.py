from flask import Blueprint, request, jsonify


# ============================================================
# CREATE CHATBOT BLUEPRINT
# ============================================================

chatbot = Blueprint("chatbot", __name__)


# ============================================================
# SMART QUEUE PROJECT KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = {

    # --------------------------------------------------------
    # PROJECT
    # --------------------------------------------------------

    "project": """
This project is called:

Smart Queue Management and Waiting Time Prediction System.

The main purpose of the project is to digitally manage
customer queues and predict how long a customer may have
to wait.

Users can register, login, join a queue and receive a token.

The system uses Machine Learning to predict waiting time.

The main technologies are:

Frontend:
HTML, CSS and JavaScript

Backend:
Python and Flask

Database:
SQLite

Machine Learning:
Random Forest Regressor

Libraries:
Pandas, NumPy, Scikit-learn and Joblib
""",


    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------

    "objective": """
The main objectives of this project are:

1. Digitally manage customer queues.
2. Generate token numbers for customers.
3. Allow users to join queues.
4. Allow administrators to manage queues.
5. Predict customer waiting time using Machine Learning.
6. Reduce unnecessary waiting and overcrowding.
7. Improve the customer experience.
""",


    # --------------------------------------------------------
    # FOLDER STRUCTURE
    # --------------------------------------------------------

    "folder structure": """
The project folder structure is:

smart_queue_predictor/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── chatbot.py
│   │
│   ├── models/
│   │   └── prediction_model.pkl
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── train_model.py
│   │   └── predict.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       ├── queue.py
│       ├── prediction.py
│       └── admin.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin.html
│   │
│   ├── css/
│   │   ├── style.css
│   │   └── chatbot.css
│   │
│   └── js/
│       ├── login.js
│       ├── register.js
│       ├── dashboard.js
│       ├── admin.js
│       └── chatbot.js
│
├── dataset/
│   └── queue_data.csv
│
├── requirements.txt
├── README.md
└── venv/

The project is divided into three major parts:

1. Backend
2. Frontend
3. Dataset

The backend contains the application logic, APIs, database
operations and Machine Learning code.

The frontend contains the user interface.

The dataset contains the data used for Machine Learning.
""",


    # --------------------------------------------------------
    # MODULES
    # --------------------------------------------------------

    "modules": """
The project contains the following major modules:

1. Authentication Module
2. Queue Management Module
3. Machine Learning Module
4. Prediction Module
5. Database Module
6. Admin Module
7. Chatbot Module
8. Frontend Module

Authentication handles registration and login.

Queue Management handles queue creation, joining queues,
token generation and serving customers.

Machine Learning trains the Random Forest model.

Prediction uses the trained model to predict waiting time.

Database manages SQLite tables.

Admin manages queues and dashboard statistics.

Chatbot answers project-related questions.

Frontend provides the user interface.
""",


    # --------------------------------------------------------
    # EVERY MODULE
    # --------------------------------------------------------

    "every module": """
Here is the complete explanation of every major module.

============================================================
1. app.py
============================================================

app.py is the main Flask application.

It creates the Flask application, enables CORS, initializes
the database and registers all API blueprints.

It connects:

Authentication
Queue Management
Prediction
Admin
Chatbot

to the Flask application.


============================================================
2. config.py
============================================================

config.py stores configuration values.

For example:

SECRET_KEY
DEBUG
PORT

It keeps configuration separate from the main application.


============================================================
3. database.py
============================================================

database.py manages the SQLite database.

It creates the database connection and creates the following
tables:

users
queues
queue_entries
predictions

The function get_db_connection() creates a connection to
queue.db.

The initialize_database() function creates the tables when
the application starts.


============================================================
4. auth.py
============================================================

auth.py handles authentication.

It contains:

Registration API
Login API

Registration receives:

name
email
password

Login checks:

email
password

The user information is stored in the users table.


============================================================
5. queue.py
============================================================

queue.py handles queue operations.

It is responsible for:

Creating queues
Listing queues
Getting queue details
Updating queues
Joining queues
Generating tokens
Checking queue status
Serving the next customer

For example:

POST /api/queue/join

allows a user to join a queue.


============================================================
6. prediction.py
============================================================

prediction.py connects the frontend with the Machine Learning
model.

It receives:

queue_length
active_counters
average_service_time
arrival_rate

The backend also determines:

hour
day_of_week

These values are passed to the Machine Learning model.

The predicted waiting time is then returned to the frontend.


============================================================
7. admin.py
============================================================

admin.py provides administrator dashboard information.

It calculates:

Total users
Active queues
People waiting
Average predicted waiting time

The Admin Dashboard uses this information to display
statistics.


============================================================
8. train_model.py
============================================================

train_model.py trains the Machine Learning model.

First, pandas reads:

dataset/queue_data.csv

The input features are:

queue_length
active_counters
avg_service_time
hour
day_of_week
arrival_rate

The target variable is:

waiting_time

The data is divided into training and testing data.

RandomForestRegressor is trained using the training data.

The model is evaluated using:

MAE
R² Score

Finally, the trained model is saved as:

backend/models/prediction_model.pkl


============================================================
9. predict.py
============================================================

predict.py loads the trained model.

It uses joblib to load:

prediction_model.pkl

It receives the queue information and passes it to the model.

The model returns the predicted waiting time.


============================================================
10. chatbot.py
============================================================

chatbot.py contains the project-specific chatbot.

It contains a knowledge base with information about:

Project
Architecture
Folder Structure
Modules
Machine Learning
Random Forest
Dataset
Flask
SQLite
APIs
Queue Management
Prediction
Viva Questions

The chatbot receives a question from the frontend and
returns a suitable answer.


============================================================
11. prediction_model.pkl
============================================================

prediction_model.pkl is the trained Machine Learning model.

It is created by train_model.py.

predict.py loads this file whenever a prediction is required.


============================================================
12. queue_data.csv
============================================================

queue_data.csv is the Machine Learning dataset.

It contains the input features and waiting_time target.

Columns are:

queue_length
active_counters
avg_service_time
hour
day_of_week
arrival_rate
waiting_time


============================================================
13. dashboard.html
============================================================

dashboard.html is the customer interface.

It allows the user to:

Join a queue
View token number
Enter prediction information
Request waiting-time prediction
Use the project chatbot


============================================================
14. admin.html
============================================================

admin.html is the administrator interface.

It allows the administrator to:

View statistics
Select queues
Update queue information
Calculate predictions
Serve the next customer
Use the chatbot


============================================================
15. login.html
============================================================

login.html provides the login form.

The user enters email and password.

login.js sends the information to the Flask login API.


============================================================
16. register.html
============================================================

register.html provides the registration form.

The user enters:

Name
Email
Password

register.js sends this information to the backend.


============================================================
17. dashboard.js
============================================================

dashboard.js controls customer dashboard operations.

It communicates with Flask APIs to:

Join queues
Receive tokens
Request waiting-time predictions


============================================================
18. admin.js
============================================================

admin.js controls the Admin Dashboard.

It communicates with the backend to:

Load statistics
Load queues
Get queue details
Update queues
Calculate predictions
Serve customers


============================================================
19. login.js
============================================================

login.js sends login information to:

POST /api/auth/login

After successful login, the user information is stored
in localStorage.


============================================================
20. register.js
============================================================

register.js sends registration information to:

POST /api/auth/register


============================================================
21. chatbot.js
============================================================

chatbot.js controls the chatbot interface.

It:

Opens the chatbot
Closes the chatbot
Sends questions
Displays user messages
Displays chatbot answers
Handles Enter key
Clears chat
Displays suggested questions


============================================================
22. style.css
============================================================

style.css controls the main website appearance.

It styles:

Containers
Headings
Buttons
Inputs
Dashboard
Cards
Forms


============================================================
23. chatbot.css
============================================================

chatbot.css controls the chatbot appearance.

It styles:

Chatbot button
Chatbot window
Header
Messages
Suggested questions
Input box
Send button
Mobile layout
""",


    # --------------------------------------------------------
    # MACHINE LEARNING
    # --------------------------------------------------------

    "machine learning": """
Machine Learning is used in this project to predict customer
waiting time.

The project uses supervised learning.

The input features are:

queue_length
active_counters
avg_service_time
hour
day_of_week
arrival_rate

The target variable is:

waiting_time
""",


    "algorithm": """
The Machine Learning algorithm used in this project is:

Random Forest Regressor.

Waiting time is a continuous numerical value, so this is a
regression problem.

Random Forest creates multiple decision trees and combines
their predictions to produce the final result.
""",


    "random forest": """
Random Forest is an ensemble Machine Learning algorithm.

It creates multiple decision trees.

Each tree produces a prediction and the predictions are
combined to produce the final result.

In this project, RandomForestRegressor is used because
waiting time is a continuous numerical value.
""",


    "why random forest": """
Random Forest was selected because:

1. It works well with multiple input features.
2. It can model non-linear relationships.
3. It is suitable for regression.
4. It is relatively robust.
5. It is easy to implement using scikit-learn.
""",


    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    "dataset": """
The Machine Learning dataset is:

queue_data.csv

It contains these columns:

1. queue_length
2. active_counters
3. avg_service_time
4. hour
5. day_of_week
6. arrival_rate
7. waiting_time

The first six columns are input features.

waiting_time is the target variable.
""",


    "features": """
The six input features used by the model are:

1. queue_length
2. active_counters
3. avg_service_time
4. hour
5. day_of_week
6. arrival_rate

The target variable is waiting_time.
""",


    "queue length": """
queue_length represents the number of customers currently
waiting in the queue.

A larger queue generally means a customer may have to wait
longer.
""",


    "active counters": """
active_counters represents the number of service counters
currently available.

More active counters can reduce customer waiting time.
""",


    "service time": """
avg_service_time represents the average amount of time
required to serve one customer.
""",


    "arrival rate": """
arrival_rate represents how quickly customers are arriving
at the queue.
""",


    "waiting time": """
waiting_time is the target variable of the Machine Learning
model.

It represents the estimated customer waiting time in minutes.
""",


    # --------------------------------------------------------
    # MODEL EVALUATION
    # --------------------------------------------------------

    "mae": """
MAE means Mean Absolute Error.

It calculates the average absolute difference between actual
waiting times and predicted waiting times.

A lower MAE generally means better prediction performance.
""",


    "r2": """
R² means R-squared.

It measures how well the model explains the variation in the
target variable.

A value closer to 1 generally indicates a better fit.
""",


    "accuracy": """
This project is a regression problem.

Therefore, classification accuracy is not the main evaluation
metric.

The project uses:

MAE
R² Score

to evaluate the Machine Learning model.
""",


    # --------------------------------------------------------
    # FLASK / PYTHON
    # --------------------------------------------------------

    "flask": """
Flask is a lightweight Python web framework.

In this project Flask is used to:

Create the backend
Create REST APIs
Handle requests
Connect frontend and backend
Connect the database
Connect the Machine Learning model
""",


    "python": """
Python is the main programming language used in this project.

Python is used for:

Flask backend
Database operations
Machine Learning
Data processing
Chatbot
""",


    "why python": """
Python was selected because it provides powerful libraries
for:

Machine Learning
Data processing
Web development
Database connectivity

It is also easy to develop and maintain.
""",


    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    "database": """
The project uses SQLite as the database.

The main tables are:

1. users
2. queues
3. queue_entries
4. predictions
""",


    "sqlite": """
SQLite is a lightweight relational database.

It is used in this project to store:

User information
Queue information
Queue entries
Prediction records

The database file is:

backend/database/queue.db
""",


    # --------------------------------------------------------
    # API
    # --------------------------------------------------------

    "api": """
Important APIs in the project are:

Authentication:

POST /api/auth/register
POST /api/auth/login

Queue:

POST /api/queue/create
GET /api/queue/list
GET /api/queue/details/<queue_id>
PUT /api/queue/update/<queue_id>
POST /api/queue/join
GET /api/queue/status/<queue_id>
POST /api/queue/next/<queue_id>

Prediction:

POST /api/prediction/predict

Admin:

GET /api/admin/dashboard

Chatbot:

POST /api/chatbot/ask
""",


    # --------------------------------------------------------
    # QUEUE
    # --------------------------------------------------------

    "queue": """
Queue Management is one of the main modules.

It allows:

Queue creation
Queue listing
Customer joining
Token generation
Queue status checking
Serving the next customer

The queue information is stored in SQLite.
""",


    "join queue": """
A logged-in user can join a queue.

The frontend sends a request to:

POST /api/queue/join

The backend creates a queue entry and generates a token
number for the customer.
""",


    "token": """
A token number represents a customer's position in the queue.

When a user joins a queue, the system generates a token
number.
""",


    # --------------------------------------------------------
    # DASHBOARDS
    # --------------------------------------------------------

    "user dashboard": """
The User Dashboard provides:

1. Queue joining
2. Token display
3. Waiting-time prediction
4. Smart Queue chatbot
""",


    "admin dashboard": """
The Admin Dashboard provides:

1. Total users
2. Active queues
3. People waiting
4. Average predicted waiting time
5. Queue selection
6. Queue update
7. Waiting-time prediction
8. Serve next customer
9. Chatbot assistance
""",


    # --------------------------------------------------------
    # ARCHITECTURE
    # --------------------------------------------------------

    "architecture": """
The architecture of the project is:

User
  ↓
Frontend
HTML + CSS + JavaScript
  ↓
Flask REST API
  ↓
Backend Logic
  ↓
SQLite Database

For waiting-time prediction:

Frontend
  ↓
Prediction API
  ↓
Machine Learning Module
  ↓
Random Forest Model
  ↓
Predicted Waiting Time
  ↓
Frontend
""",


    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    "workflow": """
The complete project workflow is:

Registration
      ↓
Login
      ↓
User Dashboard
      ↓
Select Queue
      ↓
Join Queue
      ↓
Generate Token
      ↓
Queue Information
      ↓
Machine Learning Prediction
      ↓
Display Waiting Time
      ↓
Admin Manages Queue
      ↓
Serve Customer
""",


    # --------------------------------------------------------
    # JOBLIB
    # --------------------------------------------------------

    "joblib": """
Joblib is used to save and load the trained Machine Learning
model.

The trained Random Forest model is saved as:

prediction_model.pkl

predict.py loads this file when a prediction is required.
""",


    # --------------------------------------------------------
    # PANDAS
    # --------------------------------------------------------

    "pandas": """
Pandas is used to read and process the Machine Learning
dataset.

The project uses pandas to read:

queue_data.csv
""",


    # --------------------------------------------------------
    # SCIKIT
    # --------------------------------------------------------

    "scikit": """
Scikit-learn is the Machine Learning library used in this
project.

It provides:

RandomForestRegressor
train_test_split
mean_absolute_error
r2_score
""",


    # --------------------------------------------------------
    # TECHNOLOGIES
    # --------------------------------------------------------

    "technologies": """
The technologies used in this project are:

Frontend:
HTML
CSS
JavaScript

Backend:
Python
Flask

Database:
SQLite

Machine Learning:
Scikit-learn
Random Forest Regressor

Data Processing:
Pandas
NumPy

Model Storage:
Joblib
""",


    # --------------------------------------------------------
    # ADVANTAGES
    # --------------------------------------------------------

    "advantages": """
The main advantages of the project are:

1. Digital queue management.
2. Token generation.
3. Waiting-time prediction.
4. Reduced uncertainty for customers.
5. Better queue monitoring.
6. Admin management.
7. Improved customer experience.
""",


    # --------------------------------------------------------
    # LIMITATIONS
    # --------------------------------------------------------

    "limitations": """
The main limitation is that prediction quality depends on
the training dataset.

If the dataset is small or does not represent real-world
conditions, prediction accuracy may be limited.

The predicted waiting time is an estimate and not a guarantee.
""",


    # --------------------------------------------------------
    # FUTURE SCOPE
    # --------------------------------------------------------

    "future": """
Future improvements can include:

1. Mobile application.
2. SMS notifications.
3. Email notifications.
4. Real-time queue monitoring.
5. CCTV-based customer counting.
6. Larger real-world datasets.
7. Cloud deployment.
8. Advanced Machine Learning models.
9. Real-time analytics.
10. Automatic queue optimization.
""",


    # --------------------------------------------------------
    # VIVA
    # --------------------------------------------------------

    "viva": """
Important viva questions for this project include:

1. What is the objective of the project?
2. Why did you choose this project?
3. What Machine Learning algorithm did you use?
4. Why did you use Random Forest?
5. Why is this a regression problem?
6. What are the input features?
7. What is the target variable?
8. What dataset did you use?
9. What is MAE?
10. What is R²?
11. Why did you use Flask?
12. Why did you use SQLite?
13. What are the main modules?
14. Explain the project architecture.
15. Explain the project workflow.
16. What is the role of train_model.py?
17. What is the role of predict.py?
18. What is prediction_model.pkl?
19. What are the limitations?
20. What is the future scope?
""",


    # --------------------------------------------------------
    # ONE MINUTE EXPLANATION
    # --------------------------------------------------------

    "one minute": """
My project is a Smart Queue Management and Waiting Time
Prediction System.

The system manages digital queues and predicts customer
waiting time using Machine Learning.

The frontend is developed using HTML, CSS and JavaScript.
The backend uses Python and Flask.
SQLite is used as the database.
Random Forest Regressor is used for waiting-time prediction.

Users can register, login, join queues and receive tokens.

Administrators can manage queues, monitor statistics and
serve customers.

The main aim is to reduce unnecessary waiting and improve
queue management.
"""
}


# ============================================================
# GET ANSWER
# ============================================================

def get_answer(question):

    question = question.lower().strip()


    # --------------------------------------------------------
    # FOLDER STRUCTURE
    # --------------------------------------------------------

    if (
        "folder structure" in question
        or "project structure" in question
        or "directory structure" in question
        or (
            "folder" in question
            and "structure" in question
        )
    ):

        return KNOWLEDGE_BASE["folder structure"]


    # --------------------------------------------------------
    # EVERY MODULE / CODE MODULE
    # --------------------------------------------------------

    if (
        "every module" in question
        or "each module" in question
        or "all modules" in question
        or "code in every module" in question
        or "code of every module" in question
        or "explain code modules" in question
        or "explain modules" in question
    ):

        return KNOWLEDGE_BASE["every module"]


    # --------------------------------------------------------
    # SPECIFIC MODULES
    # --------------------------------------------------------

    if "auth module" in question:
        return KNOWLEDGE_BASE["every module"]


    if "queue module" in question:
        return KNOWLEDGE_BASE["every module"]


    if "ml module" in question:
        return KNOWLEDGE_BASE["machine learning"]


    if "database module" in question:
        return KNOWLEDGE_BASE["database"]


    if "prediction module" in question:
        return KNOWLEDGE_BASE["every module"]


    if "admin module" in question:
        return KNOWLEDGE_BASE["admin dashboard"]


    # --------------------------------------------------------
    # WHY RANDOM FOREST
    # --------------------------------------------------------

    if (
        "why random forest" in question
        or "why use random forest" in question
        or "why did you use random forest" in question
    ):

        return KNOWLEDGE_BASE["why random forest"]


    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    if "random forest" in question:

        return KNOWLEDGE_BASE["random forest"]


    # --------------------------------------------------------
    # MACHINE LEARNING
    # --------------------------------------------------------

    if (
        "machine learning" in question
        or "ml algorithm" in question
        or "machine learning algorithm" in question
    ):

        return KNOWLEDGE_BASE["machine learning"]


    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    if (
        "dataset" in question
        or "csv" in question
        or "data set" in question
    ):

        return KNOWLEDGE_BASE["dataset"]


    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    if (
        "features" in question
        or "input features" in question
        or "columns" in question
    ):

        return KNOWLEDGE_BASE["features"]


    # --------------------------------------------------------
    # TARGET
    # --------------------------------------------------------

    if (
        "target variable" in question
        or "target" in question
    ):

        return """
The target variable in this project is:

waiting_time

The Machine Learning model learns from queue-related input
features and predicts waiting time in minutes.
"""


    # --------------------------------------------------------
    # MAE
    # --------------------------------------------------------

    if (
        "mae" in question
        or "mean absolute error" in question
    ):

        return KNOWLEDGE_BASE["mae"]


    # --------------------------------------------------------
    # R2
    # --------------------------------------------------------

    if (
        "r2" in question
        or "r²" in question
        or "r squared" in question
        or "r-squared" in question
    ):

        return KNOWLEDGE_BASE["r2"]


    # --------------------------------------------------------
    # FLASK
    # --------------------------------------------------------

    if "flask" in question:

        return KNOWLEDGE_BASE["flask"]


    # --------------------------------------------------------
    # SQLITE
    # --------------------------------------------------------

    if (
        "sqlite" in question
        or "database" in question
    ):

        return KNOWLEDGE_BASE["database"]


    # --------------------------------------------------------
    # API
    # --------------------------------------------------------

    if (
        "api" in question
        or "endpoint" in question
    ):

        return KNOWLEDGE_BASE["api"]


    # --------------------------------------------------------
    # ARCHITECTURE
    # --------------------------------------------------------

    if (
        "architecture" in question
        or "system architecture" in question
    ):

        return KNOWLEDGE_BASE["architecture"]


    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    if (
        "workflow" in question
        or "working process" in question
        or "how project works" in question
    ):

        return KNOWLEDGE_BASE["workflow"]


    # --------------------------------------------------------
    # TECHNOLOGIES
    # --------------------------------------------------------

    if (
        "technology" in question
        or "technologies" in question
        or "tech stack" in question
    ):

        return KNOWLEDGE_BASE["technologies"]


    # --------------------------------------------------------
    # VIVA
    # --------------------------------------------------------

    if (
        "viva" in question
        or "interview questions" in question
    ):

        return KNOWLEDGE_BASE["viva"]


    # --------------------------------------------------------
    # FUTURE
    # --------------------------------------------------------

    if (
        "future scope" in question
        or "future" in question
    ):

        return KNOWLEDGE_BASE["future"]


    # --------------------------------------------------------
    # LIMITATIONS
    # --------------------------------------------------------

    if (
        "limitation" in question
        or "limitations" in question
    ):

        return KNOWLEDGE_BASE["limitations"]


    # --------------------------------------------------------
    # ADVANTAGES
    # --------------------------------------------------------

    if (
        "advantage" in question
        or "advantages" in question
    ):

        return KNOWLEDGE_BASE["advantages"]


    # --------------------------------------------------------
    # PROJECT
    # --------------------------------------------------------

    if (
        "what is this project" in question
        or "explain project" in question
        or "about project" in question
    ):

        return KNOWLEDGE_BASE["project"]


    # --------------------------------------------------------
    # ONE MINUTE
    # --------------------------------------------------------

    if (
        "one minute" in question
        or "explain in one minute" in question
    ):

        return KNOWLEDGE_BASE["one minute"]


    # --------------------------------------------------------
    # DEFAULT RESPONSE
    # --------------------------------------------------------

    return """
I am the Smart Queue Project Assistant. 🤖

I can answer questions about:

• Project
• Objective
• Folder Structure
• Modules
• Code Modules
• Machine Learning
• Random Forest
• Dataset
• Features
• Prediction
• Flask
• SQLite
• APIs
• Queue Management
• Architecture
• Workflow
• Admin Dashboard
• User Dashboard
• MAE
• R²
• Advantages
• Limitations
• Future Scope
• Viva Questions

Try asking:

"Explain the folder structure"

or

"Explain every module in the project"
"""


# ============================================================
# CHATBOT API
# ============================================================

@chatbot.route("/ask", methods=["POST"])
def ask():

    data = request.get_json(silent=True)


    if not data:

        return jsonify({
            "success": False,
            "message": "No request data received."
        }), 400


    question = data.get("question", "").strip()


    if not question:

        return jsonify({
            "success": False,
            "message": "Please enter a question."
        }), 400


    answer = get_answer(question)


    return jsonify({
        "success": True,
        "question": question,
        "answer": answer
    })