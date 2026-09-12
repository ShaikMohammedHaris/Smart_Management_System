from flask import Blueprint, request, jsonify
from datetime import datetime

from backend.ml.predict import predict_waiting_time
from backend.database import get_db_connection


prediction = Blueprint(
    "prediction",
    __name__
)


@prediction.route(
    "/predict",
    methods=["POST"]
)
def predict():

    data = request.get_json()

    try:

        queue_id = int(
            data.get("queue_id")
        )

        queue_length = int(
            data.get("queue_length")
        )

        active_counters = int(
            data.get("active_counters")
        )

        avg_service_time = float(
            data.get("avg_service_time")
        )

        arrival_rate = float(
            data.get("arrival_rate", 1)
        )

        now = datetime.now()

        hour = now.hour

        day_of_week = now.weekday()

        waiting_time = predict_waiting_time(
            queue_length,
            active_counters,
            avg_service_time,
            hour,
            day_of_week,
            arrival_rate
        )

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO predictions
            (
                queue_id,
                queue_length,
                active_counters,
                average_service_time,
                predicted_waiting_time
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            queue_id,
            queue_length,
            active_counters,
            avg_service_time,
            waiting_time
        ))

        connection.commit()

        connection.close()

        return jsonify({
            "success": True,
            "predicted_waiting_time":
                waiting_time,
            "unit": "minutes"
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500