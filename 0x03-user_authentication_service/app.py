#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
