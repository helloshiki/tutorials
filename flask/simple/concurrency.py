from flask import Flask
from gevent.wsgi import WSGIServer
import gevent
app = Flask(__name__)


@app.route("/")
def index():
    gevent.sleep(6)
    return "<h1>hello, world</h1>"


if __name__ == "__main__":
    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()

# http://hhkbp2.github.io/gevent-tutorial/
# http://www.gevent.org/
# for i in 1 2 3 4 5; do curl http://localhost:5001 &; done
