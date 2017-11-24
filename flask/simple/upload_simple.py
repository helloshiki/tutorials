from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files['file']
    return "filename is : " + file.filename


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")


# curl -F "file=@readme.txt" http://localhost:5001/upload