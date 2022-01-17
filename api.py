# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 17.01.2022
from flask import Flask, request, jsonify
from core.utils import FindBestRouteFlatten, FindBestRouteComplex
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.route('/api/find_best_route_flatten', methods=['POST'])
def find_best_route_v1():
    content = request.get_json()
    route_solver = FindBestRouteFlatten(content)
    best_routes = route_solver.find_best_routes()
    return jsonify(best_routes)


@app.route('/api/find_best_route_complex', methods=['POST'])
def find_best_route_v2():
    content = request.get_json()
    route_solver = FindBestRouteComplex(content)
    best_routes = route_solver.find_best_routes()
    return jsonify(best_routes)


if __name__ == '__main__':
    app.run()
