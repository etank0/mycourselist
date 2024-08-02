from flask import Blueprint, request, Response, json
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.database import db
from src.models.user import User
from src.models.admin import Admin
from src.utils.message import message
from src.utils.error import error
from src.utils.upload import cloud_upload, allowed_file
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


### USER REGISTRATION
@auth.post('/user/register')
@swag_from('../docs/auth/userRegistration.yaml')
def register():
    "Register User"
    user = request.form.get("username")
    passw = request.form.get("password")
    repassw = request.form.get("repassword")
    name = request.form.get("name")
    email = request.form.get("email")

    # Validating the form results
    if not user:
        return message(400, "failed", "Provide Username!")
    if not passw or not repassw:
        return message(400, "failed", "Provide Password In Both Fields!")
    if passw != repassw:
        return error(400, "failed", "Passwords Mismatch!")
    if not user.isalnum() or len(user) < 6:
        return message(400, "failed", "Username contains special character and/or less than 6 characters!") 
    if not passw.isalnum() or len(passw) < 4:
        return message(400, "failed", "Password contains special character and/or less than 4 characters!")
    if not name or len(name) < 3:
        return message(400, "failed", "Name empty or shorter than 3 letters!")
    if not validators.email(email):
        return message(400, "failed", "Email is not valid!")

    if User.query.filter_by(username=user).first() or Admin.query.filter_by(username=user).first():
        return message(400, "failed", "User with the username already exists!")
    if User.query.filter_by(email=email).first():
        return message(400, "failed", "User with the email already exists!") 
    
    if 'file' not in request.files:
        return message(400, "failed", "No file part!")
    
    file = request.files['file']

    if file.filename == '':
        return message(400, "failed", "No selected file!")

    if not allowed_file(file.filename):
        return message(400, "failed", "Not a file from these formats: 'png', 'jpg', 'jpeg', 'gif'") 

    try:
        url = cloud_upload(file)["url"]
    except Exception as e:
        return error(e)
    
    # Creating user and updating the database
    entry = User(username=user, hash=generate_password_hash(passw), name=name, email=email, url=url)

    db.session.add(entry)
    db.session.commit()

    return message(200, "success", f"Successfully Registered: {entry.username}")


### USER LOGIN
@auth.post("/user/login")
@swag_from('../docs/auth/userLogin.yaml')
def userLogin():
    """Logging User IN"""
    # Getting results from the json
    user = request.json.get("username")
    passw = request.json.get("password")

    if not user or not passw:
        return message(400, "failed", "Username and/or Password field was empty!")

    entry = User.query.filter_by(username=user).first()

    if not entry or not check_password_hash(entry.hash, passw):
        return message(400, "failed", "No such user with the username and password found!")
    
    refresh_token = create_refresh_token(identity=user)
    access_token = create_access_token(identity=user)

    user_json = entry.json()

    user_json["refresh_token"] = refresh_token
    user_json["access_token"] = access_token

    return Response( 
        response=json.dumps({
        "status": "success",
        "message": "User Logged In Successfully!",
        "user": user_json
        }),
        status=200,
        mimetype='application/json'
    )

### ADMIN LOGIN
@auth.post("/admin/login")
@swag_from('../docs/auth/adminLogin.yaml')
def adminLogin():
    """Logging Admin IN"""
    # Getting results from the json
    user = request.json.get("username")
    passw = request.json.get("password")

    if not user or not passw:
        return message(400, "failed", "Username and/or Password field was empty!")

    entry = Admin.query.filter_by(username=user).first()

    if not entry or not check_password_hash(entry.hash, passw):
        return message(400, "failed", "No such admin with the username and password found!")
    
    refresh_token = create_refresh_token(identity=user)
    access_token = create_access_token(identity=user)

    user_json = entry.json()

    user_json["refresh_token"] = refresh_token
    user_json["access_token"] = access_token

    return Response( 
        response=json.dumps({
        "status": "success",
        "message": "Admin Logged In Successfully!",
        "admin": user_json
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Refresh User Access Token
@auth.post('/user/refresh_token')
@jwt_required(refresh=True)
@swag_from('../docs/auth/userRefresh.yaml')
def userRefresh():
    username = get_jwt_identity()

    if not User.query.filter_by(username=username).first():
        return message(401, "failed", "Unauthorized Request")
    
    access_token = create_access_token(identity=username)

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "User access token refreshed successfully!",
        "access_token": access_token
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Refresh Admin Access Token
@auth.post('/admin/refresh_token')
@jwt_required(refresh=True)
@swag_from('../docs/auth/adminRefresh.yaml')
def adminRefresh():
    username = get_jwt_identity()

    if not Admin.query.filter_by(username=username).first():
        return message(401, "failed", "Unauthorized Request")

    access_token = create_access_token(identity=username)

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "Admin access token refreshed successfully!",
        "access_token": access_token
        }),
        status=200,
        mimetype='application/json'
    )