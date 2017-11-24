import logging
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# same with Blueprint


@app.route("/")
def hello_world():
    return "Hello, cross-origin-world!"


@app.route("/api/")
def api_test():
    return "Hello, api-test!"


@app.route("/single/")
@cross_origin()
def single_test():
    return "Hello, single!"


if __name__ == "__main__":
    logging.getLogger('flask_cors').level = logging.DEBUG
    app.run(port=5001, host="0.0.0.0")


# http://flask-cors.readthedocs.io