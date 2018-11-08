
import os
import requests

from werkzeug.utils import secure_filename

from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify, make_response
import json
import ast
import imp


helper_module = imp.load_source('*', './app/helpers.py')

db = client.restfulapi
collection = db.users


@app.route("/")
def get_initial_response():

    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    resp = jsonify(message)
    return resp


def test_recipes_api_sending_file():
    with open(os.path.join('SCREENSHOT.png'), 'rb') as fp:
        response = requests.post('http://localhost:5000/api/v1/users', data={'name':'Screenshot'}, files={'image': fp})


@app.route("/api/v1/users", methods=['POST'])
def create_user():

    print request.files
    print request.get_data()

    if 'image' in request.files:
        image = request.files['image']
        print (image)
        if image:
            print image.filename
            filename = secure_filename(image.filename)
            print filename
            image.save(os.path.join('Papka_dlya_kartunok', filename))
    try:

        try:
            request.get_json()
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:

            return "", 400

        record_created = collection.insert(body)

        if isinstance(record_created, list):
            return jsonify([str(v) for v in record_created]), 201
        else:
            return jsonify(str(record_created)), 201
    except:
        return "", 500


@app.route("/api/images/<int:pid>.jpg")
def get_image(pid):
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response


@app.route("/api/v1/users", methods=['GET'])
def fetch_users():
    try:
        query_params = helper_module.parse_query_params(request.query_string)
        if query_params:
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}

            records_fetched = collection.find(query)

            if records_fetched.count() > 0:
                return dumps(records_fetched)
            else:
                return "", 404

        else:
            if collection.find().count > 0:
                return dumps(collection.find())
            else:
                return jsonify([])
    except:
        return "", 500



@app.errorhandler(404)
def page_not_found(e):
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
