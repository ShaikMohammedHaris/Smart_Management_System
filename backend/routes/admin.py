from flask import Blueprint, jsonify
from backend.database import get_db_connection

admin = Blueprint("admin", __name__)


@admin.route("/dashboard", methods=["GET"])
def dashboard():

    connection = get_db_connection()

    # Total users
    users = connection.execute("""
        SELECT COUNT(*) AS total
        FROM users
        WHERE role = 'user'
    """).fetchone()

    # Active queues
    queues = connection.execute("""
        SELECT COUNT(*) AS total
        FROM queues
        WHERE status = 'active'
    """).fetchone()

    # People waiting
    waiting = connection.execute("""
        SELECT COUNT(*) AS total
        FROM queue_entries
        WHERE status = 'waiting'
    """).fetchone()

    # Get latest prediction for each queue
    latest_predictions = connection.execute("""
        SELECT p.predicted_waiting_time
        FROM predictions p
        INNER JOIN (
            SELECT queue_id, MAX(id) AS latest_id
            FROM predictions
            GROUP BY queue_id
        ) latest
        ON p.id = latest.latest_id
    """).fetchall()

    connection.close()

    # Calculate average
    if latest_predictions:

        total_prediction = sum(
            row["predicted_waiting_time"]
            for row in latest_predictions
        )

        average = total_prediction / len(latest_predictions)

    else:

        average = 0

    return jsonify({

        "success": True,

        "dashboard": {

            "total_users": users["total"],

            "active_queues": queues["total"],

            "people_waiting": waiting["total"],

            "average_predicted_waiting_time": round(
                average,
                2
            )
        }
    })