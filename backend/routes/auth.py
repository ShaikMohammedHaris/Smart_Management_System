from flask import Blueprint, request, jsonify

from backend.database import get_db_connection


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:

        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    connection = get_db_connection()

    try:

        connection.execute("""
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
        """, (
            name,
            email,
            password
        ))

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful"
        })

    except Exception:

        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 400

    finally:

        connection.close()


@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    connection = get_db_connection()

    user = connection.execute("""
        SELECT *
        FROM users
        WHERE email = ?
        AND password = ?
    """, (
        email,
        password
    )).fetchone()

    connection.close()

    if user:

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid email or password"
    }), 401