from flask import Flask
import logging.config

logging.config.fileConfig("logger.ini")

app = Flask(__name__)
logger = logging.getLogger("mylog")


@app.route("/")
def index():
    logger.debug("access index")
    return "<h1>hello, world</h1>"


@app.route("/user/<name>")
def user(name):
    logger.error("access user")
    return "<h1>Hello, {}</h1>".format(name)


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")