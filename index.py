from flask import Flask
from flask import jsonify
from flask import request
import pymongo as pm
from pymongo import MongoClient
import json
from bson import json_util
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/v1/house',methods=['GET'])
def house():
    phone = request.args.get('phone', '')
    gender = request.args.get('gender', '')
    lessor_type = request.args.get('lessor_type', '')
    lessor_gender = request.args.get('lessor_gender', '')
    lastname = request.args.get('lastname', '')
    query = {}
    
    if phone:
        query['phone_num'] = phone
    if gender:
        query['gender_rtn'] = int(gender)
    if lessor_gender:
        query['lessor_gender'] = int(lessor_gender)
    if lastname:
        query['lastname'] = lastname
    if lessor_type:
        query['lessor_type'] = lessor_type

    client = MongoClient('mongodb://localhost:27017/')
    db = client['RawData']
    collection = db['posts']
    data = list(collection.find(query))
    
    return json.dumps(data, default=json_util.default)


if __name__ == "__main__":
    app.run()