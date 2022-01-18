# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 16.01.2022
from abc import ABC, abstractmethod


class Vehicle:
    def __init__(self, id, start_index, capacity):
        self.v_id = id
        self.start_index = start_index
        self.capacity = capacity[0]

    def __str__(self):
        return f"vehicle id:{self.v_id} start_index: {self.start_index} capacity: {self.capacity}"


class Job:
    def __init__(self, id, location_index, delivery, service):
        self.j_id = id
        self.location_index = location_index
        self.delivery = delivery[0]
        self.service = service


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def get_distance(self, start_point, target_point):
        return self.matrix[start_point][target_point]


class BaseRouteFinder(ABC):
    def __init__(self, data: dict):
        self.data = data
        self.vehicles = {}
        self.jobs = {}
        self.output = {}
        self._parse_data()

    def _parse_data(self):
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
        raise NotImplementedError("Route algorithm should be implemented.")


def get_key_from_value(my_dict, to_find):
    for k, v in my_dict.items():
        if v == to_find:
            return {k: v}
    return None


def get_min_from_dict(my_dict):
    min_val = min(my_dict.values())
    min_val_id = get_key_from_value(my_dict, min_val)
    return min_val_id
