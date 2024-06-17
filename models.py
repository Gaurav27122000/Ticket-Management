from sqlalchemy.orm import relationship

from database import Base
import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Boolean


class PlatformEnum(str, enum.Enum):
    zomato = 'ZOMATO'
    google = 'GOOGLE'
    swiggy = 'SWIGGY'


class RestaurantBranchEnum(str, enum.Enum):
    bandra = 'BANDRA'
    andheriEast = 'ANDHERI EAST'
    AndheriWest = 'ANDHERI WEST'
    BorivaliWest = 'BORIVALI WEST'
    Ghatkopar = 'GHATKOPAR'


class StatusEnum(str, enum.Enum):
    unassigned = 'UNASSIGNED'
    onHold = 'ON HOLD'
    open = 'OPEN'
    closed = 'CLOSED'


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    # tickets = relationship("Tickets", back_populates="owner")


class Ticket(Base):
    __tablename__ = 'Tickets'
    id = Column(Integer, primary_key=True, index=True)
    tittle = Column(String)
    description = Column(String)
    platform = Column(Enum(PlatformEnum), default=PlatformEnum.google)
    restaurant_branch = Column(Enum(RestaurantBranchEnum), default=RestaurantBranchEnum.andheriEast)
    name = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.unassigned)

    owner_id = Column(Integer, ForeignKey('users.id'))


class Chat(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    sender = Column(String)
    timestamp = Column(DateTime)

    ticket_id = Column(Integer, ForeignKey('Tickets.id'))
