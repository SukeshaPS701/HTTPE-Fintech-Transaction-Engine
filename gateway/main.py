from fastapi import FastAPI
from fastapi import HTTPException
from gateway.health import router as health_router

import requests


app = FastAPI(
    title="HTTPE API Gateway"
)
app.include_router(health_router)

PAYMENT_SERVICE = "http://localhost:8001"


@app.get("/")
def home():

    return {
        "gateway": "running",
        "payment_service": PAYMENT_SERVICE
    }


@app.post("/wallet/create")
def create_wallet(payload: dict):

    response = requests.post(
        f"{PAYMENT_SERVICE}/wallet/create",
        json=payload
    )

    return response.json()


@app.post("/wallet/deposit")
def deposit(payload: dict):

    response = requests.post(
        f"{PAYMENT_SERVICE}/wallet/deposit",
        json=payload
    )

    return response.json()


@app.get("/wallet/{user_id}")
def get_wallet(user_id: int):

    response = requests.get(
        f"{PAYMENT_SERVICE}/wallet/{user_id}"
    )

    return response.json()


@app.post("/transfer")
def transfer(payload: dict):

    response = requests.post(
        f"{PAYMENT_SERVICE}/transfer",
        json=payload
    )

    return response.json()


@app.get("/transactions/{user_id}")
def transactions(user_id: int):

    response = requests.get(
        f"{PAYMENT_SERVICE}/transactions/{user_id}"
    )

    return response.json()