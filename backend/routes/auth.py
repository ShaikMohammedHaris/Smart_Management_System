from flask import Blueprint, request, jsonify
from backend.database import get_db_connection

auth = Blueprint("auth", __name__)


# ============================================================
# REGISTER
# ============================================================

@auth.route("/register", methods=["POST"])
def register():

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "No registration data received."
            }), 400

        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", ""))

        # ----------------------------------------------------
        # Validate fields
        # ----------------------------------------------------

        if not name:
            return jsonify({
                "success": False,
                "message": "Please enter your full name."
            }), 400

        if not email:
            return jsonify({
                "success": False,
                "message": "Please enter your email address."
            }), 400

        if not password:
            return jsonify({
                "success": False,
                "message": "Please enter a password."
            }), 400

        if len(password) < 3:
            return jsonify({
                "success": False,
                "message": "Password must contain at least 3 characters."
            }), 400

        # ----------------------------------------------------
        # Database connection
        # ----------------------------------------------------

        connection = get_db_connection()

        try:

            # ------------------------------------------------
            # Check whether email already exists
            # ------------------------------------------------

            existing_user = connection.execute(
                """
                SELECT id
                FROM users
                WHERE LOWER(email) = ?
                """,
                (email,)
            ).fetchone()

            if existing_user:

                return jsonify({
                    "success": False,
                    "message": "Email is already registered. Please login."
                }), 409

            # ------------------------------------------------
            # Create new USER account
            # ------------------------------------------------

            cursor = connection.execute(
                """
                INSERT INTO users
                (name, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    password,
                    "user"
                )
            )

            connection.commit()

            user_id = cursor.lastrowid

            print("----------------------------------------")
            print("NEW USER REGISTERED")
            print("ID:", user_id)
            print("NAME:", name)
            print("EMAIL:", email)
            print("ROLE: user")
            print("----------------------------------------")

            return jsonify({
                "success": True,
                "message": "Registration successful.",
                "user": {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    "role": "user"
                }
            }), 201

        finally:
            connection.close()

    except Exception as error:

        print("REGISTRATION ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Registration failed. Please try again."
        }), 500


# ============================================================
# LOGIN
# ============================================================

@auth.route("/login", methods=["POST"])
def login():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "No login data received."
            }), 400

        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", ""))

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password are required."
            }), 400

        connection = get_db_connection()

        try:

            # ------------------------------------------------
            # First check email
            # ------------------------------------------------

            user = connection.execute(
                """
                SELECT *
                FROM users
                WHERE LOWER(email) = ?
                """,
                (email,)
            ).fetchone()

            if not user:

                return jsonify({
                    "success": False,
                    "message": "Email is not registered. Please create an account."
                }), 401

            # ------------------------------------------------
            # Check exact password
            # ------------------------------------------------

            if user["password"] != password:

                return jsonify({
                    "success": False,
                    "message": "Incorrect password."
                }), 401

            # ------------------------------------------------
            # Successful login
            # ------------------------------------------------

            print("----------------------------------------")
            print("LOGIN SUCCESS")
            print("ID:", user["id"])
            print("NAME:", user["name"])
            print("EMAIL:", user["email"])
            print("ROLE:", user["role"])
            print("----------------------------------------")

            return jsonify({
                "success": True,
                "message": "Login successful.",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }), 200

        finally:
            connection.close()

    except Exception as error:

        print("LOGIN ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Login failed. Please try again."
        }), 500