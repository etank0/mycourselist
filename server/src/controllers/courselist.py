from flask import Blueprint, Response, json
from src.utils.message import message
from src.database import db
from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.user import User
from flasgger import swag_from

courselist = Blueprint("courselist", __name__, url_prefix="/api/v1/list")

### Public: Get course list of a user
@courselist.get("/<username>")
@swag_from('../docs/courselist/courselist.yaml')
def courseList(username):
    """Get the course list of a user"""
    user = User.query.filter_by(username=username).first()

    if not user:
        return message(404, "failed", "User with the requested username not found!")
    
    courses = Course.query.filter_by().all()

    courses_json = []
    for course in courses:
        enroll = Enrollment.query.filter_by(userid=user.id, courseid=course.id).first()
        course_json = course.json()
        if enroll:
            course_json.update(enroll.json())
            courses_json.append(course_json)

    user.visits += 1
    db.session.commit()

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "Courses fetched Successfully!",
        "courses": courses_json
        }),
        status=200,
        mimetype='application/json'
    )

### Public: Get Course Catalog
@courselist.get("/get_catalog")
@swag_from("../docs/courselist/getCatalog.yaml")
def getCatalog():    
    courses = Course.query.filter_by().all()
    courses_json = [ course.json() for course in courses ]

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "Courses fetched Successfully!",
        "courses": courses_json
        }),
        status=200,
        mimetype='application/json'
    )
