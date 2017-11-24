from flask import Flask, abort

app = Flask(__name__)


@app.route("/abort/<code>")
def abort_test(code):
    return abort(int(code))


@app.errorhandler(401)
def page_not_found(e):
    return "00000000000000", 401


@app.errorhandler(404)
def page_not_found(e):
    return "page_not_found", 404


@app.errorhandler(500)
def internal_server_error(e):
    return "internal_server_error", 500


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")