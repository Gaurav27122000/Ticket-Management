from fastapi import FastAPI

import models
import auth
import ticket
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(ticket.router)
app.include_router(auth.router)
