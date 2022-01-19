# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 17.01.2022
from fastapi import FastAPI, Body
from starlette.responses import RedirectResponse

from core.algorithms import FindBestRouteFlatten, FindBestRouteComplex
from pydantic import BaseModel, Field
import logging
from app_consts import title, description, version, contact, sample_input

logging.basicConfig(level=logging.INFO)


class Input(BaseModel):
    """
    It is used to serialize the incoming data.
    It specifies what type of incoming data will be kept and what its contents will be.
    """
    vehicles: list = Field(description="Vehicle object in vehicles array")
    jobs: list = Field(description="Index of the vehicle’s starting location")
    matrix: list = Field(description="List of each row in the duration matrix. "
                                     "Element (i, j) indicates the amount of seconds "
                                     "it takes to travel from location index i to location index j")


app = FastAPI(title=title,
              description=description,
              version=version,
              contact=contact)


@app.get("/")
async def main():
    """
    The homepage where we can see the endpoints of the entire system.
    """
    response = RedirectResponse(url="/docs")
    return response


@app.post('/api/find_best_route_flatten')
async def find_best_route_flatten(input_data: Input = Body(..., example=sample_input)):
    """
    Route optimization algorithm that prioritizes sequential work without time constraints.
    """
    route_solver = FindBestRouteFlatten(input_data.dict())
    best_routes = route_solver.find_best_routes()
    return best_routes


@app.post('/api/find_best_route_complex')
async def find_best_route_complex(input_data: Input = Body(..., example=sample_input)):
    """
    Route optimization algorithm that optimizes the route by prioritizing road weights.
    """
    route_solver = FindBestRouteComplex(input_data.dict())
    best_routes = route_solver.find_best_routes()
    return best_routes
