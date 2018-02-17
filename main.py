from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

app = Flask(__name__)
api = Api(app)

class Identify(Resource):
    def get(self):

        return {'identity': "öffentliche Adresse"} 


 class Payment(Resource):
     def get(self, adress, amount):

        return jsonify(result)
        

api.add_resource(Identify, '/identify') # Route_1
api.add_resource(Payment, '/payments/<adress>/<amount>') # Route_2


if __name__ == '__main__':
     app.run(port=5002)