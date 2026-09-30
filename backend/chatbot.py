import re
from datetime import datetime

from flask import Blueprint, request, jsonify

from backend.database import get_db_connection
from backend.ml.predict import predict_waiting_time


chatbot = Blueprint("chatbot", __name__)


# ============================================================
# GET THE CURRENT USER'S QUEUE INFORMATION
# ============================================================

def get_user_queue_info(user_id, queue_id=None):

    connection = get_db_connection()

    base_query = """
        SELECT
            qe.id,
            qe.queue_id,
            qe.token_number,
            qe.joined_at,
            qe.status,
            q.queue_name,
            q.service_type,
            q.active_counters,
            q.average_service_time,
            q.people_waiting
        FROM queue_entries qe
        INNER JOIN queues q
            ON qe.queue_id = q.id
        WHERE qe.user_id = ?
    """

    user_entry = None

    # 1) The queue the dashboard says the user is in (waiting entry)
    if queue_id is not None:
        user_entry = connection.execute(
            base_query + """
            AND qe.queue_id = ?
            AND qe.status = 'waiting'
            ORDER BY qe.id DESC
            LIMIT 1
            """, (user_id, queue_id)
        ).fetchone()

    # 2) Otherwise the user's latest *waiting* entry in any queue
    if not user_entry:
        user_entry = connection.execute(
            base_query + """
            AND qe.status = 'waiting'
            ORDER BY qe.id DESC
            LIMIT 1
            """, (user_id,)
        ).fetchone()

    # 3) Otherwise the latest entry of any status (e.g. already served)
    if not user_entry:
        user_entry = connection.execute(
            base_query + """
            ORDER BY qe.id DESC
            LIMIT 1
            """, (user_id,)
        ).fetchone()

    if not user_entry:
        connection.close()
        return None

    queue_id = user_entry["queue_id"]
    entry_id = user_entry["id"]
    token_number = user_entry["token_number"]

    # People ahead = still-waiting entries in THIS queue joined earlier
    people_ahead = connection.execute("""
        SELECT COUNT(*) AS total
        FROM queue_entries
        WHERE queue_id = ?
        AND status = 'waiting'
        AND id < ?
    """, (queue_id, entry_id)).fetchone()["total"]

    if user_entry["status"] != "waiting":
        people_ahead = 0

    latest_prediction = connection.execute("""
        SELECT predicted_waiting_time
        FROM predictions
        WHERE queue_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (queue_id,)).fetchone()

    connection.close()

    # Same number the dashboard shows (queues.people_waiting)
    people_waiting = int(user_entry["people_waiting"] or 0)

    # Compute the estimate live for THIS queue. Relying only on the
    # stored predictions table meant queues that never had a
    # prediction saved (every queue except the first) had no answer.
    predicted_waiting_time = None

    try:
        now = datetime.now()
        predicted_waiting_time = predict_waiting_time(
            people_waiting,
            int(user_entry["active_counters"] or 1),
            float(user_entry["average_service_time"] or 1),
            now.hour,
            now.weekday(),
            1
        )
    except Exception as error:
        print("Chatbot prediction error:", error)
        if latest_prediction:
            predicted_waiting_time = latest_prediction["predicted_waiting_time"]

    return {
        "entry_id": entry_id,
        "queue_id": queue_id,
        "token_number": token_number,
        "status": user_entry["status"],
        "queue_name": user_entry["queue_name"],
        "service_type": user_entry["service_type"],
        "active_counters": user_entry["active_counters"],
        "average_service_time": user_entry["average_service_time"],
        "people_waiting": people_waiting,
        "people_ahead": people_ahead,
        "position": people_ahead + 1,
        "predicted_waiting_time": predicted_waiting_time
    }


# ============================================================
# CHATBOT API
# ============================================================

@chatbot.route("/ask", methods=["POST"])
def ask():

    data = request.get_json() or {}

    question = str(
        data.get("question", "")
    ).strip().lower()

    user_id = data.get("user_id")

    requested_queue_id = data.get("queue_id")

    try:
        requested_queue_id = (
            int(requested_queue_id)
            if requested_queue_id not in (None, "")
            else None
        )
    except (ValueError, TypeError):
        requested_queue_id = None

    # --------------------------------------------------------
    # Check question
    # --------------------------------------------------------

    if not question:

        return jsonify({
            "success": False,
            "message": "Please enter a question."
        }), 400

    # --------------------------------------------------------
    # Check logged-in user
    # --------------------------------------------------------

    if not user_id:

        return jsonify({
            "success": False,
            "message":
                "Please login first to use the Smart Queue Assistant."
        }), 401

    try:

        user_id = int(user_id)

    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "message": "Invalid user information."
        }), 400

    # --------------------------------------------------------
    # Get actual queue information from SQLite
    # --------------------------------------------------------

    try:

        queue_info = get_user_queue_info(
            user_id,
            requested_queue_id
        )

    except Exception as error:

        print("Chatbot database error:", error)

        return jsonify({
            "success": False,
            "message":
                "Unable to retrieve your queue information."
        }), 500

    # ========================================================
    # GREETING
    # ========================================================

    if re.search(
        r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b",
        question
    ):

        return jsonify({
            "success": True,
            "answer":
                "Hello! 👋\n\n"
                "I am your Smart Queue Assistant. 🤖\n\n"
                "I can help you with your token, "
                "queue position, people waiting, "
                "waiting time and queue status."
        })

    # ========================================================
    # HELP
    # ========================================================

    if (
        "help" in question
        or "what can you do" in question
        or "what do you do" in question
        or "options" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                "🤖 I can help you with:\n\n"
                "🎫 What is my token?\n"
                "👥 How many people are waiting?\n"
                "👤 How many people are ahead of me?\n"
                "🔢 What is my position?\n"
                "⏱️ How long do I need to wait?\n"
                "📋 Which queue am I in?\n"
                "🛎️ What service am I waiting for?\n"
                "🏢 How many counters are active?\n"
                "⏳ What is the average service time?\n"
                "📍 What is my queue status?\n"
                "🔔 Is my turn near?\n"
                "🎟️ How do I join a queue?"
        })

    # ========================================================
    # NO QUEUE
    # ========================================================

    if queue_info is None:

        if (
            "join" in question
            or "token" in question
            or "queue" in question
            or "waiting" in question
            or "position" in question
            or "status" in question
        ):

            return jsonify({
                "success": True,
                "answer":
                    "📋 You are not currently waiting "
                    "in any queue.\n\n"
                    "Please join a queue to receive a "
                    "token and view your waiting information."
            })

    # ========================================================
    # TOKEN NUMBER
    # ========================================================

    if (
        "what is my token" in question
        or "my token number" in question
        or "my token" in question
        or "token number" in question
        or "what's my token" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"🎫 Your token number is "
                f"{queue_info['token_number']}."
        })

    # ========================================================
    # PEOPLE WAITING
    # ========================================================

    if (
        "how many people are waiting" in question
        or "how many people waiting" in question
        or "people waiting" in question
        or "customers waiting" in question
        or "how many customers" in question
        or "number of people waiting" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"👥 There are currently "
                f"{queue_info['people_waiting']} "
                f"people waiting in your queue."
        })

    # ========================================================
    # PEOPLE AHEAD
    # ========================================================

    if (
        "people ahead" in question
        or "customers ahead" in question
        or "people before me" in question
        or "customers before me" in question
        or "how many ahead" in question
        or "how many people are ahead" in question
        or "who is ahead" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"👥 There are "
                f"{queue_info['people_ahead']} "
                f"people ahead of you."
        })

    # ========================================================
    # POSITION
    # ========================================================

    if (
        "what is my position" in question
        or "my position" in question
        or "queue position" in question
        or "what position" in question
        or "where am i in the queue" in question
        or "where am i" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"🔢 Your current position is "
                f"{queue_info['position']} "
                f"in the queue."
        })

    # ========================================================
    # WAITING TIME
    # ========================================================

    if (
        "waiting time" in question
        or "wait time" in question
        or "how long do i need to wait" in question
        or "how long will i wait" in question
        or "how long do i have to wait" in question
        or "when will my turn come" in question
        or "when is my turn" in question
        or "time remaining" in question
    ):

        if queue_info["predicted_waiting_time"] is not None:

            waiting_time = float(
                queue_info["predicted_waiting_time"]
            )

            return jsonify({
                "success": True,
                "answer":
                    f"⏱️ Your estimated waiting time "
                    f"is approximately "
                    f"{waiting_time:.2f} minutes."
            })

        # Fallback calculation
        waiting_time = (
            queue_info["people_ahead"]
            * queue_info["average_service_time"]
        ) / max(
            queue_info["active_counters"],
            1
        )

        return jsonify({
            "success": True,
            "answer":
                f"⏱️ Your estimated waiting time "
                f"is approximately "
                f"{waiting_time:.2f} minutes."
        })

    # ========================================================
    # QUEUE NAME
    # ========================================================

    if (
        "which queue" in question
        or "my queue" in question
        or "where is my queue" in question
        or "what queue" in question
        or "queue am i in" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"📋 You are currently in "
                f"'{queue_info['queue_name']}'."
        })

    # ========================================================
    # SERVICE TYPE
    # ========================================================

    if (
        "service type" in question
        or "what service" in question
        or "service am i waiting" in question
        or "which service" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"🛎️ You are waiting for "
                f"'{queue_info['service_type']}'."
        })

    # ========================================================
    # ACTIVE COUNTERS
    # ========================================================

    if (
        "active counters" in question
        or "how many counters" in question
        or "counters active" in question
        or "number of counters" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"🏢 There are currently "
                f"{queue_info['active_counters']} "
                f"active counters serving customers."
        })

    # ========================================================
    # AVERAGE SERVICE TIME
    # ========================================================

    if (
        "average service time" in question
        or "service time" in question
        or "how long does service take" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                f"⏳ The current average service time "
                f"is approximately "
                f"{float(queue_info['average_service_time']):.2f} "
                f"minutes."
        })

    # ========================================================
    # QUEUE STATUS
    # ========================================================

    if (
        "queue status" in question
        or "my status" in question
        or "what is my status" in question
        or "status of my queue" in question
    ):

        status = queue_info["status"]

        if status == "waiting":

            status_text = "Waiting"

        elif status == "served":

            status_text = "Served"

        else:

            status_text = status.capitalize()

        return jsonify({
            "success": True,
            "answer":
                f"📍 Your current queue status is "
                f"'{status_text}'.\n\n"
                f"🎫 Token: "
                f"{queue_info['token_number']}\n"
                f"📋 Queue: "
                f"{queue_info['queue_name']}"
        })

    # ========================================================
    # IS MY TURN NEAR?
    # ========================================================

    if (
        "is my turn near" in question
        or "is my turn close" in question
        or "turn near" in question
        or "turn close" in question
        or "am i next" in question
    ):

        ahead = queue_info["people_ahead"]

        if ahead == 0:

            message = (
                "🔔 You are next in line!"
            )

        elif ahead <= 3:

            message = (
                f"🔔 Your turn is getting close. "
                f"There are only {ahead} "
                f"people ahead of you."
            )

        else:

            message = (
                f"📍 You still have "
                f"{ahead} people ahead of you."
            )

        return jsonify({
            "success": True,
            "answer": message
        })

    # ========================================================
    # HOW TO JOIN
    # ========================================================

    if (
        "how do i join" in question
        or "how to join" in question
        or "join a queue" in question
        or "join queue" in question
        or "get a token" in question
        or "how can i join" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                "🎟️ To join a queue:\n\n"
                "1. Select the queue you need.\n"
                "2. Click the 'Join Queue' button.\n"
                "3. Your token number will be generated.\n"
                "4. You can then monitor your queue "
                "position and waiting time."
        })

    # ========================================================
    # WHAT HAPPENS AFTER JOINING
    # ========================================================

    if (
        "what happens after joining" in question
        or "after joining" in question
        or "what happens when i join" in question
    ):

        return jsonify({
            "success": True,
            "answer":
                "✅ After joining a queue, you receive "
                "a token number.\n\n"
                "You can then monitor your position, "
                "people ahead of you and estimated "
                "waiting time."
        })

    # ========================================================
    # REFRESH / LATEST INFORMATION
    # ========================================================

    if (
        "refresh" in question
        or "latest information" in question
        or "latest status" in question
        or "update my information" in question
        or "current information" in question
    ):

        waiting_time = queue_info[
            "predicted_waiting_time"
        ]

        if waiting_time is not None:

            waiting_text = (
                f"{float(waiting_time):.2f} minutes"
            )

        else:

            waiting_text = "Not available"

        return jsonify({
            "success": True,
            "answer":
                "🔄 Your latest queue information:\n\n"
                f"🎫 Token: "
                f"{queue_info['token_number']}\n"
                f"📋 Queue: "
                f"{queue_info['queue_name']}\n"
                f"👥 People waiting: "
                f"{queue_info['people_waiting']}\n"
                f"👤 People ahead: "
                f"{queue_info['people_ahead']}\n"
                f"🔢 Position: "
                f"{queue_info['position']}\n"
                f"⏱️ Estimated waiting time: "
                f"{waiting_text}\n"
                f"📍 Status: "
                f"{queue_info['status']}"
        })

    # ========================================================
    # THANK YOU
    # ========================================================

    if any(word in question for word in [
        "thank you",
        "thanks",
        "thank"
    ]):

        return jsonify({
            "success": True,
            "answer":
                "You're welcome! 😊\n\n"
                "I'm here to help you with your queue."
        })

    # ========================================================
    # DEFAULT
    # ========================================================

    return jsonify({
        "success": True,
        "answer":
            "🤖 I can help you with your queue.\n\n"
            "Try asking:\n\n"
            "🎫 What is my token?\n"
            "👥 How many people are waiting?\n"
            "👤 How many people are ahead of me?\n"
            "🔢 What is my position?\n"
            "⏱️ How long do I need to wait?\n"
            "📋 Which queue am I in?\n"
            "📍 What is my queue status?\n"
            "🏢 How many counters are active?"
    })