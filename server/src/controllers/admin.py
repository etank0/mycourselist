from flask import Blueprint, request, Response, json
from src.utils.get_ytdata import get_data, extract_id
from src.database import db
from src.models.course import Course
from src.models.admin import Admin
from src.models.tags import Tag
from src.utils.message import message
from src.utils.error import error
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flasgger import swag_from

admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

### Private: Add Courses
@admin.post("/add_course")
@jwt_required()
@swag_from("../docs/admin/addCourse.yaml")
def addCourse():
    """Add course by Admin"""
    username = get_jwt_identity()

    user = Admin.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")
    
    # Getting results from the json
    link = request.json.get("link")
    tags = request.json.get("tags")
    newtags = request.json.get("newtags")
    description = request.json.get("description")

    if not link:
        return message(400, "failed", "Link not provided!")

    if not description or description == "":
        return message(400, "failed", "Description not provided!")

    if tags == None or len(tags) == 0:
        return message(401, "failed", "Tags not provided!");

    if Course.query.filter_by(link=link).first():
        return message(400, "failed", "Course already exists with that link!")
    
    # fetch_link = "https://www.youtube.com/oembed?url=" + link + '&format=json'

    # try: 
    #     response = requests.get(fetch_link)
    #     response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
    #     data = response.json()
    # except requests.exceptions.RequestException as err:
    #     return message(400, "failed", "Invalid playlist link or Some error fetching data from the playlist link!")
    
    content = extract_id(link)
    data = get_data(content["id"], content["type"])

    name = data['snippet']['title']
    thumbnail = data['snippet']['thumbnails']['maxres']['url']
    creator = data['snippet']['channelTitle']
    modules = 1
    if content["type"] == 'playlist':
        modules = data['contentDetails']['itemCount']
    published_at = data['snippet']['publishedAt']
    published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    published_at = published_at.date()
    hours = data['hours']

    tag_str = "" 
    for tag in tags:
        if (not Tag.query.filter_by(name=tag).first()):
            return message(400, "failed", f"Tag '{tag}' doesn't exist in DB!")    
        tag_str += tag + ", "

    if newtags and len(newtags) > 0:
        for tag in newtags: 
            tag_str += tag + ", "
            if (Tag.query.filter_by(name=tag).first()):
                continue
            newtag_obj = Tag(name=tag)
            db.session.add(newtag_obj)

    entry = Course(
        name=name, 
        link=link, 
        hours=hours, 
        thumbnail=thumbnail, 
        creator=creator, 
        modules=modules, 
        published_at=published_at, 
        tags=tag_str,
        description=description)
        
    course_json = entry.json()

    db.session.add(entry)
    db.session.commit()

    return Response( 
        response=json.dumps({
        "status": "success",
        "message": "Course added/updated Successfully!",
        "course": course_json 
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Update Courses
@admin.post("/update_course/<id>")
@jwt_required()
@swag_from("../docs/admin/updateCourse.yaml")
def updateCourse(id):
    username = get_jwt_identity()

    user = Admin.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")

    tags = request.json.get("tags")    
    newtags = request.json.get("newtags")
    description = request.json.get("description")

    if not description or description == "":
        return message(400, "failed", "Description not provided!")

    if tags == None or len(tags) == 0:
        return message(401, "failed", "Tags not provided!");

    course = Course.query.filter_by(id=id).first()

    if (not course):
        return message(400, "failed", f"Course with id:{id} not found!")

    tag_str = ""
    for tag in tags:
        if (not Tag.query.filter_by(name=tag).first()):
            return message(400, "failed", f"Tag '{tag}' not found in DB")
        tag_str += tag + ", "

    if newtags and len(newtags) > 0:
        for tag in newtags: 
            tag_str += tag + ", "
            if (Tag.query.filter_by(name=tag).first()):
                continue
            newtag_obj = Tag(name=tag)
            db.session.add(newtag_obj)

    course.tags = tag_str 
    course.description = description
    db.session.commit()

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "Course tags updated successfully!",
        "tags": course.tags
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Get Courses
@admin.get("/get_courses")
@jwt_required()
@swag_from("../docs/admin/getCourses.yaml")
def getCourses():
    username = get_jwt_identity()

    user = Admin.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")
    
    courses = Course.query.filter_by().all()
    courses_json = [ course.json() for course in courses ]

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "Courses fetched successfully!",
        "courses": courses_json
        }),
        status=200,
        mimetype='application/json'
    )

### Private: Update Tags in DB
@admin.post("/update_tags")
@jwt_required()
@swag_from("../docs/admin/updateTags.yaml")
def update_tags():
    username = get_jwt_identity()

    user = Admin.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")

    delete_tags = request.json.get("delete_tags")
    insert_tags  = request.json.get("insert_tags")

    for tag in delete_tags: 
        tag_obj = Tag.query.filter_by(name=tag).first()
        if (tag_obj):
            db.session.delete(tag_obj)
        else: 
            message(400, "failed", f"Tag '{tag}' doesn't exist in the db!")

    for tag in insert_tags: 
        tag_obj = Tag(name=tag)
        db.session.add(tag_obj)

    db.session.commit()
    return message(200, "success", "Course deleted successfully!")

### Private: Delete Course
@admin.get("/delete_course/<id>")
@jwt_required()
@swag_from("../docs/admin/deleteCourse.yaml")
def deleteCourse(id):
    username = get_jwt_identity()

    user = Admin.query.filter_by(username=username).first()

    if (not user):
        return message(401, "failed", "Unauthorized Request!")
    
    course = Course.query.filter_by(id=id).first()
    db.session.delete(course)
    db.session.commit()
    return message(200, "success", "Course deleted successfully!")