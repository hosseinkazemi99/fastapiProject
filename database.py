from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self, database_url: str, database_name: str):
        self.client = AsyncIOMotorClient(database_url)
        self.database = self.client[database_name]


database = Database(os.environ.get("MONGO_URI"), os.environ.get("MONGO_DB"))


def get_database():
    return database.database
