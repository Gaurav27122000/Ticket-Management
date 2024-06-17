from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from sqlalchemy.testing.pickleable import User

from models import Ticket, RestaurantBranchEnum, StatusEnum, PlatformEnum
from database import SessionLocal
from auth import get_current_user

router = APIRouter(
    prefix="/ticket",
    tags=["Ticket"],
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


class TicketRequest(BaseModel):
    tittle: str = Field(min_length=4)
    description: str = Field(min_length=4, max_length=100)
    platform: PlatformEnum
    restaurant_branch: RestaurantBranchEnum
    name: str = Field(min_length=4)
    status: StatusEnum


class TicketStatus(BaseModel):
    status: StatusEnum


@router.get("/getTickets")
async def get_all(user: user_dependency,db: db_dependency):
    if(user.get('user_role')=='user'):
        return db.query(Ticket).filter(Ticket.owner_id == user.get('id')).all()
    else:
        return db.query(Ticket).all()


@router.get("/getTicket/{ticket_id}", status_code=200)
async def get_ticket_by_id(db: db_dependency, ticket_id: int = Path(gt=0)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if (ticket is not None):
        return ticket
    else:
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.post("/addTicket", status_code=status.HTTP_201_CREATED)
async def add_ticket(user: user_dependency, db: db_dependency,ticket: TicketRequest):
    if(user is None):   raise HTTPException(status_code=401, detail="User not found")
    ticket_model = Ticket(**ticket.dict(), owner_id=user.get('id'))
    db.add(ticket_model)
    db.commit()


@router.put("/updateTicket/{ticket_id}", status_code=status.HTTP_200_OK)
async def update_status(db: db_dependency, ticket_status: TicketStatus, ticket_id: int = Path(gt=0)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is not None:
        ticket.status = ticket_status.status
        db.commit()

    else:
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.delete("/deleteTicket/{ticket_id}", status_code=status.HTTP_200_OK)
async def update_status(db: db_dependency, ticket_id: int = Path(gt=0)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is not None:
        db.query(Ticket).filter(Ticket.id == ticket_id).delete()
        db.commit

    else:
        raise HTTPException(status_code=404, detail="Ticket not found")
