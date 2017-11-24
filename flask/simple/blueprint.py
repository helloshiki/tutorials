from flask import Flask, Blueprint

######################################################################
user = Blueprint("user", "_user_", url_prefix="/user")


@user.route("/nickname")
def nickname():
    return "nickname"


######################################################################
goods = Blueprint("goods", "_goods_", url_prefix="/goods")


@goods.route("/goods")
def list_goods():
    return "goods"

######################################################################


app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(goods)


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")