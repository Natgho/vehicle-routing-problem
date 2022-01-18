# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 18.01.2022
from fastapi.testclient import TestClient

from api import app
from http import HTTPStatus
from app_consts import sample_input

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_find_best_route_flatten():
    response = client.post("/api/find_best_route_flatten", json=sample_input)
    assert response.status_code == HTTPStatus.OK


def test_find_best_route_complex():
    response = client.post("/api/find_best_route_complex", json=sample_input)
    assert response.status_code == HTTPStatus.OK
