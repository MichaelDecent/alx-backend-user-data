#!/usr/bin/env python3
"""
this module handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if the email or password is missing in the request
      - 404 if no user found for the email
      - 401 for wrong password
    """
    response = request.form.to_dict()
    print(response)

    if "email" not in response:
        return jsonify({"error": "email missing"}), 400

    if "password" not in response:
        return jsonify({"error": "password missing"}), 400
    try:
        user_list = User.search({"email": response["email"]})
        print(user_list)
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(user_list) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    user_obj = user_list[0]

    if user_obj.is_valid_password(response["password"]):
        from api.v1.app import auth

        cookie_name = getenv("SESSION_NAME")
        session_id = auth.create_session(user_obj.id)
        response = jsonify(user_obj.to_json())
        response.set_cookie(cookie_name, session_id)
        return response
    else:
        return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout", methods=[
    "DELETE"], strict_slashes=False)
def logout_user() -> str:
    """POST /api/v1/auth_session/logout
    Return:
      - 200 with empty JSON dictionary
      - 404 if user not found
    """
    from api.v1.app import auth

    response = auth.destroy_session(request)
    if response is False:
        abort(404)
    return jsonify({}), 200
