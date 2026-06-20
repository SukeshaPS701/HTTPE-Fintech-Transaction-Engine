# HTTPE System Architecture

## Flow Diagram

Client
  ↓
API Gateway (FastAPI - 8000)
  ↓
Payment Service (8001)
  ↓
PostgreSQL (Sharded)
  ↓
Redis Cache Layer
  ↓
Kafka Event Stream

---

## Components

### 1. API Gateway
- Entry point
- Load balancing
- Request forwarding

---

### 2. Payment Service
- Wallet management
- Transfers
- Transaction validation
- ACID compliance

---

### 3. PostgreSQL
- Stores wallets
- Stores transactions
- Sharded by user_id

---

### 4. Redis
- Idempotency keys
- Fast lookups
- Reduces DB load

---

### 5. Kafka
- Event streaming
- Transaction logs
- Async processing

---

## Scalability

- Stateless microservices
- Horizontal scaling
- Partitioned database
- Event-driven architecture

---

## Fault Tolerance

- DB rollback on failure
- Kafka retry mechanism
- Redis TTL expiration