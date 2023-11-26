from pydantic import BaseModel


class Instagram(BaseModel):
    username: str
    password: str
