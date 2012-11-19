from flask import Flask, url_for
from view_classes import BasicView, IndexView
from nose.tools import *

app = Flask("common")
BasicView.register(app)
IndexView.register(app)

client = app.test_client()

def test_index_url():
    with app.test_request_context():
        url = url_for("IndexView:index")
        eq_("/", url)

def test_basic_index_url():
    with app.test_request_context():
        url = url_for("BasicView:index")
        eq_("/basic/", url)

def test_custom_endpoint_url():
    with app.test_request_context():
        url = url_for("basic_endpoint")
        eq_("/basic/endpoint/", url)

