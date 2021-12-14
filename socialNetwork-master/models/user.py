from pydantic import BaseModel, validator


class RegistrationModel(BaseModel):
    login: str
    password: str

    @validator("login")
    def validate_login(cls, login: str) -> str:
        assert " " not in login, "No spaces allowed in login"
        return login


class BaseUserModel(BaseModel):
    id: str
    login: str


class UserModel(BaseUserModel):
    followers: int
    follows: int
