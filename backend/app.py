from flask import Flask, jsonify
from flask_cors import CORS

from backend.database import initialize_database

from backend.routes.auth import auth
from backend.routes.queue import queue
from backend.routes.prediction import prediction
from backend.routes.admin import admin
from backend.chatbot import chatbot


# Create Flask application
app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)


# Initialize SQLite database
initialize_database()


# Register API routes
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

app.register_blueprint(
    chatbot,
    url_prefix="/api/chatbot"
)


# Home API
@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Smart Queue Management System API is running"
    })


# Health check
@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "status": "OK",
        "message": "Server is working"
    })


# Start Flask server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )