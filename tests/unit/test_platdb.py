"""Need to disable this for the DoesNotExist exceptions. I think the 
neomodels work by creating this dynamically so pylint does not really 
deal with it right."""
# pylint: disable=no-member

import datetime

from corelib.platdb import Insights, PlatDBNode, StructuredNode

def test_delete_by_attributes_object_does_not_exist(mocker):
    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    attributes = {"name" : "nonexistant" }
    mock_nodes.get.side_effect = PlatDBNode.DoesNotExist(msg=None)

    result = PlatDBNode.delete_by_attributes(attributes=attributes)

    assert result is False

def test_delete_by_attributes_object_exists(mocker):
    attributes = {}

    mock_obj = mocker.Mock(spec=PlatDBNode)
    mock_obj.name = "a name"
    mock_obj.delete.return_value = True

    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    mock_nodes.get.return_value = mock_obj

    mock_delete = mocker.patch.object(StructuredNode, "delete",
                                      return_value=True)

    result = PlatDBNode.delete_by_attributes(attributes=attributes)

    mock_delete.assert_called_once()
    assert result is True

def test_update_object_does_not_exist(mocker):
    # Attributes are really just placeholders
    attributes = {"name" : "app1" }
    new_attributes = {"name" : "new_app1" }

    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    mock_nodes.get.side_effect = PlatDBNode.DoesNotExist(msg=None)

    result = PlatDBNode.update(attributes, new_attributes)

    assert result is None

def test_update_object_exists(mocker):
    # Attributes are just placeholders
    attributes = {"name" : "app1", "data" : 5, "relationship" : "app2"}
    new_attributes = {"name" : "new_app1", "data" : 10, "relationship" : "app2"}

    mock_obj = mocker.Mock(spec=PlatDBNode)
    mock_obj.name = "app1"
    mock_obj.data = 5
    mock_obj.relationship = "app2"
    mock_obj.save.side_effect = lambda x: None

    mock_nodes = mocker.patch.object(StructuredNode, "nodes")
    mock_nodes.get.side_effect = mock_obj

    obj = PlatDBNode.update(attributes, new_attributes)

    assert obj.name != "app1"
    assert obj.name == "new_app1"
    assert obj.data != 5
    assert obj.data == 10
    assert obj.relationship == "app2"

def test_insights_save(mocker):
    insight = Insights()
    mocker.patch.object(PlatDBNode, "save")

    insight.save()

    assert isinstance(insight.updated, datetime.datetime)
    assert isinstance(insight.updated.year, int)
    assert isinstance(insight.updated.month, int)
    assert isinstance(insight.updated.day, int)
    assert insight.updated.tzinfo is datetime.timezone.utc
