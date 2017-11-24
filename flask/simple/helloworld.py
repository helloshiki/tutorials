from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>hello, world</h1>"


@app.route("/user/<name>")
def user(name):
    return "<h1>Hello, {}</h1>".format(name)


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")