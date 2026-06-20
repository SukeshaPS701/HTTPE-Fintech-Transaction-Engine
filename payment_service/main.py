from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Header
from prometheus_client import Counter, generate_latest
from fastapi import Response

from sqlalchemy.orm import Session

from payment_service.database import SessionLocal
from payment_service.models import Wallet
from payment_service.models import Transaction

from payment_service.redis_client import redis_client
from payment_service.kafka_producer import publish_transaction

from payment_service.schemas import (
    WalletCreate,
    DepositRequest,
    TransferRequest
)

app = FastAPI(
    title="HTTPE Payment Service"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "service": "HTTPE Payment Service",
        "status": "running"
    }


@app.post("/wallet/create")
def create_wallet(
    data: WalletCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Wallet).filter(
        Wallet.user_id == data.user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Wallet already exists"
        )

    wallet = Wallet(
        user_id=data.user_id,
        balance=0
    )

    db.add(wallet)
    db.commit()

    return {
        "message": "wallet created",
        "user_id": data.user_id
    }


@app.post("/wallet/deposit")
def deposit(
    data: DepositRequest,
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.user_id == data.user_id
    ).first()

    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    wallet.balance += data.amount

    db.commit()
    db.refresh(wallet)

    return {
        "user_id": wallet.user_id,
        "balance": wallet.balance
    }


@app.get("/wallet/{user_id}")
def get_wallet(
    user_id: int,
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id
    ).first()

    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    return {
        "user_id": wallet.user_id,
        "balance": wallet.balance
    }


@app.post("/transfer")
def transfer(
    data: TransferRequest,
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None)
):

    # Idempotency Check
    if idempotency_key:

        existing = redis_client.get(
            f"tx:{idempotency_key}"
        )

        if existing:
            return {
                "status": "duplicate_request"
            }

    sender = db.query(Wallet).filter(
        Wallet.user_id == data.sender_id
    ).with_for_update().first()

    receiver = db.query(Wallet).filter(
        Wallet.user_id == data.receiver_id
    ).with_for_update().first()

    if not sender:
        raise HTTPException(
            status_code=404,
            detail="Sender wallet not found"
        )

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Receiver wallet not found"
        )

    if sender.balance < data.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )

    try:

        sender.balance -= data.amount
        receiver.balance += data.amount

        tx = Transaction(
            sender_id=data.sender_id,
            receiver_id=data.receiver_id,
            amount=data.amount,
            status="SUCCESS"
        )

        db.add(tx)

        db.commit()

        if idempotency_key:
            redis_client.set(
                f"tx:{idempotency_key}",
                "processed",
                ex=3600
            )

        publish_transaction({
            "event": "TRANSFER_COMPLETED",
            "sender": data.sender_id,
            "receiver": data.receiver_id,
            "amount": data.amount
        })

        return {
            "status": "SUCCESS",
            "sender": data.sender_id,
            "receiver": data.receiver_id,
            "amount": data.amount
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/transactions/{user_id}")
def get_transactions(
    user_id: int,
    db: Session = Depends(get_db)
):

    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user_id) |
        (Transaction.receiver_id == user_id)
    ).all()

    return transactions
REQUEST_COUNT = Counter(
    "httpe_requests_total",
    "Total requests"
)
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
REQUEST_COUNT.inc()
