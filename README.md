# HTTPE - High Throughput Transaction Processing Engine

HTTPE is a distributed fintech transaction processing engine designed to simulate high-throughput payments and P2P transfers with low latency, reliability, and scalability.

## Features
- FastAPI API Gateway and Payment Service
- Wallet creation, deposit, and transfer APIs
- PostgreSQL for ACID-compliant transaction storage
- Redis for idempotency and caching
- Kafka for event-driven transaction processing
- Kafka worker for async event consumption
- Load testing simulator for TPS benchmarking

## Run
1. docker compose up -d
2. python -m payment_service.init_db
3. uvicorn payment_service.main:app --reload --port 8001
4. uvicorn gateway.main:app --reload --port 8000
5. python -m simulator.run_sim
