import pytest

from neomodel import db

from corelib.platdb import (Neo4jConnection, Application, CDN, Compute,
                            Deployments, EgressController, Insights, Repo,
                            Resource, TrafficControllers)

# Neo4jConnection seem like they are unused arguments but they are the
# DB connection objects that were yielded to the function.
# pylint: disable=unused-argument

# Pylint seems to be giving this error because the names of the fixtures
# are then reused as parameter names later, but that is how they have to
# be used...
# pylint: disable=redefined-outer-name

params = [
    (Application, {"name": "app1"}, {"name": "new_app1"}),
    (CDN, {"name": "cdn1"}, {"name": "new_cdn1"}),
    (Compute, {
        "platform": "ec2",
        "address": "1.2.3.4",
        "protocol": "TCP",
        "protocol_multiplexor": "80"
    }, {
        "name": "new_compute1",
        "platform": "k8s",
        "address": "pod-1234nv",
        "protocol": "HTTP",
        "protocol_multiplexor": "80"
    }),
    (Deployments, {
        "deployment_type": "auto_scaling_group"
    }, {
        "deployment_type": "target_group"
    }),
    (EgressController, {"name": "egress1"}, {"name": "new_egress1"}),
    (Insights, {
        "attribute_name": "attr1",
        "recommendation": "recommendation1",
        "starting_state": "state1",
        "upgraded_state": "state2"
    }, {
        "attribute_name": "new_attr1",
        "recommendation": "new_recommendation1",
        "starting_state": "new_state1",
        "upgraded_state": "new_state2"
    }),
    (Repo, {"name": "repo1"}, {"name": "new_repo1"}),
    (Resource, {"name": "resource1"}, {"name": "new_resource1"}),
    (TrafficControllers, {
        "access_names": "access1"
    }, {
        "access_names": "new_access1"
    })
]


@pytest.fixture(scope="module")
def neo4j_connection():
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "guruai11"
    driver = Neo4jConnection(uri=uri, auth=(username, password))
    driver.open()
    yield driver
    driver.close()


@pytest.fixture(scope="module", autouse=True)
def clear_database(neo4j_connection):
    db.cypher_query("MATCH (n) DETACH DELETE n")
    yield
    db.cypher_query("MATCH (n) DETACH DELETE n")


@pytest.fixture(scope="module", params=params)
def create_fixture(neo4j_connection, request):
    cls, attributes, new_name = request.param
    obj = cls(**attributes).save()
    return obj, cls, attributes, new_name


def test_create(create_fixture):
    obj, _, attributes, _ = create_fixture

    for key, value in attributes.items():
        assert getattr(obj, key) == value


def test_read(create_fixture):
    _, cls, attributes, _ = create_fixture

    read_obj = cls.nodes.get(**attributes)

    for key, value in attributes.items():
        assert getattr(read_obj, key) == value


def test_update(create_fixture):
    _, cls, attributes, new_attributes = create_fixture
    key = list(attributes.keys())[0]

    updated_obj = cls.update(attributes, new_attributes)
    assert updated_obj is not None

    for key, value in new_attributes.items():
        assert getattr(updated_obj, key) == value


def test_delete(create_fixture):
    _, cls, _, new_attributes = create_fixture

    assert cls.delete_by_attributes(attributes=new_attributes) is True


if __name__ == "__main__":
    pytest.main()
