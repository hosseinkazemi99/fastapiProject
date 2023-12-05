from contextlib import asynccontextmanager
from fastapi import FastAPI
import beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from beanie import Document, Link
from pydantic import EmailStr, Field
from typing import Optional, List

load_dotenv()


class Instagram_Collection(Document):
    instagram_account: str
    password: str
    cookie: dict
    last_update: str


class Users_Collection(Document):
    username: str = Field(max_length=20)
    email: EmailStr
    hashed_password: str
    instagram_account: Optional[List[Link[Instagram_Collection]]] = []

class Followers_Collection(Document):
    user_account: str
    followers : list
    last_update: str
    instagram_account: Optional[List[Link[Instagram_Collection]]] = []


@asynccontextmanager
async def my_database(app: FastAPI):
    client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))

    await beanie.init_beanie(database=client.FastAPIProject,
                             document_models=[Instagram_Collection, Users_Collection, Followers_Collection])

    print("Startup complete")
    yield
    print("Shutdown complete")
