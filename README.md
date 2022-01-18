# Vehicle Routing Problem
coming soon...

## Run Tests
```shell
coverage run -m pytest
coverage report -m
```

## Code Coverage:
```doctest
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
api.py                              26      0   100%
app_consts.py                        6      0   100%
core/base_models.py                 48      1    98%   55
core/utils.py                       75      0   100%
tests/__init__.py                    0      0   100%
tests/test_api.py                   14      0   100%
tests/test_core_base_models.py      40      2    95%   35, 39
--------------------------------------------------------------
TOTAL                              209      3    99%
```

## How to Run Project
```shell
pip install -r requirements.txt
uvicorn api:app --reload  
```
### Using with Docker:
```shell
docker build -t vehicle-route-optimization .
docker run -d --name vehicle-route-optimization -p 0.0.0.0:8080:80 vehicle-route-optimization
```
Open your browser at http://localhost:8080  
### Using with Docker-compose:
```shell
docker-compose up -d
```
Open your browser at http://localhost:8080

## Some personal questions
1) Why vehicle capacity and jobs delivery variable types are array? (maybe related by Vroom input style)
2) (output) sample delivery duration is not correct.
3) OrTools needs to be put "depot" step. I prefer to develop my algorithm.
4) Vroom is more suitable for this question.
5) delivery duration time is a really confusing detail :)