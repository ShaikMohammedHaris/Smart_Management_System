from flask import Blueprint, request, jsonify

from backend.database import get_db_connection


# ============================================================
# BLUEPRINT
# ============================================================

queue = Blueprint(
    "queue",
    __name__
)


# ============================================================
# CREATE QUEUE
# ============================================================

@queue.route("/create", methods=["POST"])
def create_queue():

    data = request.get_json() or {}


    queue_name = data.get("queue_name")

    service_type = data.get("service_type")

    active_counters = data.get(
        "active_counters",
        1
    )

    average_service_time = data.get(
        "average_service_time",
        5
    )

    people_waiting = data.get(
        "people_waiting",
        0
    )


    if not queue_name:

        return jsonify({
            "success": False,
            "message": "Queue name is required"
        }), 400


    if not service_type:

        return jsonify({
            "success": False,
            "message": "Service type is required"
        }), 400


    try:

        active_counters = int(
            active_counters
        )

        average_service_time = float(
            average_service_time
        )

        people_waiting = int(
            people_waiting
        )


        if active_counters < 1:

            return jsonify({
                "success": False,
                "message": "Active counters must be at least 1"
            }), 400


        if average_service_time < 0:

            return jsonify({
                "success": False,
                "message": "Average service time cannot be negative"
            }), 400


        if people_waiting < 0:

            return jsonify({
                "success": False,
                "message": "People waiting cannot be negative"
            }), 400


    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "message": "Invalid numeric values"
        }), 400


    connection = get_db_connection()


    cursor = connection.execute("""
        INSERT INTO queues
        (
            queue_name,
            service_type,
            active_counters,
            average_service_time,
            people_waiting
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        queue_name,
        service_type,
        active_counters,
        average_service_time,
        people_waiting
    ))


    connection.commit()

    queue_id = cursor.lastrowid

    connection.close()


    return jsonify({

        "success": True,

        "message": "Queue created successfully",

        "queue_id": queue_id

    })


# ============================================================
# LIST QUEUES
# ============================================================

@queue.route("/list", methods=["GET"])
def list_queues():

    connection = get_db_connection()


    queues = connection.execute("""
        SELECT
            id,
            queue_name,
            service_type,
            active_counters,
            average_service_time,
            people_waiting,
            status
        FROM queues
        WHERE status = 'active'
        ORDER BY id
    """).fetchall()


    connection.close()


    queue_list = []


    for q in queues:

        queue_list.append({

            "id": q["id"],

            "name": q["queue_name"],

            "service_type": q["service_type"],

            "active_counters": q["active_counters"],

            "average_service_time":
                q["average_service_time"],

            "people_waiting":
                q["people_waiting"],

            "status":
                q["status"]

        })


    return jsonify({

        "success": True,

        "queues": queue_list

    })


# ============================================================
# GET QUEUE DETAILS
# ============================================================

@queue.route("/details/<int:queue_id>", methods=["GET"])
def queue_details(queue_id):

    connection = get_db_connection()


    q = connection.execute("""
        SELECT
            id,
            queue_name,
            service_type,
            active_counters,
            average_service_time,
            people_waiting,
            status
        FROM queues
        WHERE id = ?
    """, (
        queue_id,
    )).fetchone()


    connection.close()


    if not q:

        return jsonify({
            "success": False,
            "message": "Queue not found"
        }), 404


    return jsonify({

        "success": True,

        "queue": {

            "id": q["id"],

            "name": q["queue_name"],

            "service_type": q["service_type"],

            "active_counters":
                q["active_counters"],

            "average_service_time":
                q["average_service_time"],

            "people_waiting":
                q["people_waiting"],

            "status":
                q["status"]

        }

    })


# ============================================================
# UPDATE QUEUE
# ============================================================

@queue.route("/update/<int:queue_id>", methods=["PUT"])
def update_queue(queue_id):

    data = request.get_json() or {}


    queue_name = data.get(
        "queue_name"
    )

    service_type = data.get(
        "service_type"
    )

    active_counters = data.get(
        "active_counters"
    )

    average_service_time = data.get(
        "average_service_time"
    )

    people_waiting = data.get(
        "people_waiting"
    )


    # --------------------------------------------------------
    # CHECK REQUIRED VALUES
    # --------------------------------------------------------

    if not queue_name:

        return jsonify({
            "success": False,
            "message": "Queue name is required"
        }), 400


    if not service_type:

        return jsonify({
            "success": False,
            "message": "Service type is required"
        }), 400


    if active_counters is None:

        return jsonify({
            "success": False,
            "message": "Active counters is required"
        }), 400


    if average_service_time is None:

        return jsonify({
            "success": False,
            "message": "Average service time is required"
        }), 400


    if people_waiting is None:

        return jsonify({
            "success": False,
            "message": "People waiting is required"
        }), 400


    # --------------------------------------------------------
    # CONVERT VALUES
    # --------------------------------------------------------

    try:

        active_counters = int(
            active_counters
        )

        average_service_time = float(
            average_service_time
        )

        people_waiting = int(
            people_waiting
        )


    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "message": "Invalid numeric values"
        }), 400


    # --------------------------------------------------------
    # VALIDATE VALUES
    # --------------------------------------------------------

    if active_counters < 1:

        return jsonify({
            "success": False,
            "message": "Active counters must be at least 1"
        }), 400


    if average_service_time < 0:

        return jsonify({
            "success": False,
            "message": "Average service time cannot be negative"
        }), 400


    if people_waiting < 0:

        return jsonify({
            "success": False,
            "message": "People waiting cannot be negative"
        }), 400


    # --------------------------------------------------------
    # UPDATE DATABASE
    # --------------------------------------------------------

    connection = get_db_connection()


    existing = connection.execute("""
        SELECT id
        FROM queues
        WHERE id = ?
    """, (
        queue_id,
    )).fetchone()


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
            average_service_time = ?,
            people_waiting = ?
        WHERE id = ?
    """, (
        queue_name,
        service_type,
        active_counters,
        average_service_time,
        people_waiting,
        queue_id
    ))


    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message": "Queue updated successfully",

        "queue": {

            "id": queue_id,

            "name": queue_name,

            "service_type": service_type,

            "active_counters":
                active_counters,

            "average_service_time":
                average_service_time,

            "people_waiting":
                people_waiting

        }

    })


