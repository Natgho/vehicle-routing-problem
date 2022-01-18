# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 18.01.2022
import pytest
from core.base_models import *


@pytest.fixture
def my_vehicle():
    return Vehicle(id=1, start_index=1, capacity=[1])


def test_vehicle_str(my_vehicle):
    assert str(my_vehicle) == "vehicle id:1 start_index: 1 capacity: 1"


def test_vehicle_properties(my_vehicle):
    assert my_vehicle.v_id == 1
    assert my_vehicle.start_index == 1
    assert my_vehicle.capacity == 1


@pytest.fixture
def my_job():
    return Job(id=1, location_index=1, delivery=[1], service=1)


def test_my_job_properties(my_job):
    assert my_job.j_id == 1
    assert my_job.service == 1
    assert my_job.delivery == 1
    assert my_job.service == 1


@pytest.fixture
def my_base_model():
    return BaseRouteFinder(data={'vehicles': [], 'jobs': [], 'matrix': []})


def test_base_model_with_incorrect_data():
    class ChildClass(BaseRouteFinder):
        def find_best_routes(self):
            pass

    with pytest.raises(Exception,
                       match="Data format is not correct. 'Vehicles' and 'jobs' and 'matrix' must be in JSON"):
        ChildClass(data={'vehicles': [], 'jobs': []})


def test_get_key_from_value():
    sample_dict = {'sample_1': "sample1", "sample_2": "sample2"}
    result = get_key_from_value(sample_dict, "sample2")
    assert result == {'sample_2': 'sample2'}


def test_get_key_from_value_without_value_parameter():
    sample_dict = {'sample_1': "sample1", "sample_2": "sample2"}
    result = get_key_from_value(sample_dict, "sample3")
    assert result is None


def test_get_min_from_dict():
    sample_dict = {"sample_1": [1], "sample_2": [2], "sample_3": [3]}
    result = get_min_from_dict(sample_dict)
    assert result == {"sample_1": [1]}
