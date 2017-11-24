from flask import Flask, g, request, abort
from flask_login import LoginManager, UserMixin, login_required, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

JWT_EXPIRES_IN = 20
app.config['SECRET_KEY'] = "SECRET_KEY"
jwt = JWT(app.config['SECRET_KEY'], expires_in=JWT_EXPIRES_IN)


class User(UserMixin):
    def __init__(self, username, password, age):
        self.id = username
        self.username = username
        self.password = password
        self.age = age


USERS = [User("Kitty", "123", 10), User("John", "123", 20)]


@login_manager.request_loader
def load_user_from_request(req):
    token = req.headers.get('Token')
    if not token:
        return None

    try:
        jwt_obj = jwt.loads(token)
        for user in USERS:
            if user.username == jwt_obj["username"]:
                return user
        return None
    except Exception as e:
        # Signature expired
        print(e)
        return None


@app.route('/')
@login_required
def index():
    print(current_user)
    return "ok"


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

    token = jwt.dumps({'username': username, 'expire_in': JWT_EXPIRES_IN})
    return token

# no logout


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")


# curl http://127.0.0.1:5001/login?username=Kitty&password=123
# => eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxMTQxNDEzMCwiaWF0IjoxNTExNDE0MDcwfQ.eyJ1c2VybmFtZSI6IktpdHR5IiwiZXhwaXJlX2luIjo2MH0.GHKCOuQ80Oe0Rl4hBns5raP4tIBeRSvodQ_5LJEAQMQ
# curl http://127.0.0.1:5001/ -H "Token:eyJhbGciOiJIUzI1NiIsImV4cCI6MTUxMTQxNDEzMCwiaWF0IjoxNTExNDE0MDcwfQ.eyJ1c2VybmFtZSI6IktpdHR5IiwiZXhwaXJlX2luIjo2MH0.GHKCOuQ80Oe0Rl4hBns5raP4tIBeRSvodQ_5LJEAQMQ"


