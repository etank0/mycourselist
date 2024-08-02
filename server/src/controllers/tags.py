from flask import Blueprint, Response, json
from src.utils.message import message
from src.database import db
from src.models.tags import Tag
from flasgger import swag_from

tags = Blueprint("tags", __name__, url_prefix="/api/v1/tags")

### Public: Get Tags from db
@tags.get("/get_tags")
@swag_from("../docs/tags/getTags.yaml")
def getCatalog():    
    tags = Tag.query.filter_by().all()
    tags_json = [ tag.json() for tag in tags ]

    return Response(
        response=json.dumps({
        "status": "success",
        "message": "Tags fetched Successfully!",
        "tags": tags_json
        }),
        status=200,
        mimetype='application/json'
    )