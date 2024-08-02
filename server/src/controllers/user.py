from flask import Blueprint, request, Response, json
from src.database import db
from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models.user import User
from src.models.comment import Comment
from src.utils.message import message
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

user = Blueprint("user", __name__, url_prefix="/api/v1/user")

### Private: Add Courses
@user.post("/add_course/<courseid>")
@jwt_required()
@swag_from("../docs/user/addCourse.yaml")
def addCourse(courseid):
    """Add course by User"""
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    if (not user):
        return message(400, "failed", "Unauthorized Request!")
    
    course = Course.query.filter_by(id=courseid).first()

    if (not course):
        return message(404, "failed", "Course with the id not found!")

    enrollment = Enrollment.query.filter_by(userid=user.id, courseid=course.id).first()

    if (enrollment):
        return message(400, "failed", "Enrollment already found!")

    modules_completed = request.json.get("modules_completed")
    rating = request.json.get("rating")
    is_completed = False

    if modules_completed is None:
        modules_completed = 0
    if rating is None:
        rating = 0
    if modules_completed < 0 or modules_completed > course.modules:
        message(400, "failed", "Invalid modules value!")
    if rating < 0 or rating > 5:
        message(400, "failed", "Invalid rating value!")
    if modules_completed == course.modules:
        is_completed = True

    enrollment = Enrollment(userid=user.id, courseid=course.id, is_completed=is_completed, modules_completed=modules_completed, rating=rating)

    if (is_completed):
        enrollment.completed_course()

    course.enrolled += 1
    if course.rating:
        course.rating = ( course.rating * (course.enrolled - 1) + rating ) / course.enrolled
    else:
        course.rating = rating

    db.session.add(enrollment)
    db.session.commit()

    return Response( 
        response=json.dumps({
        "status": "success",
        "message": "Course added Successfully!",
        "enrollment": enrollment.json()
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Get Courses
@user.get("/get_courses")
@jwt_required()
@swag_from("../docs/user/getCourses.yaml")
def getUCourses():
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")
    
    courses = Course.query.filter_by().all()
    courses_json = []
    for course in courses:
        enroll = Enrollment.query.filter_by(userid=user.id, courseid=course.id).first()
        course_json = course.json()
        if enroll:
            course_json.update(enroll.json())
            courses_json.append(course_json)

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "Courses fetched Successfully!",
        "courses": courses_json
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Update Courses
@user.patch("/update_course/<courseid>")
@user.put("/update_course/<courseid>")
@user.post("/update_course/<courseid>")
@jwt_required()
@swag_from("../docs/user/updateCourse.yaml")
def updateCourse(courseid):
    """Update course by User"""
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")
    
    course = Course.query.filter_by(id=courseid).first()

    if (not course):
        return message(404, "failed", "Course with the id not found!")

    enrollment = Enrollment.query.filter_by(userid=user.id, courseid=course.id).first()

    if (not enrollment):
        return message(404, "failed", "Enrollment not found!")

    modules_completed = request.json.get("modules_completed")
    rating = request.json.get("rating")
    is_completed = False

    if modules_completed is None:
        modules_completed = enrollment.modules_completed
    else:
        enrollment.modules_completed = modules_completed

    if rating is None:
        rating = enrollment.rating
    else:
        enrollment.rating = rating

    if modules_completed < 0 or modules_completed > course.modules:
        message(400, "failed", "Invalid modules value!")
    if rating < 0 or rating > 5:
        message(400, "failed", "Invalid rating value!")
    if modules_completed == course.modules:
        is_completed = True

    if (is_completed):
        enrollment.completed_course()
    else:
        enrollment.ongoing_course()

    if course.rating:
        course.rating = ( course.rating * (course.enrolled - 1) + rating ) / course.enrolled
    else:
        course.rating = rating

    db.session.commit()

    return Response( 
        response=json.dumps({
        "status": "success",
        "message": "Course updated Successfully!",
        "enrollment": enrollment.json()
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Delete Course Enrollment
@user.get("/delete_course/<courseid>")
@jwt_required()
@swag_from("../docs/user/deleteCourse.yaml")
def deleteCourse(courseid):
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")
    
    course = Course.query.filter_by(id=courseid).first()

    if (not course):
        return message(400, "failed", "Course with the id not found!")
    
    enrollment = Enrollment.query.filter_by(courseid=courseid, userid=user.id).first()

    if (not enrollment):
        return message(404, "failed", "Enrollment for the course not found!")
    
    if course.enrolled > 1:
        course.rating = ( course.rating * (course.enrolled) - enrollment.rating ) / (course.enrolled - 1)
    else:
        course.rating = ( course.rating * (course.enrolled) - enrollment.rating ) / (course.enrolled)

    course.enrolled -= 1
  
    db.session.delete(enrollment)
    db.session.commit()
    return message(200, "success", f"Course with id: {courseid} deleted successfully!")

### Private: Comment on user course list
@user.post("/comment/<list_username>")
@jwt_required()
def userComment(list_username):
    username = get_jwt_identity()

    if username == list_username:
        return message(400, "failed", "Cannot comment on your own list!")

    user = User.query.filter_by(username=username).first()
    list_user = User.query.filter_by(username=list_username).first()

    if not user:
        return message(401, "failed", "Unauthorized request!")
    if not list_user:
        return message(400, "failed", "User with requested username not found!")
    
    comment_obj = Comment.query.filter_by(senderid=user.id, receiverid=list_user.id).first()

    if comment_obj:
        return message(400, "failed", "You have already commented on this list! Consider deleting to post a new one.")
    
    comment = request.json.get("comment")

    if not comment or comment == "":
        return message(400, "failed", "Comment field empty or not provided!")
    
    entry = Comment(
        senderid=user.id, 
        receiverid=list_user.id,
        sender_username=username,
        receiver_username=list_username,
        comment=comment
        )

    db.session.add(entry)
    db.session.commit()

    return Response( 
        response=json.dumps({
        "status": "success",
        "message": "Comment added successfully!",
        "comment": entry.json()
        }),
        status=200,
        mimetype='application/json'
    )

### Public: Comments to be displayed on user course list page
@user.get("/get_comments/<username>")
def getComments(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return message(400, "failed", "User with username not found!")
    
    comments = [ comment.json() for comment in Comment.query.filter_by(receiverid=user.id).all() ]

    return Response( 
        response=json.dumps({
        "status": "success",
        "message": "Comment fetched successfully!",
        "comments": comments
        }),
        status=200,
        mimetype='application/json'
    )



