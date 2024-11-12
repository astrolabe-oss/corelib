# CoreLib: Astrolabe <--> Neo4j Integration

## About 

CoreLib is a Python module intended for integrating Neo4j with [Astrolabe](https://github.com/astrolabe-oss/astrolabe). 
CoreLib is written using [neomodel](https://github.com/neo4j-contrib/neomodel)
which is a Neo4j OGM that allows for OOP to be leveraged with the Neo4j database.

CoreLib contains:
* Mechanism for connection to Neo4j.
* Classes used to represent various infrastructure components.
    * All infrastructure classes are child classes of the PlatDB parent class.

## Prerequisites 

* \>=Python3.10

## Contributing

### Notes

* Adding new infrastructure/PlatDB classes is currently not supported in
Astrolabe. Astrolabe is tied to relying on certain classes.
* Astrolabe currently only makes use of a limited amount of PlatDB classes:
Application, Compute, Deployment, Resource, and TrafficController. Contributions
to these classes can be supported as well as the parent classes.

### Unit Tests

Follow contribution guidelines for tests in 
[Astrolabe](https://github.com/astrolabe-oss/astrolabe?tab=readme-ov-file#contributing).

### Integration Tests

Integration tests come with a _docker-compose.yml_ file for running a test 
instance of Neo4j.