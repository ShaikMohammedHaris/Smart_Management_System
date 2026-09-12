from flask import Flask, jsonify
from flask_cors import CORS

from backend.database import initialize_database

from backend.routes.auth import auth
from backend.routes.queue import queue
from backend.routes.prediction import prediction
from backend.routes.admin import admin

# CHATBOT
from backend.chatbot import chatbot


app = Flask(__name__)

CORS(app)


# Initialize database
initialize_database()


# ============================================================
# REGISTER ROUTES
# ============================================================

app.register_blueprint(
    auth,
    url_prefix="/api/auth"
)

app.register_blueprint(
    queue,
    url_prefix="/api/queue"
)

app.register_blueprint(
    prediction,
    url_prefix="/api/prediction"
)

app.register_blueprint(
    admin,
    url_prefix="/api/admin"
)

# CHATBOT
app.register_blueprint(
    chatbot,
    url_prefix="/api/chatbot"
)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "message":
        "Smart Queue Management System API is running"
    })


# ============================================================
# HEALTH
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "OK",
        "message": "Server is working"
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )