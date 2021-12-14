from flask import Blueprint, jsonify, request, redirect
from core import errors
from models.user import RegistrationModel
from crud import user_crud, posts_crud, follow_crud
from core.db import get_connection
from blueprints import deps

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/user")


@user_blueprint.route("", methods=["POST"])
def register():
    registration_data = deps.get_input(RegistrationModel)

    with get_connection() as conn:
        user_crud.create(conn, registration_data)

    return jsonify({"info": "OK"}), 201


@user_blueprint.route("")
def get_user_data():
    current_user = deps.get_current_user()
    return redirect(f"/api/user/{current_user.login}")


# подписчики юзера
@user_blueprint.route("/followers")
def get_user_followers():
    current_user = deps.get_current_user()
    return redirect(f"/api/user/{current_user.login}/followers")


# подписки юзера
@user_blueprint.route("/follows")
def get_user_follows():
    current_user = deps.get_current_user()
    return redirect(f"/api/user/{current_user.login}/follows")


@user_blueprint.route("<string:login>")
def get_selected_user_data(login: str):
    user_data = deps.get_user_by_login(login)
    return jsonify(user_data.dict())


@user_blueprint.route("<string:login>/follow", methods=["POST"])
def follow(login: str):
    current_user = deps.get_current_user()
    user_to_follow = deps.get_user_by_login(login)

    if current_user.id == user_to_follow.id:
        raise errors.ForbiddenError("Can not follow yourself")

    with get_connection() as conn:
        if follow_crud.exists(conn, current_user, user_to_follow):
            raise errors.ConflictError("Already subscribed")

        follow_crud.create(conn, current_user, user_to_follow)

    return jsonify({"info": "OK"})


# все подписки
@user_blueprint.route("<string:login>/follows")
def get_all_user_follows(login: str):
    user = deps.get_user_by_login(login)
    with get_connection() as conn:
        follows = follow_crud.find_follows(conn, user.id)
    return jsonify([user.dict() for user in follows])


# все подписчики
@user_blueprint.route("<string:login>/followers")
def get_all_user_followers(login):
    user = deps.get_user_by_login(login)
    with get_connection() as conn:
        follows = follow_crud.find_followers(conn, user.id)
    return jsonify([user.dict() for user in follows])


@user_blueprint.route("<string:login>/follow", methods=["DELETE"])
def unfollow(login: str):
    current_user = deps.get_current_user()
    user_to_un_follow = deps.get_user_by_login(login)

    if current_user.id == user_to_un_follow.id:
        raise errors.ForbiddenError("Can not unfollow yourself")

    with get_connection() as conn:
        if not follow_crud.exists(conn, current_user, user_to_un_follow):
            raise errors.ConflictError("Already not subscribed")

        follow_crud.delete(conn, current_user, user_to_un_follow)

    return jsonify({"info": "OK"})
