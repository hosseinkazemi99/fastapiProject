from fastapi import FastAPI
from dotenv import load_dotenv
from routers import user, protect
from database import database


app = FastAPI()
app.include_router(user.router, tags=["user"])
app.include_router(protect.router, tags=["protected"])
load_dotenv()




@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = database.client
    app.mongodb = database.database


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


