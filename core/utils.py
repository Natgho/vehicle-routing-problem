# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 15.01.2022
from pprint import pp
from core.base_models import BaseRouteFinder, Job, get_min_from_dict


class FindBestRouteFlatten(BaseRouteFinder):
    def find_best_routes(self):
        for job in self.jobs.values():  # type: Job
            print("*" * 30)
            best_vehicle = self._find_best_vehicle(job)
            self.output['routes'][best_vehicle]['jobs'].append(job.j_id)
            self.output['routes'][best_vehicle]['delivery_duration'] += job.service
        pp(self.output)
        pp([str(x) for x in self.vehicles.values()])
        return self.output

    def _find_best_vehicle(self, current_job: Job):
        best_distance = 0
        best_vehicle = None
        for vehicle in self.vehicles.values():
            if vehicle.capacity >= current_job.delivery:
                distance = self.routes.get_distance(vehicle.start_index, current_job.location_index)
                print(f"best distance: {best_distance} distance: {distance}")
                if not best_distance or distance < best_distance:
                    best_vehicle = vehicle
                    best_distance = distance
        print(f"final distance: {best_distance}")
        self.vehicles[best_vehicle.v_id].capacity -= current_job.delivery
        self.vehicles[best_vehicle.v_id].start_index = current_job.location_index
        self.output['total_delivery_duration'] += current_job.service
        return best_vehicle.v_id


class FindBestRouteComplex(BaseRouteFinder):
    def __init__(self, *args, **kwargs):
        super(FindBestRouteComplex, self).__init__(*args, **kwargs)
        self.distances = self.calculate_distances()

    def find_best_routes(self):
        while len(self.jobs) > 0:
            [print(x) for x in self.vehicles.values()]
            pp(self.distances)
            next_job = self.find_next_job()
            print(f"next job: {next_job}")
            self.do_the_job(**next_job)
            [print(x) for x in self.vehicles.values()]
            print("*" * 30)
        pp(self.output)
        return self.output

    def _find_current_distances(self, v_id):
        distances = {}
        for j_id, j_data in self.jobs.items():
            if self.vehicles[v_id].capacity >= j_data.delivery:
                distances[j_id] = self.routes.get_distance(self.vehicles[v_id].start_index,
                                                           j_data.location_index)
        return distances

    def find_next_job(self):
        min_jobs = self.get_min_jobs()
        min_distance = None
        target_min_job = None
        for v_id, min_job in min_jobs.items():
            for j_id, distance in min_job.items():
                if not min_distance or distance < min_distance:
                    min_distance = distance
                    target_min_job = {"v_id": v_id,
                                      "j_id": j_id,
                                      "distance": distance}
        return target_min_job

    def get_min_jobs(self):
        min_jobs = {}
        for v_id in self.vehicles:
            if self.vehicles[v_id].capacity > 0:
                min_vehicle_job = get_min_from_dict(self.distances[v_id])
                min_jobs[v_id] = min_vehicle_job
        return min_jobs

    def calculate_distances(self):
        return {v_id: self._find_current_distances(v_id) for v_id in self.vehicles}

    def do_the_job(self, v_id, j_id, distance):
        # TODO Check Vehicle available/unavailable status
        self.vehicles[v_id].capacity -= self.jobs[j_id].delivery
        self.vehicles[v_id].start_index = self.jobs[j_id].location_index
        self.output['total_delivery_duration'] += self.jobs[j_id].service + distance
        self.output['routes'][v_id]['jobs'].append(j_id)
        self.output['routes'][v_id]['delivery_duration'] += self.jobs[j_id].service + distance
        self.jobs.pop(j_id)
        self.distances = self.calculate_distances()
