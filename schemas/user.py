from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr


class UserInDB(User):
    hashed_password: str
