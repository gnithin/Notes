# Understanding Dgraph queries

- Trying to understand the querying structure of dgraph, by following the [tour](https://tour.dgraph.io/)

NOTE: I think I've worked on this atleast 3 times in the past 1 year and I keep forgetting it. Used it heavily for something, then abandoning it altogether. Pretty sure that my memory is the problem here. Jotting down notes to make this more concrete.

- A graph contains nodes and edges. Each of those entities can have properties of their own. Think of nodes and edges to be objects, and properties akin to actual properties of an object. This database allows us to store stuff in this format.

## Queries 
- Making a query 
    ```
    {
        myFunc(func: eq()){
            <predicate-name>
        }
    }
    ```
    - Think of it as calling a function by passing a function pointer to it
    - The func: here is called the node-filtering function 
- Helpful in debugging 
    - Printing all the edge names (predicates) `_predicate`
    - Printing all the connected predicates and values - `expand(_all_)`
    - Printing the number of outgoing edges - `count(friend)`
- In a graph, the objects (or entities) are called nodes and the relationships are called edges or predicates.
- The RDF specifies - `<node1> <predicate> <node2>`
- There apparently are two types of nodes
    - uid-nodes
    - propety-nodes
- All uid-nodes have a uid. Node1 is always a uid-node
- The node2 here are can be property-node, or itself a uid-node
- All property-nodes fall under a some form of a primitive type
- node-filters can only be applied to predicates that have been indexed
- When not used in the top level, filtering can be done using the @filter() method
- Use AND, OR, NOT to combine filters
- The root func: only accepts a single function and doesn’t accept AND, OR and NOT connectives as in filters. So the syntax (func: ...) @filter(... AND ...) is required when filtering on multiple properties at the root.
- [Explanation](https://tour.dgraph.io/basic/11/) about root-node 
- Alias for a predicate is like this - 
    ```
    {
      have_friends(func: has(friend)) {
        name@.
        age
        number_of_friends : count(friend)
      }
    }
    ```
- The `@cascade` directive removes any nodes that don’t have all matching edges in the query.
    - This is basically like a hard AND
- `@normalize` returns only those edges that have an alias, and flattens the response. Not really sure how they would do that in every type of query, but seems helpful to keep in mind
- Facets are dicts for predicates
    - You cannot have the same type of predicate between 2 nodes
    - If you try, you are going to over-write it
    - Use facets to add weights

- There are three types of deletes
    - Deleting single specific triplet `<0x13> <name> "Sarah" .`
    - Deleting triples for given edge `<0x13> <name> * .`
    - Deleting all predicates to a triple (and this removes the node itself) `<0x13> * * .`

## Migration 
- Follow [this](https://docs.dgraph.io/deploy/#fast-data-loading)
- Basically have a copy of the schema(non-gzipped) and the RDF(gzipped) file. Start both the zero graph and alpha graph.
- Run 
    ```
    $ dgraph live -r dgraph-1-2018-11-19-10-08.rdf.gz -s dgraph-1-2018-11-19-10-08.schema -d localhost:9080 -z localhost:5080
    ```
    - Note that `http` behind localhost does not work. I think that case needs to be handled properly, it's not specifically mentioned anywhere that only the host-name should be added
