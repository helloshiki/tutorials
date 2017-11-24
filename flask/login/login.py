from flask import Flask, request
from flask_login import LoginManager, UserMixin, login_required

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username, password, age):
        self.id = username
        self.username = username
        self.password = password
        self.age = age


tokens = dict()
USERS = [User("Kitty", "123", 10), User("John", "123", 20)]


@login_manager.request_loader
def load_user_from_request(req):
    token = req.headers.get('Token')
    if not token:
        return None
    return tokens.get(token, None)


@app.route("/login")
def login():
    args = request.args
    username, password = args["username"], args["password"]

    user = None
    for u in USERS:
        if u.username == username and u.password == password:
            user = u
            break

    if not user:
        return "invalid username/password", 403

    token = "test_token"
    tokens[token] = user
    return "" + token


@app.route("/logout")
@login_required
def logout():
    token = request.headers.get('Token')
    if token and token in tokens:
        del tokens[token]
    return "ok"


@app.route("/")
@login_required
def index():
    return "<h1>You are online</h1>"


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")

# http://www.pythondoc.com/flask-login
# curl http://127.0.0.1:5001/login?username=Kitty&password=123
# curl -H "Token:test_token" http://127.0.0.1:5001/
# curl -H "Token:test_token" http://127.0.0.1:5001/logout
