from fastapi import FastAPI

from api.auth.token import token_router
from api.v1.routers.user import user_router
from api.v1.routers.incident import incident_router
from core.db import Base, engine

app = FastAPI()
app.title = "UrbanWatch"
app.version = "0.0.1"

app.include_router(token_router)
app.include_router(user_router)
app.include_router(incident_router)

Base.metadata.create_all(bind=engine)