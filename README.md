# Vehicle Routing Problem
Vehicles are roaming around the neighborhood with a specific stock of products at a given time, 
delivering orders one by one. There are n vehicles roaming around the city and m orders waiting 
for the delivery. For the sake of simplicity, you can assume that vehicles carry infinite amount 
of stock and delivery process itself takes zero time (handing over the carboy, climbing the ladders, 
parking the vehicle etc). Given the input data, find the routes that minimizes the total delivery 
duration. (Note that vehicles can end their journey in any location, they do not need to return back 
to any depot since they carry infinite stock already.)

## 2 potential Solution
### Find Best Route (Flatten Version)
While calculating the route according to the input information given, 
the order of priority is taken into account. In this way, things are resolved 
as they come. After each job is completed, it is assumed that all vehicles are available 
for the next job. The work was done by choosing the vehicle with the shortest distance 
between the vehicles.
### Find Best Route (Complex Version)
While calculating the route according to the input information given, the priority is to 
complete the work as quickly as possible. In this way, it is aimed to complete the work as 
soon as possible. When the data is received, the distances for each vehicle are calculated 
in each cycle and the shortest one among these distances is selected and that work is done. 
After each job is completed, it is assumed that all vehicles are available for the next job.
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
core/algorithms.py                  75      0   100%
core/utils.py                       48      1    98%   86
tests/__init__.py                    0      0   100%
tests/test_api.py                   14      0   100%
tests/test_core_base_models.py      40      2    95%   35, 41
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