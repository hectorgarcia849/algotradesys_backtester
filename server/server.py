from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    if request.method == 'GET':
        return "Hello World!"
