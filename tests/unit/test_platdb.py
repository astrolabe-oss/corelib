# Need to disable this for the DoesNotExist exceptions. I think the 
# neomodels work by creating this dynamically so pylint does not really 
# deal with it right.
# pylint: disable=no-member

# Neo4jConnection seem like they are unused arguments but they are the
# DB connection objects that were yielded to the function.
# pylint: disable=unused-argument

import datetime

import pytest

from neomodel import ZeroOrMore

from tests.conftest import neo4j_db_fixtures

from corelib.platdb import Insights, PlatDBNode, StructuredNode


def test_delete_by_attributes_object_does_not_exist(mocker):
    # arrange
    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    attributes = {"name": "nonexistant"}
    mock_nodes.get.side_effect = PlatDBNode.DoesNotExist(msg=None)

    # act
    result = PlatDBNode.delete_by_attributes(attributes=attributes)

    # assert
    assert result is False


def test_delete_by_attributes_object_exists(mocker):
    # arrange
    attributes = {}

    mock_obj = mocker.Mock(spec=PlatDBNode)
    mock_obj.name = "a name"
    mock_obj.delete.return_value = True

    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    mock_nodes.get.return_value = mock_obj

    mock_delete = mocker.patch.object(StructuredNode, "delete",
                                      return_value=True)

    # act
    result = PlatDBNode.delete_by_attributes(attributes=attributes)

    # assert
    mock_delete.assert_called_once()
    assert result is True


def test_update_object_does_not_exist(mocker):
    # arrange
    attributes = {"name": "app1"}
    new_attributes = {"name": "new_app1"}

    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    mock_nodes.get.side_effect = PlatDBNode.DoesNotExist(msg=None)

    # act
    result = PlatDBNode.update(attributes, new_attributes)

    # assert
    assert result is None


def test_update_object_exists(mocker):
    # arrange
    name_orig, data_orig, rel_orig = "app1", 5, "app2"
    name_update, data_update, rel_update = "app1", 10, "app10"
    node_orig = {"name": name_orig, "data": data_orig, "relationship": rel_orig}
    node_update = {"name": name_update, "data": data_update, "relationship": rel_update}

    mock_obj = mocker.Mock(spec=PlatDBNode)
    mock_obj.name = name_orig
    mock_obj.data = data_orig
    mock_obj.relationship = rel_orig
    mock_obj.save.side_effect = lambda x: None

    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    mock_nodes.get.side_effect = mock_obj

    # act
    obj = PlatDBNode.update(node_orig, node_update)

    # assert
    assert obj.name == name_update
    assert obj.data == data_update
    assert obj.relationship == rel_update


def test_insights_save(mocker):
    # arrange
    insight = Insights()
    mocker.patch.object(PlatDBNode, "save")

    # act
    insight.save()

    # assert
    assert isinstance(insight.updated, datetime.datetime)
    assert isinstance(insight.updated.year, int)
    assert isinstance(insight.updated.month, int)
    assert isinstance(insight.updated.day, int)
    assert insight.updated.tzinfo is datetime.timezone.utc


@pytest.mark.parametrize('cls,attrs,updated_attrs', neo4j_db_fixtures)
def test_platdb_node_to_dict_for_all_classes(mocker, cls, attrs, updated_attrs):
    obj = cls(**attrs)
    rel = []

    mocker.patch.object(ZeroOrMore, 'all', return_value=rel)

    platdb_ht = obj.platdbnode_to_dict()

    for key, value in platdb_ht.items():
        if key in attrs:
            assert value == attrs[key]
        elif key in attrs:
            # This could be a relationship or a None object if it was a 
            # class value that was left blank
            assert value in (rel, None), f'key: {key}, value: {value}'
