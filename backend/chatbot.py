from flask import Blueprint, request, jsonify

chatbot = Blueprint("chatbot", __name__)


def get_answer(question):

    question = question.lower().strip()

    # =========================================================
    # 1. PROJECT
    # =========================================================

    if (
        "what is this project" in question
        or "about this project" in question
        or "explain the project" in question
    ):
        return """
The project is a Smart Queue Management and Waiting Time
Prediction System.

It is a web-based application that manages customer queues
and predicts approximate waiting time using Machine Learning.

Technologies used:

• Python
• Flask
• HTML
• CSS
• JavaScript
• SQLite
• Scikit-learn
• Random Forest Regressor

Users can join queues and receive tokens.

Administrators can manage queues and counters.

The Machine Learning model predicts waiting time using
queue-related information.
"""

    # =========================================================
    # 2. OBJECTIVE
    # =========================================================

    elif (
        "objective" in question
        or "purpose" in question
        or "aim of the project" in question
        or "goal of the project" in question
    ):
        return """
The main objective of this project is to manage customer
queues and predict their approximate waiting time.

Main objectives:

• Manage queues efficiently.
• Generate tokens for customers.
• Allow users to join queues.
• Allow administrators to manage queues.
• Predict waiting time using Machine Learning.
• Store queue information in SQLite.
• Provide a simple web-based interface.
"""

    # =========================================================
    # 3. FOLDER STRUCTURE
    # =========================================================

    elif (
        "folder structure" in question
        or "folderstructure" in question
        or ("folder" in question and "structure" in question)
        or "explain folders" in question
        or "project folders" in question
        or "folderstreure" in question
        or "folder struture" in question
        or "folder stucture" in question
    ):
        return """
SMART QUEUE PROJECT FOLDER STRUCTURE

smart_queue_predictor/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── chatbot.py
│   │
│   ├── models/
│   │   └── prediction_model.pkl
│   │
│   ├── ml/
│   │   ├── train_model.py
│   │   └── predict.py
│   │
│   └── routes/
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
└── README.md

The backend contains the Python Flask application, APIs,
database, Machine Learning code and chatbot.

The frontend contains HTML, CSS and JavaScript.

The dataset folder contains the Machine Learning dataset.

The models folder contains the trained prediction model.
"""

    # =========================================================
    # 4. MODULES
    # =========================================================

    elif (
        "all modules" in question
        or "every module" in question
        or "what modules" in question
        or "modules used" in question
        or "explain modules" in question
        or "modules in the project" in question
    ):
        return """
The main modules of the project are:

1. Authentication Module
   File: backend/routes/auth.py

   Handles registration and login.

2. Queue Management Module
   File: backend/routes/queue.py

   Handles queue creation, joining queues, queue status
   and serving customers.

3. Machine Learning Module
   Files:
   backend/ml/train_model.py
   backend/ml/predict.py

   Trains the Random Forest model and generates predictions.

4. Database Module
   File: backend/database.py

   Handles the SQLite database.

5. Prediction Module
   File: backend/routes/prediction.py

   Provides the waiting-time prediction API.

6. Admin Module
   File: backend/routes/admin.py

   Provides administrator dashboard information.

7. Chatbot Module
   File: backend/chatbot.py

   Answers questions about the project.

8. Frontend Module
   Contains HTML, CSS and JavaScript files.

9. Dataset Module
   File: dataset/queue_data.csv

   Contains data used for Machine Learning.
"""

    # =========================================================
    # 5. CODE OF EVERY MODULE
    # =========================================================

    elif (
        "code in every module" in question
        or "explain every module code" in question
        or "explain code of every module" in question
        or "how every module works" in question
    ):
        return """
MAIN MODULE CODE EXPLANATION

app.py:
Creates the Flask application and registers all API routes.

database.py:
Creates the SQLite database and its tables.

auth.py:
Handles user registration and login.

queue.py:
Handles queue creation, queue joining, queue status,
queue updates and serving the next customer.

train_model.py:
Loads the CSV dataset, selects features, trains the
Random Forest Regressor and saves the trained model.

predict.py:
Loads prediction_model.pkl and generates predictions.

prediction.py:
Receives prediction requests from the frontend and
calls the Machine Learning prediction function.

admin.py:
Provides administrator dashboard statistics.

chatbot.py:
Receives questions and returns relevant project
explanations.

dashboard.js:
Handles user dashboard operations and prediction requests.

admin.js:
Handles administrator queue management and dashboard operations.

chatbot.js:
Sends questions to the chatbot API and displays responses.
"""

    # =========================================================
    # 6. HOW WAITING TIME IS PREDICTED
    # =========================================================

    elif (
        "prediction logic" in question
        or "waiting time logic" in question
        or "logic used for prediction" in question
        or "how prediction works" in question
        or "how does prediction work" in question
        or "how is waiting time predicted" in question
        or "how does the system predict waiting time" in question
        or "what logic is performed to predict waiting time" in question
        or (
            "logic" in question
            and "waiting" in question
        )
    ):
        return """
WAITING TIME PREDICTION LOGIC

The system uses Random Forest Regressor to predict
waiting time.

The model uses six input features:

1. Queue Length
2. Active Counters
3. Average Service Time
4. Hour
5. Day of the Week
6. Arrival Rate

The target variable is:

Waiting Time

TRAINING:

queue_data.csv
       ↓
Input Features
       ↓
Training and Testing Data
       ↓
Random Forest Regressor
       ↓
Model Training
       ↓
prediction_model.pkl

PREDICTION:

Current Queue Information
       ↓
Flask Prediction API
       ↓
predict.py
       ↓
Random Forest Model
       ↓
Predicted Waiting Time
       ↓
Displayed to User

Random Forest combines predictions from multiple
decision trees to produce the final numerical
waiting-time prediction.
"""

    # =========================================================
    # 7. RANDOM FOREST
    # =========================================================

    elif (
        "random forest" in question
        or "explain random forest" in question
        or "what is random forest" in question
        or "why random forest" in question
    ):
        return """
Random Forest Regressor is the Machine Learning
algorithm used in this project.

It is an ensemble algorithm that uses multiple
decision trees.

For this project, the model receives:

• Queue length
• Active counters
• Average service time
• Hour
• Day of the week
• Arrival rate

The model produces:

• Predicted waiting time

Multiple decision trees generate predictions and
the Random Forest combines them to produce the
final regression prediction.
"""

    # =========================================================
    # 8. WHY RANDOM FOREST
    # =========================================================

    elif (
        "why did you choose random forest" in question
        or "why choose random forest" in question
        or "reason for random forest" in question
    ):
        return """
Random Forest was selected because it is suitable for
regression problems and can learn relationships between
multiple queue-related features and waiting time.

It can model non-linear relationships and combines
multiple decision trees to produce a regression prediction.

In this project it is used to learn from historical
queue data and predict waiting time.
"""

    # =========================================================
    # 9. INPUT FEATURES
    # =========================================================

    elif (
        "input features" in question
        or "features used" in question
        or "what are the input features" in question
    ):
        return """
The Machine Learning model uses six input features:

1. queue_length
2. active_counters
3. avg_service_time
4. hour
5. day_of_week
6. arrival_rate

These features describe the current queue conditions
and are used by the Random Forest model to predict
waiting_time.
"""

    # =========================================================
    # 10. TARGET VARIABLE
    # =========================================================

    elif (
        "target variable" in question
        or "what is target" in question
        or "target of the model" in question
    ):
        return """
The target variable is:

waiting_time

It represents the actual waiting time in minutes.

The Machine Learning model learns the relationship
between the input features and this target variable.
"""

    # =========================================================
    # 11. DATASET
    # =========================================================

    elif (
        "dataset" in question
        or "csv" in question
        or "dataset columns" in question
        or "data columns" in question
    ):
        return """
The Machine Learning dataset is:

dataset/queue_data.csv

Columns:

• queue_length
• active_counters
• avg_service_time
• hour
• day_of_week
• arrival_rate
• waiting_time

The first six columns are input features.

waiting_time is the target variable.
"""

    # =========================================================
    # 12. DATASET PREPARATION
    # =========================================================

    elif (
        "how dataset is prepared" in question
        or "dataset preparation" in question
        or "prepare the dataset" in question
        or "data preprocessing" in question
    ):
        return """
The dataset preparation process is:

1. Load queue_data.csv using pandas.
2. Read the queue-related columns.
3. Separate input features from the target variable.
4. Use the first six columns as input features.
5. Use waiting_time as the target.
6. Split the data into training and testing data.
7. Use the training data to train Random Forest.
8. Use the testing data to evaluate the model.
"""

    # =========================================================
    # 13. MODEL TRAINING
    # =========================================================

    elif (
        "how model is trained" in question
        or "model training" in question
        or "training process" in question
        or "train model" in question
    ):
        return """
MODEL TRAINING PROCESS

1. Load queue_data.csv.
2. Select the six input features.
3. Select waiting_time as the target.
4. Split data into training and testing sets.
5. Create RandomForestRegressor.
6. Train the model.
7. Generate predictions using test data.
8. Calculate MAE and R² Score.
9. Save the trained model using joblib.

The saved model is:

backend/models/prediction_model.pkl
"""

    # =========================================================
    # 14. MODEL EVALUATION
    # =========================================================

    elif (
        "mae" in question
        or "mean absolute error" in question
        or "r2 score" in question
        or "model evaluation" in question
        or "evaluate the model" in question
    ):
        return """
The model is evaluated using:

1. MAE - Mean Absolute Error

MAE measures the average absolute difference between
actual waiting times and predicted waiting times.

Lower MAE means smaller average prediction errors.

2. R² Score

R² indicates how well the model explains the variation
in the target values.

The values are calculated during model training using
the test dataset.
"""

    # =========================================================
    # 15. FLASK
    # =========================================================

    elif (
        "what is flask" in question
        or "flask" in question
        or "why flask" in question
    ):
        return """
Flask is a lightweight Python web framework.

In this project Flask is used to create the backend
and REST API endpoints.

The frontend sends requests to Flask.

Flask processes the request and returns JSON responses.

Main API groups include:

/api/auth
/api/queue
/api/prediction
/api/admin
/api/chatbot
"""

    # =========================================================
    # 16. SQLITE
    # =========================================================

    elif (
        "what database" in question
        or "database used" in question
        or "sqlite" in question
        or "why sqlite" in question
    ):
        return """
The project uses SQLite as its database.

Database file:

backend/database/queue.db

Important tables:

• users
• queues
• queue_entries
• predictions

SQLite is lightweight and does not require a separate
database server, making it suitable for this project.
"""

    # =========================================================
    # 17. API
    # =========================================================

    elif (
        "what is api" in question
        or "api" in question
        or "rest api" in question
        or "explain api" in question
    ):
        return """
API stands for Application Programming Interface.

In this project, Flask provides REST API endpoints.

Examples:

POST /api/auth/register
POST /api/auth/login

POST /api/queue/create
GET /api/queue/list
POST /api/queue/join

POST /api/prediction/predict

GET /api/admin/dashboard

POST /api/chatbot/ask

JavaScript fetch() is used by the frontend to
communicate with these APIs.
"""

    # =========================================================
    # 18. DATABASE TABLES
    # =========================================================

    elif (
        "database tables" in question
        or "tables in database" in question
        or "what tables" in question
    ):
        return """
The SQLite database contains four main tables:

1. users
   Stores user information and roles.

2. queues
   Stores queue information such as queue name,
   service type, active counters and service time.

3. queue_entries
   Stores customers who join queues and their tokens.

4. predictions
   Stores Machine Learning prediction information.
"""

    # =========================================================
    # 19. PREDICTION MODEL FILE
    # =========================================================

    elif (
        "prediction_model.pkl" in question
        or "pkl file" in question
        or "trained model file" in question
    ):
        return """
prediction_model.pkl is the saved trained Machine
Learning model.

Location:

backend/models/prediction_model.pkl

It is created by train_model.py using joblib.

predict.py loads this file and uses it to generate
waiting-time predictions.
"""

    # =========================================================
    # 20. QUEUE MANAGEMENT
    # =========================================================

    elif (
        "queue management" in question
        or "how queue works" in question
        or "manage queue" in question
    ):
        return """
QUEUE MANAGEMENT PROCESS

1. Administrator creates a queue.
2. Queue information is stored in SQLite.
3. User selects a queue.
4. User joins the queue.
5. A token number is generated.
6. The queue entry is stored in the database.
7. Administrator serves the next customer.
8. Queue information is updated.
9. A new waiting-time prediction can be generated.
"""

    # =========================================================
    # 21. TOKEN
    # =========================================================

    elif (
        "how token is generated" in question
        or "token generation" in question
        or "what is token" in question
    ):
        return """
A token identifies a customer's position in a queue.

When a user joins a queue:

1. The selected queue is identified.
2. The system checks existing queue entries.
3. A token number is assigned.
4. The token is stored in queue_entries.
5. The token is displayed to the user.
"""

    # =========================================================
    # 22. WORKFLOW
    # =========================================================

    elif (
        "workflow" in question
        or "project flow" in question
        or "how system works" in question
        or "working of the project" in question
    ):
        return """
PROJECT WORKFLOW

Administrator
      ↓
Creates Queue
      ↓
Queue stored in SQLite
      ↓
User selects Queue
      ↓
User joins Queue
      ↓
Token generated
      ↓
Queue information updated
      ↓
Prediction requested
      ↓
Random Forest Model
      ↓
Waiting Time Prediction
      ↓
Prediction displayed
      ↓
Administrator serves next customer
"""

    # =========================================================
    # 23. TECHNOLOGIES
    # =========================================================

    elif (
        "technologies used" in question
        or "technology used" in question
        or "tech stack" in question
        or "what technologies" in question
    ):
        return """
TECHNOLOGIES USED

Frontend:
• HTML
• CSS
• JavaScript

Backend:
• Python
• Flask
• Flask-CORS

Database:
• SQLite

Machine Learning:
• Scikit-learn
• Random Forest Regressor
• Pandas
• NumPy
• Joblib
"""

    # =========================================================
    # 24. ADVANTAGES
    # =========================================================

    elif (
        "advantages" in question
        or "benefits" in question
        or "advantages of project" in question
    ):
        return """
Advantages of the system:

• Reduces uncertainty about waiting time.
• Provides automated queue management.
• Generates customer tokens.
• Provides Machine Learning based predictions.
• Allows administrators to update queue information.
• Stores information in a database.
• Provides a web-based interface.
• Provides a project-specific chatbot.
"""

    # =========================================================
    # 25. LIMITATIONS
    # =========================================================

    elif (
        "limitations" in question
        or "limitations of project" in question
        or "disadvantages" in question
    ):
        return """
Current limitations include:

• Prediction quality depends on the training dataset.
• A small dataset may not represent every real-world queue.
• Sudden changes in customer arrivals can affect predictions.
• The current prototype uses a simple authentication system.
• Internet or server availability is required for the web application.
"""

    # =========================================================
    # 26. FUTURE SCOPE
    # =========================================================

    elif (
        "future scope" in question
        or "future enhancement" in question
        or "future improvements" in question
        or "future" in question
    ):
        return """
Possible future enhancements include:

• Larger real-world datasets.
• Real-time queue monitoring.
• Mobile application.
• Push notifications.
• Multiple service counters.
• Advanced Machine Learning models.
• Real-time analytics.
• Improved authentication and security.
• Cloud deployment.
• Integration with hospital, bank or government service systems.
"""

    # =========================================================
    # 27. VIVA QUESTIONS
    # =========================================================

    elif (
        "viva questions" in question
        or "give me viva" in question
        or "viva" in question
        or "interview questions" in question
    ):
        return """
IMPORTANT VIVA QUESTIONS

1. What is the objective of the project?
2. Which Machine Learning algorithm is used?
3. Why is Random Forest used?
4. What are the input features?
5. What is the target variable?
6. What dataset is used?
7. How is the model trained?
8. How is waiting time predicted?
9. What is Flask?
10. Why is SQLite used?
11. What is an API?
12. What is MAE?
13. What is R² Score?
14. What is prediction_model.pkl?
15. Explain the system architecture.
16. Explain the folder structure.
17. Explain the database tables.
18. How does a customer join a queue?
19. How is a token generated?
20. What are the limitations of the project?
21. What are the future enhancements?
"""

    # =========================================================
    # 28. DEFAULT RESPONSE
    # =========================================================

    else:
        return """
I can explain different parts of your Smart Queue
Management and Waiting Time Prediction System.

Try asking:

• What is this project?
• What is the objective?
• Explain the folder structure
• Explain every module
• Explain code of every module
• What logic is performed to predict waiting time?
• What are the input features?
• What is the target variable?
• What ML algorithm does this project use?
• Explain Random Forest
• Why did you choose Random Forest?
• What are the dataset columns?
• How is the dataset prepared?
• How is the model trained?
• What is MAE?
• What is R² Score?
• Explain the architecture
• What is Flask?
• What database is used?
• What are the database tables?
• What is an API?
• How is a token generated?
• Explain the workflow
• What are the technologies used?
• What are the advantages?
• What are the limitations?
• What is the future scope?
• Give me viva questions
"""


# =============================================================
# CHATBOT API
# =============================================================

@chatbot.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "No question received"
            }), 400

        question = data.get("question", "").strip()

        if not question:

            return jsonify({
                "success": False,
                "message": "Please enter a question"
            }), 400

        answer = get_answer(question)

        return jsonify({
            "success": True,
            "question": question,
            "answer": answer
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500