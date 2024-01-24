#!/usr/bin/env python3
"""
Starts A flask App
"""
from flask import Flask, jsonify, request, abort, url_for, redirect
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def get_json():
    """
    returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Registers new user"""
    form_data = request.form.to_dict()
    try:
        new_user = AUTH.register_user(
            form_data.get("email"), form_data.get("password"))
    except ValueError:
        return jsonify({"message": "email already registered"})

    return jsonify({"email": f"{new_user.email}", "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """Logs in a user"""
    form_data = request.form.to_dict()

    if not AUTH.valid_login(form_data.get("email"), form_data.get("password")):
        abort(401)

    session_id = AUTH.create_session(form_data.get("email"))
    response = jsonify({"email": form_data.get('email'), "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logs the user out"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect(url_for('/'))
    else:
        abort(403)

@app.route("/profile", methods=["GET"])
def profile():
    """"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    print(user)
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
