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
- There are situations where if an instance goes down and it's replica is set up as the master, then it is not the exact state that of the instance that went down. It might a bit old, because there would've been some writes which were missed (maybe it was being written when the replica was turned into a master, maybe there was temporary network partioning for sometime, and the replica has some data that is missing during that period)
- Implementation details are on the site. It seems really simple though. Love their simplicity for everything

## Redis Sentinel
TODO


