from werkzeug.exceptions import HTTPException


class AuthError(HTTPException):
    code = 401
