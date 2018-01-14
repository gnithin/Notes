# Kafka basics 

Source - https://www.tutorialspoint.com/apache_kafka/apache_kafka_introduction.htm

- It's a distributed pub-sub

- What is stream processing?

- What is a broker, in pub-sub?
	- Broker is the component that publishers write to and the subscribers read from
	- Kafka has multiple brokers, called a kafka cluster, to perform load balancing.

- What is zookeeper?
	- Each kafka cluster is a collection of brokers. each broker is stateless.
	- I am assuming that also means they are not aware of other brokers in the system
	- They have a leader and others are followers
	- The synchronization between different brokers inside a kafka cluster is done by zookeeper

- Each message has an id called an offset


Source - https://kafka.apache.org/intro

- I did not quite understand how connectors API would work
- Is the streams API a kind of ETL? It is a kind of transformer between services

- "Kafka's performance is effectively constant with respect to data size so storing data for a long time is not a problem." How does this work?

- In fact, the only metadata retained on a per-consumer basis is the offset or position of that consumer in the log. This offset is controlled by the consumer: normally a consumer will advance its offset linearly as it reads records, but, in fact, since the position is controlled by the consumer it can consume records in any order it likes. 

### Producers -
- The producer is responsible for choosing which record to assign to which partition within the topic. 
- This can be done in a round-robin fashion simply to balance load or it can be done according to some semantic partition function (say based on some key in the record).

### Mixing of queing and pub-sub
- If for one topic, there are N consumer-groups. Each message in that topic goes to every consumer-group (aka broadcasting, like a pub-sub)
- When a consumer group receives a message, it's alloted to one consumer instance. Not to multiple. This is similar to the queuing model.

## Unresolved questions -

- What exactle do streams mean?
	- Do they mean a sequence of bytes? Like the C++ iostream?
- What are streams of records?
	- Do they mean a sequence of records?
	- Why not use the word sequence of records? Maybe it's not that then. Hmm...
- [RESOLVED] Kafka only provides a total order over records within a partition, not between different partitions in a topic. Per-partition ordering combined with the ability to partition data by key is sufficient for most applications. However, if you require a total order over records this can be achieved with a topic that has only one partition, though this will mean only one consumer process per consumer group. 
	- Does this mean, that number of consumer instances in a consumer group for a topic has an upper-limit of total number of partitions for a topic?
	- Yes it is - "Note however that there cannot be more consumer instances in a consumer group than partitions."

- What is HDFS?
	- Got something to do with hadoop right?