from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from .database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, unique=True, index=True)

    balance = Column(Float, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    sender_id = Column(Integer, index=True)

    receiver_id = Column(Integer, index=True)

    amount = Column(Float)

    status = Column(String(50))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )