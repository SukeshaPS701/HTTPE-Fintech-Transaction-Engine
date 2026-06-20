# HTTPE Capacity Planning

## Target System Load

- Target TPS: 12,000 transactions/sec
- Peak multiplier: 1.5x (18,000 TPS peak)

---

## System Breakdown

### API Gateway
- Handles routing only
- Capacity: 50,000 req/sec
- Stateless → horizontally scalable

---

### Payment Service

- Target: 12,000 TPS
- 4 instances → 3,000 TPS each

---

### PostgreSQL (Sharded)

- 2 shards minimum
- Each shard handles ~6,000 TPS
- Write optimized indexes

---

### Redis

- Used for:
  - Idempotency keys
  - Cache wallet balances
- Expected hit ratio: 80%

---

### Kafka

- Throughput: 100K+ messages/sec
- Used for async transaction logging
- 3 partitions minimum

---

## Latency Budget

| Component | Latency |
|----------|--------|
| API Gateway | 2 ms |
| Service Logic | 10 ms |
| DB Write | 20 ms |
| Kafka Publish | 5 ms |
| Redis Check | 1 ms |

### Total P95 latency: ~38 ms

---

## Bottlenecks

- DB write contention
- Network IO
- Locking conflicts

---

## Scaling Strategy

- Horizontal scaling (stateless services)
- DB sharding
- Redis caching layer
- Kafka async processing