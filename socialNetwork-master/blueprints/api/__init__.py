from flask import Blueprint, jsonify
from .user import user_blueprint
from .posts import posts_blueprint

from werkzeug.exceptions import HTTPException

api_blueprint = Blueprint("api_blueprint", __name__, url_prefix="/api")
api_blueprint.register_blueprint(user_blueprint)
api_blueprint.register_blueprint(posts_blueprint)




@api_blueprint.errorhandler(HTTPException)
def register_default_error(error: HTTPException):
    return (
        jsonify({"error": type(error).__name__, "info": error.description}),
        error.code,
    )
