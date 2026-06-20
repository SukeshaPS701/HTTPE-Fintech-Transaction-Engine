from pydantic import BaseModel


class WalletCreate(BaseModel):
    user_id: int


class DepositRequest(BaseModel):
    user_id: int
    amount: float


class TransferRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float