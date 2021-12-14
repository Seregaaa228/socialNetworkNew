from flask import request
from crud import user_crud, posts_crud
from core.db import get_connection
from core import errors
from models.user import UserModel
from pydantic import BaseModel
from models.posts import ReturnPostModel


def get_current_user() -> UserModel:
    auth_data = request.authorization
    if auth_data is None:
        raise errors.AuthError("Auth headers not provided")

    with get_connection() as conn:
        user_data = user_crud.authenticate(conn, auth_data)

    return user_data


def get_user_by_login(login: str) -> UserModel:
    with get_connection() as conn:
        user_data = user_crud.get(conn, login)

    if user_data is None:
        raise errors.NotFoundError(f"User with login '{login}' was not found")

    return user_data


def get_post_by_id(id: str) -> ReturnPostModel:
    with get_connection() as conn:
        post_data = posts_crud.get(conn, id)

    if not post_data:
        raise errors.NotFoundError(f"Post with id '{id}' was not found")

    return post_data



def get_input(ModelType: type[BaseModel]) -> BaseModel:
    data = request.get_json(True)
    if data is None:
        raise errors.InvalidDataFormat("Json not found")

    return ModelType(**data)
