import datetime
import neo4j
import pytest

from tests.conftest import neo4j_db_fixtures

# Neo4jConnection seem like they are unused arguments but they are the
# DB connection objects that were yielded to the function.
# pylint: disable=unused-argument


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


def test_get_full_graph_as_json(mocker, mock_complex_graph, neo4j_connection):
    mock_create_platdb_ht = mocker.patch.object(
        neo4j_connection, 
        '_create_platdb_ht',
        side_effect=neo4j_connection._create_platdb_ht)  # pylint: disable=protected-access

    vertices, edges = neo4j_connection.get_full_graph_as_json()

    # The number is 4 because that is how many vertices are in mock_complex_graph
    assert mock_create_platdb_ht.call_count == 4

    for edge in edges:
        start = edge['start_node']
        dest = edge['end_node']
        v_type = edge['type']

        assert start in vertices
        assert dest in vertices

        if v_type == 'RUNS':
            assert vertices[start]['type'] == 'Compute'
            assert vertices[dest]['type'] == 'Application'

            if vertices[start]['name'] == 'compute1':
                assert vertices[dest]['name'] == 'app1'

            if vertices[start]['name'] == 'compute2':
                assert vertices[dest]['name'] == 'app2'

        if v_type == 'CALLS':
            assert vertices[start]['name'] == 'app1'
            assert vertices[dest]['name'] == 'app2'

        if v_type == 'CALLED BY':
            assert vertices[start]['name'] == 'app2'
            assert vertices[dest]['name'] == 'app1'

@pytest.mark.parametrize('cls,orig_attrs,updated_attrs', neo4j_db_fixtures)
def test_platdb_time_attrs(cls, orig_attrs, updated_attrs):
    """This function is for testing the PlatDB attrs which are inherited 
    by the other neomodel classes. This could have maybe been added to one 
    of the other test functions like test_read(), but this seemed easier.
    """
    attrs = orig_attrs.copy()
    time_now = datetime.datetime.now(datetime.timezone.utc)
    attrs['profile_timestamp'] = time_now
    attrs['profile_lock_time'] = time_now

    # This attr should not get written to the DB because it is not specified
    # in any of the neomodel classes.
    attrs['missing_attr'] = 'Should not end up in DB'

    cls(**attrs).save()
    read_obj = cls.nodes.get(**orig_attrs)

    assert read_obj.profile_timestamp == time_now
    assert read_obj.profile_lock_time == time_now
    assert hasattr(read_obj, 'missing_attr') is False
