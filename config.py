from fastapi import FastAPI
from dotenv import load_dotenv
from routers import user
from database import database


app = FastAPI()
app.include_router(user.router, tags=["user"])
load_dotenv()




@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = database.client
    app.mongodb = database.database


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


