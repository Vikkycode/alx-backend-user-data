#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, make_response, redirect, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def welcome_message() -> str:
    """
    Handles GET requests to the root route.

    Returns:
        A JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    Handles POST requests to the /users route.
    Registers a new user if the email is not already registered.

    Returns:
        A JSON payload with user creation status.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        # Improved error handling
        abort(400, description="missing email or password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Handles POST requests to the /sessions route for user login.

    Returns:
        A JSON payload with login status and sets a session ID cookie.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        # 401 for missing credentials
        abort(401, description="Unauthorized")
    if not AUTH.valid_login(email, password):
        # 401 for invalid credentials
        abort(401, description="Unauthorized")
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    # Explicit 200 status code
    return response, 200


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Handles DELETE requests to /sessions for user logout.

    Logs the user out and redirects to the home page.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)  # Forbidden if no user found for the session ID

    AUTH.destroy_session(user.id)
    return redirect("/", code=302)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Handles GET requests to the /profile route.
    Retrieves user information based on session ID.

    Returns:
        User's email as JSON if session is valid, 403 otherwise.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
