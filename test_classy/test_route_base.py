from flask import Flask
from .view_classes import BasicView, RouteBaseView, ModifiedSuffixAPI
from nose.tools import *

app = Flask('route_base')
RouteBaseView.register(app, route_base="/rb_test2/")
ModifiedSuffixAPI.register(app)


def test_route_base_override():
    client = app.test_client()
    resp = client.get('/rb_test2/')
    eq_(b"Index", resp.data)

def test_modified_suffix():
    client = app.test_client()
    resp = client.get('/modifiedsuffix/')
    eq_(b"Modified Suffix", resp.data)
