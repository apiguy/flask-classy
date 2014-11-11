from flask import Flask
from .view_classes import BasicView, RouteBaseView, RouteBaseView2
from nose.tools import *



def test_route_base_override():
    app = Flask('route_base')
    RouteBaseView.register(app, route_base="/rb_test2/")
    client = app.test_client()
    resp = client.get('/rb_test2/')
    eq_(b"Index", resp.data)

def test_route_base_with_parameter_in_class():
    app = Flask('route_base')
    RouteBaseView2.register(app)
    client = app.test_client()
    resp = client.get('/rb_test3/id/')
    eq_(b"Index with parameter id", resp.data)

def test_route_base_with_parameter_in_override():
    app = Flask('route_base')
    RouteBaseView2.register(app, route_base="/rb_test3/<ident>/")
    client = app.test_client()
    resp = client.get('/rb_test3/id/')
    eq_(b"Index with parameter id", resp.data)
