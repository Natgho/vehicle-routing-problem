# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 17.01.2022
from flask import Flask, request, jsonify
from core.utils import FindBestRouteFlatten, FindBestRouteComplex

app = Flask(__name__)


@app.route('/api/find_best_route_flatten', methods=['POST'])
def find_best_route_v1():
    content = request.get_json()
    route_solver = FindBestRouteFlatten(content)
    best_routes = route_solver.find_best_routes()
    print(request.get_json())
    return jsonify(best_routes)


@app.route('/api/find_best_route_complex', methods=['POST'])
def find_best_route_v2():
    content = request.get_json()
    route_solver = FindBestRouteComplex(content)
    best_routes = route_solver.find_best_routes()
    app.logger.info("sample sample")
    print(request.get_json())
    return jsonify(best_routes)


if __name__ == '__main__':
    app.run()
