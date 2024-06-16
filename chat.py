from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import Ticket, Chat
from database import SessionLocal
from auth import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class ChatRequest(BaseModel):
    message: str
    ticket_id: int

async def check_permission(user:user_dependency,db: db_dependency,ticket_id: int):
    if user is None: raise HTTPException(status_code=401, detail="User not found")

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is None or (user.get('role')!="admin" and ticket.owner_id != user.get('id')):
        return False
    return True


@router.get("/getChats/{ticket_id}")
async def get_chat(user:user_dependency,db: db_dependency, ticket_id: int = Path(gt=0)):
    if(await check_permission(user,db,ticket_id)):
        return db.query(Chat).filter(Chat.ticket_id == ticket_id).all()
    else:
        raise HTTPException(status_code=401, detail="Not enough permissions")


@router.post("/addMessage", status_code=status.HTTP_201_CREATED)
async def add_chat(user: user_dependency, db: db_dependency, chat_request: ChatRequest):
    if(await check_permission(user,db,chat_request.ticket_id)):
        chat_model = Chat(**chat_request.dict(), username=user.get('username'))
        db.add(chat_model)
        db.commit()

    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
