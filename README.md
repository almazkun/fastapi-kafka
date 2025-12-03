## 5-Day Kafka & FastAPI Course

![kafka](https://upload.wikimedia.org/wikipedia/commons/b/b4/Kafka.jpg)

**Day 1 — Architecture & Mental Models**
* Why event-driven beats request-response for specific problems
* Kafka's distributed log model vs message queues
* Core components: brokers, topics, partitions, replication factor
* Consumer groups and partition assignment strategies
* Message ordering guarantees and delivery semantics (at-most-once, at-least-once, exactly-once)
* Local stack: Docker Compose with Kafka, Zookeeper/KRaft, Schema Registry
* FastAPI async foundations: when to use background tasks vs separate consumers
* **Lab**: Spin up local environment, produce/consume via CLI

**Day 2 — Producer Patterns & Schema Evolution**
* Event design: granularity, naming conventions, schema-first approach
* Avro/Protobuf schema definition and evolution rules
* Producer configurations: acks, idempotence, batching, compression
* FastAPI integration patterns: sync endpoints with async producers
* Transactional producers for atomic multi-topic writes
* Handling network failures and retry logic
* **Lab**: Build order processing API with schema-validated events, test idempotency

**Day 3 — Consumer Engineering & Offset Management**
* Manual vs auto-commit tradeoffs and exactly-once consumption
* Building FastAPI background workers vs standalone consumer services
* Partition rebalancing: cooperative sticky assignor behavior
* Error handling strategies: retry topics, dead letter queues, circuit breakers
* Graceful shutdown and in-flight message handling
* Processing guarantees: deduplication, transactional reads
* **Lab**: Build inventory update consumer with manual commits, implement DLQ pattern

**Day 4 — Production Operations & Performance**
* Horizontal scaling: stateless producers, consumer group expansion
* Performance tuning: fetch sizes, poll intervals, linger.ms, batch.size
* Monitoring stack: JMX metrics, consumer lag tracking, offset monitoring
* Kafka Connect for database CDC and external system integration
* Stream processing patterns: joins, windowing, state stores (intro to Kafka Streams/Flink)
* Testing strategies: Testcontainers, mock producers/consumers, contract testing
* **Lab**: Scale consumer group, implement metrics collection, performance benchmark

**Day 5 — Security, Reliability & System Design**
* Authentication: SASL/SCRAM, mTLS configuration
* Authorization: ACLs and RBAC patterns
* Encryption: in-transit (SSL) and at-rest considerations
* Disaster recovery: topic replication, backup strategies, failover procedures
* Chaos engineering: partition failures, broker crashes, network splits
* Cloud deployment: MSK, Confluent Cloud, self-managed tradeoffs
* **Capstone**: Design multi-service event-driven system (payment processing or order fulfillment)
  - Event storming exercise
  - Schema design across 3+ services
  - Implement with failure injection
  - Load testing and observability dashboard
