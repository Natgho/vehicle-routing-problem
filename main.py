# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 15.01.2022
import json
from utils import FindBestRouteFlatten, FindBestRouteComplex

if __name__ == '__main__':
    with open('materials/algo_input.json') as f:
        data = json.load(f)
        # company = FindBestRouteFlatten(data)
        company = FindBestRouteComplex(data)
    company.find_best_routes()
