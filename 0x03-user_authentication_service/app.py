#!/usr/bin/env python3
"""
Starta A flask App
"""
from flask import Flask, jsonify, request
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
def register_user():
    """Registers new user"""
    response = request.form.to_dict()
    try:
        new_user = AUTH.register_user(
            response.get("email"), response.get("password"))
    except ValueError:
        return jsonify({"message": "email already registered"})

    return jsonify({"email": f"{new_user.email}", "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
