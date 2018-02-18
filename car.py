from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify
from iota_api import Car
from flask_cors import CORS

try:
    import configparser
    config = configparser.ConfigParser()
    config.read('config.cfg')
    seed = config['IOTA']['seed']
except Exception:
    import os
    seed = os.environ['SEED']

app = Flask(__name__)
CORS(app)
api = Api(app)

car = Car(seed)


# class Identify(Resource):
@app.route("/identify")
def Identify():
    address = str(car.getAddress(1)['addresses'][0])
    return {'identity': address}


# class Payment(Resource):
@app.route("/payments/<adress>/<amount>")
def Payment(adress, amount=0):
    car.sendiota(adress, float(amount))
    return {'payment': 'OK'}


# api.add_resource(Identify, '/identify')  # Route_1
# api.add_resource(Payment, '/payments/<adress>/<amount>')  # Route_2


if __name__ == '__main__':
    app.run(port=5002, debug=True)
