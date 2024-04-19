import os
from flask import Flask, render_template, redirect, session, flash, jsonify, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import requests

from modules import error, message

# instantiate the db
db = SQLAlchemy()

# starting the web app
app = Flask(__name__)

# config for the databse
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mycourselist.db"

db.init_app(app)

# creating a class to represent the table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    link = db.Column(db.String, unique=True, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.String, nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

class Enrollment(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    courseid = db.Column(db.Integer, primary_key=True)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/user/register", methods=["POST"])
def register():
    """Registering User"""
    if request.method == "POST":
        # Getting results from the json
        user = request.json.get("username")
        passw = request.json.get("password")
        repassw = request.json.get("repassword")
        name = request.json.get("name")

        # Validating the json results
        if not user:
            return error("Provide Username!")
        if not passw or not repassw:
            return error("Provide Password In Both Fields!")
        if passw != repassw:
            return error("Passwords Mismatch!")
        if not user.isalnum() or len(user) < 6:
            return error("Username contains special character and/or less than 6 characters!") 
        if not passw.isalnum() or len(passw) < 4:
            return error("Password contains special character and/or less than 4 characters!")
        if not name or not name.isalnum() or len(name) < 3:
            return error("Name empty or shorter than 3 letters!")

        if User.query.filter_by(username=user).first():
            return error("Username already exists!")
        # Creating user and updating the database
        entry = User(username=user, hash=generate_password_hash(passw), name=name)

        db.session.add(entry)
        db.session.commit()

        return message(f"Successfully Registered: {entry.username}")

@app.route("/user/login", methods=["POST"])
def userLogin():
    """Logging User IN"""
    if request.method == "POST":
        # Getting results from the json
        user = request.json.get("username")
        passw = request.json.get("password")

        if not user or not passw:
            return error("Username and/or Password field was empty!")

        entry = User.query.filter_by(username=user).first()

        if not entry or not check_password_hash(entry.hash, passw):
            return error("Invalid Username and/or Password!")

        entry_dict = {
            "name": entry.name,
            "username": entry.username,
            "user_id": entry.id
        }

        return jsonify({"message": "Successfully Logged In!", "user": entry_dict})

@app.route("/admin/login", methods=["POST"])
def adminLogin():
    """Logging User IN"""
    if request.method == "POST":
        # Getting results from the json
        user = request.json.get("username")
        passw = request.json.get("password")

        if not user or not passw:
            return error("Username and/or Password field was empty!")

        entry = Admin.query.filter_by(username=user).first()

        if not entry or not check_password_hash(entry.hash, passw):
            return error("Invalid Username and/or Password!")

        if not entry or not check_password_hash(entry.hash, passw):
            return error("Invalid Username and/or Password!")

        entry_dict = {
            "name": entry.name,
            "username": entry.username,
            "admin_id": entry.id
        }

        return jsonify({"message": "Successfully Logged In!", "admin": entry_dict})

@app.route("/admin/add", methods=["POST"])
def addCourse():
    """Add course by Admin"""

    # Getting results from the json
    link = request.json.get("link")
    hours = request.json.get("hours")

    if not link or not hours:
        return error("Name, link or hours field was empty!")
    
    if Course.query.filter_by(link=link).first():
        return error("Course already exists with that link!")
    
    fetch_link = "https://www.youtube.com/oembed?url=" + link + '&format=json'

    try: 
        response = requests.get(fetch_link)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
    except requests.exceptions.RequestException as err:
        return error(err)
    
    if (data is None):
        return error("Invalid link provided!")
    
    thumbnail = data['thumbnail_url']
    creator = data['author_name']
    name = data['title']

    entry = Course(name=name, link=link, hours=hours, thumbnail=thumbnail, creator=creator)

    db.session.add(entry)
    db.session.commit()

    return message(f"Course successfully added with course id {entry.id}")

@app.route("/admin/get", methods=["GET"])
def getCourses():
    """Get courses by Admin"""

    entries = Course.query.filter_by().all()

    entries_list = []
    for entry in entries:
        entry_dict = {
            "name": entry.name,
            "thumbnail": entry.thumbnail,
            "hours": entry.hours,
            "creator": entry.creator,
            "id": entry.id
        }

        entries_list.append(entry_dict)

    return jsonify({ "message": "Successfully fetched courses", "courses": entries_list } )

@app.route("/user/get/<userid>", methods=["GET"])
def getCatalog(userid):
    """Get courses by User"""
    print(userid)
    entries = Course.query.filter_by().all()

    entries_list = []
    for entry in entries:
        entry_dict = {
            "name": entry.name,
            "thumbnail": entry.thumbnail,
            "hours": entry.hours,
            "creator": entry.creator,
            "id": entry.id,
            "link": entry.link
        }
        if Enrollment.query.filter_by(userid=userid, courseid=entry_dict["id"]).first() is None:
            entries_list.append(entry_dict)

    return jsonify({ "message": "Successfully fetched courses", "courses": entries_list } )

@app.route("/user/enroll", methods=["POST"])
def enroll():
    """Add courses by User"""
    courseid = request.json.get("courseid")
    userid = request.json.get("userid")
    if Enrollment.query.filter_by(userid=userid, courseid=courseid).first():
        return error("Enrollment already exists!")

    entry = Enrollment(userid=userid, courseid=courseid)

    db.session.add(entry)
    db.session.commit()

    return jsonify({ "message": "Successfully enrolled in the course!" + str(entry.courseid) } )

@app.route("/user/unenroll", methods=["POST"])
def unenroll():
    """Delete courses by User"""
    courseid = request.json.get("courseid")
    userid = request.json.get("userid")
    enrollment = Enrollment.query.filter_by(userid=userid, courseid=courseid).first()
    if not enrollment:
        return jsonify({ "error": "Enrollment doesn't exist!" }), 404

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({ "message": "Successfully enrolled in the course!" + str(enrollment.courseid) } )

@app.route("/courselist/<username>", methods=["GET"])
def getUserList(username):
    """Get courses by Admin"""

    entries = Course.query.filter_by().all()
    user = User.query.filter_by(username=username).first()
    print(user.id)
    if (user is None):
        return error("Username doesn't exist!")
    
    user_dict = {
        "name": user.name,
        "username": user.username
    }

    entries_list = []
    for entry in entries:
        entry_dict = {
            "name": entry.name,
            "thumbnail": entry.thumbnail,
            "hours": entry.hours,
            "creator": entry.creator,
            "id": entry.id,
            "link": entry.link
        }
        if Enrollment.query.filter_by(userid=user.id, courseid=entry_dict["id"]).first():
            entries_list.append(entry_dict)

    return jsonify({ "message": "Successfully fetched course list of user", "user": user_dict,"courses": entries_list } )

@app.route("/admin/delete/<courseid>", methods=["GET"])
def delete_course(courseid):
    """Delete courses by User"""
    course = Course.query.filter_by(id=courseid).first()
    if not course:
        return jsonify({ "error": "Enrollment doesn't exist!" }), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({ "message": "Successfully enrolled in the course!" } )

if __name__ == "__main__":
    # creating the tables
    with app.app_context():
        db.create_all()
   
    app.run(host='127.0.0.1',port=4000,debug=True)