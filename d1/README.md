# Architecture & Mental Models**

## Why event-driven beats request-response for specific problems
1. Decoupling: Producers don't care who listens. Services evolve independently, deployment stops stepping on each other, and downstream slowdowns don't freeze your API.

1. Resilience: If a consumer dies, event stays in the log. in req-res cycle, a blip becomes a failed call, in event-driven, it's usually just delayed work.

1. Throughput: Batching, partitioning, and parallel consumption let you process a hug workload without a swarm of synchronous HTTP call dragging the system down.

1. Elasticity: Need 10x processing power for a spike. Scale consumers horizontally. Producers barely feel the change.

1. Temporal Flexibility: Events can be replayed. You can rebuild state, audit behavior, and bootstrap new services without new APIs or backfills.

1. Loose Coupling of Workflows: Complex chains turn into simple publishes. Req-res spaghetti becomes a clean stream of facts the whole system can subscribe to.

1. Geo-friendly: Asynchronous pipelines tolerate latency far better than synchronous hops, making cross-region architecture practical. 

1. Ideal when:
    * Work is heavy or slow
    * Work happens later
    * Multiple systems needs the same fact
    * Failure must not drop data
    * Traffic is spiky

## Kafka's distributed log model vs message queues
1. Message queue: A message goes in, a consumer grabs it and poof - it's gone. One-time delivery, great for simple pipelines, but less so then multiple services need the same data or then you want to replay anything.

1. Kafka's distributed logs: Event's do not disappear. THey are written to an ordered, replicated log and stay there for configurable time (or forever). Every consumer group reads the same steam at its own pace, keeping its own offset. You are not pushing messages, you reading history. 

1. Key contrasts:
    * Fan-out vs single consumption: Queues deliver each message to exactly one consumer; Kafka lets unlimited groups read the same stream independently.
    * Replayability: Queues can't rewind; Kafka can replay events for debugging, reprocessing or feeding new services. 
    * Ordering: Queues often lose ordering under scale; Kafka preserves ordering within partition, giving predictable parallelism.
    * Throughput: Queues chock under massive firehouse workload; Kafka's append-only log, partitioning, and sequential dick writes crush high volume traffic.
    * State building: Queues push work; Kafka lets services materialize state by continuously reading the log.
    * Durability and retention: Queues drop messages ofter consumption. Kafka retains them, making the log a shared source of truth.

## Core components: brokers, topics, partitions, replication factor
1. Brokers: The servers. Each one stores chunk of the log, answers client requests, and keeps the cluster humming, aka "Data Librarians".

1. Topics: Names streams of events. Everything in Kafka flows into and out of topic. Topic is the category the log lives in.

1. Partitions: Slices of a topic. They give you parallelism, ordering guarantees, and scale. One partition - one ordered log. More partitions - more throughput.

1. Replication Factor: How many brokers hold copies of each partition. Higher replication - stronger fault tolerance, if one broker dies, another replica steps in with zero drama.


## Consumer groups and partition assignment strategies
1. Consumer Groups: A group is a team of consumers that share the work of a topic. Each partition is assigned to exactly *one* consumer *within* that group. Add consumers -> more parallelism. Remove consumers -> Kafka rebalances. Every group reads the topic independently of other groups. 
    - Why they matter:
        * Parallel Processing
        * Fault tolerance
        * Independent downstream workloads
        * Clean scaling patterns

1. Partition assignment strategies
    - Range: Splits partitions by consecutive ranges. Simple, predictable, but can create uneven loads when keys skew or partitions counts don't match consumer counts
    - Round Robin: Distributes 

## Message ordering guarantees and delivery semantics (at-most-once, at-least-once, exactly-once)
## Local stack: Docker Compose with Kafka, Zookeeper/KRaft, Schema Registry
## FastAPI async foundations: when to use background tasks vs separate consumers
## **Lab**: Spin up local environment, produce/consume via CLI