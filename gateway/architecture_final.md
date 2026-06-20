# HTTPE FINAL ARCHITECTURE

Client
  ↓
API Gateway (FastAPI - 8000)
  ↓
Payment Service (FastAPI - 8001)
  ↓
PostgreSQL (Sharded DB)
  ↓
Redis (Idempotency + Cache)
  ↓
Kafka (Event Streaming)
  ↓
Kafka Worker (Async Processor)

---

## Observability Layer

Prometheus → Metrics Collection  
Grafana → Visualization Dashboard  
Kafka UI → Event Monitoring  

---

## Design Principles

- Microservices architecture
- Event-driven system
- Horizontal scalability
- Fault tolerance
- ACID compliance