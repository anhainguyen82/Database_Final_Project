#!flask/bin/python
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
from os import listdir
from pymongo import MongoClient
from bs4 import BeautifulSoup
import json
import csv
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "Your Rest Service is Working"


#rest service to upload json files within a directory.  Make sure to end your address with a /
@app.route('/query/<category>', methods=['GET'])
def JodiRestService(category):
    
    #Mongo is the chosen database, make sure your MongoDB is running before execution of this program
    client = MongoClient()

    #database name is "HotelReviews"
    db = client.HotelReviews
    api = Api(app)
    
    #get current date and time
    class Reviews (Resource):
        def get(self, Address):
            conn = db.connect()
            query = conn.execute("select HotelID, Author from Reviews where Address = %d" %int(Reviews))
            result = {'data': [dict(zip(tuple (query.keys()) , i)) for i in query.cursor]}
            return jsonify(result)

    api.add_resource(Reviews, '/reviews/<Address>')

## Starts the server for serving Rest Ser.vices 
if __name__ == '__main__':
    app.run(debug=True)