# ============================================================
# JOIN QUEUE
# ============================================================

@queue.route("/join", methods=["POST"])
def join_queue():

    data = request.get_json() or {}


    queue_id = data.get("queue_id")

    user_id = data.get("user_id")


    if queue_id is None:

        return jsonify({
            "success": False,
            "message": "Queue ID is required"
        }), 400


    if user_id is None:

        return jsonify({
            "success": False,
            "message": "User ID is required"
        }), 400


    try:

        queue_id = int(queue_id)

        user_id = int(user_id)

    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "message": "Invalid queue ID or user ID"
        }), 400


    connection = get_db_connection()


    q = connection.execute("""
        SELECT *
        FROM queues
        WHERE id = ?
        AND status = 'active'
    """, (
        queue_id,
    )).fetchone()


    if not q:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Queue not found"
        }), 404


    # --------------------------------------------------------
    # Generate next token
    # --------------------------------------------------------

    last_token = connection.execute("""
        SELECT MAX(token_number) AS last_token
        FROM queue_entries
        WHERE queue_id = ?
    """, (
        queue_id,
    )).fetchone()


    if last_token["last_token"] is None:

        token_number = 1

    else:

        token_number = (
            last_token["last_token"] + 1
        )


    # --------------------------------------------------------
    # Add customer
    # --------------------------------------------------------

    connection.execute("""
        INSERT INTO queue_entries
        (
            queue_id,
            user_id,
            token_number,
            status
        )
        VALUES (?, ?, ?, 'waiting')
    """, (
        queue_id,
        user_id,
        token_number
    ))


    # --------------------------------------------------------
    # Increase people waiting
    #
    # This keeps manual value and real joins synchronized.
    # Admin can later change it manually.
    # --------------------------------------------------------

    connection.execute("""
        UPDATE queues
        SET people_waiting =
            people_waiting + 1
        WHERE id = ?
    """, (
        queue_id,
    ))


    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message": "Successfully joined queue",

        "queue_id": queue_id,

        "token_number": token_number

    })


# ============================================================
# QUEUE STATUS
# ============================================================

@queue.route("/status/<int:queue_id>", methods=["GET"])
def queue_status(queue_id):

    connection = get_db_connection()


    q = connection.execute("""
        SELECT
            id,
            queue_name,
            service_type,
            active_counters,
            average_service_time,
            people_waiting,
            status
        FROM queues
        WHERE id = ?
    """, (
        queue_id,
    )).fetchone()


    if not q:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Queue not found"
        }), 404


    waiting_entries = connection.execute("""
        SELECT
            token_number,
            user_id,
            joined_at,
            status
        FROM queue_entries
        WHERE queue_id = ?
        AND status = 'waiting'
        ORDER BY id
    """, (
        queue_id,
    )).fetchall()


    connection.close()


    entries = []


    for entry in waiting_entries:

        entries.append({

            "token_number":
                entry["token_number"],

            "user_id":
                entry["user_id"],

            "joined_at":
                entry["joined_at"],

            "status":
                entry["status"]

        })


    return jsonify({

        "success": True,

        "queue": {

            "id": q["id"],

            "name": q["queue_name"],

            "service_type":
                q["service_type"],

            "active_counters":
                q["active_counters"],

            "average_service_time":
                q["average_service_time"],

            "people_waiting":
                q["people_waiting"],

            "status":
                q["status"]

        },

        "waiting_entries":
            entries

    })


# ============================================================
# SERVE NEXT CUSTOMER
# ============================================================

@queue.route("/next/<int:queue_id>", methods=["POST"])
def serve_next(queue_id):

    connection = get_db_connection()


    entry = connection.execute("""
        SELECT *
        FROM queue_entries
        WHERE queue_id = ?
        AND status = 'waiting'
        ORDER BY id
        LIMIT 1
    """, (
        queue_id,
    )).fetchone()


    if not entry:

        connection.close()

        return jsonify({
            "success": False,
            "message": "No customers are waiting"
        }), 404


    # --------------------------------------------------------
    # Mark token as served
    # --------------------------------------------------------

    connection.execute("""
        UPDATE queue_entries
        SET status = 'served'
        WHERE id = ?
    """, (
        entry["id"],
    ))


    # --------------------------------------------------------
    # Decrease people waiting
    # --------------------------------------------------------

    connection.execute("""
        UPDATE queues
        SET people_waiting =
            CASE
                WHEN people_waiting > 0
                THEN people_waiting - 1
                ELSE 0
            END
        WHERE id = ?
    """, (
        queue_id,
    ))


    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message":
            "Customer served successfully",

        "served_token":
            entry["token_number"]

    })