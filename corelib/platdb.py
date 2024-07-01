import datetime

from typing import Optional

from neo4j import GraphDatabase
from neomodel import (db, DoesNotExist, DateTimeProperty, FloatProperty,
                      RelationshipFrom, RelationshipTo, StringProperty,
                      StructuredNode)

class Neo4jConnection:
    def __init__(self, uri: str, auth: tuple[str, str]):
        self._uri = uri
        self._auth = auth

        self._driver = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self._driver = GraphDatabase.driver(self._uri, auth=self._auth)
        db.set_connection(self._uri, self._driver)

        # Clear sensitive information
        self._auth = None

        return self

    def close(self):
        self._driver.close()

class PlatDBNode(StructuredNode):
    __abstract_node__ = True  # prevents neo4j from adding `PlatDBNode` as a "label" in the graph db

    @classmethod
    def delete_by_attributes(cls, attributes: dict) -> bool:
        try:
            obj = cls.nodes.get(**attributes) # pylint: disable=no-member
            return super(PlatDBNode, obj).delete()
        except DoesNotExist:
            return False

    @classmethod
    def update(cls, attributes: dict, new_attributes: dict
               ) -> Optional["PlatDBNode"]:
        try:
            obj = cls.nodes.get(**attributes) # pylint: disable=no-member

            for key, value in new_attributes.items():
                setattr(obj, key, value)

            obj.save()

            return obj
        except DoesNotExist:
            return None

class Application(PlatDBNode):
    name = StringProperty(unique_index=True)

    application_to = RelationshipTo('Application', 'CALLS')
    application_from = RelationshipFrom('Application', 'CALLED_BY')
    compute = RelationshipFrom('Compute', 'RUNS')
    egress_controller = RelationshipTo('EgressController', 'DEPENDS_ON')
    insights = RelationshipFrom('Insights', 'APPLIES_TO')
    repo = RelationshipFrom('Repo', 'STORES')
    resources = RelationshipTo('Resource', 'USES')
    traffic_controllers = RelationshipTo('TrafficControllers', 'DEPENDS_ON')

class CDN(PlatDBNode):
    name = StringProperty()
    traffic_controllers = RelationshipTo('TrafficControllers', 'DEPENDS_ON')

class Compute(PlatDBNode):
    platform = StringProperty(required=True)
    address = StringProperty(required=True)
    protocol = StringProperty(required=True)
    protocol_multiplexor = StringProperty(required=True)

    name = StringProperty()
    applications = RelationshipTo('Application', 'RUNS')
    compute_to = RelationshipTo('Compute', 'CALLS')
    compute_from = RelationshipFrom('Compute', 'CALLED_BY')

class Deployments(PlatDBNode):
    deployment_type = StringProperty(choices={
        "auto_scaling_group": "Auto Scaling Group",
        "target_group": "Target Group",
        "k8s_deployment": "K8s Deployment"})
    applications = RelationshipTo('Application', 'PROVIDE')

class EgressController(PlatDBNode):
    name = StringProperty()
    applications = RelationshipFrom('Application', 'DEPENDS_ON')

class Insights(PlatDBNode):
    """Assuming id is managed internally by Neo4j as a unique identifier
    UniqueIdProperty can be used to generate a UUID but isn't a direct 
    analogue of an auto_increment field. For a direct MySQL 'id' 
    equivalent, you can use an IntegerProperty and manage it manually.
    """
    attribute_name = StringProperty(required=True)
    recommendation = StringProperty(required=True)
    starting_state = StringProperty(required=True)
    upgraded_state = StringProperty(required=True)
    min_improvement = FloatProperty()
    max_improvement = FloatProperty()
    note = StringProperty()

    # Automatically set to current date & time when created
    created = DateTimeProperty(default_now=True)

    # Automatically updated to current date & time when node is saved
    updated = DateTimeProperty(default_now=True)

    # Relationships
    applications = RelationshipTo('Application', 'APPLIES_TO')

    def save(self, *args, **kwargs):
        # Update the 'updated' property to current time when saving
        self.updated = datetime.datetime.now(datetime.timezone.utc)
        return super().save(*args, **kwargs)

class Repo(PlatDBNode):
    name = StringProperty()
    applications = RelationshipTo('Application', 'STORES')

class Resource(PlatDBNode):
    name = StringProperty()
    applications = RelationshipFrom('Application', 'USES')

class TrafficControllers(PlatDBNode):
    access_names = StringProperty()
    deployments = RelationshipTo('Deployments', 'DEPENDS_ON')
    applications = RelationshipFrom('Application', 'PROVIDE')
