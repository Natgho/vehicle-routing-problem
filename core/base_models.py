# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 16.01.2022
from abc import ABC, abstractmethod


class Vehicle:
    """
    It allows to take the vehicle data as a list and store its variables in a usable way.
    """

    def __init__(self, id, start_index, capacity):
        self.v_id = id
        self.start_index = start_index
        self.capacity = capacity[0]

    def __str__(self):
        return f"vehicle id:{self.v_id} start_index: {self.start_index} capacity: {self.capacity}"


class Job:
    """
    It allows taking job data as a list and storing its variables in a usable way.
    """

    def __init__(self, id, location_index, delivery, service):
        self.j_id = id
        self.location_index = location_index
        self.delivery = delivery[0]
        self.service = service


class Matrix:
    """
    It allows taking route matrix data as a list and storing its variables in a usable way.
    """

    def __init__(self, matrix):
        self.matrix = matrix

    def get_distance(self, start_point, target_point):
        """
        Returns the distance, in seconds, between two points, relative to the start and end points.
        :param start_point: starting point of desired distance (in seconds)
        :param target_point: target point of desired distance (in seconds)
        :return:
        """
        return self.matrix[start_point][target_point]


class BaseRouteFinder(ABC):
    """
    It serializes the json data that comes as input so that route finder algorithms can access the data.
    Passes it to the relevant variables.
    """

    def __init__(self, data: dict):
        self.data = data
        self.vehicles = {}
        self.jobs = {}
        self.output = {}
        self._parse_data()

    def _parse_data(self):
        """
        the input data is of json type when it is sent, it serializes the data to properties under the class.
        :return:
        """
        if not all(key in self.data.keys() for key in ['vehicles', 'jobs', 'matrix']):
            raise Exception("Data format is not correct. 'Vehicles' and 'jobs' and 'matrix' must be in JSON")

        for vehicle in self.data['vehicles']:
            self.vehicles[vehicle['id']] = Vehicle(**vehicle)

        for job in self.data['jobs']:
            self.jobs[job['id']] = Job(**job)

        self.routes = Matrix(self.data['matrix'])
        self.output['routes'] = {vehicle_id: {'jobs': [], 'delivery_duration': 0} for vehicle_id in self.vehicles}
        self.output['total_delivery_duration'] = 0

    @abstractmethod
    def find_best_routes(self):
        """
        The abstract version of the function that processes the serialized data in the child class.
        :return:
        """
        raise NotImplementedError("Route algorithm should be implemented.")


def get_key_from_value(my_dict, to_find):
    """
    Allows searching by value in a dict.
    :param my_dict: dictionary to search
    :param to_find: value to be found.
    :return:
    """
    for k, v in my_dict.items():
        if v == to_find:
            return {k: v}
    return None


def get_min_from_dict(my_dict):
    """
    It allows to find the minimum values among the values of type list with multiple key values as:
    {
        "key1": [],
        "key2":[]
    }
    :param my_dict: dictionary in which minimum values are desired.
    :return:
    """
    min_val = min(my_dict.values())
    min_val_id = get_key_from_value(my_dict, min_val)
    return min_val_id
