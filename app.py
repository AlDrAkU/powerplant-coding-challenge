
from flask import Flask, request
from utils import calc_load_balancing


app = Flask(__name__)

@app.route("/calculate",methods=['POST'])
def calculate():


    data = request.stream.read().decode("utf-8")
    return calc_load_balancing(data)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000)
