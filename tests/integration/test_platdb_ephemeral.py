import pytest

from neomodel import db

from corelib.platdb import (Neo4jConnection, Application, CDN, Compute,
                            Deployments, EgressController, Insights, Repo,
                            Resource, TrafficControllers)

# Neo4jConnection seem like they are unused arguments but they are the
# DB connection objects that were yielded to the function.
# pylint: disable=unused-argument

neo4j_db_fixtures = [
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


@pytest.fixture(autouse=True)
def clear_database(neo4j_connection):
    db.cypher_query("MATCH (n) DETACH DELETE n")
    yield
    db.cypher_query("MATCH (n) DETACH DELETE n")


@pytest.mark.parametrize('neomodel_class, create_attrs, update_attrs', neo4j_db_fixtures)
def test_create(neomodel_class, create_attrs, update_attrs):
    # arrange/act
    obj = neomodel_class(**create_attrs).save()

    # assert
    for key, value in create_attrs.items():
        assert getattr(obj, key) == value


@pytest.mark.parametrize('neomodel_class, create_attrs, update_attrs', neo4j_db_fixtures)
def test_read(neomodel_class, create_attrs, update_attrs):
    # arrange
    neomodel_class(**create_attrs).save()

    # act
    read_obj = neomodel_class.nodes.get(**create_attrs)

    # assert
    for key, value in create_attrs.items():
        assert getattr(read_obj, key) == value


@pytest.mark.parametrize('neomodel_class, create_attrs, update_attrs', neo4j_db_fixtures)
def test_update(neomodel_class, create_attrs, update_attrs):
    # arrange
    neomodel_class(**create_attrs).save()

    # act
    updated_obj = neomodel_class.update(create_attrs, update_attrs)

    # assert
    assert updated_obj is not None
    for key, value in update_attrs.items():
        assert getattr(updated_obj, key) == value


@pytest.mark.parametrize('neomodel_class, create_attrs, update_attrs', neo4j_db_fixtures)
def test_delete(neomodel_class, create_attrs, update_attrs):
    # arrange
    neomodel_class(**create_attrs).save()

    # act
    assert neomodel_class.delete_by_attributes(attributes=create_attrs)