#!/usr/bin/env python3
"""
Starts A flask App
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def get_json() -> str:
    """
    returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """Registers new user"""
    form_data = request.form.to_dict()

    email = form_data.get("email")
    password = form_data.get("password")

    try:
        new_user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"})

    return jsonify({"email": new_user.email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Logs in a user"""
    form_data = request.form.to_dict()

    email = form_data.get("email")
    password = form_data.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """logs the user out"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """Gets the profile of the user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
