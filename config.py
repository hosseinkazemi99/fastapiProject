from fastapi import FastAPI
from dotenv import load_dotenv
from routers import user, protect, instalogin, instafollowers
from database import my_database

app = FastAPI(
    lifespan=my_database
)
app.include_router(user.router, tags=["user"])
app.include_router(protect.router, tags=["protected"])
app.include_router(instalogin.router, tags=["instagram"])
app.include_router(instafollowers.router, tags=["instafollowers"])
load_dotenv()

# @app.on_event("startup")
# async def startup_db_client():
#     app.mongodb_client = database.client
#     app.mongodb = database.database
#
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     app.mongodb_client.close()
