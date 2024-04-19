from flask import request, session, redirect, jsonify
from functools import wraps
import os, requests

# login_required decorator
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None and session.get("admin_id") is None:
            return error("Unauthorized access!")
        return f(*args, **kwargs)
    return decorated_function

def message(message):
    return jsonify({"message": message}), 200

# error function for any errors
def error(message):
    return jsonify({"error": message}) , 400