from flask import Flask, make_response
from flask_classy import FlaskView
import json
from nose.tools import *


class JsonResource(object):
    content_type = 'application/json'

    def output(self, data, code, headers=None):
        dumped = json.dumps(data)
        response = make_response(dumped, code)
        if headers:
            headers.extend({'Content-Type': self.content_type})
        else:
            headers = {'Content-Type': self.content_type}
        response.headers.extend(headers)

        return response


    def input(self, data):
        loaded = loads(data)
        
        return loaded

# Test Responses
response_1 = {
    'internal_string':"just a string",
    'integer': 5,
    'validate_int': 1,
    'input_required': 'just another string'
}
response_2 = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'Nothing'
}
response_get = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'GET'
}
response_put = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'PUT'
}
response_post = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'POST'
}
response_delete = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'DELETE'
}

headers = [('Content-Type', 'application/json')]
data = {'input_required': 'required'}


class RepresentationView(FlaskView):
    representations = {'application/json': JsonResource()}
    base_args = ['fields']


    def index(self):
        return [response_1, response_2]

    def get(self, obj_id):
        return response_get

    def put(self, obj_id):
        return response_put

    def post(self):
        return response_post

    def delete(self, obj_id):
        return response_delete

app = Flask("representations")
RepresentationView.register(app)

client = app.test_client()

def test_index_representation():
    resp = client.get("/representation/")
    eq_(json.dumps([response_1, response_2]), str(resp.data))

def test_get_representation():
    resp = client.get("/representation/1")
    eq_(json.dumps(response_get), str(resp.data))

def test_post_representation():
    resp = client.post("/representation/", headers=headers, data=json.dumps(data))
    eq_(json.dumps(response_post), str(resp.data))

def test_put_representation():
    resp = client.put("/representation/1", headers=headers, data=json.dumps(data))
    eq_(json.dumps(response_put), str(resp.data))

def test_delete_representation():
    resp = client.delete("/representation/1")
    eq_(json.dumps(response_delete), str(resp.data))
