from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
import auth
import ticket
import chat
from database import engine

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(ticket.router)
app.include_router(auth.router)
app.include_router(chat.router)


@app.get("/")
async def first_api():
    return {"message": "Welcome to CRM Builder. Check /docs for more information."}
