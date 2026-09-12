from flask import Blueprint, request, jsonify
from backend.database import get_db_connection

queue = Blueprint("queue", __name__)


# ==========================================
# CREATE QUEUE
# ==========================================
@queue.route("/create", methods=["POST"])
def create_queue():

    data = request.get_json()

    queue_name = data.get("queue_name")
    service_type = data.get("service_type")
    active_counters = data.get("active_counters", 1)
    average_service_time = data.get("average_service_time", 5)

    if not queue_name or not service_type:
        return jsonify({
            "success": False,
            "message": "Queue name and service type are required"
        }), 400

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO queues
        (
            queue_name,
            service_type,
            active_counters,
            average_service_time
        )
        VALUES (?, ?, ?, ?)
    """, (
        queue_name,
        service_type,
        active_counters,
        average_service_time
    ))

    connection.commit()

    queue_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "success": True,
        "queue_id": queue_id,
        "message": "Queue created successfully"
    })


# ==========================================
# LIST QUEUES
# ==========================================
@queue.route("/list", methods=["GET"])
def list_queues():

    connection = get_db_connection()

    queues = connection.execute("""
        SELECT *
        FROM queues
        WHERE status = 'active'
        ORDER BY id
    """).fetchall()

    connection.close()

    result = []

    for q in queues:

        result.append({
            "id": q["id"],
            "name": q["queue_name"],
            "service_type": q["service_type"],
            "active_counters": q["active_counters"],
            "average_service_time": q["average_service_time"]
        })

    return jsonify({
        "success": True,
        "queues": result
    })


# ==========================================
# GET QUEUE DETAILS
# ==========================================
@queue.route("/details/<int:queue_id>", methods=["GET"])
def queue_details(queue_id):

    connection = get_db_connection()

    queue_info = connection.execute("""
        SELECT *
        FROM queues
        WHERE id = ?
        AND status = 'active'
    """, (queue_id,)).fetchone()

    if not queue_info:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Queue not found"
        }), 404

    waiting = connection.execute("""
        SELECT COUNT(*) AS total
        FROM queue_entries
        WHERE queue_id = ?
        AND status = 'waiting'
    """, (queue_id,)).fetchone()

    connection.close()

    return jsonify({
        "success": True,
        "queue": {
            "id": queue_info["id"],
            "name": queue_info["queue_name"],
            "service_type": queue_info["service_type"],
            "active_counters": queue_info["active_counters"],
            "average_service_time": queue_info["average_service_time"],
            "people_waiting": waiting["total"]
        }
    })


# ==========================================
# UPDATE QUEUE
# ==========================================
@queue.route("/update/<int:queue_id>", methods=["PUT"])
def update_queue(queue_id):

    data = request.get_json()

    queue_name = data.get("queue_name")
    service_type = data.get("service_type")
    active_counters = data.get("active_counters")
    average_service_time = data.get("average_service_time")

    if not queue_name or not service_type:
        return jsonify({
            "success": False,
            "message": "Queue name and service type are required"
        }), 400

    try:

        active_counters = int(active_counters)
        average_service_time = float(average_service_time)

        if active_counters <= 0:
            return jsonify({
                "success": False,
                "message": "Active counters must be greater than 0"
            }), 400

        if average_service_time <= 0:
            return jsonify({
                "success": False,
                "message": "Average service time must be greater than 0"
            }), 400

    except (TypeError, ValueError):

        return jsonify({
            "success": False,
            "message": "Invalid numeric values"
        }), 400

    connection = get_db_connection()

    existing = connection.execute("""
        SELECT *
        FROM queues
        WHERE id = ?
    """, (queue_id,)).fetchone()

    if not existing:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Queue not found"
        }), 404

    connection.execute("""
        UPDATE queues
        SET
            queue_name = ?,
            service_type = ?,
            active_counters = ?,
            average_service_time = ?
        WHERE id = ?
    """, (
        queue_name,
        service_type,
        active_counters,
        average_service_time,
        queue_id
    ))

    connection.commit()

    connection.close()

    return jsonify({
        "success": True,
        "message": "Queue updated successfully"
    })


# ==========================================
# JOIN QUEUE
# ==========================================
@queue.route("/join", methods=["POST"])
def join_queue():

    data = request.get_json()

    queue_id = data.get("queue_id")
    user_id = data.get("user_id")

    connection = get_db_connection()

    queue_exists = connection.execute("""
        SELECT id
        FROM queues
        WHERE id = ?
        AND status = 'active'
    """, (queue_id,)).fetchone()

    if not queue_exists:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Queue not found"
        }), 404

    result = connection.execute("""
        SELECT MAX(token_number) AS last_token
        FROM queue_entries
        WHERE queue_id = ?
    """, (queue_id,)).fetchone()

    last_token = result["last_token"]

    token_number = 1 if last_token is None else last_token + 1

    connection.execute("""
        INSERT INTO queue_entries
        (
            queue_id,
            user_id,
            token_number
        )
        VALUES (?, ?, ?)
    """, (
        queue_id,
        user_id,
        token_number
    ))

    connection.commit()

    connection.close()

    return jsonify({
        "success": True,
        "token_number": token_number,
        "message": "Successfully joined queue"
    })


# ==========================================
# QUEUE STATUS
# ==========================================
@queue.route("/status/<int:queue_id>", methods=["GET"])
def queue_status(queue_id):

    connection = get_db_connection()

    queue_info = connection.execute("""
        SELECT *
        FROM queues
        WHERE id = ?
    """, (queue_id,)).fetchone()

    waiting = connection.execute("""
        SELECT COUNT(*) AS total
        FROM queue_entries
        WHERE queue_id = ?
        AND status = 'waiting'
    """, (queue_id,)).fetchone()

    connection.close()

    if not queue_info:

        return jsonify({
            "success": False,
            "message": "Queue not found"
        }), 404

    return jsonify({
        "success": True,
        "queue": {
            "id": queue_info["id"],
            "name": queue_info["queue_name"],
            "service_type": queue_info["service_type"],
            "active_counters": queue_info["active_counters"],
            "average_service_time": queue_info["average_service_time"],
            "people_waiting": waiting["total"]
        }
    })


# ==========================================
# SERVE NEXT CUSTOMER
# ==========================================
@queue.route("/next/<int:queue_id>", methods=["POST"])
def serve_next(queue_id):

    connection = get_db_connection()

    person = connection.execute("""
        SELECT *
        FROM queue_entries
        WHERE queue_id = ?
        AND status = 'waiting'
        ORDER BY token_number
        LIMIT 1
    """, (queue_id,)).fetchone()

    if not person:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Queue is empty"
        })

    connection.execute("""
        UPDATE queue_entries
        SET status = 'served'
        WHERE id = ?
    """, (person["id"],))

    connection.commit()

    connection.close()

    return jsonify({
        "success": True,
        "served_token": person["token_number"],
        "message": "Next customer served"
    })