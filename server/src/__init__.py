from flask import Flask, Response, json
from src.controllers.auth import auth
from src.controllers.admin import admin
from src.controllers.user import user
from src.controllers.courselist import courselist
from src.controllers.tags import tags
from src.constants.http_status_codes import *
from src.database import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.config.swagger import template, swagger_config
from datetime import timedelta
import os

def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
            JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
            SWAGGER={
                'title': 'MyCourseList API',
                'uiversion': 3
            }
        )
    else: 
        app.config.from_mapping(test_config)
    
    # db
    db.app=app
    db.init_app(app)
    migrate = Migrate(app, db)

    # JWT
    JWTManager(app)

    # Swagger
    Swagger(app, config=swagger_config, template=template)

    # controllers
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(courselist)
    app.register_blueprint(tags)

    # Error Handling
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_400(e):
        return Response( 
        response=json.dumps({
        "status": "failed",
        "message": "Some error occurred!",
        "error": "Not Found!",
        }),
        status=HTTP_404_NOT_FOUND,
        mimetype='application/json'
        )
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return Response( 
        response=json.dumps({
        "status": "failed",
        "message": "Some error occurred!",
        "error": "Internal Server Error: Something went wrong!",
        }),
        status=HTTP_500_INTERNAL_SERVER_ERROR,
        mimetype='application/json'
        )
    
    return app
