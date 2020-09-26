Redis is ridiculously useful to be used as a cache for application-level data (and some people dare to use it as a db too. Brave brave people). But a single redis node, with somewhat ephemeral data going down frequently would negatively impact the performance of the application which will depend on that. 

Redis Labs presents a couple of solutions, Namely Redis-cluster and Redis-sentinel.


## Partitioning in Redis
- This is notes for this page - https://redis.io/topics/partitioning
- Contains multiple single redis nodes - say R0, R1 and R2
- For every key that needs to be inserted, it first selects the correct instance and then adds it into it. 
- Sharding is a type of Partitioning, wherein you divide up a single entity across different machines (Think database partitioning with a database-table in another machine). There are some [wonderful answers here in this question](https://stackoverflow.com/questions/20771435/database-sharding-vs-partitioning)
- Is this partitioning such a difficult thing to do? It's basically something that the application side can do itself right?
	- That depends. If the data contains inherently paritionable (don't know if that's a word) data, then that logic must be on the application side.
	- That kind of means more work

There are different types of partitioning - 
- Application level partitioning - The application data does it's own thing
- Proxy level partitioning - The application writes to redis like it normally would, but there is a proxy between the application and the redis instance. Think of it like a load-balancer, that'll route to the correct redis instance.
- Auto-partition by redis - Redis will tell the client where to make the request. Apparently Redis Cluster does this

NOTE: That the paritioning logic mentioned above is not specific - It can be consistent or inconsistent. The beauty of using Redis as a cache is that in-consistent hashing can be applied, so that 2 different instances can have the same data. This would make the logic for determining the instance extremely simple and won't be a bottleneck. This would also mean that if an instance goes down, or a new one is added, it's fair game. Inconsistent hashing basically would mean that the proxy would effectively act like a load-balancer.

But in the case of Redis being used as a data-store. That would mean that everytime you look up something, the proxy needs to know exactly where to look for it. This would mean that the redirection to a partition must follow consistent hashing. If it used inconsistent hashing then it wouldn't find the data most of the time and fail. That's not a good data-store. This took time for me to understand, and I had to spell it out here just so that I get it in the future.

Due to this problem with using Redis as a data-store, we need to use fixzed number of nodes, with a fixed keys to node map, using consistent hashing. Everytime an event happens, wherein a node goes down, or comes back up, the keys need to be redistributed, and the hashing algorithm needs to account for all the changes. This seems like a lot of work. Redis Cluster automatically does all of this for us apparently.


## Redis Cluster
- Notes for this page - https://redis.io/topics/cluster-tutorial
- It partitions your redis data into different logical and/or physical redis instances, and manages accessing them.
- This is built for performance, for a large amount of data being used in Redis
- In the event of partial node failures, This gives the ability for a subset of your application to continue using Redis instances that have not gone down
- In a cluster too, there are replicasets available
- Lookup Redis cluster sharding section to get an idea of how the sharding happens internally (It's pretty simple to be honest, expected something more complex)


### Redis cluster sharding
- Does not use consistent hashing (key to instance map not available)
- Given a key - `hash = CRC16($key) % 16384` 
	- Question - why 16384? 
	- It's 2^14. What does that signify though?
	- Does this mean we can have a total of 16384 clusters that redis can handle?
	- But why that number though? Is there a field inside the redis cluster management tool around 14 bits or something? This seems like the most likely thing. Also 16384 is a lot of instances. But if there are products that have that requirement, then cool. Not envying that person who's managing that at all :p 
- So given N instances, the N0 instance will take up - `0 - hash/N`, N1 - `hash/N : 2*(hash/N)`, N2 - `2*(hash/N) - 3 * (hash/N)`; Given any Nx it's range will be - `x(hash/N) - (x+1)*(hash/N)`, with each instance holding `hash/N` keys.
- So whenever a new instance comes up, or we manually take down an instance, the keys are redistributed in the remaining instances. Note that not all keys would be redistributed. I believe this is why whenever restarting a cluster, it takes sometime (long time apparently) for the cluster to be functional since pre-sharding of the existing keys happens across all the instances of the cluster
	- But this is contrary what is being said - `Because moving hash slots from a node to another does not require to stop operations, adding and removing nodes, or changing the percentage of hash slots hold by nodes, does not require any downtime.`
	- I've got to understand this statement better


## Redis cluster replication
- Each instance can have replicas of itself. There can be mulitple replicas for an instance.
- If an instance goes down, then it's replica can take it's place. 
- Note that the instance and the replicas might not be in the same state all the time. 
- Redis does not guarantee strong consistency between the instances and replicas.
- The reason for this is that it writes to the replicas asynchronously. If it wrote ynchronously, then the client application would need to wait for a particular key to be written to the instance and all it's replicas, before getting back control. Apparently, this is a bottleneck
- There are situations where if an instance goes down and it's replica is set up as the primary-instance, then it is not the exact state that of the instance that went down. It might a bit old, because there would've been some writes which were missed (maybe it was being written when the replica was turned into a primary, maybe there was temporary network partioning for sometime, and the replica has some data that is missing during that period)
- Implementation details are on the site. It seems really simple though. Love their simplicity for everything

## Redis Sentinel
- Referring to this guide - https://redis.io/topics/sentinel
- Although Redis Cluster is a solution to sharding a large amount of data into different redis instances, it still has the problem of availability.
- Redis Sentinel is a solution to that. 
- Sentinel also providers monitoring, notifications and config provider for clients (microservices can hit a Redis Sentinel for discovering other services. Sentinel will be the source of truth)
- There could be multiple Sentinel processes cooperating with each other
- So in a Redis Sentinel distributed system, you'll have Sentinel processes, Redis instances (some primary, some replicas) and client applications.
- Sentinel processes basically look out for the functioning of the Redis instances.
- In order to start Sentinel processes, we need to provide a configuration file, with only the details about the primary instances
- QUESTION - I wonder how redis auto-discovers the replicas? It does not. When starting a replica, you have to state that something is a replica of something.
- The main line in the config file is - 
  ```sentinel monitor <master-group-name> <ip> <port> <quorum>```
- The sentinel processes mark the instance with the given ip-port as primary.
- The quorum field is important. Quorum is basically the number of Sentinel processes that need to agree so that the primary is marked as failing. Note that Quorum only talks about the pre-condition for failure. Not for starting failover.
- So if the command looks like - `sentinel monitor random-master 127.0.0.1 6739 2` where the quorum is 2
- The `random-master` will be marked as failure if atleast 2 sentinel processes fail to reach it.
- Either of the 2 sentinel processes are eligible to start the fail-over. There needs to be an election to determine the Sentinel process responsible to start the fail-over.
- If there are a total of 5 Sentinel processes, and there's a network partition of 2 and 3 nodes, the failover will not start from the minority paritition (the 2 nodes partition).
- I think this is so that there aren't multiple copies of primary instance.
- The working of Sentinel failovers heavily depends upon the configuration. Since it is a distributed system, different configurations can deliver different results

The "Quick Tutorial" section in the redis guide is quite amazing. It's very simple to do. Some pain-points that I encountered - 
- My redis-sentinels were not discovering each other. At first I thought it's because of the garbage I have inside `etc/hosts` but that was not the case. Seems like it needs to run on ports which are not being used elsewhere (also, Yes, multiple processes [can listen on the same TCP/UDP port apparently under some configuration](https://stackoverflow.com/a/8824852/1518924))
- For some reason I somehow misunderstood that I just have to setup multiple redis instances by simply running `redis-server` and by virtue of sentinel configuration, it'll pick the primary and make the other one the replica. This is not true. Make sure to set the replicas explicitly - `$ redis-server --port 10002 --replicaof 127.0.0.1 10001`

- [QUESTION] How will using redis-sentinel with client libraries work? There needs to be a persistent connection with a sentinel and then changes to primary, and other things. I am not super sure of that.

## Understanding Redis Persistence
- Referring this first - http://oldblog.antirez.com/post/redis-persistence-demystified.html

An oversimplied view of writing from application layer to disk
- Application writes to DB (redis in this case)
- Db calls a system call to write the data into the disk. This system call sends the data into the kernel buffer
- The OS writes the data into the disk-controller, the kernel buffer is flushed into the disk-cache
- From the disk-cache the data is finally written into physical disks by the disk controller

All I notice here is a bunch of abstractions that are introduced so that any kind of mix and match will work as intended (different physical disk, different OS, different DB, different application). This realization is important.

Another important thing to note here is that the buffer is important otherwise waiting to write to the physical disk is slow

One important distinction to have in mind when thinking about persistence - using write and fsync.
When a user-process calls write, the data is moved from the user-space to the kernel space. That's it. In the kernel space, it would be in a buffer. So when the write returns, there's no guarantee that the data has actually been persisted on the disk (Depends on how often the OS flushes the buffer onto the disk. Linux apparently does this every 30 seconds (doesn't that seem like a long time though?)). So this would mean that if after a write operation is performed, and the process crashes/fails, we can be sure that the data is not lost, and will be written to the disk in eventually. But if after write operation, there's a power-loss, then there could be a possibility of data-loss, since the data might still be in the kernel buffer, and not flushed entirely into the disk.

Fsync solves this. Fsync returns when we know that the data is written to the disk completely. This is what dbs use. This protects against power failures, the way write call cannot. Note that this is an expensive operation. Here's a [good answer](https://stackoverflow.com/a/10371152/1518924) that illustrates this. Note that if at the disk level, there's another disk buffer or something like that, then fsync might fail too! (Soo many buffers!)

What the DBs can possibly do to when data-corruption is identified - 
- If there is heavy replication, the client can be told to use a replica (I guess this works for downtime as well)
- Store the sequence of commands that change the state of the db. Can possibly revert all the commands to some point before corruption.
- The root of corruption is modifying something in-place. If the DB is append-only, then we are basically un-corruptible

Redis provides 2 ways to prevent corruption - 

#### Snapshotting
- Take data-dumps of the db based on a certain set of conditions - 
	- Time passed
	- Number of writes
- Taking Snapshots can cause some data-loss, depending on the conditions encountered on the said snapshot. If the snapshot is taken every 15 mins, then we should be ready to lose 15 mins of user-data, when data-corruption or failure happens.
- For primary-replica synchronization, Snapshots are used.

#### Append Only File
- For any kind of write operation, an AOF is created, that'll append the commands onto a file. The operative keyword here is not just "write" but anything that actually modifies the existing data-set. So deleting a key that does not exist, does not update the AOF file.
- This file can be re-run on restart of an instance
- AOF is an always growing file
- If the AOF gets too big (I guess there is a configuration somewhere that controls this size), the process to create a new AOF is initiated.
- This new AOF is created from the data in the memory (This is similar to an rdb dump, but with commands I guess)
- The new data is written to the disk using fsync, replacing the old one. While the rewrite process is going on, the new commands are written to the old AOF file and also a temporary user-buffer which will be written into the new rewrite AOF before fsyncing.
- We can control the rate at which the AOF is populated by tuning the appendfsync command. This basically tunes how often fsync is run. The most optimal way (with regard to how expensive fsync is vs how durable we want our system to be) is to use `appendfsync everysec`
- Using `appendfsync always` is apparently akin to using a database. Although I am not sure about this comparision, since this is talking about backups. But I think the underlying point is about persistence so, I guess it's a fair compaision to make.


## Redis pipeling vs transactions vs scripting
- Refer this - https://rafaeleyng.github.io/redis-pipelining-transactions-and-lua-scripts
- An important thing to remember here is that redis is single-threaded

### Pipelining
- This is batching. Send a bunch of commands to run, and then get the responses all together. 
- Saves a lot of network time
- The whole pipeline is not atomic
- If there's an error, the next command will be run as usual
- No way to use intermediate responses

### Transactions
- Refer to this as well - https://redis.io/topics/transactions
- The whole set of commands is atomic
- There will be no commands from other client being run when a transaction is being performed
- The commands will be queued one by one, and will be executed at once using the EXEC
- If for some reason we don't need the transaction anymore, we can run DISCARD (I think that can be used for checkout pages or something like that)
- Transactions are aborted if there are errors that happen while queuing or while exec-ing
- No way to use intermediate responses

### Lua scripts,
- The entire running of the script is atomic, much like a transaction 
- Can use intermediate responses
- Basically does everything the other 2 don't (Haha)











