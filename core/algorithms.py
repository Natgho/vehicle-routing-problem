# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 15.01.2022
from core.utils import BaseRouteFinder, Job, get_min_from_dict
from fastapi.logger import logger


class FindBestRouteFlatten(BaseRouteFinder):
    """
    It prioritizes the sequential retrieval of jobs while optimizing the route.
    By paying attention to the order given for each job,
    it finds the vehicle that will do the job in the shortest time among all the vehicles.
    """
    def find_best_routes(self):
        for job in self.jobs.values():  # type: Job
            logger.info("*" * 30)
            best_vehicle, best_distance = self._find_best_vehicle(job)
            self.output['routes'][best_vehicle]['jobs'].append(job.j_id)
            self.output['routes'][best_vehicle]['delivery_duration'] += job.service + best_distance
        logger.info(self.output)
        logger.info([str(x) for x in self.vehicles.values()])
        return self.output

    def _find_best_vehicle(self, current_job: Job):
        """
        Finds the vehicle that can do this job as soon as possible among the tools for the desired job.
        :param current_job: The job for which the shortest duration is desired.
        :return:  vehicle that does the given job in the shortest time
        """
        best_distance = 0
        best_vehicle = None
        for vehicle in self.vehicles.values():
            if vehicle.capacity >= current_job.delivery:
                distance = self.routes.get_distance(vehicle.start_index, current_job.location_index)
                logger.info(f"best distance: {best_distance} distance: {distance}")
                if not best_distance or distance < best_distance:
                    best_vehicle = vehicle
                    best_distance = distance
        logger.info(f"final distance: {best_distance}")
        self.vehicles[best_vehicle.v_id].capacity -= current_job.delivery
        self.vehicles[best_vehicle.v_id].start_index = current_job.location_index
        self.output['total_delivery_duration'] += current_job.service + best_distance
        return best_vehicle.v_id, best_distance


class FindBestRouteComplex(BaseRouteFinder):
    """
    The algorithm that prioritizes the completion of all jobs as soon as possible while calculating the route.
    """
    def __init__(self, *args, **kwargs):
        super(FindBestRouteComplex, self).__init__(*args, **kwargs)
        self.distances = self.calculate_distances()

    def find_best_routes(self):
        while len(self.jobs) > 0:
            [logger.info(x) for x in self.vehicles.values()]
            logger.info(self.distances)
            next_job = self.find_next_job()
            logger.info(f"next job: {next_job}")
            self.do_the_job(**next_job)
            [logger.info(x) for x in self.vehicles.values()]
            logger.info("*" * 30)
        logger.info(self.output)
        return self.output

    def _find_current_distances(self, v_id):
        """
        Calculates the distance of vehicles to jobs when each job is done.
        :param v_id: the ID value of the specified vehicle
        :return:
        """
        distances = {}
        for j_id, j_data in self.jobs.items():
            if self.vehicles[v_id].capacity >= j_data.delivery:
                distances[j_id] = self.routes.get_distance(self.vehicles[v_id].start_index,
                                                           j_data.location_index)
        return distances

    def find_next_job(self):
        """
        Finds the next job with the shortest time to do in each loop.
        :return: next job id, vehicle id, shortest distance.
        """
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
        """
        Returns the work that each tool can do in the shortest amount of time.
        :return: shortest jobs and vehicles
        """
        min_jobs = {}
        for v_id in self.vehicles:
            if self.vehicles[v_id].capacity > 0:
                min_vehicle_job = get_min_from_dict(self.distances[v_id])
                min_jobs[v_id] = min_vehicle_job
        return min_jobs

    def calculate_distances(self):
        """
        Calculates the distances of each vehicle to the currently existing jobs.
        :return: dict of vehicles and jobs.
        """
        return {v_id: self._find_current_distances(v_id) for v_id in self.vehicles}

    def do_the_job(self, v_id, j_id, distance):
        """
        The function that makes the updates in the data to be done for the job to be done.
        :param v_id: the id of the vehicle that will do the job
        :param j_id: id of the job to be done
        :param distance: distance of job
        :return:
        """
        # TODO Check Vehicle available/unavailable status
        self.vehicles[v_id].capacity -= self.jobs[j_id].delivery
        self.vehicles[v_id].start_index = self.jobs[j_id].location_index
        self.output['total_delivery_duration'] += self.jobs[j_id].service + distance
        self.output['routes'][v_id]['jobs'].append(j_id)
        self.output['routes'][v_id]['delivery_duration'] += self.jobs[j_id].service + distance
        self.jobs.pop(j_id)
        self.distances = self.calculate_distances()
