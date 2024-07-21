import pytest
from pytest import raises

from blockchain.models import Network # just need something to generate querysets off of
from helpers import exceptions, randomly


##############################
# select_from_query_set
##############################
@pytest.mark.django_db
def test_select_from_query_set():
    model_instance = Network.objects.create(name='1', chain_id='0x1')
    assert randomly.select_from_query_set(Network.objects.all()) == model_instance


@pytest.mark.django_db
def test_select_from_empty_queryset():
    assert randomly.select_from_query_set(Network.objects.all()) is None


##############################
# select_n_from_query_set
##############################
@pytest.mark.django_db
def test_select_n_from_query_set():
    num_model_instances = 5
    for i in range(0, num_model_instances):
        Network.objects.create(name=str(i), chain_id=f"0x{i}")
    assert Network.objects.count() == num_model_instances
    for i in range(1, num_model_instances+1):
        assert randomly.select_n_from_query_set(
            Network.objects.all(),
            number_of_selections=i,
        ).count() == i
    selected_instances = randomly.select_n_from_query_set(
        Network.objects.all(),
        number_of_selections=num_model_instances,
    )
    assert selected_instances.count() == num_model_instances
    for instance in Network.objects.all():
        assert selected_instances.filter(id=instance.id).exists()
    for instance in selected_instances:
        assert Network.objects.filter(id=instance.id).exists()


@pytest.mark.django_db
def test_select_n_from_query_set_returns_empty_query_set_for_zero_selections():
    assert not Network.objects.exists()
    assert not randomly.select_n_from_query_set(
        Network.objects.all(),
        number_of_selections=0,
    ).exists()


@pytest.mark.django_db
def test_select_n_from_query_set_fails_with_too_many_selections():
    assert not Network.objects.exists()
    with raises(exceptions.MoreSelectionsThanOptions):
        randomly.select_n_from_query_set(
            Network.objects.all(),
            number_of_selections=1,
        )
