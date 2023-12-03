
from contextlib import asynccontextmanager
from fastapi import FastAPI
import beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from beanie import Document
from pydantic import EmailStr, Field


load_dotenv()




class Instagram_Collection(Document):
    instagram_account: str
    password: str
    cookie: dict
    last_update: str

    def to_json(self):
        return {
            "id": str(self.id),
            "instagram_account": self.instagram_account,
            "password": self.password,
            "cookie": self.cookie,
            "last_update": self.last_update
        }


class Users_Collection(Document):
    username: str = Field(max_length=20)
    email: EmailStr
    hashed_password: str
    instagram_account: dict | None = Field(default=None)

    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "instagram_account": self.instagram_account,

        }



@asynccontextmanager
async def my_database(app: FastAPI):
    client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))

    await beanie.init_beanie(database=client.FastAPIProject,
                             document_models=[Instagram_Collection, Users_Collection])

    print("Startup complete")
    yield
    print("Shutdown complete")
