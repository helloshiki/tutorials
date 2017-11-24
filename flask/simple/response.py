from flask import Flask
from flask import make_response, redirect, abort

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>hello, world</h1>"


@app.route("/set_cookie")
def set_cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie("answer", "42")
    return response


@app.route("/redirect")
def redirect_test():
    return redirect("/")


@app.route("/abort")
def abort_test():
    return abort(401)


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")