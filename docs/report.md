# HTTPE - High Throughput Transaction Processing Engine

## Overview
This project is a distributed fintech system designed to simulate and process high-volume financial transactions (12,000+ TPS target).

---

## Architecture

- API Gateway (FastAPI)
- Payment Service (FastAPI)
- PostgreSQL (ACID transactions)
- Redis (cache + idempotency)
- Kafka (event streaming)
- Kafka Worker (async processing)

---

## Features

- Wallet creation system
- Deposit and transfer functionality
- ACID-compliant transactions
- Idempotency handling using Redis
- Event-driven architecture using Kafka
- Load testing simulator with concurrency
- TPS measurement system

---

## Load Testing

- Multi-threaded transaction simulator
- Concurrent request execution
- TPS calculation
- Failure tracking

---

## Observability

- Prometheus metrics endpoint
- Grafana dashboard support
- Kafka UI monitoring

---

## Fault Tolerance

- Transaction rollback on failure
- Kafka retry mechanism
- Request timeout handling
- Safe database sessions

---

## Tech Stack

Python, FastAPI, PostgreSQL, Redis, Kafka, Docker, Prometheus, Grafana

---

## Conclusion

This system demonstrates a scalable, distributed fintech architecture with real-world concepts such as microservices, event-driven design, and high-throughput simulation.