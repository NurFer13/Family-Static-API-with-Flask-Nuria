"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
member1 = {
            "id": jackson_family._generateId(),
            "first_name": "John",
            "last_name": jackson_family.last_name,
            "age": 34,
            "lucky_numbers": [7,13,22]
            }
member2 = {
                 "id": jackson_family._generateId(),
            "first_name": "Jane",
            "last_name": jackson_family.last_name,
            "age": 36,
            "lucky_numbers": [10,14,3]
            }
member3 = { 
                "id": jackson_family._generateId(),
            "first_name": "Jimmy",
            "last_name": jackson_family.last_name,
            "age": 12,
            "lucky_numbers": []
            }
jackson_family.add_member(member1)
jackson_family.add_member(member2)
jackson_family.add_member(member3)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
