from werkzeug.exceptions import HTTPException


class UserExistsError(HTTPException):
    code = 409
