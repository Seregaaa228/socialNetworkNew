# .../api/posts
from flask import Blueprint, jsonify, request
from crud import posts_crud
from core.db import get_connection
from blueprints import deps
from models.posts import BaseCreatePostModel

posts_blueprint = Blueprint("posts_blueprint", __name__, url_prefix="/posts")


@posts_blueprint.route("", methods=["POST"])
def create_post():
    current_user = deps.get_current_user()
    post_data = deps.get_input(BaseCreatePostModel)

    with get_connection() as conn:
        posts_crud.create(conn, post_data, current_user)

    return jsonify({"info": "OK"}), 201


# посты из подписок
@posts_blueprint.route("/follows")
def get_posts_feed():
    current_user = deps.get_current_user()

    with get_connection() as conn:
        posts = posts_crud.get_by_follower(conn, current_user)

    return jsonify([post.dict() for post in posts])


# все посты
@posts_blueprint.route("")
def get_all_posts_feed():
    with get_connection() as conn:
        posts = posts_crud.get_by_all(conn)

    return jsonify([post.dict() for post in posts])


# личные посты
@posts_blueprint.route("/personal")
def get_personal_posts_feed():
    current_user = deps.get_current_user()

    with get_connection() as conn:
        posts = posts_crud.get_by_creator(conn, current_user)

    return jsonify([post.dict() for post in posts])


# поиск поста по айди
@posts_blueprint.route("<string:id>/findPost")
def show_post(id: str):
    return jsonify([post.dict() for post in deps.get_post_by_id(id)]), 201


# удаление поста по айди
@posts_blueprint.route("<string:id>/deletePost", methods=["DELETE"])
def delete_post(id: str):
    current_user = deps.get_current_user()
    post = deps.get_post_by_id(id)
    with get_connection() as conn:
        if current_user.id == post.creator:
            posts_crud.delete(conn,id)
            return jsonify({"info": "OK"}), 201
        else:
            return jsonify({"info": "Its not your post"}), 404
